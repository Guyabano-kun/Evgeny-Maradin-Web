"""Generates the static multi-page site into web/ (run once; output is committed)."""
import os, sys, html

OUT = sys.argv[1]
LI = "https://www.linkedin.com/in/evgeny-maradin-5279b85a/"
PULSE = "https://www.linkedin.com/pulse/"
EMAIL = "enmaradin@gmail.com"
UPDATED = "October 2026"
SITE = "https://evgeny-maradin.pages.dev"
PAGES = []  # paths written by page(), for sitemap.xml
# search titles (<= ~65 chars) and descriptions (<= ~160 chars) for the key pages
SEO = {
    "": ("Evgeny Maradin | Pre-FEED Study Manager, FEL1–FEL2, Upstream O&G",
         "Study Manager and Senior Concept Engineer, 19 years in upstream oil & gas: FEL1–FEL2, Pre-FEED, brownfield and CAPEX optimisation. Middle East, Africa, Asia."),
    "about": ("About Evgeny Maradin | Lead Project Engineer, Pre-FEED & FEL",
              "19 years in upstream oil & gas, mostly operator side (Shell JV, Gazprom Neft, Rosneft): FEL1–FEL2, Pre-FEED, FEED and brownfield development. Career, education and tools."),
    "advisory": ("FEL & Pre-FEED Advisory for Upstream Oil & Gas | Evgeny Maradin",
                 "Independent FEL and Pre-FEED reviews, concept select, brownfield constraint analysis and EPC bid support for operators, contractors and investors."),
    "cases": ("Case Studies: Concept Select, Brownfield, CAPEX | Evgeny Maradin",
              "Nine upstream oil & gas cases: portfolio integration (-57% CAPEX), water injection re-engineering, gas debottlenecking Pre-FEED, well-pad siting, EPC bid analysis."),
    "insights": ("Upstream FEL Insights & Interactive Models | Evgeny Maradin",
                 "Frameworks, interactive models and regional analysis on FEL, Pre-FEED and brownfield development in Iraq, Kuwait, Oman, UAE and Kazakhstan."),
    "contact": ("Contact Evgeny Maradin | Projects, Expert Calls, Hiring",
                "Send a message or book a free 30-minute intro call about a role, a study or an expert call. Based in the Philippines, available to mobilise within 2 weeks."),
}
PERSON = ('{"@context":"https://schema.org","@type":"Person","name":"Evgeny Maradin","url":"%s/",'
          '"jobTitle":"Study Manager / Senior Concept Engineer (FEL, Pre-FEED)","email":"mailto:%s",'
          '"image":"%s/og.png","sameAs":["%s"],"homeLocation":{"@type":"Place","name":"Philippines"},'
          '"knowsAbout":["FEL1–FEL2","Pre-FEED","Concept Selection","Brownfield Development","CAPEX Optimisation","Upstream Oil and Gas"]}'
          % (SITE, EMAIL, SITE, LI))

NAV = [("/cases/", "Cases", ""), ("/advisory/", "Advisory", ""), ("/insights/", "Insights", ""),
       ("/about/", "About", "hide-sm"), ("/contact/", "Contact", "hide-sm")]


