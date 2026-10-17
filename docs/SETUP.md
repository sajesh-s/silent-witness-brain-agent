# Silent Witness — Multi-AI Brain: setup guide

## What's in this package

| File | What it is | Where it goes |
|---|---|---|
| `db/silent-witness-database.sql` | Complete database: seven stages with guidelines, content library, assets, publications, website requests, search + similarity functions, Journey view, security, realtime | Supabase SQL Editor |
| `db/002_brand_context.sql` | The brand bible every AI reads (voice, audience, framework principles, claims rules, formats, Aadu & Coco bible, things to avoid) | Supabase SQL Editor (after the first script) |
| `docs/brand-bible.md` | Readable version of the same brand bible, plus open decisions | Read and review |
| `n8n/silent-witness-content-pipeline.json` | Research → ideas → draft → critic → revision loop → save to library (tags, embedding, originality check) | n8n (import) |
| `n8n/silent-witness-brain-agent.json` | Claude as executive: decides when to research, brainstorm, search the library, write short content or run the full pipeline | n8n (import) |
| `lovable/silent-witness-lovable-prompt.md` | Studio (chat), Library and Journey website | Lovable (paste) |

## How it flows

```
Lovable Studio ──insert──▶ ai_requests ──Database Webhook──▶ n8n Brain Agent (Claude)
                                                              │  search_library / research_gemini /
                                                              │  brainstorm_chatgpt / save_short_content
                                                              └─▶ write_full_script ─▶ Content Pipeline
                                                                                        │
content_items (library) ◀── saved, tagged, embedded, similarity-checked ◀───────────────┘
        │                              ai_requests.response ◀── answer written back
        ▼                                     │
Lovable Library + Journey  ◀── realtime ──────┘          (later: the public app reads app_library)
```

## Before you start — accounts and keys
- Supabase project (the one Lovable is connected to, or a new one)
- n8n (Cloud or self-hosted, a recent version with AI Agent and `$fromAI` support)
- API keys: Anthropic, OpenAI, Google Gemini (Google AI Studio)

## Step 1 — Database (Supabase)
1. Supabase → **SQL Editor** → New query → paste all of `silent-witness-database.sql` → **Run**.
2. New query → paste all of `002_brand_context.sql` → **Run**. (Re-running it never overwrites sections you edited later.)
3. Check: **Table Editor** shows `stages` (7 rows), `series` (3 rows), `brand_context` (10 rows), `content_items`, `assets`, `publications`, `ai_requests`.
4. Note from **Project Settings → API**: the Project URL and the **service_role** key (keep it secret — it is only for n8n).

> If you used the earlier Lovable prompt, `ai_requests` already exists; the script safely adds the new columns.

## Step 2 — n8n credentials (create once)
| Credential | Type | Value |
|---|---|---|
| Gemini | Header Auth | name `x-goog-api-key`, value = Gemini key |
| OpenAI | Header Auth | name `Authorization`, value = `Bearer sk-…` |
| Anthropic (HTTP) | Header Auth | name `x-api-key`, value = Anthropic key |
| Anthropic (Agent) | Anthropic | your Anthropic key |
| Supabase | Supabase API | Project URL + service_role key |
| Webhook secret | Header Auth | name `x-webhook-secret`, value = a long random string |

## Step 3 — Content Pipeline (n8n)
1. Import `silent-witness-content-pipeline.json`.
2. Attach credentials: Gemini → *Gemini - Research*, *Gemini - Critic*; OpenAI → *ChatGPT - Ideas*, *OpenAI - Embedding*; Anthropic (HTTP) → *Claude - Write*; Supabase → *Fetch Stages*, *Fetch Brand Context*, *Save to Library*, *Store Embedding*, *Find Similar*.
3. Open **Config**: set `supabaseUrl` and check model names. (Brand voice, audience and the Aadu & Coco bible come from `brand_context`.)
4. **Save**.

## Step 4 — Brain Agent (n8n)
1. Import `silent-witness-brain-agent.json`.
2. Attach credentials: Webhook secret → *Webhook*; Anthropic → *Claude (Executive)*; Gemini → *research_gemini*; OpenAI → *brainstorm_chatgpt*; Supabase → *brand_guide*, *search_library*, *save_short_content*, *Mark Processing*, *Save Answer*, *Save Error*.
3. In **brand_guide**, **search_library** and **save_short_content**, replace `YOUR-PROJECT` in the URL with your Supabase project.
4. In **write_full_script**, choose *Silent Witness - Content Pipeline* from the Workflow list.
5. **Save** and **Activate**. Copy the Webhook's **Production URL**.

## Step 5 — Connect Supabase to n8n
Supabase → **Database → Webhooks** → Create:
- Table `ai_requests`, events: **Insert** only
- Type HTTP Request, method POST, URL = the n8n Production URL
- HTTP header `x-webhook-secret` = the same secret as in n8n

## Step 6 — Website (Lovable)
1. Connect Lovable to the same Supabase project.
2. Paste `silent-witness-lovable-prompt.md` (the part below the line).
3. In Supabase → **Authentication → URL Configuration**, add your Lovable site URL to the redirect URLs so magic-link login works.
4. Log in once to create your account, then in Supabase → **Authentication → Sign In / Providers**, turn **off** "Allow new users to sign up". You are the only user; anyone else who could sign up could spend your API credits and edit the brand bible.

## Step 7 — Test, in this order
1. "What's in the library?" → quick answer (tests webhook → agent → answer).
2. "Give me 3 reels for Stage 5 about noticing anger" → short content saved as drafts (check Library).
3. "Full guided meditation on letting go, about 10 minutes" → pipeline runs 1–4 minutes; the reply shows score, rounds and similarity; the item appears in Library as *in_review*.
4. Open Journey → Stage 5 shows the new items.

## Troubleshooting
- **Reply stuck on "Thinking…"** → Supabase webhook not firing or secret mismatch: check n8n *Executions* and Supabase *Database → Webhooks → logs*.
- **Stuck on "Working with the team…"** → open the Brain Agent execution in n8n; a failed tool shows the error.
- **Library empty but reply says saved** → the pipeline used a different Supabase project URL in *Config*, or owner_id is missing (it comes from the logged-in user).
- **401/403 from Supabase in n8n** → use the service_role key, not the anon key.
- **Model errors** → update model names in *Config* and in the agent's tool nodes to models your keys can access.

## Keeping the brand bible current
- Edit sections in the Studio's **Brand** page; the next request uses the new text. "Preview what the AI sees" shows exactly what each track receives.
- To also keep the repo copy in sync, edit `scripts/brand_sections.py`, run `python3 scripts/brand_sections.py`, and commit. (New installs seed from it; existing rows are never overwritten.)
- Resolve the **Open decisions** at the end of `docs/brand-bible.md` when you can.

## Good habits
- Review everything in *in_review* before publishing; the critic is a filter, not a final authority.
- Set `synthetic_media` on items with realistic AI visuals or voice and disclose it on YouTube.
- Use **Journey** weekly to spot empty stages.
- Record your screen while building — that's your Builder channel.
