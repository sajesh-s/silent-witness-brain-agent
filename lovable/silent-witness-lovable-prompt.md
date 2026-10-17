# Lovable prompt — Silent Witness Studio

**Before pasting:** connect Lovable to the Supabase project where you already ran `silent-witness-database.sql` and `002_brand_context.sql` (Lovable → Integrations → Supabase). Then paste everything below the line as your first prompt.

---

Build **"Silent Witness Studio"**, a private web app where I send requests to my multi-AI content team, review what it produces, and track my content across a seven-stage framework.

## Important: the database already exists
The Supabase schema has already been created with SQL. **Do not create, drop or alter any tables, enums, views, functions or policies.** Generate TypeScript types from the existing schema and use it as-is:

- `stages` (id 1–7, slug, name, core_question, orientation, description, content_guidelines) — read only
- `series` (id, name, track, description) — read only
- `content_items` — the content library. Key columns: id, owner_id, title, summary, body, track (`content_track` enum: spiritual, kids, builder, lifestyle), format (`content_format` enum: reel, short, post, carousel, story, long_video, guided_meditation, sleep_video, music, kids_story, coloring_page, article, recipe, script), series_id, episode_number, primary_stage, secondary_stages (smallint[]), themes, practices, traditions (text[]), audience, language, duration_seconds, status (`content_status` enum: idea, draft, in_review, approved, scheduled, published, archived), critic_score, critic_feedback, revision_rounds, uniqueness_note, ai_contributions (jsonb), synthetic_media (bool), source_request_id, target_channels (`channel[]` enum: yt_meditation, yt_builder, instagram, amazon_kdp, app), app_visible (bool), created_at, updated_at. **Never select or send the `embedding` or `search_text` columns.**
- `assets` (id, content_item_id, kind, storage_path, tool, duration_seconds, width, height, created_at)
- `publications` (id, content_item_id, channel, external_id, url, published_at, metrics jsonb, metrics_updated_at)
- `ai_requests` (id, user_id, session_id, message, stage, track, format, status: pending | processing | done | error, response, content_item_id, created_at, updated_at) — users can only INSERT and SELECT their own rows
- `brand_context` (slug, title, content markdown, applies_to text[] with values all | spiritual | kids | builder | lifestyle, sort_order, active, updated_at) — the brand bible the AI reads; logged-in users can read and edit
- View `stage_coverage` (stage_id, name, core_question, total, published, in_pipeline, drafts)
- RPC `search_library(q text, stage_filter int, max_results int)`
- RPC `get_brand_context(p_track text)` returns `{ track, sections, content }` — the combined brand text the AI receives for a track

Row Level Security is already configured. The browser must only use the Supabase anon key with the logged-in user's session. **Never call any AI API or webhook from the browser** — the backend (n8n) reacts to new `ai_requests` rows by itself.

## Auth
Email magic-link login with Supabase Auth. Every page requires login.

## Layout
Left sidebar on desktop, bottom tab bar on mobile, with four sections: **Studio** (chat), **Library**, **Journey**, **Brand**. Show the logged-in email and a sign-out button.

## 1. Studio (chat) — `/`
- Chat thread: my messages on the right, AI replies on the left.
- Render AI replies as **Markdown** (headings, lists, bold, blockquotes), with a **Copy** button on each reply.
- A compact **settings bar** above the input with three dropdowns, all defaulting to **Auto** (sent as `null`):
  - **Stage**: Auto, then "1 · Survival" … "7 · Liberation / Realization", loaded from `stages`. Show the stage's `core_question` as a helper line when one is selected.
  - **Track**: Auto, Spiritual, Kids (Aadu & Coco), Builder, Lifestyle.
  - **Format**: Auto plus all `content_format` values with friendly labels (e.g. guided_meditation → "Guided meditation").
- Input: multi-line textarea (Enter sends, Shift+Enter adds a new line) and a Send button.
- Quick-start chips: "5 reels for Stage 5 · Awareness", "Full guided meditation on letting go", "Aadu & Coco story about patience", "Builder video: how I built my AI brain", "What have we already made about gratitude?".
- On send: insert `{ session_id, message, stage, track, format }` into `ai_requests`.
- **New conversation** button: new `session_id` via `crypto.randomUUID()`, clears the thread. Persist the current session_id in localStorage (wrap in try/catch).
- On load, fetch the current session's `ai_requests` ordered by `created_at`.
- Subscribe with Supabase Realtime to INSERT and UPDATE on `ai_requests` filtered by `user_id=eq.<my id>` and update bubbles live.
- While `pending` show "Thinking…", while `processing` show "Working with the team…" with a typing animation and a hint: "Full scripts can take a few minutes."
- If `status = error`: show the response in a soft red bubble with **Retry** (inserts the same message and settings again).
- If a reply has `content_item_id`: show a chip **"Saved to library → Open"** linking to that item.