def page(path, title, desc, body, active="", seo=None, og=None, ld_json=None):
    nav = "".join(
        f'<a href="{h}"{" class=%s" % c if c else ""}{" aria-current=page" if h == active else ""}>{t}</a>'
        for h, t, c in NAV)
    full_title = "Evgeny Maradin | Concept Development / FEL" if path == "" else f"{title} | Evgeny Maradin"
    if path in SEO:
        full_title, desc = SEO[path]
    if seo:
        full_title, desc = seo
    url = f"{SITE}/{path}/" if path else f"{SITE}/"
    ld = f'<script type="application/ld+json">{PERSON}</script>' if path == "" else ""
    if ld_json:
        ld = f'<script type="application/ld+json">{ld_json}</script>'
    og_type, og_img = ("article", og) if og else ("website", None)
    og_img_tags = (f'<meta property="og:image" content="{og_img}">' if og_img else
                   f'<meta property="og:image" content="{SITE}/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">')
    PAGES.append(url)
    # market ticker only on the Insights page (next to the production data), not site-wide
    ticker = ('<div class="ticker" id="ticker" aria-label="Oil and gas benchmark prices"><div class="container ticker-row"><b>Markets</b>'
              '<span class="ticker-items" id="ticker-items"></span><small id="ticker-time"></small></div></div>\n') if path == "insights" else ""
    ticker_js = '<script src="/ticker.js" defer></script>\n' if path == "insights" else ""
    doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(full_title)}</title><meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:title" content="{html.escape(full_title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:type" content="{og_type}">
<meta property="og:url" content="{url}">{og_img_tags}
<meta name="twitter:card" content="summary_large_image">{ld}
<link rel="stylesheet" href="/style.css"></head><body>
{ticker}<header><div class="container nav"><a class="brand" href="/" aria-label="Evgeny Maradin, home"><i class="bn-full">Evgeny Maradin</i><i class="bn-short">EM</i><span>.</span></a><nav>{nav}</nav></div></header>
<main id="top">{body}</main>
<section id="contact" class="contact"><div class="container contact-grid"><div><p class="eyebrow">Contact</p><h2>For studies, project development and engineering leadership.</h2></div><div><a href="mailto:{EMAIL}">{EMAIL}</a><button class="copy" type="button" data-copy="{EMAIL}">Copy email</button><a href="tel:+639669813383">+63 966 981 3383</a><a class="wa" href="https://wa.me/639669813383" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.4.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3z"/></svg> WhatsApp ↗</a><a href="/contact/?type=call">Book a free 30-min call →</a><a href="{LI}" target="_blank" rel="noopener">LinkedIn ↗</a><p class="avail">CV and project enquiries by email. Based in the Philippines, available to mobilise within 2 weeks.</p></div></div></section>
<footer><div class="container"><span>Evgeny Maradin · <a href="/cases/">Cases</a> · <a href="/advisory/">Advisory</a> · <a href="/insights/">Insights</a> · <a href="/about/">About</a></span><span>Concept Development / FEL | Upstream Oil &amp; Gas · Updated {UPDATED}</span></div></footer>
<script>document.querySelectorAll('[data-copy]').forEach(b=>b.addEventListener('click',async()=>{{const t=b.dataset.copy;try{{await navigator.clipboard.writeText(t)}}catch(e){{const a=document.createElement('textarea');a.value=t;document.body.appendChild(a);a.select();document.execCommand('copy');a.remove()}}b.textContent='Copied: '+t;setTimeout(()=>b.textContent='Copy email',2500)}}))</script>
{ticker_js}</body></html>'''
    d = os.path.join(OUT, path)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(doc)


NUM = {7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten", 11: "Eleven", 12: "Twelve"}

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
    dict(slug="water-injection", n="02", label="Salym Petroleum · Asset Integrity", years="2023–2024",
         title="Water Injection Re-engineering",
         teaser='Merged a development scope and an asset-integrity programme into one study and replaced a disproportionate redevelopment concept: VRR from 70% to 95% at 80% lower CAPEX.',
         metric="80%", metric_l="CAPEX reduction<br>$3.6M saved", big='80% CAPEX reduction ($3.6M saved), Profitability Index up 300% and voidage replacement from 70% to 95%. Approved at Decision Review Board and adopted as best practice.',
         tags=["Brownfield", "DRB", "Economics"],
         meta=[('Client', 'Salym Petroleum Development'), ('Period', '2023–2024'), ('Role', 'Concept Development Manager'), ('Gate', 'Decision Review Board')],
         context='A mature oil field with a voidage replacement ratio (VRR) of about 70%, a direct threat to reservoir pressure and recovery. The water injection system had been designed for low rates and could no longer deliver the required pressure or capacity. Separately, an asset-integrity scope for the same area was already heading to the DRB with its own budget.',
         role='Concept lead: overall management, concept definition and flow assurance, leading five discipline leads from development, production engineering, integrity, operations and finance.',
         challenge='Six months to reach VRR close to 1 by cluster with a Profitability Index above 1 while cutting base CAPEX. The original redevelopment concept was technically valid but commercially disproportionate for the remaining asset life.',
         action=['Merged the development scope and the asset-integrity programme into one study to capture the synergy.', 'Ran root-cause and flow-assurance analysis and set the key indicators.', 'Designed reconfiguration scenarios, from a partial upgrade to local flow rerouting.', 'Applied competitive scoping to balance risk, cost and performance, re-using existing infrastructure wherever possible.', 'Built the economic model and defended the business case at the Decision Review Board.'],
         result='Endorsed as the base development scenario: debottleneck the well pad nearest the main high-pressure injection corridor and move producers and injectors to remote pads supported by produced water. 80% CAPEX reduction ($3.6M), Profitability Index +300%, VRR from 70% to 95%, asset life extended. Adopted as best practice for re-engineering and asset-integrity projects.',
         insight="shopping-cart"),
    dict(slug="apg-pre-feed", n="03", label="Salym Petroleum · Associated gas", years="2023–2024",
         title="APG Utilisation Pre-FEED",
         teaser='Owner-side Pre-FEED on associated gas: found the facility was gas-limited, selected a right-sized debottlenecking fix and screened about 19 gas-use routes with my own scoring method.',
         metric="$160M", metric_l="project scale<br>Pre-FEED", big='Gas loading peaking at 2.15× installed capacity; a compact pre-separation takeoff about 3× cheaper than separator options and the only one stable at peak gas-oil ratio. Pre-FEED for a $160M project.',
         tags=["Study Management", "Pre-FEED", "Gas"],
         meta=[("Client", "Salym Petroleum Development"), ("Period", "2023–2024"), ("Role", "Study lead"), ("Duration", "8 months")],
         context='Associated petroleum gas utilisation at a mature onshore oil asset. As the field gassed out, the gas-oil ratio was set to rise roughly 13-fold over field life, and the existing processing facility was already close to capacity.',
         role='Study lead on the owner side as Concept Development Manager. Engineering was executed by an external technical centre under my direction; the evaluation criteria, the weighted scoring method and the one-page decision-brief format were my design.',
         challenge='Find the true capacity constraint over the full life of field, fix it without building permanent worst-case steel, and decide what to do with the gas, all within an eight-month Pre-FEED that had to align production, facilities and contractor scopes.',
         action=['Screened facility loading phase by phase (liquid, oil, water, gas) with a hydraulic throughput model over a 17-year profile: the asset was gas-limited, not liquid-limited.', 'Checked equipment adequacy unit by unit: actual against rated flow on every separator, scrubber, flare and multiphase pump.', 'Identified the system bottlenecks together with the process engineer and set the engineering direction; proposed most of the practical options, with the contractor adding the unconventional ones.', 'Defined three debottlenecking configurations to comparable maturity and screened them on cost and on stability at peak inlet gas-oil ratio.', 'Defined the weighted scoring method, trained the engineering centre to apply it and required a one-page technical note per option, so weak options were dropped before deep engineering.', 'Screened about 19 gas-use routes, from third-party processing, reinjection and power to GTL, methanol and LNG, down to a realistic shortlist.', 'Flagged early that the inlet tie-in needed a facility shutdown, so the work was folded into a planned turnaround.'],
         result='Compact pre-separation gas takeoff selected: about 3× cheaper than the separator-based options and the only configuration stable at peak gas-oil ratio. The gas peak lasts about five years, so capacity was phased instead of sized for permanent worst case, and the short plateau ruled out gas chemistry as the wrong scale of solution. Pre-FEED delivered for the $160M project as the basis for concept selection and investment readiness.',
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
         metric="$300M+", metric_l="programme scale<br>within schedule", big='New facilities integrated without production disruption on a $300M+ programme; FEED interface gap closed in a week, so the construction permit came on schedule.',
         tags=["FEED", "Brownfield", "Execution"],
         meta=[("Client", "Gazprom Neft · Arcticgas JV"), ("Period", "2014–2017"), ("Role", "Study Manager → Project Engineer / PMO"), ("Phase", "Pre-FEED → Detailed design")],
         context="Greenfield-to-brownfield transition on an active producing asset in Arctic conditions.",
         role="Led Pre-FEED and FEED as Study Manager, then supported detailed engineering as Project Engineer / PMO, including construction and pre-start-up readiness assessments.",
         challenge="New facilities had to be tied into live production in a remote Arctic environment. Civil works were possible only in winter, so a month's slip in design approval risked a one-year deferral, and survey data and key tie-in areas were split across several FEED contractors.",
         action=['Coordinated engineering disciplines through Pre-FEED and FEED.', 'On my own initiative ran an integrated review of key FEED documents and found a mismatch at the export pipeline and central processing facility tie-in point.', 'Brought the contractors and stakeholders together, set roles, responsibility zones and a short correction plan across FEED and detailed design; the changes were aligned within a week.', 'Led risk management and change control during execution preparation.'],
         result='FEED documentation submitted to state expert review on time with no interface findings, and the construction permit secured on schedule. Facilities integrated without production disruption on a $300M+ programme. The lesson, interface checks in a dedicated early FEED stage, was added to the Gazprom Neft corporate lessons-learned register.',
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
    dict(slug="minor-capex", n="07", label="Salym Petroleum · Asset & Integrity", years="2012–2024",
         title="Minor CAPEX Portfolio – Debottlenecking & Integrity",
         teaser="Led FEL for minor CAPEX projects that kept a mature asset running: debottlenecking, integrity and reliability of the gathering system and field facilities.",
         metric="$1–20M", metric_l="TEC per project<br>FEL1–FEL2", big="A continuous stream of $1M–$20M projects taken through FEL: debottlenecking up to 10% value uplift, integrity cost savings up to 20%, Profitability Index up to +25%.",
         tags=["Minor CAPEX", "Debottlenecking", "Integrity & Reliability"],
         meta=[("Client", "Salym Petroleum Development"), ("Scope", "Gathering system & field facilities"), ("Role", "Concept lead / Front-End Development Manager"), ("Project size", "TEC $1M–$20M")],
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
    dict(slug="well-pad-siting", n="09", label="Shell JV · Field infrastructure", years="2018–2023",
         title="Well-Pad & Corridor Siting Method",
         teaser="Built an integrated method for choosing well-pad locations and infrastructure corridors that cut lifecycle cost by 10–50%.",
         metric="10–50%", metric_l="lifecycle cost<br>reduction", big="10–50% lifecycle cost reduction depending on the case, with corridor length down 15–35% and earthworks down 10–30%. Adopted as company best practice for well-pad planning.",
         tags=["Concept Select", "Field Infrastructure", "Method"],
         meta=[("Client", "Salym Petroleum Development (Shell JV)"), ("Period", "2018–2023"), ("Role", "Senior Concept Engineer"), ("Gate", "Decision Review Board")],
         context="Well-pad locations had historically been set mainly by the well pattern. That worked for simple structures, but with horizontal drilling and more complex topography it was pushing unit technical cost up and development efficiency down.",
         role="Senior Concept Engineer: led a cross-discipline group across geology, drilling, infrastructure, economics and legal, and designed the evaluation framework.",
         challenge="Hit drilling and geology targets at minimum lifecycle cost, within environmental and land-allocation limits, while balancing technical achievability against economics under high input-data uncertainty.",
         action=["Set up a group across geology, drilling, infrastructure, economics and legal.",
                 "Built an evaluation framework with more than 20 parameters: horizontal section length, entry angle, logistics, crossings, land-allocation limits, CAPEX and OPEX.",
                 "Generated 9 to 30 alternative pad locations per case, ranked them and shortlisted the top 3 to 5 with GIS models, cost models and scenario analysis.",
                 "Produced a recommended and an alternative option with quantified savings per driver and aligned them at the DRB."],
         result="10–50% lifecycle cost reduction depending on the case; corridor length down 15–35% and earthworks down 10–30%. The method became company best practice for well-pad planning, with faster alignment between technical and economic teams and more predictable budgets.",
         insight="integrated-fd"),
]


def case_card(c, full=False, num=True):
    cls = "case feature" if c.get("feature") else "case"
    n = f'{c["n"]} · ' if num else ""
    return (f'<a class="{cls}" href="/cases/{c["slug"]}/"><small>{n}{c["label"].upper()}{" · " + c["years"].upper() if c["years"] else ""}</small>'
            f'<h3>{c["title"]}</h3><p>{c["teaser"]}</p>'
            f'<div class="result"><b>{c["metric"]}</b><span>{c["metric_l"]}</span></div>'
            + (f'<div class="tags">{"".join(f"<i>{t}</i>" for t in c["tags"])}</div>' if full else "")
            + '<span class="more">Read case →</span></a>')


# ---------------- case figures ----------------
_gas = [.84, .79, .77, .73, .76, 1.05, 1.57, 1.77, 1.64, 1.8, 2.01, 2.15, 2.05, 1.54, 1.06, .68, .45]
_pts = " ".join(f"{60 + i * 47.5:.1f},{280 - v / 2.3 * 250:.1f}" for i, v in enumerate(_gas))
FIGURES = {
    "apg-pre-feed": f'''<figure class="case-fig"><figcaption>Gas loading against installed capacity over the life of field</figcaption>
<svg viewBox="0 0 860 330" role="img" aria-label="Gas loading peaks at 2.15 times installed capacity around year 12 and falls back below 1 by year 15">
<line x1="60" y1="280" x2="820" y2="280" class="ax"/><line x1="60" y1="30" x2="60" y2="280" class="ax"/>
<g class="lab"><text x="30" y="284">0</text><text x="26" y="228">0.5</text><text x="26" y="175">1.0</text><text x="26" y="120">1.5</text><text x="26" y="65">2.0</text>
<text x="60" y="300" text-anchor="middle">Y1</text><text x="250" y="300" text-anchor="middle">Y5</text><text x="440" y="300" text-anchor="middle">Y9</text><text x="630" y="300" text-anchor="middle">Y13</text><text x="820" y="300" text-anchor="middle">Y17</text>
<text x="440" y="322" text-anchor="middle">project year (life of field)</text></g>
<line x1="60" y1="171.3" x2="820" y2="171.3" class="cap"/><text x="70" y="164" class="lab">installed capacity = 1.0</text>
<line x1="250" y1="30" x2="250" y2="280" class="fix"/><text x="256" y="250" class="fixt">pre-separation gas takeoff</text>
<polyline points="{_pts}" class="load"/>
<circle cx="582.5" cy="46.2" r="4.5" class="pk"/><text x="582.5" y="36" text-anchor="middle" class="pkt">peak 2.15×</text>
</svg>
<table><thead><tr><th>Debottlenecking option</th><th>Relative CAPEX</th><th>At peak gas-oil ratio</th><th>Verdict</th></tr></thead><tbody>
<tr><td>Compact pre-separation gas takeoff</td><td>1.0×</td><td>stable</td><td><b>selected</b></td></tr>
<tr><td>Three-phase separator train</td><td>~3.1×</td><td>unstable</td><td>rejected</td></tr>
<tr><td>Gas–liquid separator train</td><td>~4.5×</td><td>unstable</td><td>rejected</td></tr>
</tbody></table>
<p class="fig-note">Illustrative figures: loading fractions, ratios and relative CAPEX only. No asset name, contractor or absolute costs.</p></figure>''',
}

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
<div><h4>Result</h4><p>{c["result"]}</p></div></div>{FIGURES.get(c["slug"], "")}
<div class="tags" style="margin:30px 0 50px">{"".join(f"<i>{t}</i>" for t in c["tags"])}</div>
<div style="margin-bottom:50px">@@RELATED:{c["insight"]}@@</div>
<div class="pager"><a href="/cases/{prev_c["slug"]}/"><small>← Previous case</small><b>{prev_c["title"]}</b></a><a href="/cases/{next_c["slug"]}/"><small>Next case →</small><b>{next_c["title"]}</b></a></div>
</div></section>'''
    page(f"cases/{c['slug']}", c["title"], c["teaser"], body, "/cases/")

page("cases", "Cases", "Selected cases in concept development, brownfield optimisation and project decision support.",
     f'''<section class="hero small"><div class="container"><p class="eyebrow">Selected cases</p><h1 class="page">Evidence,<br>not job titles.</h1>
<p class="lead">{NUM[len(CASES)]} cases from concept development, brownfield optimisation and project decision support. Each one: the context, my role, what was hard, what I did and what changed.</p></div></section>
<section class="section tight" style="border-top:0"><div class="container"><div class="case-grid">{"".join(case_card(c, True) for c in CASES)}</div></div></section>''',
     "/cases/")

# ---------------- INSIGHTS ----------------
import math, datetime
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
    if key in ARTICLE_MD:  # full text hosted on this site
        href, more = f'href="/insights/{key}/"', "Read article →"
    else:
        href, more = f'href="{a["u"]}" target="_blank" rel="noopener"', "Read on LinkedIn ↗"
    return (f'<a class="acard {size}" {href}><div class="pic">{pic}</div>'
            f'<div class="abody"><small>{a["tag"].upper()} · {a["d"].upper()} · {mins(a["w"])} MIN</small><b>{a["t"]}</b><p>{a["s"]}</p><span class="more">{more}</span></div></a>')


# ---------------- full article texts (content/articles/<key>.md, copied verbatim from LinkedIn) ----------------
import re, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTICLE_MD = {}
for _k in ARTICLES:
    _p = os.path.join(ROOT, "content", "articles", _k + ".md")
    if os.path.exists(_p):
        _t = open(_p, encoding="utf-8").read()
        _fm, _body = _t.split("\n---\n", 1)
        _meta = dict(re.findall(r'^(\w+): "?(.*?)"?$', _fm.strip("-\n"), re.M))
        ARTICLE_MD[_k] = (_meta, _body.strip("\n"))
_IMG_SIZES = json.load(open(os.path.join(ROOT, "tools", "img_sizes.json"), encoding="utf-8"))
# search titles (title + " | Evgeny Maradin" <= 65) and descriptions (<= 160) for article pages
ART_SEO = {
    "kirkuk": ("Kirkuk: Fast First Barrels, Slow Gas Outlets",
               "Kirkuk is going from 320,000 to 420,000 bpd. Early barrels come quickly from existing wells; gas outlets take years. The real question is sequencing."),
    "pressure": ("Pressure Decisions: Reservoir vs Facilities", None),
    "kazakhstan": ("Kazakhstan's 24 Blocks: Options, Not Acreage", None),
    "kuwait": ("Kuwait 4 MMbpd: Not a Drilling Problem", None),
    "portfolio-risk": ("Portfolio Integration Risk Nobody Owns", None),
    "kurdistan": ("Kurdistan and Delivery Certainty in Upstream", None),
    "integrated-fd": ("Field Development Is About Managing Constraints", None),
    "oman": ("Oman 2026 Onshore Bid Round: Five Blocks", None),
    "me-brownfields": ("Middle East Brownfields: Early-Phase Decisions", None),
    "digital-oilfield": ("Digital Oilfield System: Lessons Learned", None),
}


def _inline(s):
    """Markdown inline subset used by the LinkedIn exports: links, bold, italic, line breaks."""
    links = []

    def keep(m):
        url = m.group(2)
        ext = url.startswith("http")
        links.append(f'<a href="{html.escape(url)}"' + (' target="_blank" rel="noopener"' if ext else "") + f'>{_inline(m.group(1))}</a>')
        return f"\x00{len(links) - 1}\x00"
    s = re.sub(r"\[((?:[^\[\]]|\[[^\]]*\])*)\]\(([^)\s]+)\)", keep, s)
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*\*(\S(?:.*?\S)?)\*\*\*", r"<b><i>\1</i></b>", s)
    s = re.sub(r"\*\*(\S(?:.*?\S)?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<![\*\w])\*(\S(?:.*?\S)?)\*(?![\*\w])", r"<i>\1</i>", s)
    s = s.replace("  \n", "<br>").replace("\n", " ")
    return re.sub(r"\x00(\d+)\x00", lambda m: links[int(m.group(1))], s)


def md_to_html(md):
    out = []
    for blk in re.split(r"\n{2,}", md.strip()):
        lines = blk.split("\n")
        if blk.strip() == "---":
            out.append("<hr>")
        elif re.match(r"#{1,6} ", blk):
            n = min(max(len(blk) - len(blk.lstrip("#")), 2), 4)
            out.append(f"<h{n}>{_inline(blk.lstrip('#').strip())}</h{n}>")
        elif blk.startswith("![") and re.match(r"!\[(.*?)\]\((.*?)\)$", lines[0]):
            alt, src = re.match(r"!\[(.*?)\]\((.*?)\)$", lines[0]).groups()
            w, h = _IMG_SIZES.get(src, (1200, 675))
            cap = lines[1].strip("*").strip() if len(lines) > 1 else ""
            out.append(f'<figure><img src="{html.escape(src)}" alt="{html.escape(alt or cap)}" loading="lazy" width="{w}" height="{h}">'
                       + (f"<figcaption>{_inline(cap)}</figcaption>" if cap else "") + "</figure>")
        elif all(l.startswith("> ") or l == ">" for l in lines):
            out.append(f"<blockquote><p>{_inline(chr(10).join(l[2:] for l in lines))}</p></blockquote>")
        elif all(l.startswith("- ") for l in lines):
            out.append("<ul>" + "".join(f"<li>{_inline(l[2:])}</li>" for l in lines) + "</ul>")
        elif all(re.match(r"\d+\. ", l) for l in lines):
            start = int(lines[0].split(".")[0])
            out.append(f'<ol{" start=%d" % start if start != 1 else ""}>' + "".join(f"<li>{_inline(l.split('. ', 1)[1])}</li>" for l in lines) + "</ol>")
        else:
            out.append(f"<p>{_inline(blk)}</p>")
    return "\n".join(out)


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
# analyst note under the production chart: content/production-note.md (front matter: date, data_to; body = paragraphs)
_pn = os.path.join(ROOT, "content", "production-note.md")
PROD_NOTE = ""
if os.path.exists(_pn):
    _fm, _pb = open(_pn, encoding="utf-8").read().split("\n---\n", 1)
    _pm = dict(re.findall(r'^(\w+): ?(.*)$', _fm.strip("-\n"), re.M))
    _d = datetime.date.fromisoformat(_pm["date"])
    PROD_NOTE = (f'<div class="prod-note"><p class="eyebrow">Evgeny&#8217;s note · {_d.strftime("%B %Y")} · data to {html.escape(_pm.get("data_to", ""))}</p>'
                 + md_to_html(_pb) + "</div>")
page("insights", "Insights", "Frameworks, interactive models and regional analysis on FEL, brownfield and upstream development.",
     f'''<section class="hero small"><div class="container"><p class="eyebrow">Insights</p><h1 class="page">From project experience<br>to reusable engineering logic.</h1>
<p class="lead">Frameworks, interactive models and regional analysis. Mostly MENA, always through the lens of early-phase decisions.</p></div></section>
<section class="section" style="border-top:0;padding-top:20px"><div class="container"><div class="section-head"><div><p class="eyebrow">Latest</p><h2>Most recent analysis.</h2></div></div>{art_card(ORDER[0], "wide")}</div></section>
<section class="section" id="production"><div class="container"><div class="section-head"><div><p class="eyebrow">Production data</p><h2>Who is producing, month by month.</h2></div><p>Crude oil production by country, refreshed monthly. Top producers shown, the rest summed. Filter by period and region; click countries in the table to compare your own selection.</p></div>
<div class="prod" id="prod"><div class="prod-bar"><div class="prod-period" role="group" aria-label="Period"></div>
<label>Region <select class="prod-region"></select></label><label>Show <select class="prod-top"></select></label></div>
<p class="prod-total"></p><p class="prod-auto"></p><div class="prod-chart"><p class="prod-err">Loading production data…</p></div><div class="prod-legend"></div>{PROD_NOTE}
<details class="prod-more" open><summary>All countries <span class="prod-mode"></span><button type="button" class="prod-reset" hidden>Back to top producers</button></summary>
<div class="prod-scroll"><table class="prod-table"><thead><tr><th>#</th><th>Country</th><th>Region</th><th>Latest month</th><th>Last 12 m avg</th><th>vs prior 12 m</th></tr></thead><tbody></tbody></table></div></details>
<p class="prod-src"></p></div></div></section>
<script src="/production.js" defer></script>
<section class="section"><div class="container"><div class="section-head"><div><p class="eyebrow">Interactive models</p><h2>Move the levers.</h2></div><p>Move the inputs and watch the binding constraint migrate. Open any model to use it full screen.</p></div><div class="agrid two">{"".join(model_card(m) for m in MODELS)}</div></div></section>
<section class="section"><div class="container"><div class="section-head"><div><p class="eyebrow">Frameworks</p><h2>How I approach front-end decisions.</h2></div></div>{art_grid([k for k in FRAMEWORK_KEYS])}</div></section>
<section class="section"><div class="container"><div class="section-head"><div><p class="eyebrow">Regional analysis</p><h2>Reading the news as an early-phase engineer.</h2></div><p>Public deals and announcements, and the front-end questions behind them.</p></div>{art_grid([k for k in regional if k != ORDER[0]])}</div></section>''',
     "/insights/")

# ---------------- ARTICLE PAGES (/insights/<key>/) ----------------
for i, key in enumerate(ORDER):
    if key not in ARTICLE_MD:
        continue
    a = ARTICLES[key]; meta, body = ARTICLE_MD[key]
    url = f"{SITE}/insights/{key}/"
    img = cover(key)
    st, sd = ART_SEO.get(key, (None, None))
    seo_title = (st or meta["title"]) + " | Evgeny Maradin"
    seo_desc = sd or a["s"]
    assert len(seo_title) <= 65 and len(seo_desc) <= 160, (key, len(seo_title), len(seo_desc))
    ld = json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": meta["title"][:110],
                     "description": seo_desc, "datePublished": meta["date"],
                     "author": {"@type": "Person", "name": "Evgeny Maradin", "url": f"{SITE}/about/"},
                     "image": f"{SITE}{img}" if img else f"{SITE}/og.png",
                     "mainEntityOfPage": {"@type": "WebPage", "@id": url}, "url": url,
                     "isBasedOn": meta["url"]}, ensure_ascii=False)
    cases_rel = [c for c in CASES if c["insight"] == key]
    models_rel = [m for m in MODELS if m["related"] == key]
    others = [k for k in ORDER[i + 1:] + ORDER[:i] if k != key][:2]
    rel = ""
    if cases_rel:
        rel += f'<div class="case-grid{" three" if len(cases_rel) > 2 else ""}" style="margin-bottom:28px">{"".join(case_card(c, num=False) for c in cases_rel)}</div>'
    if models_rel:
        rel += f'<div class="agrid two" style="margin-bottom:28px">{"".join(model_card(m) for m in models_rel)}</div>'
    rel += art_grid(others, "agrid two")
    body_html = md_to_html(body)
    page(f"insights/{key}", meta["title"], seo_desc,
         f'''<article><section class="hero small"><div class="container narrow"><p class="eyebrow"><a href="/insights/">Insights</a> / {a["tag"]}</p>
<h1 class="page article-title">{html.escape(meta["title"])}</h1><p class="lead">{a["s"]}</p>
<p class="art-meta"><time datetime="{meta["date"]}">{a["d"]}</time> · {mins(a["w"])} min read · Evgeny Maradin</p></div></section>
<section class="section tight" style="border-top:0;padding-top:0"><div class="container narrow">
{f'<img class="art-cover" src="{img}" alt="" width="{_IMG_SIZES[img][0]}" height="{_IMG_SIZES[img][1]}">' if img else ""}
<div class="prose">
{body_html}
</div>
<p class="art-source"><a href="{a["u"]}" target="_blank" rel="noopener">Originally published on LinkedIn ↗</a></p>
</div></section></article>
<section class="section"><div class="container"><p class="eyebrow">Related reading</p>{rel}</div></section>''',
         "/insights/", seo=(seo_title, seo_desc), og=f"{SITE}{img}" if img else None, ld_json=ld)

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
<div class="actions"><a class="button primary" href="/contact/?type=call">Discuss a project</a><a class="button secondary" href="{LI}" target="_blank" rel="noopener">LinkedIn profile ↗</a></div></div>
<aside class="metrics"><div><b>50+</b><span>FEL studies led</span></div><div><b>19</b><span>years upstream O&amp;G</span></div><div><b>$6B+</b><span>EPC portfolio reviewed</span></div><div><b>GMT+8</b><span>remote or on-site</span></div></aside></div></section>
<section class="section" style="border-top:0;padding-top:40px"><div class="container"><div class="section-head"><div><p class="eyebrow">What I do</p><h2>Six ways to work together.</h2></div><p>Each grounded in cases I have delivered. See <a class="textlink" href="/cases/">cases</a>.</p></div>
<div class="services">{"".join(f'<div><b>{n}</b><h3>{t}</h3><p>{d}</p><ul>{"".join(f"<li>— {x}</li>" for x in li)}</ul></div>' for n, t, d, li in SERVICES)}</div></div></section>
<section class="section alt"><div class="container"><p class="eyebrow">Formats</p><h2 style="margin-bottom:40px">From one call to a full study.</h2>
<div class="formats">{"".join(f"<div><b>{t}</b><span>{d}</span></div>" for t, d in FORMATS)}</div>
<div class="actions"><a class="button primary" href="/contact/?type=call">Discuss a project</a></div></div></section>''',
     "/advisory/")

# ---------------- ABOUT ----------------
TIMELINE = [
    ("2024 – now", "Upstream Project Development Advisor", "Independent · Remote", "Early-phase advisory for operators and contractors in the Middle East and CIS: concept and feasibility support, brownfield system optimisation, EPC bid analysis. Independent industry expert with GLG."),
    ("2023 – 2024", "Concept Development Manager", "Salym Petroleum Development", "Led a portfolio of 50+ FEL1–FEL2 and Pre-FEED studies ($1M–$300M+) through Decision Review Board approvals. 10-year surface facilities strategy across six fields. Built and led a team of five senior engineers."),
    ("2017 – 2023", "Senior Concept Engineer", "Salym Petroleum Development (Shell JV)", "Front-End Development Manager on FEL1–FEL2 and Pre-FEED studies up to $300M+. Cross-field integration programme: 57% portfolio CAPEX reduction. Flow assurance at Technical Authority level 2."),
    ("2014 – 2017", "Senior Project Engineer", "Gazprom Neft · Arctic onshore", "Study Manager for Pre-FEED and FEED on Yaro-Yakhinskoye ($300M+), then Project Engineer / PMO through detailed design and pre-start-up readiness."),
    ("2012 – 2014", "Conceptual Design Engineer", "Salym Petroleum Development (Shell JV)", "15 concept studies ($1M–$26M). Managed international contractors, including KBR and Granherne, on a $46M shale appraisal project. Introduced the engineering MoC system."),
    ("2008 – 2011", "Head of Concept Design / Concept Engineer", "Rosneft", "Engineering-centre (contractor) side: delivered 10+ greenfield and brownfield concept and Pre-FEED studies for Rosneft subsidiaries, held the study budget and competed with other centres for scope. Led a team of seven engineers."),
    ("2007 – 2008", "Senior Field Mechanic (LPG/NGL)", "Rosneft · Krasnodarneftegas", "Four-stage oil–gas separation train feeding a DEG gas treatment plant (dry gas, LPG, stabilised condensate): commissioning of a new pump station, start-up, maintenance and post-incident recovery, including winter operation. Team of 11–13 technicians, zero LTI."),
]
page("about", "About", "Evgeny Maradin: 19 years in upstream oil & gas, mostly on the operator side, focused on FEL1–FEL2, Pre-FEED and brownfield development.",
     f'''<section class="hero small"><div class="container"><p class="eyebrow">About</p><h1 class="page">Operator-side engineer<br><em>for the front end.</em></h1>
