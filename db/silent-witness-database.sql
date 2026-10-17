-- =====================================================================
-- Silent Witness - Complete database (v1.0)
-- Content library (the "global workspace") + website requests
--
-- Run in Supabase: SQL Editor -> New query -> paste all -> Run.
-- Safe to run again (idempotent). Run it BEFORE the Lovable prompt.
-- Every piece of content the AI brain makes is stored and tagged here.
-- Channels publish from it; the app later reads from it.
-- =====================================================================

create extension if not exists vector;   -- for similarity search (pgvector)

-- ---------------------------------------------------------------------
-- 1. The seven stages (reference table, also read by the AI critic)
-- ---------------------------------------------------------------------
create table if not exists stages (
  id            smallint primary key,
  slug          text unique not null,
  name          text not null,
  core_question text not null,
  orientation   text not null,
  description   text not null,
  content_guidelines text not null      -- injected into writer + critic prompts
);

insert into stages (id, slug, name, core_question, orientation, description, content_guidelines) values
(1, 'survival', 'Survival', 'How do I get through this?', 'Getting through life',
 'Meeting immediate needs, coping with threats, and getting through each day.',
 'Be practical, gentle and grounding. Never spiritually bypass real hardship or suggest suffering is deserved or a lesson. Offer small, doable steps. If content touches despair, hopelessness or crisis, encourage reaching out to trusted people or professional help.'),
(2, 'stability', 'Stability', 'How do I become secure?', 'Securing life',
 'Building financial security, relationships, a home, routines and a stable foundation.',
 'Focus on routines, habits, relationships and steadiness. Respect material needs as legitimate; avoid framing security as unspiritual.'),
(3, 'achievement', 'Achievement / Growth', 'What can I accomplish?', 'Improving life',
 'Pursuing success, recognition, wealth, mastery, freedom and personal potential.',
 'Support ambition and mastery without hustle culture or guilt. Link growth to values and wellbeing; avoid get-rich or guaranteed-outcome claims.'),
(4, 'meaning', 'Meaning', 'What is it all for?', 'Understanding life''s purpose',
 'Questioning whether external success is enough and searching for purpose, fulfillment and deeper understanding.',
 'Invite reflection rather than give answers. Draw on wisdom traditions with accurate attribution; name the source tradition when quoting or paraphrasing.'),
(5, 'awareness', 'Awareness', 'Why am I the way I am?', 'Understanding the mind',
 'Observing thoughts, emotions, conditioning, desires and reactions instead of automatically identifying with them.',
 'Teach observation of thoughts, emotions and conditioning. Keep it experiential and practical (noticing, labelling, witnessing). Do not present observation of the mind as awakening.'),
(6, 'awakening', 'Awakening', 'Who am I beneath all of this?', 'Investigating the nature of the self',
 'Deep self-inquiry into the nature of the self, the observer and consciousness itself.',
 'Use self-inquiry (e.g. "Who am I?") as an invitation, not a promise. Do not equate a glimpse, a peak experience or a feeling of oneness with lasting awakening. Avoid guru-style certainty.'),
(7, 'realization', 'Liberation / Realization', 'What am I, beyond the separate self?', 'Realizing what lies beyond identification with the self',
 'Freedom from identification with the limited self and realization of one''s true nature (moksha / self-realization in Advaita).',
 'Treat with humility. Never claim the creator or viewer has attained realization, and never sell it as an outcome. Distinguish clearly between unusual experiences and stable realization. Quote traditional sources (e.g. Advaita texts and teachers) accurately and attribute them.')
on conflict (id) do update set
  slug = excluded.slug, name = excluded.name, core_question = excluded.core_question,
  orientation = excluded.orientation, description = excluded.description,
  content_guidelines = excluded.content_guidelines;

-- ---------------------------------------------------------------------
-- 2. Controlled vocabularies (enums keep tags consistent across tools)
-- ---------------------------------------------------------------------
do $$ begin
  create type content_track as enum ('spiritual', 'kids', 'builder', 'lifestyle');
exception when duplicate_object then null; end $$;

do $$ begin
  create type content_format as enum (
    'reel', 'short', 'post', 'carousel', 'story',
    'long_video', 'guided_meditation', 'sleep_video', 'music',
    'kids_story', 'coloring_page', 'article', 'recipe', 'script');
