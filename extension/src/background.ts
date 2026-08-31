// Background service worker: the only place that talks to the backend over
// the network and the only place that messages content scripts. The popup
// never calls fetch() or chrome.tabs.* directly -- it only exchanges
// messages with this service worker, which keeps the actual localhost
// requests out of the (less trusted) UI surfaces, mirroring the same
// security boundary VS Code webviews are built around.
import type {
  AskSource,
  BackgroundToContentMessage,
  BackgroundToPopupResponse,
  ExtractedPage,
  PopupToBackgroundMessage,
} from "./messages";

const DEFAULT_BACKEND_URL = "http://localhost:8000";

// TODO(options-page): backend URL is only configurable via chrome.storage.local
// today (set the "backendUrl" key). A real options page to edit this from the
// UI is not implemented yet.
async function getBackendUrl(): Promise<string> {
  const stored = await chrome.storage.local.get("backendUrl");
  return (stored.backendUrl as string | undefined) || DEFAULT_BACKEND_URL;
}

async function postJson<T>(path: string, body: unknown): Promise<T> {
  const backendUrl = await getBackendUrl();
  const res = await fetch(`${backendUrl}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    let detail = res.statusText;
    try {
      const errBody = (await res.json()) as { detail?: string };
      if (errBody?.detail) {
        detail = errBody.detail;
      }
    } catch {
      // response body wasn't JSON; fall back to statusText
    }
    throw new Error(`ContextOS backend error (${res.status}): ${detail}`);
  }

  return (await res.json()) as T;
}

async function extractActiveTabText(): Promise<ExtractedPage> {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab?.id) {
    throw new Error("No active tab found to index.");
  }

  const message: BackgroundToContentMessage = { type: "EXTRACT_PAGE_TEXT" };
  const response = (await chrome.tabs.sendMessage(tab.id, message)) as ExtractedPage | undefined;

  if (!response) {
    throw new Error(
      "Could not extract page text. The content script may not have loaded on this page (e.g. chrome:// pages are not accessible)."
    );
  }

  return response;
}

async function handleIndexPage(): Promise<BackgroundToPopupResponse> {
  const page = await extractActiveTabText();

  const content = `${page.title}\n\n${page.text}`;
  const result = await postJson<{ documents_ingested: number; chunks_created: number }>(
    "/ingest/documents",
    { documents: [{ path: page.url, content }] }
  );

  return {
    ok: true,
    kind: "INDEX_PAGE",
    documentsIngested: result.documents_ingested,
    chunksCreated: result.chunks_created,
  };
}

async function handleAsk(question: string): Promise<BackgroundToPopupResponse> {
  const result = await postJson<{ answer: string; sources: AskSource[] }>("/query/ask", {
    question,
    top_k: 5,
  });

  return { ok: true, kind: "ASK", answer: result.answer, sources: result.sources };
}

chrome.runtime.onMessage.addListener((message: PopupToBackgroundMessage, _sender, sendResponse) => {
  (async () => {
    try {
      if (message.type === "INDEX_PAGE") {
        sendResponse(await handleIndexPage());
      } else if (message.type === "ASK") {
        sendResponse(await handleAsk(message.question));
      }
    } catch (err) {
      const response: BackgroundToPopupResponse = {
        ok: false,
        error: err instanceof Error ? err.message : String(err),
      };
      sendResponse(response);
    }
  })();

  return true; // keep the message channel open for the async sendResponse above
});
