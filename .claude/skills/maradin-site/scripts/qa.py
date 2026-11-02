"""Site QA: every page at phone (390px) and desktop (1280px) width.

Usage: python3 .claude/skills/maradin-site/scripts/qa.py web <out_dir>
Needs: pip install playwright (Chromium: preinstalled in cloud sessions, else `playwright install chromium`).
Checks horizontal scroll, elements past the screen edge, broken images and internal links,
JS errors and 404s, small tap targets / tiny text (info), and the contact form flow with an
API stub that validates like web/functions/api/contact.js. Full-page screenshots go to <out_dir>.
Expected and harmless: label.hp off-screen (anti-spam honeypot) and 404 /api/prices on /insights/
(Cloudflare Pages Function, not served locally).
"""
import sys, os, json, glob, threading, http.server, functools, urllib.request
from playwright.sync_api import sync_playwright

WEB, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
PORT = 8799
BASE = f"http://127.0.0.1:{PORT}"

class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
handler = functools.partial(Q, directory=WEB)
srv = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), handler)
threading.Thread(target=srv.serve_forever, daemon=True).start()

pages = []
for f in sorted(glob.glob(os.path.join(WEB, "**", "*.html"), recursive=True)):
    rel = os.path.relpath(f, WEB).replace(os.sep, "/")
    if rel.startswith("_"):
        continue
    pages.append("/" + (rel[:-10] if rel.endswith("index.html") else rel))

