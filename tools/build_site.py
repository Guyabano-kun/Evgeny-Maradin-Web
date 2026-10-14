"""Generates the static multi-page site into web/ (run once; output is committed)."""
import os, sys, html

OUT = sys.argv[1]
LI = "https://www.linkedin.com/in/evgeny-maradin-5279b85a/"
PULSE = "https://www.linkedin.com/pulse/"
EMAIL = "enmaradin@gmail.com"
UPDATED = "October 2026"
SITE = "https://evgeny-maradin.pages.dev"
PAGES = []  # paths written by page(), for sitemap.xml
PERSON = ('{"@context":"https://schema.org","@type":"Person","name":"Evgeny Maradin","url":"%s/",'
          '"jobTitle":"Study Manager / Senior Concept Engineer (FEL, Pre-FEED)","email":"mailto:%s",'
          '"image":"%s/og.png","sameAs":["%s"],"homeLocation":{"@type":"Place","name":"Philippines"},'
          '"knowsAbout":["FEL1–FEL2","Pre-FEED","Concept Selection","Brownfield Development","CAPEX Optimisation","Upstream Oil and Gas"]}'
          % (SITE, EMAIL, SITE, LI))

NAV = [("/cases/", "Cases", ""), ("/advisory/", "Advisory", ""), ("/insights/", "Insights", ""),
       ("/about/", "About", "hide-sm"), ("/contact/", "Contact", "hide-sm")]


