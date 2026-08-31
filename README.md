# ContextOS

ContextOS is a context-aware AI knowledge system that combines hybrid RAG,
temporal retrieval, and knowledge graphs to connect information across a
person's heterogeneous data sources -- documents, notes, emails, calendar,
and tasks -- so questions like *"what decisions did I make about my thesis
last month, and what tasks are still unresolved?"* can be answered by
reasoning across sources, not just matching a single chunk of a single file.

It ships as a **Chrome extension (Manifest V3, TypeScript)** for the UI --
so it can index whatever page you're actually looking at (webpages, Gmail,
Google Docs, in-browser notes apps) alongside files, which is what the
multi-source ingestion goal below needs -- talking to a local
**Python/FastAPI backend** (run via Docker Compose) that does the actual
chunking, embedding, retrieval, and LLM work.

> **Status: working skeleton, not a finished product.** This repo implements
> one real, complete, end-to-end slice (see below) and scaffolds the rest of
> the target architecture as clearly-labeled stubs -- see
> [Implemented vs. stubbed](#implemented-vs-stubbed) and
> [Roadmap / stubbed modules](#roadmap--stubbed-modules).

## Architecture

```
                         ┌─────────────────────────────┐
                         │   Chrome Extension (MV3)     │
                         │                              │
                         │  content.ts  ── extracts     │
                         │    current page's text       │
                         │       │ chrome.tabs.sendMessage
                         │       ▼                      │
                         │  background.ts (service      │
                         │   worker) ── the only place   │
                         │   that calls fetch() or       │
                         │   messages content scripts    │
                         │       ▲ chrome.runtime.sendMessage
                         │       │                      │
                         │  popup/ (React + Tailwind)   │
                         │   - "Index This Page" button │
                         │   - question input           │
                         │   - answer + citations view  │
                         └───────────────┬──────────────┘
                                         │ HTTP (fetch, background worker only)
                                         ▼
                         ┌─────────────────────────────┐
                         │   backend/  (FastAPI, :8000) │
                         │   CORS enabled for extension  │
                         │                              │
                         │  routers/ingest  ──► chunk + embed
                         │  routers/query   ──► embed question,
                         │                       pgvector search,
                         │                       call LLM
                         │  routers/graph   ──► STUB (empty list)
                         │                              │
                         │  retrieval/ (bm25, hybrid,   │
                         │              temporal) STUBS │
                         │  analysis/  (contradiction,  │
                         │              tasks, timeline)│
                         │              STUBS           │
                         └───┬──────────┬───────────┬───┘
                             │          │           │
                    ┌────────▼───┐ ┌────▼─────┐ ┌───▼────┐
                    │  Postgres  │ │  Redis   │ │ Neo4j  │
                    │ + pgvector │ │ (unused  │ │ (STUB, │
                    │ documents  │ │  yet)    │ │ empty) │
                    │  + chunks  │ │          │ │        │
                    │ + embeddings│ │          │ │        │
                    └────────────┘ └──────────┘ └────────┘
```

## The working end-to-end slice

1. Click **"Index This Page"** in the popup. The popup asks the background
   service worker to index the current tab; the background worker messages
   the content script (`extension/src/content.ts`) to extract the page's
   `document.title` + `document.body.innerText`, then POSTs it to
   `POST /ingest/documents` as `{path: <page URL>, content: <extracted text>}`
   (the `path` field just holds a URL here -- no backend schema change
   needed).
2. The backend chunks the text (`app/chunking.py`), embeds every chunk
   locally with a HuggingFace `sentence-transformers` model
   (`app/embeddings.py`), and stores chunks + embeddings in
   Postgres+pgvector (`app/models.py`), upserting by path/URL.
3. Type a question into the popup and hit **Ask**. The popup messages the
   background service worker, which POSTs to `POST /query/ask` (the popup
   never calls the backend directly).
4. The backend embeds the question, runs a pgvector cosine-similarity search
   for the top-k chunks, assembles a context block, calls the configured LLM
   (Google Gemini by default, Anthropic Claude or OpenAI as alternates) with
   the question + context, and returns a grounded answer plus cited sources.
5. The popup renders the answer and its citations (rendered as clickable
   links when a citation's path is a URL).

That's it -- single data source (the page you're currently on), single
retrieval signal (vector similarity), no graph, no timeline, no
task/contradiction analysis. Everything past that is scaffolded, not built.

## Implemented vs. stubbed

**Implemented (real, working code):**
- Page text extraction + "Index This Page" flow (`extension/src/content.ts`, `extension/src/background.ts`)
- Chunking (`backend/app/chunking.py`)
- Local embeddings via sentence-transformers (`backend/app/embeddings.py`)
- Postgres + pgvector storage (`backend/app/models.py`, `backend/app/db.py`)
- Vector similarity search + LLM answer + citations (`backend/app/routers/query.py`)
- Gemini/Anthropic/OpenAI provider abstraction (`backend/app/llm/client.py`)
- Ask popup UI (`extension/src/popup/`)

**Stubbed (interface/module scaffolded, `NotImplementedError` or empty
result, no fake data):**
- **Neo4j knowledge graph** -- `backend/app/graph.py` + `GET /graph/entities`
  always returns `[]`. See its docstring for what real entity/relationship
  extraction would do.
- **BM25/keyword retrieval** -- `backend/app/retrieval/bm25.py`
- **Temporal retrieval** -- `backend/app/retrieval/temporal.py`
- **Hybrid retrieval fusion** (vector + BM25 + graph + temporal) --
  `backend/app/retrieval/hybrid.py`
- **Contradiction detection** -- `backend/app/analysis/contradiction.py`
- **Automatic task extraction** -- `backend/app/analysis/tasks.py`
- **Timeline construction** -- `backend/app/analysis/timeline.py`
- Redis is provisioned in `docker-compose.yml` but nothing reads/writes it
  yet (reserved for future caching / job-queue use).

## Roadmap / stubbed modules

The full target feature set, and where each piece would live once built:

| Feature | Where it would live | Status |
|---|---|---|
| Multi-source ingestion (PDFs, emails, webpages, calendar, tasks -- not just workspace text files) | new `backend/app/ingestion/` sources, feeding the existing `routers/ingest.py` pipeline | Not started |
| Hybrid retrieval: vector + BM25/keyword + knowledge graph + temporal, fused | `backend/app/retrieval/hybrid.py` (fusion stub), `bm25.py`, `temporal.py` | Stub only |
| Automatic knowledge-graph construction (entity + relationship extraction) | `backend/app/graph.py` | Stub only |
| Timeline of decisions/events, "why did I make this decision?" retrieval | `backend/app/analysis/timeline.py` | Stub only |
| Contradiction detection between documents | `backend/app/analysis/contradiction.py` | Stub only |
| Automatic task extraction | `backend/app/analysis/tasks.py` | Stub only |
| Source citations for every answer | `backend/app/routers/query.py` | **Implemented** (working slice) |

None of the "Stub only" rows contain placeholder/fake logic -- each stub
module has a clear TODO docstring describing the intended design and raises
`NotImplementedError` (or, for the Neo4j endpoint, returns `[]`) rather than
returning made-up results.

## Quickstart

1. Copy `.env.example` to `.env` and fill in at least one LLM provider API
   key (`GEMINI_API_KEY` by default, or set `LLM_PROVIDER=anthropic`/`openai`
   and fill in the matching key).

2. Start the backend + datastores:

   ```bash
   docker compose up -d
   ```

   This starts Postgres (with pgvector), Redis, Neo4j, and the FastAPI
   backend on `http://localhost:8000`. Check `http://localhost:8000/health`.

3. Build the extension (background/content bundle + popup app):

   ```bash
   cd extension
   npm install
   npm run build
   ```

   This produces a complete unpacked extension at `extension/dist/`
   (`manifest.json`, `background.js`, `content.js`, `popup/`).

4. Load it into Chrome: open `chrome://extensions`, enable **Developer
   mode**, click **Load unpacked**, and select `extension/dist`.

5. Open any webpage, click the ContextOS icon, click **Index This Page**,
   then ask a question.

### Notes

- `GEMINI_MODEL` defaults to `gemini-2.5-flash`. Provider model ids change
  over time -- if requests start failing with a model-not-found error, check
  the current available model id for your configured `LLM_PROVIDER` and
  update `.env` (or the default in `backend/app/config.py`).
- No extension icon assets are included -- `manifest.json` omits the
  `icons` key, so Chrome shows a generic icon. Add real icons before any
  Chrome Web Store submission.
- Packaging for the Chrome Web Store (zipping `dist/`, a developer account,
  store listing) is out of scope here; see `extension/README.md`.
- `docker compose up` was not run as part of building this scaffold (Docker
  may not be available in every environment) -- verify it yourself once
  Docker is available.
