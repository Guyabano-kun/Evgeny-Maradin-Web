// Cloudflare Pages Function: POST /api/contact
// Sends the website enquiry to the site owner via Resend.
// Required env var (Cloudflare Pages > Settings > Environment variables): RESEND_API_KEY
// Optional: CONTACT_TO (defaults to the owner's address)

const DEFAULT_TO = "enmaradin@gmail.com";
const MAX = { name: 120, email: 160, company: 160, topic: 80, message: 4000 };

const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const icsText = (s) => String(s).replace(/\\/g, "\\\\").replace(/\n/g, "\\n").replace(/[,;]/g, (c) => "\\" + c);
const icsDate = (d) => d.toISOString().replace(/[-:]/g, "").replace(/\.\d{3}/, "");

function buildIcs({ start, minutes, name, email, topic, message, owner }) {
  const end = new Date(start.getTime() + minutes * 60000);
  const uid = `${start.getTime()}-${Math.random().toString(36).slice(2)}@evgeny-maradin.pages.dev`;
  const lines = [
    "BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Evgeny Maradin//Website booking//EN", "CALSCALE:GREGORIAN", "METHOD:REQUEST",
    "BEGIN:VEVENT", `UID:${uid}`, `DTSTAMP:${icsDate(new Date())}`, `DTSTART:${icsDate(start)}`, `DTEND:${icsDate(end)}`,
    `SUMMARY:${icsText(`Intro call: ${name} / Evgeny Maradin`)}`,
    `DESCRIPTION:${icsText(`Free ${minutes}-min intro call booked via website.\nTopic: ${topic}\n\n${message}`)}`,
    `ORGANIZER;CN=Evgeny Maradin:mailto:${owner}`,
    `ATTENDEE;CN=${icsText(name)};RSVP=TRUE:mailto:${email}`,
    "STATUS:TENTATIVE", "END:VEVENT", "END:VCALENDAR",
  ];
  return lines.join("\r\n");
}

const json = (obj, status = 200) => new Response(JSON.stringify(obj), { status, headers: { "content-type": "application/json" } });

export async function onRequestPost({ request, env }) {
  let d;
  try { d = await request.json(); } catch { return json({ ok: false, error: "Bad request" }, 400); }
  if (d.website) return json({ ok: true }); // honeypot: silently accept bots

  const field = (k) => String(d[k] || "").trim().slice(0, MAX[k] || 200);
  const name = field("name"), email = field("email"), company = field("company"), topic = field("topic") || "General", message = field("message");
  const isCall = d.type === "call";
  if (!name || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return json({ ok: false, error: "Please enter your name and a valid email." }, 400);
  if (!isCall && !message) return json({ ok: false, error: "Please write a short message." }, 400);

  let start = null;
  if (isCall) {
    start = new Date(d.start);
    if (isNaN(start) || start.getTime() < Date.now()) return json({ ok: false, error: "Please choose a future date and time." }, 400);
  }
  if (!env.RESEND_API_KEY) return json({ ok: false, error: "Form is not configured yet. Please email directly." }, 503);

  const owner = env.CONTACT_TO || DEFAULT_TO;
  const visitorTz = String(d.tz || "").slice(0, 60);
  const whenOwner = start ? start.toLocaleString("en-GB", { timeZone: "Asia/Manila", dateStyle: "full", timeStyle: "short" }) + " (Cebu, GMT+8)" : "";
  const whenVisitor = start && visitorTz ? start.toLocaleString("en-GB", { timeZone: visitorTz, dateStyle: "full", timeStyle: "short" }) + ` (${visitorTz})` : "";

  const subject = isCall ? `Intro call request: ${name}${company ? " (" + company + ")" : ""} — ${whenOwner}` : `Website message: ${name}${company ? " (" + company + ")" : ""} — ${topic}`;
  const rows = [["Type", isCall ? "Free 30-min intro call" : "Message"], ["Name", name], ["Email", email], ["Company", company || "—"], ["Topic", topic]];
  if (isCall) rows.push(["Time (your side)", whenOwner], ["Time (their side)", whenVisitor || "—"]);
  const html = `<h2 style="font-family:Arial">${esc(isCall ? "New intro call request" : "New website message")}</h2>
<table style="font-family:Arial;font-size:14px;border-collapse:collapse">${rows.map(([k, v]) => `<tr><td style="padding:4px 12px 4px 0;color:#666">${esc(k)}</td><td style="padding:4px 0"><b>${esc(v)}</b></td></tr>`).join("")}</table>
<p style="font-family:Arial;font-size:14px;white-space:pre-wrap;border-top:1px solid #ddd;padding-top:12px">${esc(message || "(no message)")}</p>
${isCall ? '<p style="font-family:Arial;font-size:13px;color:#666">The calendar invite is attached (invite.ics). Open it to add the call to your calendar, then reply to confirm or propose another time.</p>' : ""}`;
  const text = rows.map(([k, v]) => `${k}: ${v}`).join("\n") + "\n\n" + (message || "(no message)");

  const payload = { from: "Website <onboarding@resend.dev>", to: [owner], reply_to: email, subject, html, text };
  if (isCall) {
    const ics = buildIcs({ start, minutes: 30, name, email, topic, message, owner });
    payload.attachments = [{ filename: "invite.ics", content: btoa(unescape(encodeURIComponent(ics))) }];
  }

  const r = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!r.ok) return json({ ok: false, error: "Could not send right now. Please email directly." }, 502);
  return json({ ok: true });
}

export const onRequest = () => json({ ok: false, error: "Method not allowed" }, 405);
