// Shared message contracts between popup <-> background <-> content script.
// Kept in one file so all three sides stay in sync.

export interface AskSource {
  path: string;
  score: number;
  snippet: string;
}

// --- popup -> background ---

export type PopupToBackgroundMessage =
  | { type: "INDEX_PAGE" }
  | { type: "ASK"; question: string };

export type BackgroundToPopupResponse =
  | { ok: true; kind: "INDEX_PAGE"; documentsIngested: number; chunksCreated: number }
  | { ok: true; kind: "ASK"; answer: string; sources: AskSource[] }
  | { ok: false; error: string };

// --- background -> content script ---

export type BackgroundToContentMessage = { type: "EXTRACT_PAGE_TEXT" };

export interface ExtractedPage {
  url: string;
  title: string;
  text: string;
}
