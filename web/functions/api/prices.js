// Cloudflare Pages Function: GET /api/prices
// Delayed benchmark prices for the ticker at the top of every page.
// No API keys. Sources: Yahoo Finance chart API (front-month futures), Stooq CSV as a fallback.
// (OPEC Basket was tried: opec.org returns 403 to Cloudflare servers.) The result is cached at the edge for 15 minutes,
// so the upstream sources are hit at most a few times per hour.

const TTL = 900; // seconds

// key, label, unit, Yahoo symbol, Stooq fallback symbol
const FUTURES = [
  ["brent", "Brent", "$/bbl", "BZ=F", "cb.f"],
  ["wti", "WTI", "$/bbl", "CL=F", "cl.f"],
  ["hh", "Henry Hub", "$/MMBtu", "NG=F", "ng.f"],
  ["ttf", "TTF (EU gas)", "€/MWh", "TTF=F", null],
];
const UA = { "user-agent": "Mozilla/5.0 (compatible; evgeny-maradin.pages.dev price ticker)" };
const num = (x) => (typeof x === "number" && isFinite(x) ? x : null);

async function yahoo(symbol) {
  const r = await fetch(`https://query1.finance.yahoo.com/v8/finance/chart/${encodeURIComponent(symbol)}?range=5d&interval=1d`, { headers: UA });
  if (!r.ok) throw new Error(`yahoo ${r.status}`);
  const res = (await r.json())?.chart?.result?.[0];
  const m = res?.meta;
  const price = num(m?.regularMarketPrice);
  if (price === null) throw new Error("yahoo no price");
  // previous daily settlement: the last daily bar before the one that contains the latest trade
  const ts = res.timestamp || [], closes = res.indicators?.quote?.[0]?.close || [];
  const day = (t) => new Date(t * 1000).toISOString().slice(0, 10);
  const today = m.regularMarketTime ? day(m.regularMarketTime) : null;
  let prev = num(m.previousClose);
  for (let k = ts.length - 1; prev === null && k >= 0; k--) if (day(ts[k]) !== today && num(closes[k]) !== null) prev = closes[k];
  return { price, prev, time: m.regularMarketTime ? m.regularMarketTime * 1000 : null };
}

async function stooq(symbol) {
  const r = await fetch(`https://stooq.com/q/l/?s=${symbol}&f=sd2t2c&h&e=csv`, { headers: UA });
  if (!r.ok) throw new Error(`stooq ${r.status}`);
  const row = (await r.text()).trim().split("\n")[1]?.split(",");
  const price = row ? parseFloat(row[3]) : NaN;
  if (!isFinite(price)) throw new Error("stooq no price");
  return { price, prev: null, time: Date.parse(`${row[1]}T${row[2]}Z`) || null };
}

async function build() {
  const errors = [];
  const jobs = FUTURES.map(async ([key, label, unit, ysym, ssym]) => {
    try { return { key, label, unit, src: "Yahoo Finance", ...(await yahoo(ysym)) }; }
    catch (e) {
      errors.push(`${key}: ${e.message}`);
      if (!ssym) return null;
      try { return { key, label, unit, src: "Stooq", ...(await stooq(ssym)) }; } catch (e2) { errors.push(`${key}: ${e2.message}`); return null; }
    }
  });
  const items = (await Promise.all(jobs)).filter(Boolean).map((i) => ({
    ...i, change: i.prev ? +(((i.price - i.prev) / i.prev) * 100).toFixed(2) : null,
  }));
  return { updated: Date.now(), items, errors };
}

export async function onRequestGet({ request, waitUntil }) {
  const cache = caches.default;
  const key = new Request(new URL("/api/prices", request.url).toString());
  const hit = await cache.match(key);
  if (hit) return hit;
  const data = await build();
  const res = new Response(JSON.stringify(data), {
    headers: { "content-type": "application/json", "cache-control": `public, max-age=${data.items.length ? TTL : 60}` },
  });
  if (data.items.length) waitUntil(cache.put(key, res.clone()));
  return res;
}