exception when duplicate_object then null; end $$;

do $$ begin
  create type content_status as enum (
    'idea', 'draft', 'in_review', 'approved', 'scheduled', 'published', 'archived');
exception when duplicate_object then null; end $$;

do $$ begin
  create type channel as enum (
    'yt_meditation', 'yt_builder', 'instagram', 'amazon_kdp', 'app');
exception when duplicate_object then null; end $$;

-- ---------------------------------------------------------------------
-- 3. Series (Aadu & Coco, Seven Stages reels, Builder log, ...)
-- ---------------------------------------------------------------------
create table if not exists series (
  id          uuid primary key default gen_random_uuid(),
  name        text unique not null,
  track       content_track not null,
  description text,
  created_at  timestamptz default now()
);

insert into series (name, track, description) values
  ('Seven Stages', 'spiritual', 'Reels, meditations and posts organised by the seven stages'),
  ('Aadu & Coco', 'kids', 'Kids stories, Instagram series and KDP coloring books'),
  ('Builder Log', 'builder', 'How I built the multi-AI brain, app and pipelines')
on conflict (name) do nothing;

-- ---------------------------------------------------------------------
-- 4. Content items - the heart of the library
-- ---------------------------------------------------------------------
create table if not exists content_items (
  id               uuid primary key default gen_random_uuid(),
  owner_id         uuid references auth.users(id) default auth.uid(),

  -- What it is
  title            text not null,
  summary          text,                           -- 1-2 sentences, used in app cards
  body             text,                           -- script, caption or story text
  track            content_track not null,
  format           content_format not null,
  series_id        uuid references series(id),
  episode_number   int,

  -- Where it sits in the framework (null for builder/lifestyle content)
  primary_stage    smallint references stages(id),
  secondary_stages smallint[] default '{}',

  -- Discovery tags
  themes           text[] default '{}',            -- e.g. {letting go, gratitude, patience}
  practices        text[] default '{}',            -- e.g. {breathwork, body scan, self-inquiry, visualization}
  traditions       text[] default '{}',            -- e.g. {Advaita, Buddhism, Stoicism}
  audience         text default 'adults',          -- adults | kids | family
  language         text default 'en',
  duration_seconds int,

  -- Production + quality (the critic loop writes here)
  status           content_status not null default 'idea',
  critic_score     numeric(3,1),
  critic_feedback  text,
  revision_rounds  int default 0,
  uniqueness_note  text,                           -- what makes THIS piece original (YouTube authenticity)
  ai_contributions jsonb default '{}'::jsonb,      -- e.g. {"research":"gemini","ideas":"chatgpt","script":"claude"}
  synthetic_media  boolean default false,          -- realistic AI visuals/voice -> disclose on YouTube
  source_request_id uuid,                          -- link to ai_requests.id from the Lovable site

  -- Distribution
  target_channels  channel[] default '{}',
  app_visible      boolean default false,          -- the app shows only published + app_visible items

  -- Memory: semantic search + duplicate detection
  embedding        vector(1536),                   -- OpenAI text-embedding-3-small size; change if you use another model
  search_text      tsvector generated always as (
                     setweight(to_tsvector('english', coalesce(title, '')), 'A') ||
                     setweight(to_tsvector('english', coalesce(summary, '')), 'B') ||
                     setweight(to_tsvector('english', coalesce(body, '')), 'C')
                   ) stored,

  created_at       timestamptz default now(),
  updated_at       timestamptz default now(),

  constraint secondary_stages_valid check (secondary_stages <@ array[1,2,3,4,5,6,7]::smallint[]),
  constraint stage_for_spiritual check (track <> 'spiritual' or primary_stage is not null)
);

create index if not exists content_stage_idx   on content_items (primary_stage);
create index if not exists content_status_idx  on content_items (status);
create index if not exists content_track_idx   on content_items (track, format);
create index if not exists content_themes_idx  on content_items using gin (themes);
create index if not exists content_search_idx  on content_items using gin (search_text);
create index if not exists content_embed_idx   on content_items using hnsw (embedding vector_cosine_ops);

-- keep updated_at fresh
create or replace function touch_updated_at() returns trigger language plpgsql as $$
begin new.updated_at = now(); return new; end $$;

drop trigger if exists content_items_touch on content_items;
create trigger content_items_touch before update on content_items
  for each row execute function touch_updated_at();