## 2. Library — `/library` and `/library/:id`
- **Stage pills** across the top: All, 1–7 (number + name; tooltip with the core question), and "No stage". Filters on `primary_stage`.
- Filters: Track, Format, Status (multi-select), and "In app" toggle (`app_visible`).
- **Search box** that calls RPC `search_library` (debounced 300 ms); when empty, query `content_items` directly with the filters, newest first.
- Grid of cards: title, stage badge (colour per stage), format, track, status badge, critic score (e.g. "9.0 / 10"), summary (2 lines), updated date. Realtime-subscribe to `content_items` so new items appear without refresh.
- **Detail page** `/library/:id`:
  - Header: title (editable inline), stage badge, track, format, status dropdown, critic score.
  - Body rendered as Markdown with **Edit** (textarea) and **Copy** buttons.
  - Sidebar panels:
    - **Tags**: primary stage (select), secondary stages (multi-select 1–7), themes, practices, traditions (editable chip inputs), audience, target channels (multi-select), series (select from `series`), episode number.
    - **Quality**: critic score, revision rounds, critic feedback (collapsible), uniqueness note, AI contributions (small key/value list), `synthetic_media` toggle with a note: "Disclose realistic AI visuals or voice on YouTube".
    - **App**: `app_visible` toggle — only allowed when status is `published` (otherwise disabled with an explanation).
    - **Publications**: list rows from `publications`; an **Add publication** form (channel select, URL, external id, published date) that inserts a row and, if the item isn't published yet, sets its status to `published`.
    - **Assets**: list from `assets` (kind, tool, link) and an "Add asset link" form (kind, URL as `storage_path`, tool).
  - Status workflow buttons for quick moves: draft → in_review → approved → scheduled → published, plus Archive.
  - Save edits with optimistic UI and a toast; show errors clearly.

## 3. Journey — `/journey`
- Seven horizontal **stage cards** in order (Survival → Liberation / Realization), each showing the stage name, core question, and counts from `stage_coverage`: published, in pipeline, drafts. A thin stacked bar per stage visualises the three counts.
- Highlight stages with **zero published items** as gaps with a "Create for this stage" button that opens Studio with that Stage preselected.
- Below: "Recently published" (last 10 `publications` joined to item titles) and "Awaiting review" (items with status `in_review`, highest critic score first).

## 4. Brand — `/brand`
This is where I maintain the brand bible that every AI in the system reads.
- List of `brand_context` sections ordered by `sort_order`: title, "Used for" chips (`applies_to`), active toggle, last updated.
- Section editor: title, markdown content (side-by-side editor and rendered preview on desktop, tabs on mobile), `applies_to` multi-select (all, spiritual, kids, builder, lifestyle), sort order, active toggle. Save with a toast; show a warning before leaving with unsaved changes.
- **"Preview what the AI sees"**: a track selector (spiritual, kids, builder, lifestyle) that calls RPC `get_brand_context` and shows the combined markdown plus the section count.
- Add new section (slug auto-generated from the title, lowercase with dashes) and a confirm-before-deactivate flow (no hard delete).

## Design
Match The Silent Witness brand: dark, minimalist, cinematic, black and gold.
- Near-black background (#0B0B0C), raised surfaces (#151517), hairline borders (#2A2A2E), warm off-white text (#EDE8DF), muted secondary text (#9A958C), gold accent (#C9A54C) for primary actions, focus rings and highlights. Use a soft golden halo glow sparingly as the logo motif (a simple dark silhouette with a gold ring) in the sidebar.
- Seven stage colours, muted to sit on black and progressing from earthy to luminous: 1 terracotta, 2 clay, 3 amber, 4 sage, 5 teal, 6 indigo, 7 soft violet — used for badges and pills with accessible contrast.
- Serif for AI replies and content bodies (e.g. Cormorant Garamond or Lora), clean sans for UI (e.g. Inter). Generous spacing, restrained typography, subtle borders, no heavy shadows, plenty of breathing room.
- A light theme option in settings (warm cream background, near-black text, same gold accent), default dark.
- Fully responsive and good on mobile.
