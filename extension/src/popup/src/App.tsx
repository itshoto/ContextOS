import { useState } from "react";
import type { AskSource, BackgroundToPopupResponse, PopupToBackgroundMessage } from "../../messages";

function sendToBackground(message: PopupToBackgroundMessage): Promise<BackgroundToPopupResponse> {
  return chrome.runtime.sendMessage(message);
}

function isUrl(value: string): boolean {
  try {
    const parsed = new URL(value);
    return parsed.protocol === "http:" || parsed.protocol === "https:";
  } catch {
    return false;
  }
}

export default function App() {
  const [indexStatus, setIndexStatus] = useState<string | null>(null);
  const [indexing, setIndexing] = useState(false);

  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState<string | null>(null);
  const [sources, setSources] = useState<AskSource[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [asking, setAsking] = useState(false);

  async function handleIndexPage(): Promise<void> {
    setIndexing(true);
    setIndexStatus(null);
    try {
      const response = await sendToBackground({ type: "INDEX_PAGE" });
      if (response.ok && response.kind === "INDEX_PAGE") {
        setIndexStatus(`Indexed this page (${response.chunksCreated} chunk(s)).`);
      } else if (!response.ok) {
        setIndexStatus(`Error: ${response.error}`);
      }
    } catch (err) {
      setIndexStatus(`Error: ${err instanceof Error ? err.message : String(err)}`);
    } finally {
      setIndexing(false);
    }
  }

  async function handleAsk(): Promise<void> {
    const trimmed = question.trim();
    if (!trimmed) {
      return;
    }
    setAsking(true);
    setError(null);
    try {
      const response = await sendToBackground({ type: "ASK", question: trimmed });
      if (response.ok && response.kind === "ASK") {
        setAnswer(response.answer);
        setSources(response.sources);
      } else if (!response.ok) {
        setError(response.error);
        setAnswer(null);
        setSources([]);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setAsking(false);
    }
  }

  return (
    <div className="p-3 flex flex-col gap-3 text-sm">
      <h1 className="text-base font-semibold">ContextOS</h1>

      <div className="flex flex-col gap-1">
        <button
          onClick={handleIndexPage}
          disabled={indexing}
          className="px-3 py-1.5 rounded bg-blue-600 text-white disabled:opacity-60 hover:bg-blue-700"
        >
          {indexing ? "Indexing..." : "Index This Page"}
        </button>
        {indexStatus && <p className="text-xs opacity-70">{indexStatus}</p>}
      </div>

      <div className="flex gap-2">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              handleAsk();
            }
          }}
          placeholder="Ask a question..."
          className="flex-1 px-2 py-1 rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-inherit"
        />
        <button
          onClick={handleAsk}
          disabled={asking}
          className="px-3 py-1 rounded bg-gray-800 dark:bg-gray-200 text-white dark:text-gray-900 disabled:opacity-60"
        >
          {asking ? "..." : "Ask"}
        </button>
      </div>

      {error && (
        <div className="p-2 rounded text-xs bg-red-100 text-red-800 dark:bg-red-950 dark:text-red-300">
          {error}
        </div>
      )}

      {answer && (
        <div className="flex flex-col gap-2">
          <div>
            <h2 className="text-xs font-semibold uppercase opacity-70 mb-1">Answer</h2>
            <p className="whitespace-pre-wrap">{answer}</p>
          </div>

          {sources.length > 0 && (
            <div>
              <h2 className="text-xs font-semibold uppercase opacity-70 mb-1">Sources</h2>
              <ul className="flex flex-col gap-2">
                {sources.map((source, i) => (
                  <li
                    key={`${source.path}-${i}`}
                    className="p-2 rounded text-xs bg-gray-100 dark:bg-gray-800"
                  >
                    <div className="font-mono font-semibold truncate">
                      {isUrl(source.path) ? (
                        <a
                          href={source.path}
                          target="_blank"
                          rel="noreferrer"
                          className="text-blue-600 dark:text-blue-400 underline"
                        >
                          {source.path}
                        </a>
                      ) : (
                        source.path
                      )}
                    </div>
                    <div className="opacity-70">score: {source.score.toFixed(3)}</div>
                    <div className="mt-1 whitespace-pre-wrap opacity-90">{source.snippet}</div>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