-- ---------------------------------------------------------------------
-- 5. Assets - the files belonging to a content item
-- ---------------------------------------------------------------------
create table if not exists assets (
  id               uuid primary key default gen_random_uuid(),
  content_item_id  uuid not null references content_items(id) on delete cascade,
  kind             text not null,                  -- video | audio | image | thumbnail | pdf | subtitle
  storage_path     text not null,                  -- Supabase Storage path or external URL
  tool             text,                           -- flow | suno | firefly | elevenlabs | camera ...
  duration_seconds int,
  width            int,
  height           int,
  created_at       timestamptz default now()
);
create index if not exists assets_item_idx on assets (content_item_id);

-- ---------------------------------------------------------------------
-- 6. Publications - where and when it went out, plus performance
-- ---------------------------------------------------------------------
create table if not exists publications (
  id               uuid primary key default gen_random_uuid(),
  content_item_id  uuid not null references content_items(id) on delete cascade,
  channel          channel not null,
  external_id      text,                           -- YouTube video id, Instagram media id, ASIN ...
  url              text,
  published_at     timestamptz,
  metrics          jsonb default '{}'::jsonb,      -- {"views":..,"likes":..,"saves":..,"avg_view_pct":..}
  metrics_updated_at timestamptz,
  unique (channel, external_id)
);
create index if not exists publications_item_idx on publications (content_item_id);

-- ---------------------------------------------------------------------
-- 7. Helpers called by n8n (via Supabase REST /rpc/...)
-- ---------------------------------------------------------------------

-- 7a. Similar existing content (originality check + "related" in app)
drop function if exists match_content(vector, float, int);
create or replace function match_content(
  query_embedding vector(1536),
  similarity_threshold float default 0.85,
  max_results int default 5,
  exclude_id uuid default null
) returns table (id uuid, title text, primary_stage smallint, format content_format, similarity float)
language sql stable as $$
  select c.id, c.title, c.primary_stage, c.format,
         1 - (c.embedding <=> query_embedding) as similarity
  from content_items c
  where c.embedding is not null
    and (exclude_id is null or c.id <> exclude_id)
    and 1 - (c.embedding <=> query_embedding) >= similarity_threshold
  order by c.embedding <=> query_embedding
  limit max_results;
$$;

-- 7b. Keyword search of the library (agent tool + Lovable search box)
create or replace function search_library(
  q text default '',
  stage_filter int default null,
  max_results int default 8
) returns table (id uuid, title text, summary text, primary_stage smallint, track content_track,
                 format content_format, status content_status, critic_score numeric, updated_at timestamptz)
language sql stable as $$
  select c.id, c.title, c.summary, c.primary_stage, c.track, c.format, c.status, c.critic_score, c.updated_at
  from content_items c
  where (coalesce(q, '') = '' or c.search_text @@ websearch_to_tsquery('english', q))
    and (stage_filter is null or stage_filter = 0 or c.primary_stage = stage_filter)
  order by
    case when coalesce(q, '') = '' then 0
         else ts_rank(c.search_text, websearch_to_tsquery('english', q)) end desc,
    c.updated_at desc
  limit least(greatest(coalesce(max_results, 8), 1), 50);
$$;

-- ---------------------------------------------------------------------
-- 8. App-facing view: only what the app may show
-- ---------------------------------------------------------------------
create or replace view app_library
with (security_invoker = true) as
select c.id, c.title, c.summary, c.track, c.format, c.series_id, c.episode_number,
       c.primary_stage, s.name as stage_name, s.core_question,
       c.secondary_stages, c.themes, c.practices, c.audience, c.language,
       c.duration_seconds, c.updated_at
from content_items c
left join stages s on s.id = c.primary_stage
where c.status = 'published' and c.app_visible;

-- ---------------------------------------------------------------------
-- 9. Security (Row Level Security)
--    n8n uses the service_role key and bypasses RLS.
--    You (logged in) manage your own items. The public app reads only
--    published + app_visible items.
-- ---------------------------------------------------------------------
alter table stages        enable row level security;
alter table series        enable row level security;
alter table content_items enable row level security;
alter table assets        enable row level security;
alter table publications  enable row level security;

drop policy if exists "stages readable" on stages;
create policy "stages readable" on stages for select using (true);

