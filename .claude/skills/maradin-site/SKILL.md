---
name: maradin-site
description: Build, update, check and publish Evgeny Maradin's website (evgenymaradin.com, this repo). Use for any change to the site - adding a LinkedIn article, adding or editing a case, CV/education/experience facts, SEO titles, the social preview image, the production-data note, design or mobile fixes, indexing, testing the site on phone and desktop. Triggers include "сайт", "добавь статью на сайт", "актуализируй сайт", "добавь кейс", "проверь сайт на телефоне", "SEO", "site", "case", "article".
---

# Evgeny Maradin's website

Static personal site of an upstream oil & gas engineer (FEL, Pre-FEED, brownfield) looking for roles and advisory work. Every visitor is a potential employer or client, so facts must be exact and the site must work on a phone.

The owner writes in Russian: answer in Russian, short, with what changed and the PR link. Code, commits, PRs and site text are in English.

## Repo map (details in README.md)

- `tools/build_site.py` generates almost every page into `web/`. Content is data in the script:
  `CASES` (case pages; optional chart per case in `FIGURES[slug]`), `ARTICLES` + `ORDER` (insights, newest first), `ART_SEO`, `MODELS`, `SERVICES`, `TIMELINE` (About), `SEO` (titles/descriptions of key pages), `featured` (3 cases on the home page; cards there carry no case numbers on purpose).
- `content/articles/<key>.md`: full LinkedIn article texts (front matter `title`, `date`, `url`; body verbatim). If the file exists, the build writes `/insights/<key>/` and cards link there.
- `web/img/insights/<key>.webp` cover; `web/img/insights/<key>/NN.webp` in-article images; pixel sizes in `tools/img_sizes.json`.
- `content/production-note.md`: monthly note under the production chart (update `date`/`data_to`). `web/data/production.json` is refreshed by a GitHub workflow; do not hand-edit it.
- Hand-maintained: `web/style.css`, `web/contact.js`, `web/functions/api/*.js`, `web/models/*` (interactive models), `web/docs/` (UK ENIC PDF).
- `tools/make_og.py` regenerates `web/og.png` (social card with headline and metrics) and `web/favicon.svg`; rerun when the headline or headline metrics change.
- Generated, commit them: `web/sitemap.xml`, `web/robots.txt`, `tools/lastmod.json` (sitemap dates change only when a page's HTML changes).
- Keep `web/google5ee18c8586b05b2f.html` (Search Console verification) and `web/d64e44d74df91f311902d640a0627c67.txt` (IndexNow key).

## Facts policy

1. Use only facts the owner gave: his messages, his CVs and interview notes, existing site text. Do not invent numbers, clients, dates, roles or outcomes. If a source marks something as reconstructed or to be verified (for example the three-pipe gathering and VSM water injection stories), leave it out until he confirms.
2. Employer labels: Salym Petroleum Development is "Shell JV" only up to March 2023, when Shell exited; 2023–2024 work is "Salym Petroleum". Experience is operator side plus the Rosneft engineering centre (contractor side); no "PMC" wording.
3. Experience: 19 years in upstream oil & gas (since 2007), the same number everywhere, including `make_og.py`. Do not call the whole period "operator side": 2024–now is independent advisory.
4. Education: Specialist Diploma (5-year), Kuban State Technological University, 2007; UK ENIC: comparable to UK Bachelor (Honours), RQF Level 6. Not "Master's".
5. No unverifiable claims ("adopted as best practice", named NOC clients, management adoption) unless he confirms them. Anonymised studies keep "illustrative figures, relative values only", with no asset names or absolute costs.
6. When in doubt, ask one short question instead of guessing. Case 09 (well-pad siting) is SPD, 2018–2023.

## Workflows

**New LinkedIn article.** Needs the URL, the full text and the cover. Cloud sessions cannot open LinkedIn, so either the owner pastes text, link and cover, or the work runs in a local Claude Desktop session with Claude in Chrome. Then: save `content/articles/<key>.md` (verbatim, keep links), save the cover as `web/img/insights/<key>.webp` (about 800x449), add the entry to `ARTICLES` (copy the shape of an existing one: `t`, `tag`, `d` like "26 Oct 2026", `w` word count, `u`, summary), put the key first in `ORDER`, add `ART_SEO[key]` (title up to 65 characters including " | Evgeny Maradin", description up to 160), and add sizes for any in-article images.

**New or edited case.** Edit the dict in `CASES` (slug, n, label, years, title, teaser, metric, metric_l, big, tags, meta with 4 pairs, context, role, challenge, action list, result, insight key for related reading). A new case gets the next `n` and goes at the end; the case count text comes from `NUM[len(CASES)]` (add a word to `NUM` if needed). Optional chart: inline SVG in `FIGURES[slug]` using the `.case-fig` classes; check its labels at 390 px.

**Headline, metrics or title change.** Update the page text and `SEO`, then rerun `make_og.py`.

## Build, test, hand over

1. Run `python3 tools/build_site.py web` twice; the second run must change nothing. On Windows, write files with LF line endings (CRLF churns every page and every sitemap date).
2. `pip install playwright` if needed, then `python3 .claude/skills/maradin-site/scripts/qa.py web <tmp_dir>`. Expected and harmless: `label.hp` (anti-spam honeypot) and `404 /api/prices` on /insights/ (a Cloudflare Pages Function for the price ticker, not served by the local test server). Look at screenshots of changed pages at both widths, and at 360 px for anything wide (models, charts, tables).
3. Work on a branch `claude/<topic>`, commit with a clear message and open a PR to `main`. Cloudflare Pages deploys `main` within 1–2 minutes of a merge and posts a preview check on the PR. Merge only when the owner asks for it in the current conversation.
4. Report in Russian: what changed (a small table is fine), the PR link, and what to check on the phone. Say what you could not verify yourself (the live site and LinkedIn are not reachable from cloud sessions).

## Known limits

- The site lives on `evgenymaradin.com` (registered at Cloudflare, November 2026; renews yearly). `web/functions/_middleware.js` 301-redirects `www.evgenymaradin.com` to it. The old `evgeny-maradin.pages.dev` still serves the site (owner wants it reachable for now; canonical tags point to the new domain); to retire it, add it to `REDIRECT_FROM`. LinkedIn Post Inspector could not fetch `*.pages.dev`, which was the reason for the domain.
- Cloud sessions cannot reach LinkedIn, the live site or the owner's browser.
- Google Search Console is verified with the HTML file. The sitemap and IndexNow submissions are automatic; "Request indexing" is the owner's button and has a daily quota.
- Fonts: the CSS names Inter but does not load it, so visitors see Arial. Loading it is an open task; ask before restyling. Design option B ("Engineering": IBM Plex, blue accent) was proposed but not chosen yet.
