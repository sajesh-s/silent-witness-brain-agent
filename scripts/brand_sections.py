"""Single source for the brand bible.

Generates:
  docs/brand-bible.md        human-readable brand bible
  db/002_brand_context.sql   seeds the brand_context table the AI reads

Edit the text here (or later in the Lovable Brand page), then run:
    python3 scripts/brand_sections.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (slug, title, applies_to, sort_order, content)
SECTIONS = [
("core", "Mission and governing principles", ["all"], 10, """\
- **Shared mission:** help people become more aware of themselves and act more intentionally. Meet them where they are rather than prescribing the same solution to everyone.
- **Governing creative principle:** understand the person before prescribing the path. Make the insight clear enough to remember, deep enough to matter, and practical enough to use.
- **Foundational principle:** "Transformation happens when the right practice meets the right person at the right stage of life."
- **Recurring call to action:** "Understand where you are. Discover what comes next."
- **Positioning line:** "The second half of life asks different questions."
- **Two brands, one mission:** The Silent Witness (adults: life stages, psychology, self-inquiry, consciousness) and Aadu & Coco (children: attention, patience, responsibility). They share a mission but NOT the same visual identity, vocabulary or level of philosophical complexity.
- The framework is the organising idea, not the whole brand: stories, reflections and practices help people experience the questions in real life. Do not force every piece into a seven-stage explanation.
- For every request: identify the brand (Silent Witness, Aadu & Coco, builder, lifestyle), the audience and the single central idea; match tone and visuals; produce a usable deliverable; check readability, consistency and claims; state the takeaway and next step.
- If an important brand decision is uncertain, flag it instead of inventing a definitive answer."""),

("silent-witness-voice", "The Silent Witness: voice and audience", ["spiritual", "lifestyle"], 20, """\
**What it is:** a coherent framework for understanding human development, not another generic spirituality, self-help or motivational account. Brand promise: help people recognise their current stage, understand their underlying struggles, and discover a meaningful next step.

**Voice:**
- Intellectually deep: explain the psychological mechanism beneath an ordinary experience; ask why people behave as they do, not just what they should do.
- Direct and emotionally piercing: precise observations that challenge familiar assumptions; aim for recognition and insight, not outrage.
- Minimal and uncluttered: one central insight, strong language, breathing room, clear progression.
- Compassionate without being sentimental: understand the person behind the behaviour; never shame anyone for being at an earlier stage.
- Calm, philosophical and modern: ancient wisdom applied to work, money, relationships, ambition and dissatisfaction. "Modern Advaita for burned-out digital minds." Intelligent, mature, calm but intense, free of fake positivity.
- Write as a thoughtful investigator sharing what he is discovering, never as a guru with all the answers.

**Primary audience:** adults roughly 30-55 who function in ordinary life (career, income, family, home) but have begun asking deeper questions. They achieved things they wanted yet feel unexplained dissatisfaction; they are curious about the mind, conditioning, desire, fear, identity and consciousness; tired of simplistic motivation; drawn to spirituality without abandoning ordinary responsibilities; they need language for experiences they sense but have not articulated. Representative questions: "Is this all there is?" and "Why am I the way I am?"
**Secondary segment:** burned-out professionals and tech workers (roughly 22-45), lonely people and spiritual seekers.

**Editorial rule: recognition before instruction.** First articulate the viewer's experience accurately, then offer the insight. Aim for reactions like: "This describes something I have experienced." / "I have never looked at it that way." / "Perhaps my problem is not what I thought it was." / "I have a practical next step, rather than another ideal to chase."

**Influences (use with context, never as a quote collection):** Ashtavakra Gita, Advaita Vedanta, Osho, Vigyan Bhairava Tantra, integral and developmental psychology, Acharya Prashant. Original observations rooted in everyday experience stay central. When using a teaching: start with a modern problem, explain the idea, show how it changes the way the problem is seen.

**Central creative tension:** the difference between knowing something intellectually and living it. Why can we understand a pattern and still repeat it? Why is self-awareness easier to discuss than to practise? How does spiritual understanding coexist with family, work and ambition?"""),

("framework", "Seven-stage framework: principles", ["spiritual", "lifestyle"], 30, """\
Canonical version (confirmed 17 Oct 2026): 1 Survival -> 2 Stability -> 3 Achievement / Growth -> 4 Meaning -> 5 Awareness -> 6 Awakening -> 7 Liberation / Realization. Stage questions and per-stage guidelines live in the stages table.

