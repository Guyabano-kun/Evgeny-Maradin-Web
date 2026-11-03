// Canonical host: evgenymaradin.com. The old *.pages.dev address and www redirect here (301).
// Preview deployments (<hash>.evgeny-maradin.pages.dev) are left alone, and so is the
// Search Console verification file, so the old property stays verified.
const CANONICAL = "evgenymaradin.com";
const REDIRECT_FROM = new Set(["evgeny-maradin.pages.dev", "www.evgenymaradin.com"]);
const KEEP = new Set(["/google5ee18c8586b05b2f.html"]);

export async function onRequest(ctx) {
  const url = new URL(ctx.request.url);
  if (REDIRECT_FROM.has(url.hostname) && !KEEP.has(url.pathname)) {
    url.hostname = CANONICAL;
    url.protocol = "https:";
    url.port = "";
    return Response.redirect(url.toString(), 301);
  }
  return ctx.next();
}
