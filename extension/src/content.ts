// Content script: extracts the current page's text when asked by the
// background service worker. Runs on every page (see manifest.json's
// content_scripts.matches) but does nothing until it receives a message.
import type { BackgroundToContentMessage, ExtractedPage } from "./messages";

// Cap extracted text so we don't ship enormous pages to the backend in one
// request; the backend chunks whatever it receives anyway, but this keeps
// the request body reasonable.
const MAX_TEXT_LENGTH = 50_000;

// TODO(extraction-quality): this is a naive `document.body.innerText` dump.
// It includes nav bars, ads, cookie banners, etc. A real implementation
// should use a readability-style extraction (e.g. Mozilla's Readability.js)
// to isolate the main article/content region before sending it to the
// backend. Not implemented -- this is a deliberately simple placeholder,
// not faked data (it does return the page's real, if noisy, text).
function extractPageText(): ExtractedPage {
  const text = document.body?.innerText?.trim().slice(0, MAX_TEXT_LENGTH) ?? "";
  return {
    url: location.href,
    title: document.title,
    text,
  };
}

chrome.runtime.onMessage.addListener((message: BackgroundToContentMessage, _sender, sendResponse) => {
  if (message?.type === "EXTRACT_PAGE_TEXT") {
    sendResponse(extractPageText());
  }
  return false;
});