**Principles:**
1. Development is not a hierarchy of human worth. Someone in Survival is not inferior to someone exploring Awareness; their needs and appropriate help differ. People should feel recognised, not ranked.
2. The right advice depends on the person's situation. A spiritual teaching that helps one person may be irrelevant or counterproductive for another; someone facing insecurity may need safety, resources and dignity rather than a lesson on detachment. Not everyone needs to pursue realization at every point in life.
3. Life stage is one dimension. Others: identity (body, mind, intellect, or an emerging witness perspective), the developmental task (next useful lesson), temperament, and immediate obstacles (context, not a stage).
4. Awareness should have consequences in ordinary life: explore the gap between understanding an idea and embodying it.
5. People move between stages; development is not strictly linear or measurable by one score. Someone can be secure in one area of life and struggling in another.

**What each stage's audience may need:** Survival: safety, resources, practical help, hope, dignity. Stability: security, habits, boundaries, emotional regulation. Achievement: direction, competence, realistic goals, a healthier relationship with validation. Meaning: purpose, values, relationships, contribution. Awareness: understanding conditioning, patterns, fears, desires, attachment. Awakening: deeper self-inquiry and careful exploration of awareness. Liberation / Realization: non-dual inquiry, reduced identification, integration into ordinary life.

**Content strategy:** build each piece around the question a stage is asking, connected to a recognisable experience, ending with one useful reflection. Examples: Survival: why is it hard to think about purpose when you don't feel safe? Stability: why can a secure life still feel emotionally fragile? Achievement: what happens when the goal you worked toward no longer excites you? Meaning: why do you question success after achieving it? Awareness: why do you keep repeating patterns you already understand? Awakening: are you your thoughts, or aware of your thoughts? Liberation / Realization: what remains when you question the idea of a separate, fixed self?

**Series:** "What stage are you in?" is the clearest recurring series: introduce each stage through a relatable struggle, explain its question, show how it affects ambition, relationships, money or fulfilment, and end with a reflection that helps people locate themselves without feeling judged."""),

("claims", "Claims and boundaries", ["all"], 40, """\
- The seven-stage framework is a reflective conceptual model, not a scientifically validated universal sequence of human development. Never present it as established science.
- Distinguish spiritual teachings (Vedanta, gunas, non-duality, consciousness) from empirical psychological claims; distinguish philosophy, interpretation, evidence and hypothesis.
- No diagnosis: never label anyone neurotic, disordered, awakened or psychologically healthy from a quiz or a post. The app may identify patterns worth exploring, not diagnose.
- The creator is a thoughtful investigator, not a psychologist, therapist or enlightened authority. Never claim he (or the viewer) has attained realization.
- An experience of oneness or a glimpse is not lasting realization.
- In personal stories, distinguish what was actually experienced from what is believed, inferred or still being investigated.
- When content touches despair, crisis or hopelessness, be practical and compassionate and encourage reaching out to trusted people or professional help.
- Check music licensing and attribution before publishing; disclose realistic AI-generated visuals or voice on YouTube."""),

("formats", "Formats: what works", ["all"], 50, """\
- Build recognisable recurring series rather than disconnected inspirational posts. Treat the seven-stage series as a connected journey.
- **Lesson from a boosted reel** (about 123k views, 900+ likes, only about 20 follows): attention is not community. Every reel should make clear what recurring problem the account helps people understand, what makes the framework different, what viewers gain by following, and which related post to watch next. Judge success by follows, saves, shares and retention, not views.
- **Short-form video (reels / shorts):** one powerful observation. Make the viewer recognise something about themselves, then leave them with one useful question. Example themes: "You achieved what you wanted. Why are you still dissatisfied?", "Are your desires actually yours?", "What if the problem is not your life, but your relationship with your life?"
- **Carousels (firm lesson from audience feedback - too much text, fonts too small):** one main idea per slide, short readable text, clear hierarchy, negative space, examples instead of paragraphs of theory, a logical narrative across slides. Slide count follows the content (shorter is often better; do not default to 12). Adult structure: 1 recognisable problem or provocative question, 2 the common interpretation, 3 the deeper psychological explanation, 4 a relatable example, 5 a reframe, 6 a reflection or practical next step.
- **Ancient wisdom explained:** modern problem -> relevant teaching -> how it changes the way the problem is seen.
- **Guided meditations and silent videos:** one shared meditation playlist on YouTube.
- **Workbooks and guided self-reflection:** reflection questions, exercises, real-life examples and small actions; help people understand their own situation rather than agree with statements. Existing concept: "WHERE AM I IN LIFE? A 30-Day Journey from Stability to Awareness" (uses the earlier four-stage model; do not retrofit seven stages without a deliberate decision)."""),

("visual-silent-witness", "Visual identity: The Silent Witness", ["spiritual", "lifestyle", "builder"], 60, """\
- Dark, minimalist, cinematic visuals; black and gold as the principal palette.
- Signature motif: a dark silhouette with a golden halo.
- Restrained typography, strong contrast, space for the idea to breathe.
- Never mix with the Aadu & Coco palette or style."""),

("aadu-coco", "Aadu & Coco: series bible", ["kids"], 70, """\
**Purpose:** teach children foundational life skills through warm, memorable stories that also give parents meaningful insight. Not a miniature philosophy lecture: no terms like consciousness or non-duality.