drop policy if exists "series readable" on series;
create policy "series readable" on series for select using (true);

drop policy if exists "owner manages content" on content_items;
create policy "owner manages content" on content_items
  for all to authenticated using (owner_id = auth.uid()) with check (owner_id = auth.uid());

drop policy if exists "public reads app content" on content_items;
create policy "public reads app content" on content_items
  for select to anon, authenticated using (status = 'published' and app_visible);

drop policy if exists "owner manages assets" on assets;
create policy "owner manages assets" on assets
  for all to authenticated
  using (exists (select 1 from content_items c where c.id = content_item_id and c.owner_id = auth.uid()))
  with check (exists (select 1 from content_items c where c.id = content_item_id and c.owner_id = auth.uid()));

drop policy if exists "owner manages publications" on publications;
create policy "owner manages publications" on publications
  for all to authenticated
  using (exists (select 1 from content_items c where c.id = content_item_id and c.owner_id = auth.uid()))
  with check (exists (select 1 from content_items c where c.id = content_item_id and c.owner_id = auth.uid()));

-- =====================================================================
-- 10. Website requests (Lovable chat -> n8n Brain Agent -> answer)
--     Works whether or not an earlier Lovable prompt already created it.
-- =====================================================================
create table if not exists ai_requests (
  id          uuid primary key default gen_random_uuid(),
  user_id     uuid not null references auth.users(id) default auth.uid(),
  session_id  text not null,
  message     text not null,
  status      text not null default 'pending',
  response    text,
  created_at  timestamptz default now()
);

alter table ai_requests add column if not exists stage           smallint references stages(id);
alter table ai_requests add column if not exists track           content_track;
alter table ai_requests add column if not exists format          content_format;
alter table ai_requests add column if not exists content_item_id uuid references content_items(id) on delete set null;
alter table ai_requests add column if not exists updated_at      timestamptz default now();

do $$ begin
  alter table ai_requests add constraint ai_requests_status_check
    check (status in ('pending', 'processing', 'done', 'error'));
exception when duplicate_object then null; end $$;

create index if not exists ai_requests_user_session_idx on ai_requests (user_id, session_id, created_at);

drop trigger if exists ai_requests_touch on ai_requests;
create trigger ai_requests_touch before update on ai_requests
  for each row execute function touch_updated_at();

alter table ai_requests enable row level security;

drop policy if exists "sw users insert own requests" on ai_requests;
create policy "sw users insert own requests" on ai_requests
  for insert to authenticated with check (user_id = auth.uid() and status = 'pending');

drop policy if exists "sw users read own requests" on ai_requests;
create policy "sw users read own requests" on ai_requests
  for select to authenticated using (user_id = auth.uid());
-- No user UPDATE/DELETE: only n8n (service_role) writes answers.

-- When n8n saves content made for a website request, link it back to that
-- request so the chat bubble can show "Open in library".
create or replace function link_request_to_content() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  if new.source_request_id is not null then
    update ai_requests set content_item_id = new.id where id = new.source_request_id;
  end if;
  return new;
end $$;

drop trigger if exists content_items_link_request on content_items;
create trigger content_items_link_request after insert on content_items
  for each row execute function link_request_to_content();

-- =====================================================================
-- 11. Journey dashboard: content coverage per stage (shows gaps)
-- =====================================================================
create or replace view stage_coverage
with (security_invoker = true) as
select s.id as stage_id, s.name, s.core_question,
       count(c.id)                                                          as total,
       count(c.id) filter (where c.status = 'published')                     as published,
       count(c.id) filter (where c.status in ('in_review','approved','scheduled')) as in_pipeline,
       count(c.id) filter (where c.status in ('idea','draft'))               as drafts
from stages s
left join content_items c on c.primary_stage = s.id
group by s.id, s.name, s.core_question
order by s.id;

-- =====================================================================
-- 12. Realtime: live updates for the chat and the library pages
-- =====================================================================
do $$
declare t text;
begin
  if exists (select 1 from pg_publication where pubname = 'supabase_realtime') then
    foreach t in array array['ai_requests', 'content_items'] loop
      if not exists (select 1 from pg_publication_tables
                     where pubname = 'supabase_realtime' and schemaname = 'public' and tablename = t) then
        execute format('alter publication supabase_realtime add table public.%I', t);
      end if;
    end loop;
  end if;
end $$;