def page(path, title, desc, body, active=""):
    nav = "".join(
        f'<a href="{h}"{" class=%s" % c if c else ""}{" aria-current=page" if h == active else ""}>{t}</a>'
        for h, t, c in NAV)
    full_title = "Evgeny Maradin | Concept Development / FEL" if path == "" else f"{title} | Evgeny Maradin"
    url = f"{SITE}/{path}/" if path else f"{SITE}/"
    ld = f'<script type="application/ld+json">{PERSON}</script>' if path == "" else ""
    PAGES.append(url)
    doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(full_title)}</title><meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:title" content="{html.escape(full_title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:type" content="website">
<meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">{ld}
<link rel="stylesheet" href="/style.css"></head><body>
<header><div class="container nav"><a class="brand" href="/">EM<span>.</span></a><nav>{nav}</nav></div></header>
<main id="top">{body}</main>
<section id="contact" class="contact"><div class="container contact-grid"><div><p class="eyebrow">Contact</p><h2>For studies, project development and engineering leadership.</h2></div><div><a href="mailto:{EMAIL}">{EMAIL}</a><button class="copy" type="button" data-copy="{EMAIL}">Copy email</button><a href="tel:+639669813383">+63 966 981 3383</a><a class="wa" href="https://wa.me/639669813383" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.4.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3z"/></svg> WhatsApp ↗</a><a href="/contact/?type=call">Book a free 30-min call →</a><a href="{LI}" target="_blank" rel="noopener">LinkedIn ↗</a><p class="avail">CV and project enquiries by email. Based in the Philippines, available to mobilise within 2 weeks.</p></div></div></section>
<footer><div class="container"><span>Evgeny Maradin · <a href="/cases/">Cases</a> · <a href="/advisory/">Advisory</a> · <a href="/insights/">Insights</a> · <a href="/about/">About</a></span><span>Concept Development / FEL | Upstream Oil &amp; Gas · Updated {UPDATED}</span></div></footer>
<script>document.querySelectorAll('[data-copy]').forEach(b=>b.addEventListener('click',async()=>{{const t=b.dataset.copy;try{{await navigator.clipboard.writeText(t)}}catch(e){{const a=document.createElement('textarea');a.value=t;document.body.appendChild(a);a.select();document.execCommand('copy');a.remove()}}b.textContent='Copied: '+t;setTimeout(()=>b.textContent='Copy email',2500)}}))</script>
</body></html>'''
    d = os.path.join(OUT, path)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(doc)


# ---------------- CASES ----------------
CASES = [
    dict(slug="portfolio-integration", n="01", label="Shell JV · Western Siberia", years="2017–2023",
         title="Portfolio Integration – 6 Fields", feature=True,
         teaser="Restructured development across six mature assets and identified shared infrastructure that changed the portfolio investment case.",
         metric="~57%", metric_l="CAPEX reduction<br>≈ $48M", big="~57% portfolio CAPEX reduction (≈ $48M). Investment recommendation approved at shareholder level.",
         tags=["FEL1–FEL2", "Integration", "CAPEX"],
         meta=[("Client", "Salym Petroleum Development (Shell JV)"), ("Period", "2017–2023"), ("Role", "Concept development lead"), ("Phase", "FEL1 – Pre-FEED")],
         context="Multiple mature assets with fragmented, duplicated infrastructure and high combined CAPEX.",
         role="Led concept development and the cross-field integration study (FEL1 – Pre-FEED).",
         challenge="Each asset was planned independently, with no visibility of cross-field synergies. Individual CAPEX estimates were commercially unviable as a portfolio.",
         action=["Restructured the development approach across six fields.", "Identified infrastructure sharing opportunities between assets.", "Prepared the integrated investment case for the JV shareholders."],
         result="~57% CAPEX reduction (≈ $48M). The investment recommendation was approved at shareholder level.",
         insight="portfolio-risk"),
    dict(slug="water-injection", n="02", label="Shell JV · Asset Integrity", years="2023–2024",
         title="Water Injection Re-engineering",
         teaser="Challenged a technically valid but commercially disproportionate end-of-life redevelopment concept and developed an alternative.",
         metric="80%", metric_l="CAPEX reduction<br>$3.6M saved", big="80% CAPEX reduction ($3.6M saved) and a 300% increase in Profitability Index. Approved at Decision Review Board.",
         tags=["Brownfield", "DRB", "Economics"],
         meta=[("Client", "Salym Petroleum Development (Shell JV)"), ("Period", "2023–2024"), ("Role", "Concept lead"), ("Gate", "Decision Review Board")],
         context="An existing water injection system approaching end-of-life, with a significant CAPEX requirement under the original redevelopment concept.",
         role="Concept lead. Initiated the re-evaluation of the original approach.",
         challenge="The original concept was technically valid but commercially disproportionate given the remaining asset life and production profile.",
         action=["Challenged the original concept.", "Developed an alternative engineering approach.", "Structured the business case and prepared the DRB submission."],
         result="80% CAPEX reduction ($3.6M saved). Profitability Index increased by 300%. Approved at Decision Review Board.",
         insight="shopping-cart"),
    dict(slug="apg-pre-feed", n="03", label="Shell JV · Associated gas", years="2023–2024",
         title="APG Utilisation Pre-FEED",
         teaser="Led an eight-month multidisciplinary Pre-FEED covering development planning, contractor interfaces and production–facilities integration.",
         metric="$160M", metric_l="project scale<br>Pre-FEED", big="An eight-month Pre-FEED for a $160M associated petroleum gas utilisation project, supporting concept selection and investment readiness.",
         tags=["Study Management", "Pre-FEED", "Gas"],
         meta=[("Client", "Salym Petroleum Development (Shell JV)"), ("Period", "2023–2024"), ("Role", "Study lead"), ("Duration", "8 months")],
         context="Associated petroleum gas utilisation project at a mature oil asset, requiring a Pre-FEED to support concept selection and investment readiness.",
         role="Led the Pre-FEED study as Concept Development Manager.",
         challenge="Align production, facilities and contractor scopes into one development plan within an eight-month study window.",
         action=["Coordinated multidisciplinary engineering and contractor interfaces.", "Developed the scope and the development plan across production and facilities.", "Prepared execution planning inputs for the investment decision."],
         result="Pre-FEED delivered for a $160M project, providing the basis for concept selection and investment readiness.",
         insight="pressure"),
    dict(slug="epc-bid-analysis", n="04", label="MENA · Independent advisory", years="2026",
         title="EPC Bid Analysis & Contract Strategy",
         teaser="Decomposed bid escalation drivers across a major upstream portfolio and structured scenarios around schedule, FEED maturity, scope and risk allocation.",
         metric="$6B+", metric_l="portfolio assessed<br>decision support", big="Scenario and decision-support framework adopted by management as the basis for contract renegotiation.",
         tags=["EPC", "Risk", "Commercial"],
         meta=[("Client", "National oil company, MENA"), ("Period", "2026"), ("Role", "Independent advisory"), ("Scope", "Separation & water injection packages")],
         context="A national oil company with several major EPC packages (separation and water injection facilities) where bids came in significantly above approved estimates. Tenders were cancelled under management pressure.",
         role="Independent advisory: analytical support on contracting strategy and scenario development.",
         challenge="The cost estimate was approved years before tender. Market escalation, an outdated FEED and aggressive schedule and LD terms combined into a risk premium that contractors priced fully upfront under LSTK.",
         action=["Decomposed the bid-to-estimate gap into controllable and non-controllable components.", "Quantified risk exposure per package.", "Built a scenario framework: renegotiation (schedule extension and LD reduction), selective BOOT restructuring for long-life assets, phased scope.", "Designed a pre-tender gate KPI set: Schedule Confidence Index, TCE Age Index, Interface Register Completeness."],
         result="The framework was presented to and adopted by management as the basis for contract renegotiation. Renegotiations were initiated.",
         insight="iraq-cycle"),
    dict(slug="yaro-yakhinskoye", n="05", label="Gazprom Neft · Arctic onshore", years="2014–2017",
         title="Yaro-Yakhinskoye Field Development",
         teaser="Led Pre-FEED and FEED, then supported detailed engineering and execution readiness for facilities tied into live production.",
         metric="$300M+", metric_l="programme scale<br>within schedule", big="New facilities integrated without production disruption. Delivered within schedule on a $300M+ programme.",
         tags=["FEED", "Brownfield", "Execution"],
         meta=[("Client", "Gazprom Neft · Arcticgas JV"), ("Period", "2014–2017"), ("Role", "Study Manager → Project Engineer / PMO"), ("Phase", "Pre-FEED → Detailed design")],
         context="Greenfield-to-brownfield transition on an active producing asset in Arctic conditions.",
         role="Led Pre-FEED and FEED as Study Manager, then supported detailed engineering as Project Engineer / PMO, including construction and pre-start-up readiness assessments.",
         challenge="New facilities had to be integrated into live production infrastructure with no production interruption, across multiple contractor interfaces in a remote environment.",
         action=["Coordinated engineering disciplines through FEED.", "Managed contractor interfaces.", "Led risk management and change control during execution preparation."],
         result="Facilities integrated without production disruption. Delivered within schedule on a $300M+ programme.",
         insight="integrated-fd"),
    dict(slug="south-hub", n="06", label="Shell JV · Upper Salym field", years="2017–2018",
         title="South Hub – Brownfield Expansion",
         teaser="Synchronised subsurface and surface decisions so that new facilities could be brought online and integrated into a live producing asset.",
         metric="7", metric_l="technical authority disciplines<br>signed off the concept", big="Concept selection approved: existing plant and pump station expanded in place, new water injection station at the tie-in point, phased in two stages.",
         tags=["Brownfield", "Concept Select", "Subsurface–Surface"],
         meta=[("Client", "Salym Petroleum Development (Shell JV)"), ("Asset", "South Hub, Upper Salym field"), ("Role", "Senior Concept Engineer"), ("Phase", "Assess / Concept Select")],
         context="New South Hub wells were set to raise production at the Upper Salym field. The existing dehydration plant (its first stage still under construction), the multiphase pump station and the water injection system all had to absorb it, while the field kept producing.",
         role="Senior Concept Engineer and author of the concept selection report. My job was to keep subsurface and surface decisions synchronised: bringing new facilities online and integrating them into the operating asset.",
         challenge="Facility capacity depended on development scenarios that were still moving. Every option had to fit live gathering, treatment, water injection and power systems, with brownfield limits on location and tie-ins.",
         action=["Tested facility capacity against the likely South Hub development scenarios together with reservoir engineering.", "Screened expansion and new-build options for the dehydration plant, the multiphase pump station and a new well-pad water injection station: location, capacity and phasing.", "Integrated the external power supply strategy into the concept.", "Recommended moving the main technical solutions into a separate early design stage, so the project could progress faster with lower design risk."],
         result="Concept selection approved by the Petroleum Engineering Manager after review by reservoir engineering, design and seven technical authority disciplines. Expand the existing plant and pump station in place, build a new water injection station near the tie-in point, phase the work in two stages.",
         insight="me-brownfields"),
    dict(slug="minor-capex", n="07", label="Shell JV · Asset & Integrity", years="2012–2024",
         title="Minor CAPEX Portfolio – Debottlenecking & Integrity",
         teaser="Led FEL for minor CAPEX projects that kept a mature asset running: debottlenecking, integrity and reliability of the gathering system and field facilities.",
         metric="$1–20M", metric_l="TEC per project<br>FEL1–FEL2", big="A continuous stream of $1M–$20M projects taken through FEL: debottlenecking up to 10% value uplift, integrity cost savings up to 20%, Profitability Index up to +25%.",
         tags=["Minor CAPEX", "Debottlenecking", "Integrity & Reliability"],
         meta=[("Client", "Salym Petroleum Development (Shell JV)"), ("Scope", "Gathering system & field facilities"), ("Role", "Concept lead / Front-End Development Manager"), ("Project size", "TEC $1M–$20M")],
         context="A mature producing asset where much of the value sits in many small projects rather than one large one: removing bottlenecks, restoring integrity and improving the reliability of pipelines, gathering networks and field facilities.",
         role="Led minor CAPEX projects through FEL (FEL1–FEL2), from problem framing to an approved concept, as concept lead and Front-End Development Manager.",
         challenge="Each project is small on its own, so the risk is either over-engineering it or approving it without testing alternatives. Every option also had to fit a live system without disrupting production.",
         action=["Framed each problem against production, integrity and operating data before defining scope.", "Screened alternatives, including doing less: re-routing, re-use of existing equipment, phased scope.", "Used flow assurance and network analysis (PIPESIM, PETEX GAP) to size debottlenecking options.", "Applied competitive scoping and cost engineering, then took each concept to approval."],
         result="Debottlenecking and plant optimisation with up to 10% value uplift, integrity cost savings of up to 20%, and fast-track quick wins that raised Profitability Index by up to 25%.",
         insight="shopping-cart"),
    dict(slug="bazhenov-appraisal", n="08", label="Shell JV · Unconventional", years="2012–2014",
         title="Bazhenov Shale Appraisal – Early Production Facility",
         teaser="Coordinated international technical contractors to deliver the early production facility design for an HPHT shale appraisal project on schedule.",
         metric="$46M", metric_l="appraisal project<br>EPF design on schedule", big="EPF design package for a $46M Bazhenov HPHT shale appraisal project delivered on schedule, with KBR and Granherne as technical contractors.",
         tags=["Unconventional", "HPHT", "Contractor Management"],
         meta=[("Client", "Salym Petroleum Development (Shell JV)"), ("Period", "2012–2014"), ("Role", "Conceptual Design Engineer"), ("Scope", "Early Production Facility")],
         context="Appraisal of the Bazhenov formation, a high-pressure, high-temperature shale in Western Siberia, at a Shell JV asset. Appraisal wells needed an early production facility to handle test production while the resource was still being understood.",
         role="Conceptual Design Engineer responsible for the surface facilities scope: coordination of KBR and Granherne as technical contractors and delivery of the EPF design package.",
         challenge="HPHT conditions and an unconventional reservoir with limited operating history meant the facility had to be designed around uncertain fluid and flow behaviour. Two international contractors had to work to one scope and one schedule.",
         action=["Coordinated KBR and Granherne as technical contractors on the early production facility design.", "Aligned the facility scope with the appraisal programme and the operating requirements of the asset.", "Managed contractor interfaces, deliverables and schedule through to the final design package."],
         result="EPF design package delivered on schedule for the $46M appraisal project.",
         insight="kazakhstan"),
]


def case_card(c, full=False, num=True):
    cls = "case feature" if c.get("feature") else "case"
    n = f'{c["n"]} · ' if num else ""
    return (f'<a class="{cls}" href="/cases/{c["slug"]}/"><small>{n}{c["label"].upper()} · {c["years"].upper()}</small>'
            f'<h3>{c["title"]}</h3><p>{c["teaser"]}</p>'
            f'<div class="result"><b>{c["metric"]}</b><span>{c["metric_l"]}</span></div>'
            + (f'<div class="tags">{"".join(f"<i>{t}</i>" for t in c["tags"])}</div>' if full else "")
            + '<span class="more">Read case →</span></a>')


for i, c in enumerate(CASES):
    prev_c, next_c = CASES[i - 1], CASES[(i + 1) % len(CASES)]
    meta = "".join(f"<div><span>{k}</span><b>{v}</b></div>" for k, v in c["meta"])
    actions = "".join(f"<li>{a}</li>" for a in c["action"])
    body = f'''<section class="hero small"><div class="container"><p class="eyebrow"><a href="/cases/">Cases</a> / {c["n"]} · {c["label"]}</p>
<h1 class="page">{c["title"]}</h1><p class="lead">{c["teaser"]}</p><div class="case-meta">{meta}</div></div></section>
<section class="section tight" style="border-top:0"><div class="container narrow">
<div class="big-result"><b>{c["metric"]}</b><span>{c["big"]}</span></div>
<div class="story"><div><h4>Context</h4><p>{c["context"]}</p></div><div><h4>Role</h4><p>{c["role"]}</p></div>
<div><h4>Challenge</h4><p>{c["challenge"]}</p></div><div><h4>Action</h4><ul>{actions}</ul></div>
<div><h4>Result</h4><p>{c["result"]}</p></div></div>
<div class="tags" style="margin:30px 0 50px">{"".join(f"<i>{t}</i>" for t in c["tags"])}</div>
<div style="margin-bottom:50px">@@RELATED:{c["insight"]}@@</div>
<div class="pager"><a href="/cases/{prev_c["slug"]}/"><small>← Previous case</small><b>{prev_c["title"]}</b></a><a href="/cases/{next_c["slug"]}/"><small>Next case →</small><b>{next_c["title"]}</b></a></div>
</div></section>'''
    page(f"cases/{c['slug']}", c["title"], c["teaser"], body, "/cases/")

page("cases", "Cases", "Selected cases in concept development, brownfield optimisation and project decision support.",
     f'''<section class="hero small"><div class="container"><p class="eyebrow">Selected cases</p><h1 class="page">Evidence,<br>not job titles.</h1>
<p class="lead">Eight cases from concept development, brownfield optimisation and project decision support. Each one: the context, my role, what was hard, what I did and what changed.</p></div></section>
<section class="section tight" style="border-top:0"><div class="container"><div class="case-grid">{"".join(case_card(c, True) for c in CASES)}</div></div></section>''',
     "/cases/")

# ---------------- INSIGHTS ----------------
import math
ARTICLES = {
 "kirkuk": dict(t="Kirkuk: The First Barrels Will Be Fast. Their Gas Outlets Will Not.", tag="Iraq · Kirkuk", d="9 Oct 2026", w=1925, u=PULSE+"kirkuk-first-barrels-fast-gas-outlets-evgeny-maradin-ymsoc/",
   s="Kirkuk is going from 320,000 to 420,000 bpd. The first barrels come quickly from existing wells, but the outlets for their gas take years. The real question is sequencing."),
 "pressure": dict(t="Pressure decisions are made in the reservoir – and paid for in the facilities", tag="Framework · UAE / Iraq", d="28 Sep 2026", w=1485, u=PULSE+"pressure-decisions-made-reservoir-paid-facilities-evgeny-maradin-yh2hc/",
   s="Umm Shaif and southern Iraq's seawater project, two sides of the same FEL problem: who owns the pressure-maintenance decision between subsurface and facilities."),
 "kazakhstan": dict(t="Kazakhstan just put 24 blocks on the table. The number that matters isn't 24.", tag="Kazakhstan", d="10 Sep 2026", w=1503, u=PULSE+"kazakhstan-just-put-24-blocks-table-number-matters-isnt-maradin-ihiac/",
   s="An auction of options, not acreage: a cheap entry ticket, an expensive strike price, and constraints that move from geology to wells, surface and export."),
 "shopping-cart": dict(t="The Production Profile Is a Shopping Cart", tag="Framework · Brownfield", d="25 Aug 2026", w=2537, u=PULSE+"production-profile-shopping-cart-evgeny-maradin-fy03c/",
   s="The profile in the corporate plan is a procurement plan for physical capacity. Each barrel has to be bought as water handling, compression, separation or power.", model="production-profile"),
 "kuwait": dict(t="Kuwait's 4 MMbpd target is not a drilling problem", tag="Kuwait", d="17 Aug 2026", w=2453, u=PULSE+"kuwaits-4-mmbpd-target-drilling-problem-evgeny-maradin-k3frc/",
   s="From 2.72 to 4.0 MMbpd is a system integration problem. Gas handling already caps crude output, and the next bottleneck is created by today's investment."),
 "iraq-deals": dict(t="What Iraq's 2026 deals are really about", tag="Iraq", d="11 Aug 2026", w=2153, u=PULSE+"what-iraqs-2026-deals-really-evgeny-maradin-21pac/",
   s="Five companies, five different strategies, one common logic behind the wave of upstream agreements signed in Iraq this year."),
 "portfolio-risk": dict(t="Portfolio integration risk: The uncertainty nobody owns", tag="Framework · Portfolio", d="28 Jul 2026", w=1263, u=PULSE+"portfolio-integration-risk-uncertainty-nobody-owns-evgeny-maradin-ht6rf/",
   s="The risk that sits between projects: shared infrastructure, execution capacity and capital that no single project team is accountable for."),
 "kurdistan": dict(t="The industry spent a decade reducing engineering uncertainty. Kurdistan added two more variables.", tag="Kurdistan", d="21 Jul 2026", w=1595, u=PULSE+"industry-spent-decade-reducing-engineering-kurdistan-added-maradin-vmj8f/",
   s="Project value depends on more than reserves. In Kurdistan, two variables outside engineering can make or break the investment case."),
 "iraq-cycle": dict(t="Iraq's next upstream cycle", tag="Iraq · White paper", d="9 Jul 2026", w=2965, u=PULSE+"iraqs-next-upstream-cycle-evgeny-maradin-pdmhf/",
   s="A white paper on brownfield redevelopment, infrastructure constraints and why program integration, not individual projects, decides value in Iraq's new cycle."),
 "integrated-fd": dict(t="Integrated Field Development Is Not About Building Facilities. It Is About Managing Constraints.", tag="Framework · Concept Select", d="25 Jun 2026", w=1126, u=PULSE+"integrated-field-development-building-facilities-managing-maradin-yezuc/",
   s="Why synchronisation, not infrastructure, determines project value long before first oil."),
 "oman": dict(t="Oman's 2026 Onshore Licensing Round: Five Blocks, Three Failed Campaigns", tag="Oman", d="14 Apr 2026", w=1922, u=PULSE+"omans-2026-onshore-licensing-round-five-blocks-three-failed-maradin-j7i3c/",
   s="Block-by-block history, the brownfield-adjacent versus greenfield split, and what it means for FEL scope and the timing of front-end hiring."),
 "me-brownfields": dict(t="Unlocking Middle East Brownfields: The Early-Phase Decisions That Make or Break a Project", tag="Framework · Brownfield", d="28 Nov 2025", w=1238, u=PULSE+"unlocking-middle-east-brownfields-early-phase-make-break-maradin-prvpe/",
   s="Lessons from 50+ early-phase projects on mature and new onshore assets: the decisions that set a brownfield project's outcome before FEED."),
 "digital-oilfield": dict(t="Oilfield Development System: Bridging Engineering and Digital Intelligence", tag="Digital", d="21 Oct 2025", w=806, u=PULSE+"oilfield-development-system-bridging-engineering-digital-maradin-isame/",
   s="Lessons from building a digital oilfield MVP that linked SmartField data, PETEX GAP models and GIS with field systems."),
}
ORDER = ["kirkuk","pressure","kazakhstan","shopping-cart","kuwait","iraq-deals","portfolio-risk","kurdistan","iraq-cycle","integrated-fd","oman","me-brownfields","digital-oilfield"]
FRAMEWORK_KEYS = ["shopping-cart","pressure","integrated-fd","portfolio-risk","me-brownfields"]
MODELS = [
 dict(slug="production-profile", t="Production profile as a shopping cart", u="/models/production-profile/",
      s="Move water cut, target rate and availability and watch the binding surface constraint migrate: water handling, compression, separation, power.", related="shopping-cart"),
 dict(slug="eor-constraint-migration", t="EOR constraint migration", u="/models/eor-constraint-migration/",
      s="Polymer flooding on a light-oil carbonate: concentration, injectivity limit, surface de-rating, CAPEX and NPV on one screen.", related=None),
 dict(slug="kuwait-constraint-map", t="Kuwait 4 MMbpd: system constraint map", u="/models/kuwait-constraint-map/",
      s="Four system layers from reservoir to export. Click each layer to see where the binding constraint sits and how it migrates as capacity is added.", related="kuwait", note="Built on public data from KPC's 2025/26 annual reporting. An analytical view, not an official forecast."),
 dict(slug="kuwait-fields-map", t="Kuwait oil & gas fields: constraint context map", u="/models/kuwait-fields-map/",
      s="The onshore producing base against the 2024–2026 offshore discoveries, with export terminals and Hormuz exposure. Hover over fields for details.", related="kuwait", note="Built on public KOC/KPC information, 2024–2026. An analytical view, not an official map."),
]
IMG_DIR = os.path.join(OUT, "img", "insights")


def cover(key):
    return f"/img/insights/{key}.webp" if os.path.exists(os.path.join(IMG_DIR, key + ".webp")) else None


def mins(w):
    return max(3, math.ceil(w / 230))


def art_card(key, size=""):
    a = ARTICLES[key]; img = cover(key)
    pic = (f'<img src="{img}" alt="" loading="lazy" width="800" height="449">' if img
           else f'<div class="ph"><span>{a["tag"].split(" · ")[0]}</span></div>')
    return (f'<a class="acard {size}" href="{a["u"]}" target="_blank" rel="noopener"><div class="pic">{pic}</div>'
            f'<div class="abody"><small>{a["tag"].upper()} · {a["d"].upper()} · {mins(a["w"])} MIN</small><b>{a["t"]}</b><p>{a["s"]}</p><span class="more">Read on LinkedIn ↗</span></div></a>')


def art_grid(keys, cls="agrid"):
    return f'<div class="{cls}">' + "".join(art_card(k) for k in keys) + "</div>"


def model_card(m):
    return (f'<a class="acard dark" href="/insights/models/{m["slug"]}/"><div class="pic"><img src="/img/insights/model-{m["slug"]}.webp" alt="" loading="lazy"></div>'
            f'<div class="abody"><small>INTERACTIVE MODEL</small><b>{m["t"]}</b><p>{m["s"]}</p><span class="more">Open the model →</span></div></a>')


def related(key):
    return f'<p class="eyebrow" style="margin-top:10px">Related reading</p>{art_grid([key], "agrid one")}'


for m in MODELS:
    rel = related(m["related"]) if m["related"] else ""
    page(f"insights/models/{m['slug']}", m["t"], m["s"],
         f'''<section class="hero small"><div class="container"><p class="eyebrow"><a href="/insights/">Insights</a> / Interactive model</p><h1 class="page">{m["t"]}</h1>
<p class="lead">{m["s"]}</p><p class="avail">{m.get("note", "A mechanism demonstrator calibrated to published analogues, not to any named field.")}</p>
<div class="actions"><a class="button secondary" href="{m["u"]}" target="_blank" rel="noopener">Open full screen ↗</a></div></div></section>
<section class="section tight" style="border-top:0;padding-top:0"><div class="container"><div class="embed"><iframe src="{m["u"]}" title="{m["t"]}" loading="lazy"></iframe></div>
<div style="margin-top:50px">{rel}</div></div></section>''', "/insights/")

regional = [k for k in ORDER if k not in FRAMEWORK_KEYS]
page("insights", "Insights", "Frameworks, interactive models and regional analysis on FEL, brownfield and upstream development.",
     f'''<section class="hero small"><div class="container"><p class="eyebrow">Insights</p><h1 class="page">From project experience<br>to reusable engineering logic.</h1>
<p class="lead">Frameworks, interactive models and regional analysis. Mostly MENA, always through the lens of early-phase decisions.</p></div></section>
<section class="section" style="border-top:0;padding-top:20px"><div class="container"><div class="section-head"><div><p class="eyebrow">Latest</p><h2>Most recent analysis.</h2></div></div>{art_card(ORDER[0], "wide")}</div></section>
<section class="section"><div class="container"><div class="section-head"><div><p class="eyebrow">Interactive models</p><h2>Move the levers.</h2></div><p>Move the inputs and watch the binding constraint migrate. Open any model to use it full screen.</p></div><div class="agrid two">{"".join(model_card(m) for m in MODELS)}</div></div></section>
<section class="section"><div class="container"><div class="section-head"><div><p class="eyebrow">Frameworks</p><h2>How I approach front-end decisions.</h2></div></div>{art_grid([k for k in FRAMEWORK_KEYS])}</div></section>
<section class="section"><div class="container"><div class="section-head"><div><p class="eyebrow">Regional analysis</p><h2>Reading the news as an early-phase engineer.</h2></div><p>Public deals and announcements, and the front-end questions behind them.</p></div>{art_grid([k for k in regional if k != ORDER[0]])}</div></section>''',
     "/insights/")

# ---------------- ADVISORY ----------------
SERVICES = [
    ("01", "Independent FEL / Pre-FEED review", "A second pair of eyes before a gate: are the concept, assumptions and interfaces strong enough for DRB, FEED entry or FID?", ["Gate-readiness review", "Assumption and interface check", "Clear go / fix / stop findings"]),
    ("02", "Concept select & option screening", "Structure the option space, the selection criteria and the economics so the recommended concept survives scrutiny.", ["Option screening", "Selection criteria and scoring", "CAPEX and NPV comparison"]),
    ("03", "Brownfield constraint analysis", "Find the binding constraint in a mature asset (water, gas, power, separation) and sequence what to buy and when.", ["Debottlenecking", "Constraint migration", "Investment sequencing"]),
    ("04", "EPC bid & contract strategy", "When bids land far above the estimate: decompose the gap, quantify risk per package and build renegotiation scenarios.", ["Bid-to-estimate analysis", "Risk allocation", "Renegotiation scenarios"]),
    ("05", "Expert calls", "One-hour calls for investors, consultants and operators on upstream development, brownfield and FEL topics.", ["Directly or via GLG", "Iraq, Kurdistan, Gulf, CIS", "Facilities and gas"]),
    ("06", "FEL & Concept Select workshops", "One- or two-day workshops for engineering teams, built on real gate cases rather than textbook theory.", ["FEL1–FEL2 process", "Concept select in practice", "Decision quality"]),
]
FORMATS = [("Expert call", "1 hour. A focused answer to a specific question."), ("Review sprint", "1–2 weeks, remote. A written review with findings and recommendations."), ("Embedded study lead", "Contract, remote or on-site. Leading a study or FEL phase end to end.")]

page("advisory", "Advisory", "Independent FEL, Pre-FEED and concept select advisory for upstream operators, contractors and investors.",
     f'''<section class="hero small"><div class="container hero-grid"><div><p class="eyebrow">Advisory</p><h1 class="page">Independent front&#8209;end advice,<br>when it matters.</h1>
<p class="lead">For operators, contractors and investors who need an experienced view before committing to FEED, FID or a contract, without hiring a full team.</p>
<div class="actions"><a class="button primary" href="/contact/?type=call">Discuss a project</a><a class="button secondary" href="https://www.linkedin.com/services/page/4540aa333982b8584b/" target="_blank" rel="noopener">LinkedIn Services ↗</a></div></div>
<aside class="metrics"><div><b>50+</b><span>FEL studies led</span></div><div><b>18+</b><span>years operator side</span></div><div><b>$6B+</b><span>EPC portfolio reviewed</span></div><div><b>GMT+8</b><span>remote or on-site</span></div></aside></div></section>
<section class="section" style="border-top:0;padding-top:40px"><div class="container"><div class="section-head"><div><p class="eyebrow">What I do</p><h2>Six ways to work together.</h2></div><p>Each grounded in cases I have delivered. See <a class="textlink" href="/cases/">cases</a>.</p></div>
<div class="services">{"".join(f'<div><b>{n}</b><h3>{t}</h3><p>{d}</p><ul>{"".join(f"<li>— {x}</li>" for x in li)}</ul></div>' for n, t, d, li in SERVICES)}</div></div></section>
<section class="section alt"><div class="container"><p class="eyebrow">Formats</p><h2 style="margin-bottom:40px">From one call to a full study.</h2>
<div class="formats">{"".join(f"<div><b>{t}</b><span>{d}</span></div>" for t, d in FORMATS)}</div>
<div class="actions"><a class="button primary" href="/contact/?type=call">Discuss a project</a></div></div></section>''',
     "/advisory/")

# ---------------- ABOUT ----------------
TIMELINE = [
    ("2024 – now", "Upstream Project Development Advisor", "Independent · Remote", "Early-phase advisory for operators and contractors in the Middle East and CIS: concept and feasibility support, brownfield system optimisation, EPC bid analysis. Independent industry expert with GLG."),
    ("2023 – 2024", "Concept Development Manager", "Salym Petroleum Development (Shell JV)", "Led a portfolio of 50+ FEL1–FEL2 and Pre-FEED studies ($1M–$300M+) through Decision Review Board approvals. 10-year surface facilities strategy across six fields. Built and led a team of five senior engineers."),
    ("2017 – 2023", "Senior Concept Engineer", "Salym Petroleum Development (Shell JV)", "Front-End Development Manager on FEL1–FEL2 and Pre-FEED studies up to $300M+. Cross-field integration programme: 57% portfolio CAPEX reduction. Flow assurance at Technical Authority level 2."),
    ("2014 – 2017", "Senior Project Engineer", "Gazprom Neft · Arctic onshore", "Study Manager for Pre-FEED and FEED on Yaro-Yakhinskoye ($300M+), then Project Engineer / PMO through detailed design and pre-start-up readiness."),
    ("2012 – 2014", "Conceptual Design Engineer", "Salym Petroleum Development (Shell JV)", "15 concept studies ($1M–$26M). Managed international contractors, including KBR and Granherne, on a $46M shale appraisal project. Introduced the engineering MoC system."),
    ("2008 – 2011", "Head of Concept Design / Concept Engineer", "Rosneft", "10+ greenfield and brownfield concept studies. Managed Pre-FEED contractor scopes. Led a team of seven engineers."),
    ("2007 – 2008", "Senior Field Mechanic (LPG/NGL)", "Rosneft · Krasnodarneftegas", "Gas treatment plant and separation station: commissioning, start-up, maintenance and post-incident recovery. Team of 11–13 technicians, zero LTI."),
]
page("about", "About", "Evgeny Maradin: 18+ years in upstream oil & gas on the operator side, focused on FEL1–FEL2, Pre-FEED and brownfield development.",
     f'''<section class="hero small"><div class="container"><p class="eyebrow">About</p><h1 class="page">Operator-side engineer<br><em>for the front end.</em></h1>
<p class="lead">18+ years in upstream oil &amp; gas, most of it on the operator side, focused on the phase where project value, constraints and decision logic are set: FEL1–FEL2, Pre-FEED and brownfield development.</p>
<p class="avail">Based in the Philippines · available to mobilise within 2 weeks · Iraq, Oman, UAE, wider Middle East, Africa, Southeast Asia</p></div></section>
<section class="section" style="border-top:0;padding-top:30px"><div class="container"><p class="eyebrow">Career</p><h2 style="margin-bottom:40px">Where the experience comes from.</h2>
<div class="timeline">{"".join(f"<div><time>{y}</time><div><b>{r}</b><i>{o}</i><p>{d}</p></div></div>" for y, r, o, d in TIMELINE)}</div></div></section>
<section class="section alt"><div class="container"><div class="facts">
<div><h4>Education</h4><p>Specialist Diploma (5-year), Machinery and Equipment of Oil &amp; Gas Fields, Kuban State Technological University, 2007. Assessed by UK ENIC as comparable to a UK Bachelor (Honours) degree, RQF Level 6.</p><a class="doc" href="/docs/uk-enic-statement-of-comparability.pdf" target="_blank" rel="noopener"><img src="/img/docs/uk-enic.webp" alt="UK ENIC Statement of Comparability for Evgeny Maradin" loading="lazy" width="640" height="506"><span>UK ENIC Statement of Comparability · PDF ↗</span></a><p class="doc-note">Reference 4002501645 · verify at <a href="https://www.enic.org.uk/verification" target="_blank" rel="noopener">enic.org.uk/verification</a></p></div>
<div><h4>Tools</h4><p>Petex GAP · PIPESIM · HYSYS · PI Vision · Power BI · SmartField · SAP S/4HANA (PPM) · MS Project · AutoCAD</p></div>
<div><h4>Languages</h4><p>English: professional working proficiency.<br>Russian: native.</p></div>
</div></div></section>''',
     "/about/")


# ---------------- CONTACT ----------------
TOPICS = ["Job opportunity", "Advisory project", "Expert call", "FEL / Concept Select workshop", "Other"]
page("contact", "Contact", "Send a message or book a free 30-minute intro call with Evgeny Maradin.",
     f"""<section class="hero small"><div class="container"><p class="eyebrow">Contact</p><h1 class="page">Let's talk.</h1>
<p class="lead">Send a short message, or book a free 30-minute intro call. I reply within one working day.</p></div></section>
<section class="section" style="border-top:0;padding-top:20px"><div class="container contact-page">
<div><form id="enquiry" class="form" novalidate>
<fieldset class="mode"><legend class="eyebrow">I would like to</legend>
<label><input type="radio" name="type" value="message" checked> Send a message</label>
<label><input type="radio" name="type" value="call"> Book a free 30-min call</label></fieldset>
<div class="row"><label>Name<input name="name" required maxlength="120" autocomplete="name"></label><label>Email<input name="email" type="email" required maxlength="160" autocomplete="email"></label></div>
<div class="row"><label>Company <span>(optional)</span><input name="company" maxlength="160" autocomplete="organization"></label>
<label>Topic<select name="topic">{"".join(f"<option>{t}</option>" for t in TOPICS)}</select></label></div>
<div id="call-fields" hidden><div class="row"><label>Date<input name="date" type="date"></label><label>Time <span>(your time zone: <b id="tz-label"></b>)</span><input name="time" type="time" step="1800"></label></div>
<p id="time-hint" class="hint"></p></div>
<label>Message<textarea name="message" rows="6" maxlength="4000"></textarea></label>
<label class="hp" aria-hidden="true">Website<input name="website" tabindex="-1" autocomplete="off"></label>
<button class="button primary" type="submit">Send message</button>
<p id="form-status" class="form-status" role="status"></p>
</form>
<div id="form-done" class="form-done" hidden><p class="eyebrow">Done</p><h3></h3><p></p></div></div>
<aside class="direct"><p class="eyebrow">Or directly</p>
<a href="mailto:{EMAIL}">{EMAIL}</a>
<a class="wa" href="https://wa.me/639669813383" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.4.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3z"/></svg> WhatsApp: +63 966 981 3383 ↗</a>
<a href="{LI}" target="_blank" rel="noopener">LinkedIn ↗</a>
<p class="avail">Cebu, Philippines (GMT+8). Calls usually work best between 12:00 and 22:00 my time, which covers Gulf mornings and afternoons.</p></aside>
</div></section><script src="/contact.js" defer></script>""",
     "/contact/")

# ---------------- HOME ----------------
featured = [CASES[0], CASES[1], CASES[3]]
page("", "", "Study Manager and Senior Concept Engineer: FEL1–FEL2, Pre-FEED and brownfield development in upstream oil & gas.",
     f'''<section class="hero"><div class="container hero-grid"><div><p class="eyebrow">Concept Development / FEL | Upstream Oil &amp; Gas</p><h1>Engineering decisions<br><em>before FEED.</em></h1>
<p class="lead">Study Manager and Senior Concept Engineer focused on FEL1–FEL2, Pre-FEED, brownfield development and multidisciplinary integration, turning complex project constraints into decision-ready concepts.</p>
<p class="avail">Based in the Philippines · available to mobilise within 2 weeks · Iraq, Oman, UAE, wider Middle East, Africa, Southeast Asia</p>
<div class="actions"><a class="button primary" href="/cases/">View cases</a><a class="button secondary" href="/advisory/">Advisory</a><a class="button secondary" href="{LI}" target="_blank" rel="noopener">LinkedIn ↗</a></div></div>
<aside class="metrics"><div><b>18+</b><span>years upstream O&amp;G</span></div><div><b>50+</b><span>projects &amp; studies</span></div><div><b>$300M+</b><span>project scale</span></div><div><b>57%</b><span>portfolio CAPEX reduction</span></div></aside></div></section>
<section class="trust"><div class="container trust-row"><div><span>Operator side</span><b>Shell JV (Salym Petroleum) · Gazprom Neft · Rosneft</b></div><div><span>Contractors managed</span><b>KBR · Granherne</b></div><div><span>Expert network</span><b>GLG</b></div></div></section>
<section class="statement"><div class="container narrow"><p>Project value is often determined long before detailed engineering starts. The critical work is making assumptions visible, integrating disciplines, testing options and creating a decision that can survive the transition into execution.</p></div></section>
<section class="section"><div class="container"><div class="section-head"><div><p class="eyebrow">Selected cases</p><h2>Evidence, not job titles.</h2></div><p><a class="textlink" href="/cases/">All eight cases →</a></p></div>
<div class="case-grid three">{"".join(case_card(c, num=False) for c in featured)}</div></div></section>
<section class="section alt"><div class="container"><p class="eyebrow">Engineering scope</p><h2>Where I create value.</h2><div class="expertise">
<div><b>01</b><h3>Concept Development</h3><p>FEL1–FEL2, Pre-FEED, option screening, concept selection and investment readiness.</p></div>
<div><b>02</b><h3>Brownfield Optimisation</h3><p>Re-engineering, debottlenecking, live-asset interfaces and execution constraints.</p></div>
<div><b>03</b><h3>Integrated Development</h3><p>Production, subsurface, facilities and operations aligned around one development logic.</p></div>
<div><b>04</b><h3>Economics &amp; Risk</h3><p>CAPEX optimisation, technical uncertainty, execution risk and decision scenarios.</p></div>
<div><b>05</b><h3>Study Leadership</h3><p>Multidisciplinary teams, contractor interfaces, governance and gate-ready deliverables.</p></div>
<div><b>06</b><h3>Digital Decision Support</h3><p>Digital Oilfield experience and interactive models that make constraints visible.</p></div></div></div></section>
<section class="section"><div class="container"><div class="section-head"><div><p class="eyebrow">Latest insights</p><h2>Reading the region as an early-phase engineer.</h2></div><p><a class="textlink" href="/insights/">All insights and models →</a></p></div>{art_grid(ORDER[:3])}</div></section>''',
     "/")

# ---------------- 404 ----------------
with open(os.path.join(OUT, "404.html"), "w", encoding="utf-8") as f:
    f.write('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Not found | Evgeny Maradin</title><meta name="robots" content="noindex"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/style.css"></head><body><section class="hero"><div class="container"><p class="eyebrow">404</p><h1 class="page">This page does not exist.</h1><div class="actions"><a class="button primary" href="/">Home</a><a class="button secondary" href="/cases/">Cases</a></div></div></section></body></html>')

# ---------------- sitemap / robots ----------------
with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "".join(f"<url><loc>{u}</loc></url>\n" for u in sorted(PAGES)) + "</urlset>\n")
with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as f:
    f.write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
print("built")

# ---------------- related-reading placeholders in case pages ----------------
import re as _re, glob as _glob
for _f in _glob.glob(os.path.join(OUT, "cases", "*", "index.html")):
    _h = open(_f, encoding="utf-8").read()
    _h2 = _re.sub(r"@@RELATED:([a-z0-9-]+)@@", lambda m: related(m.group(1)), _h)
    if _h2 != _h: open(_f, "w", encoding="utf-8").write(_h2)