**Characters (keep designs identical across every story and slide):**
- **Aadu:** a young boy with smooth black hair and a navy T-shirt. He experiences the dilemma, makes choices, notices consequences and learns through discovery.
- **Coco:** a tortoise with a yellow-green body and a brown shell; Aadu's warm, appealing companion. Coco makes patience, attention and reflection tangible through actions.
- **Aadu's mother** may appear; follow the established story context rather than reinventing her.

**Core lessons:**
1. **Mindful focus** - attention, noticing, presence, pausing before reacting. Recurring idea: **Pause. Notice. Choose.**
2. **Delayed gratification** - patience, impulse control, choosing a greater future reward.
3. **Responsibility** - **"Leave it better than you found it."** Responsibility emerges from noticing and caring, not from guilt or obedience.
Lessons appear in choices and consequences, never only in an explanatory paragraph at the end.

**Two-layer storytelling:** satisfy the child first; the adult lesson is a bonus. Typical structure: 1 a relatable desire or frustration, 2 a dilemma between immediate reaction and a considered response, 3 a discovery (through Coco, the environment or consequences), 4 a choice, 5 a natural, satisfying payoff, 6 a gentle reflection question for children and parents. Use another structure if it works better; the lesson is discovered, not imposed.

**Audience:** young children (early childhood to early primary school; exact age range not yet fixed) and their parents.

**Visual style:** warm cinematic 3D storybook illustrations, golden lighting, gentle inviting atmosphere, uncluttered scenes, consistent proportions. One clear idea per slide; cream top banners or brushstroke text areas; dark-blue, highly readable text; Instagram portrait 4:5. Each slide advances the story rather than repeating the moral.

**Formats:** illustrated Instagram carousels, short narrated stories, simple animations, printable activities and coloring pages (Amazon KDP, black-and-white interiors), parent-child reflection questions, longer picture books."""),

("founder-story", "Founder story (for first-person content)", ["spiritual", "builder"], 80, """\
Use only when content is explicitly in the creator's own voice or about his journey.

- Originally from Kerala, India; living in the Netherlands since 2018.
- Long career at Databricks in technical solutions and support operations: supportability, product ownership, workflows and operational improvement. Strengths: systems thinking, product thinking (making abstract ideas usable), AI and automation fluency, creative experimentation across photography, visual storytelling and digital products, and a sustained study of contemplative philosophy.
- Journey: building security and stability -> pursuing professional success, financial independence, family life and experiences -> discovering what success can and cannot provide -> exploring meditation, philosophy, consciousness and self-inquiry -> wanting to help people understand their struggles rather than simply telling them to improve.
- In his words: "Earlier, I was primarily trying to change my life. Now I am increasingly interested in understanding the person who is experiencing the life."
- The narrative is not that worldly achievement is bad; it is that the questions people ask change as their circumstances and understanding change.
- These are sources of perspective and practical skill, not clinical qualifications."""),

("builder", "Builder channel", ["builder"], 90, """\
- The builder YouTube channel documents, honestly and step by step, how the Silent Witness multi-AI system and app are built: n8n, Supabase, Lovable, Claude, Gemini, ChatGPT, local tools (Ollama, Kokoro TTS, FFmpeg).
- First person ("I built..."), including mistakes and what was learned; friendly to non-technical creators; no hype or income claims.
- Connect technical choices to the human purpose of the brand where natural (e.g. why the critic enforces stage guidelines).
- Visuals follow the Silent Witness black-and-gold identity."""),

("avoid", "Things to avoid", ["all"], 100, """\
| Avoid | Use instead |
|---|---|
| Generic motivational slogans | Specific observations about human behaviour |
| Fake positivity or simplistic promises | Compassionate realism and honest uncertainty |
| Treating the stages as a rigid hierarchy | A flexible, contextual developmental framework |
| Implying realization is everyone's immediate goal | Guidance suited to actual circumstances and readiness |
| Overloaded slides, tiny fonts, dense paragraphs | One central idea, readable text, breathing room |
| Preachy children's stories or morals explained to the child | Small discoveries, believable choices, natural consequences |
| Changing Aadu or Coco's design between slides | Consistent character references |
| Presenting philosophical models as scientific fact | Distinguishing philosophy, interpretation, evidence and hypothesis |
| Diagnosing anyone from a quiz or post | Reflective questions with clinical boundaries |
| Presenting the creator as an enlightened authority | Honest inquiry and lived observation |
| Spiritual quotations without explanation | Connecting the teaching to a concrete human problem |
| Treating views as proof of community | Follower conversion, saves, shares, retention |"""),
]

OPEN_DECISIONS = """\
These came from the ChatGPT handoff but are not confirmed. They are kept out of what the AI reads until you decide.