VIEWS = {
    "mobile": dict(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True,
                   user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"),
    "desktop": dict(viewport={"width": 1280, "height": 800}),
}

PROBE = r"""() => {
 const vw = document.documentElement.clientWidth, out = {};
 out.scrollW = document.documentElement.scrollWidth; out.vw = vw;
 const sel = e => e.tagName.toLowerCase() + (e.id ? '#' + e.id : '') + (e.className && typeof e.className === 'string' ? '.' + e.className.trim().split(/\s+/).join('.') : '');
 const clipped = e => { for (let p = e.parentElement; p; p = p.parentElement) { const s = getComputedStyle(p); if (/(hidden|auto|scroll|clip)/.test(s.overflowX)) return true; } return false; };
 const over = [];
 for (const e of document.body.querySelectorAll('*')) {
   const r = e.getBoundingClientRect(); if (!r.width || !r.height) continue;
   const s = getComputedStyle(e); if (s.position === 'fixed' || s.visibility === 'hidden') continue;
   if ((r.right > vw + 1 || r.left < -1) && !clipped(e)) over.push(sel(e) + ' [' + Math.round(r.left) + '..' + Math.round(r.right) + ']');
 }
 out.overflow = over.slice(0, 8);
 // text overflowing its own box (e.g. long words)
 const tx = [];
 for (const e of document.body.querySelectorAll('h1,h2,h3,h4,p,a,span,b,small,label,button,li,td,th')) {
   if (e.children.length && e.tagName !== 'A' && e.tagName !== 'LABEL') continue;
   if (e.scrollWidth > e.clientWidth + 2 && getComputedStyle(e).overflowX === 'visible' && e.clientWidth > 0 && getComputedStyle(e).display !== 'inline') tx.push(sel(e) + ' "' + e.textContent.trim().slice(0, 40) + '"');
 }
 out.textOverflow = tx.slice(0, 8);
 out.brokenImg = [...document.images].filter(i => i.complete && i.naturalWidth === 0 && !/^https?:\/\/(?!127\.0\.0\.1)/.test(i.src)).map(i => i.getAttribute('src'));
 const small = [];
 if (vw < 500) for (const e of document.querySelectorAll('a,button,input,select,textarea')) {
   const r = e.getBoundingClientRect(); if (!r.width || !r.height) continue;
   if (e.closest('p,li') && e.tagName === 'A') continue; // inline text links are fine
   if (r.height < 24 || r.width < 24) small.push(sel(e) + ' ' + Math.round(r.width) + 'x' + Math.round(r.height) + ' "' + (e.textContent || e.name || '').trim().slice(0, 25) + '"');
 }
 out.smallTargets = small.slice(0, 8);
 const tiny = new Set();
 if (vw < 500) for (const e of document.body.querySelectorAll('*')) {
   if (!e.childNodes.length || ![...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) continue;
   const fs = parseFloat(getComputedStyle(e).fontSize); if (fs < 11) tiny.add(sel(e) + ' ' + fs + 'px');
 }
 out.tinyText = [...tiny].slice(0, 6);
 out.links = [...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href'));
 out.iframes = [...document.querySelectorAll('iframe')].map(f => f.getAttribute('src'));
 out.title = document.title; out.h1 = document.querySelectorAll('h1').length;
 out.viewportMeta = !!document.querySelector('meta[name=viewport]');
 return out;
}"""

report, all_links = {}, set()
with sync_playwright() as p:
    exe = "/opt/pw-browsers/chromium"
    b = p.chromium.launch(executable_path=exe) if os.path.exists(exe) else p.chromium.launch()
    for vname, vopts in VIEWS.items():
        ctx = b.new_context(**vopts)
        for path in pages:
            pg = ctx.new_page()
            errs, failed = [], []
            pg.on("console", lambda m, errs=errs: m.type == "error" and errs.append(m.text[:200]))
            pg.on("pageerror", lambda e, errs=errs: errs.append("JS: " + str(e)[:200]))
            pg.on("requestfailed", lambda r, failed=failed: failed.append(r.url[:120]))
            pg.on("response", lambda r, failed=failed: r.status >= 400 and r.url.startswith(BASE) and failed.append(f"{r.status} {r.url[len(BASE):]}"))
            resp = pg.goto(BASE + path, wait_until="load")
            pg.wait_for_timeout(600)
            d = pg.evaluate(PROBE)
            d["status"] = resp.status
            d["consoleErrors"] = errs
            d["failed"] = [f for f in failed if BASE in f or f.startswith(("4", "5"))]
            d["externalFailed"] = sorted({f.split("/")[2] for f in failed if f.startswith("http") and BASE not in f})
            all_links.update(l for l in d.pop("links") if l.startswith("/"))
            all_links.update(s for s in d["iframes"] if s and s.startswith("/"))
            report.setdefault(path, {})[vname] = d
            shot = os.path.join(OUT, f"{vname}{path.strip('/').replace('/', '__') or '_home'}.png")
            pg.screenshot(path=shot, full_page=True)
            pg.close()
        ctx.close()

    # contact form behaviour on mobile
    ctx = b.new_context(**VIEWS["mobile"])
    pg = ctx.new_page()
    form = {}
    def api(r):
        d = json.loads(r.request.post_data or "{}")
        if not d.get("name") or "@" not in d.get("email", ""):
            return r.fulfill(status=400, content_type="application/json", body='{"ok":false,"error":"Please enter your name and a valid email."}')
        if d.get("type") != "call" and not d.get("message"):
            return r.fulfill(status=400, content_type="application/json", body='{"ok":false,"error":"Please write a short message."}')
        r.fulfill(status=200, content_type="application/json", body='{"ok":true}')
    pg.route("**/api/contact", api)
    pg.goto(BASE + "/contact/")
    form["defaultMode"] = pg.eval_on_selector("input[name=type]:checked", "e => e.value")
    pg.click("text=Book a free 30-min call")
    form["callFieldsVisible"] = pg.is_visible("#call-fields")
    form["submitLabelCall"] = pg.inner_text("button[type=submit]")
    pg.click("text=Send a message")
    form["callFieldsHiddenAgain"] = not pg.is_visible("#call-fields")
    pg.click("button[type=submit]"); pg.wait_for_timeout(500)
    form["emptySubmitError"] = pg.inner_text("#form-status")[:60]
    pg.fill("input[name=name]", "Test User"); pg.fill("input[name=email]", "test@example.com"); pg.fill("textarea[name=message]", "Hello")
    pg.click("button[type=submit]"); pg.wait_for_timeout(800)
    form["successShown"] = pg.is_visible("#form-done")
    form["successText"] = pg.inner_text("#form-done h3") if form["successShown"] else None
    pg.screenshot(path=os.path.join(OUT, "flow_contact_success.png"), full_page=False)
    # call flow
    pg.goto(BASE + "/contact/?type=call")
    form["queryParamSelectsCall"] = pg.eval_on_selector("input[name=type]:checked", "e => e.value") == "call"
    pg.fill("input[name=name]", "Test"); pg.fill("input[name=email]", "t@example.com")
    pg.fill("input[name=date]", "2030-01-15"); pg.fill("input[name=time]", "10:00")
    pg.dispatch_event("input[name=time]", "change")
    form["timeHint"] = pg.inner_text("#time-hint")
    pg.click("button[type=submit]"); pg.wait_for_timeout(800)
    form["callSuccess"] = pg.is_visible("#form-done") and "Call requested" in pg.inner_text("#form-done h3")
    form["calendarButtons"] = pg.locator("#form-done .actions a").count()
    # copy email button
    pg.goto(BASE + "/")
    ctx.grant_permissions(["clipboard-read", "clipboard-write"], origin=BASE)
    pg.click("button.copy"); pg.wait_for_timeout(200)
    form["copyButtonText"] = pg.inner_text("button.copy")
    ctx.close()
    b.close()

# internal links
broken = []
for l in sorted(all_links):
    u = l.split("#")[0].split("?")[0]
    if not u:
        continue
    try:
        urllib.request.urlopen(BASE + u, timeout=5)
    except Exception as e:
        broken.append(f"{l} -> {e}")
srv.shutdown()

json.dump({"pages": report, "form": form, "brokenLinks": broken, "linksChecked": len(all_links)},
          open(os.path.join(OUT, "report.json"), "w"), indent=1, ensure_ascii=False)

issues = 0
for path, vv in report.items():
    for v, d in vv.items():
        prob = {k: d[k] for k in ("overflow", "textOverflow", "brokenImg", "consoleErrors", "failed") if d.get(k)}
        if d["scrollW"] > d["vw"]:
            prob["horizontalScroll"] = f'{d["scrollW"]} > {d["vw"]}'
        if d["status"] != 200:
            prob["status"] = d["status"]
        if prob:
            issues += 1
            print(f"[{v}] {path}: {json.dumps(prob, ensure_ascii=False)}")
print("\nINFO small tap targets / tiny text (mobile):")
for path, vv in report.items():
    d = vv["mobile"]
    if d["smallTargets"] or d["tinyText"]:
        print(f"  {path}: targets={d['smallTargets'][:4]} tiny={d['tinyText'][:3]}")
print("\nexternal hosts not reachable from sandbox:", sorted({h for vv in report.values() for d in vv.values() for h in d["externalFailed"]}))
print("form:", json.dumps(form, ensure_ascii=False))
print("broken internal links:", broken, "of", len(all_links))
print(f"pages: {len(pages)} x {len(VIEWS)} views, pages with issues: {issues}")
