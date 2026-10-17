# Changelog

## v1.1 — 2026-10-17
Brand context: the knowledge previously locked in ChatGPT's memory is now shared by every model.

- **Brand bible:** curated from the ChatGPT handoff into 10 sections (mission, Silent Witness voice and audience, framework principles, claims and boundaries, formats, visual identity, Aadu & Coco series bible, founder story, builder channel, things to avoid). Private details removed; unconfirmed items listed as open decisions. `docs/brand-bible.md`, generated with `db/002_brand_context.sql` from `scripts/brand_sections.py`.
- **Database:** `brand_context` table and `get_brand_context(track)` function; re-running never overwrites edits.
- **Pipeline:** fetches the brand context for the track; ideas, draft and critic follow it. Critic now checks claims and boundaries, recognition-before-instruction, one central idea, and Aadu & Coco storytelling and character consistency. Updated reel, carousel and kids-story format rules (one idea per slide, follow-conversion lesson, 4:5). Default audience updated. Hard-coded brand voice removed from Config.
- **Agent:** brand summary in its instructions and a new `brand_guide` tool it must use before writing content itself.
- **Lovable:** new Brand page to edit sections and preview what the AI sees per track; Studio redesigned in the Silent Witness black-and-gold identity.
- **Setup:** run the brand script; disable public sign-ups after creating your account.

## v1.0 — 2026-10-17
First complete version of the Multi-AI Brain.

- **Database:** seven stages with content guidelines; content library with tags, critic data, originality note and embeddings; assets; publications; website requests linked to the content they produce; `search_library` and `match_content` functions; `stage_coverage` and `app_library` views; Row Level Security; Realtime.
- **Content Pipeline (n8n):** Gemini research → ChatGPT ideas → Claude draft → Gemini critic with up to 2 revision rounds → saved to library with auto-tagging, embedding and similarity check.
- **Brain Agent (n8n):** Claude executive with tools for library search, research, brainstorming, saving short content, and running the full pipeline; triggered by Supabase Database Webhook.
- **Lovable prompt:** Studio (chat with stage/track/format), Library (filter, edit, review, publish) and Journey (stage coverage) pages.