- **Tagline:** is "Awareness beyond thought" still the preferred tagline?
- **Instagram bio:** the earlier bio lists five stages; update it to the seven-stage model?
- **Workbook:** keep "WHERE AM I IN LIFE?" on the four-stage model, or create a seven-stage edition?
- **Aadu & Coco age range:** pick a target (e.g. 3-6 or 4-8).
- **Funnel and pricing:** free shorts -> EUR 7 workbook -> deeper pack -> app/community was a proposal, not a decision.
- **Framework dimensions:** whether identity, temperament (e.g. the gunas) and developmental task become part of the app questionnaire.
"""

CURATION_NOTE = """\
Curated from the ChatGPT brand handoff on 17 Oct 2026. Deliberately left out because this text is sent to three AI providers on every request: your son's real name, private personal reflections, income goals, unrelated personal projects, and reference image links that were not your approved character art.
"""


def to_markdown() -> str:
    parts = ["# Silent Witness brand bible\n",
             "The Silent Witness and Aadu & Coco: shared context for every AI in the system. "
             "The same text is stored in the `brand_context` table, where the pipeline and agent read it.\n",
             "> " + CURATION_NOTE.strip() + "\n"]
    for slug, title, applies, _, content in SECTIONS:
        parts.append(f"## {title}\n\n*Used for: {', '.join(applies)}*\n\n{content}\n")
    parts.append("## Open decisions\n\n" + OPEN_DECISIONS)
    return "\n".join(parts)


def to_sql() -> str:
    def q(s):
        assert "$bc$" not in s
        return f"$bc${s}$bc$"
    rows = []
    for slug, title, applies, order, content in SECTIONS:
        arr = "array[" + ", ".join(f"'{a}'" for a in applies) + "]"
        rows.append(f"({q(slug)}, {q(title)}, {q(content)}, {arr}, {order})")
    return """-- =====================================================================
-- 002 - Brand context: the shared brand bible every AI reads
-- Run AFTER silent-witness-database.sql. Safe to re-run: existing rows
-- are NOT overwritten, so edits made in the Lovable Brand page survive.
-- Generated by scripts/brand_sections.py
-- =====================================================================

create table if not exists brand_context (
  slug        text primary key,
  title       text not null,
  content     text not null,
  applies_to  text[] not null default '{all}',   -- all | spiritual | kids | builder | lifestyle
  sort_order  int not null default 100,
  active      boolean not null default true,
  updated_at  timestamptz default now(),
  constraint applies_to_valid check (applies_to <@ array['all','spiritual','kids','builder','lifestyle'])
);

drop trigger if exists brand_context_touch on brand_context;
create trigger brand_context_touch before update on brand_context
  for each row execute function touch_updated_at();

-- Single-owner studio: any logged-in user may read and edit.
-- Turn OFF public sign-ups in Supabase Auth so you are the only user.
alter table brand_context enable row level security;
drop policy if exists "studio users read brand" on brand_context;
create policy "studio users read brand" on brand_context for select to authenticated using (true);
drop policy if exists "studio users edit brand" on brand_context;
create policy "studio users edit brand" on brand_context for all to authenticated using (true) with check (true);

-- Returns all active sections for a track (plus 'all') as one Markdown text.
-- n8n calls: POST /rest/v1/rpc/get_brand_context  {"p_track":"kids"}
create or replace function get_brand_context(p_track text default 'all')
returns json language sql stable as $$
  select json_build_object(
    'track', p_track,
    'sections', count(*),
    'content', coalesce(string_agg('## ' || title || E'\\n' || content, E'\\n\\n' order by sort_order), '')
  )
  from brand_context
  where active and applies_to && array['all', coalesce(nullif(p_track, ''), 'all')];
$$;

insert into brand_context (slug, title, content, applies_to, sort_order) values
""" + ",\n".join(rows) + "\non conflict (slug) do nothing;\n"


if __name__ == "__main__":
    (ROOT / "docs").mkdir(exist_ok=True)
    (ROOT / "docs" / "brand-bible.md").write_text(to_markdown(), encoding="utf-8")
    (ROOT / "db" / "002_brand_context.sql").write_text(to_sql(), encoding="utf-8")
    print(f"Wrote docs/brand-bible.md and db/002_brand_context.sql ({len(SECTIONS)} sections)")