<p class="lead">19 years in upstream oil &amp; gas, most of it on the operator side, focused on the phase where project value, constraints and decision logic are set: FEL1–FEL2, Pre-FEED and brownfield development.</p>
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
     f'''<section class="hero"><div class="container hero-grid"><div><p class="hero-name">Evgeny Maradin</p><p class="eyebrow">Concept Development / FEL | Upstream Oil &amp; Gas</p><h1>Engineering decisions<br><em>before FEED.</em></h1>
<p class="lead">Study Manager and Senior Concept Engineer focused on FEL1–FEL2, Pre-FEED, brownfield development and multidisciplinary integration, turning complex project constraints into decision-ready concepts.</p>
<p class="avail">Based in the Philippines · available to mobilise within 2 weeks · Iraq, Oman, UAE, wider Middle East, Africa, Southeast Asia</p>
<div class="actions"><a class="button primary" href="/cases/">View cases</a><a class="button secondary" href="/advisory/">Advisory</a><a class="button secondary" href="{LI}" target="_blank" rel="noopener">LinkedIn ↗</a></div></div>
<aside class="metrics"><div><b>19</b><span>years upstream O&amp;G</span></div><div><b>50+</b><span>projects &amp; studies</span></div><div><b>$300M+</b><span>project scale</span></div><div><b>57%</b><span>portfolio CAPEX reduction</span></div></aside></div></section>
<section class="trust"><div class="container trust-row"><div><span>Operator side</span><b>Shell JV (Salym Petroleum) · Gazprom Neft · Rosneft</b></div><div><span>Contractors managed</span><b>KBR · Granherne</b></div><div><span>Expert network</span><b>GLG</b></div></div></section>
<section class="statement"><div class="container narrow"><p>Project value is often determined long before detailed engineering starts. The critical work is making assumptions visible, integrating disciplines, testing options and creating a decision that can survive the transition into execution.</p></div></section>
<section class="section"><div class="container"><div class="section-head"><div><p class="eyebrow">Selected cases</p><h2>Evidence, not job titles.</h2></div><p><a class="textlink" href="/cases/">All {NUM[len(CASES)].lower()} cases →</a></p></div>
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

print("built")

# ---------------- related-reading placeholders in case pages ----------------
import re as _re, glob as _glob
for _f in _glob.glob(os.path.join(OUT, "cases", "*", "index.html")):
    _h = open(_f, encoding="utf-8").read()
    _h2 = _re.sub(r"@@RELATED:([a-z0-9-]+)@@", lambda m: related(m.group(1)), _h)
    if _h2 != _h: open(_f, "w", encoding="utf-8").write(_h2)

# ---------------- sitemap / robots ----------------
import hashlib, json, datetime
LASTMOD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lastmod.json")
try:
    lm = json.load(open(LASTMOD, encoding="utf-8"))
except FileNotFoundError:
    lm = {}
today = datetime.date.today().isoformat()
for u in PAGES:
    rel = u[len(SITE) + 1:]
    h = hashlib.sha1(open(os.path.join(OUT, rel, "index.html"), "rb").read()).hexdigest()
    if lm.get(u, {}).get("sha1") != h:
        lm[u] = {"sha1": h, "date": today}
json.dump({u: lm[u] for u in sorted(PAGES)}, open(LASTMOD, "w", encoding="utf-8"), indent=1)
with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "".join(f"<url><loc>{u}</loc><lastmod>{lm[u]['date']}</lastmod></url>\n" for u in sorted(PAGES)) + "</urlset>\n")
with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as f:
    f.write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
