// Canonical host: evgenymaradin.com. www redirects to it (301).
// The old evgeny-maradin.pages.dev address keeps serving the same site for now
// (owner's request); canonical tags on every page point Google to evgenymaradin.com.
// To retire it later, add "evgeny-maradin.pages.dev" to REDIRECT_FROM.
const CANONICAL = "evgenymaradin.com";
const REDIRECT_FROM = new Set(["www.evgenymaradin.com"]);

export async function onRequest(ctx) {
  const url = new URL(ctx.request.url);
  if (REDIRECT_FROM.has(url.hostname)) {
    url.hostname = CANONICAL;
    url.protocol = "https:";
    url.port = "";
    return Response.redirect(url.toString(), 301);
  }
  return ctx.next();
}
