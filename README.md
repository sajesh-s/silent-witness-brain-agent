# Silent Witness — Multi-AI Brain

A multi-model AI content system modelled loosely on how the brain divides work. Claude plans and writes, Gemini researches and critiques, ChatGPT brainstorms, and a shared Supabase library acts as memory. Everything it makes feeds the Silent Witness channels and, later, the Silent Witness app.

> Private repository. Contains brand prompts and framework content — do not make public without removing them.

## How it works

| Brain analogy | Component | Role |
|---|---|---|
| Prefrontal cortex (executive) | Claude — n8n AI Agent | Plans, chooses specialists, integrates results |
| Sensory cortex (perception) | Gemini + Google Search | Research and fact-checking |
| Default mode network (divergent ideas) | ChatGPT | Hooks, titles, angles, metaphors |
| Anterior cingulate (error detection) | Gemini critic | Scores drafts, enforces stage guidelines, triggers revisions |
| Hippocampus / global workspace (memory) | Supabase content library + embeddings | Stores, tags, searches and de-duplicates all content |
| Semantic memory (identity, values) | `brand_context` brand bible | Voice, audience, framework principles, claims rules, Aadu & Coco bible — read by every model |
| Basal ganglia (learned routines) | n8n Content Pipeline | The reliable research → write → critic → revise routine |

```
Lovable Studio ──▶ ai_requests ──Database Webhook──▶ Brain Agent (Claude)
                                                      ├─ search_library
                                                      ├─ research_gemini
                                                      ├─ brainstorm_chatgpt
                                                      ├─ save_short_content
                                                      └─ write_full_script ─▶ Content Pipeline
                                                                               research → ideas → draft
                                                                               → critic ↻ revise (max 2)
                                                                               → save + tag + embed
content_items (library) ◀───────────────────────────────────────────────────────┘
      ▼
Lovable Library / Journey  ──later──▶  Silent Witness app (reads app_library view)
```

## The seven stages

| # | Stage | Core question |
|---|---|---|
| 1 | Survival | How do I get through this? |
| 2 | Stability | How do I become secure? |
| 3 | Achievement / Growth | What can I accomplish? |
| 4 | Meaning | What is it all for? |
| 5 | Awareness | Why am I the way I am? |
| 6 | Awakening | Who am I beneath all of this? |
| 7 | Liberation / Realization | What am I, beyond the separate self? |

Each stage carries content guidelines in the `stages` table; the writer and critic follow them. A reflective framework, not a scientifically validated sequence.

## Outputs

- **Meditation YouTube** — guided meditations, sleep videos
- **Builder YouTube** — how the system was built
- **Instagram** — reels, posts, carousels across the seven stages
- **Aadu & Coco** — kids stories, Instagram series, KDP coloring books
- **Silent Witness app** — reads published, app-visible content from the library

## Repository layout

```
db/        silent-witness-database.sql     Complete Supabase schema (idempotent)
           002_brand_context.sql           Brand bible table, seed and get_brand_context()
n8n/       silent-witness-content-pipeline.json
           silent-witness-brain-agent.json
lovable/   silent-witness-lovable-prompt.md   Prompt for the Studio / Library / Journey / Brand site
docs/      SETUP.md                          Step-by-step setup and troubleshooting
           brand-bible.md                    Readable brand bible + open decisions
scripts/   sanitize_n8n_export.py            Clean n8n exports before committing
           brand_sections.py                 Source of the brand bible; regenerates docs + seed SQL
```

## Setup

See [docs/SETUP.md](docs/SETUP.md). Order: database (both scripts) → pipeline → agent → Supabase webhook → Lovable → disable sign-ups.

The brand bible ([docs/brand-bible.md](docs/brand-bible.md)) was curated from years of ChatGPT conversations so that every model, not just one vendor's app, shares the same context.

## Working with this repo

- **Changing a workflow:** edit in n8n → *Download* the workflow → run
  `python3 scripts/sanitize_n8n_export.py path/to/export.json` → replace the file in `n8n/` → commit.
- **Changing the database:** keep `db/silent-witness-database.sql` idempotent (safe to re-run). For larger changes, add numbered migration files (`db/002_*.sql`).
- **Never commit secrets:** API keys, the Supabase service_role key, webhook secrets or `.env` files. Use `.env.example` to document what's needed.
- Note changes in [CHANGELOG.md](CHANGELOG.md).

## Tech stack

n8n · Supabase (Postgres, pgvector, Realtime, Auth) · Lovable · Anthropic Claude · Google Gemini · OpenAI
