// Cloudflare Pages Function: POST /api/contact
// Sends the website enquiry to the site owner via Resend.
// Required env var (Cloudflare Pages > Settings > Environment variables): RESEND_API_KEY
// Optional: CONTACT_TO (defaults to the owner's address)
// Optional: MAIL_FROM (sender; evgenymaradin.com is verified in Resend, Nov 2026). The visitor gets a confirmation email.

const DEFAULT_TO = "enmaradin@gmail.com";
const DEFAULT_FROM = "Evgeny Maradin <hello@evgenymaradin.com>";
const MAX = { name: 120, email: 160, company: 160, topic: 80, message: 4000 };

const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const icsText = (s) => String(s).replace(/\\/g, "\\\\").replace(/\n/g, "\\n").replace(/[,;]/g, (c) => "\\" + c);
const icsDate = (d) => d.toISOString().replace(/[-:]/g, "").replace(/\.\d{3}/, "");

// RFC 5545: lines over 75 octets are folded; Google and Outlook mangle long unfolded lines
const fold = (line) => {
  const out = []; let cur = "", n = 0;
  for (const ch of line) {
    const b = new TextEncoder().encode(ch).length;
    if (n + b > (out.length ? 74 : 75)) { out.push(cur); cur = ""; n = 0; }
    cur += ch; n += b;
  }
  out.push(cur);
  return out.join("\r\n ");
};

// Event for the owner's own calendar (METHOD:PUBLISH): Gmail adds it as a plain event
// instead of treating it as an invitation the owner has sent to himself.
function buildIcs({ start, minutes, name, email, company, topic, message }) {
  const end = new Date(start.getTime() + minutes * 60000);
  const uid = `${start.getTime()}-${Math.random().toString(36).slice(2)}@evgenymaradin.com`;
  const lines = [
    "BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Evgeny Maradin//Website booking//EN", "CALSCALE:GREGORIAN", "METHOD:PUBLISH",
    "BEGIN:VEVENT", `UID:${uid}`, `DTSTAMP:${icsDate(new Date())}`, `DTSTART:${icsDate(start)}`, `DTEND:${icsDate(end)}`,
    `SUMMARY:${icsText(`Intro call: ${name}${company ? " (" + company + ")" : ""}`)}`,
    `DESCRIPTION:${icsText(callDetails({ minutes, name, email, company, topic, message }))}`,
    "STATUS:CONFIRMED", "END:VEVENT", "END:VCALENDAR",
  ];
  return lines.map(fold).join("\r\n") + "\r\n";
}

const callDetails = ({ minutes, name, email, company, topic, message }) =>
  `Free ${minutes}-min intro call booked via evgenymaradin.com\nWith: ${name} <${email}>${company ? "\nCompany: " + company : ""}\nTopic: ${topic}${message ? "\n\n" + message : ""}`;

// One click in Google Calendar: event pre-filled, visitor added as guest; on Save Google
// offers to send the invitation, so the visitor gets a real invite from the owner's calendar.
function googleLink({ start, minutes, name, email, company, topic, message }) {
  const end = new Date(start.getTime() + minutes * 60000);
  const q = new URLSearchParams({
    action: "TEMPLATE",
    text: `Intro call: ${name} / Evgeny Maradin`,
    dates: `${icsDate(start)}/${icsDate(end)}`,
    details: callDetails({ minutes, name, email, company, topic, message }).slice(0, 1500),
    add: email,
  });
  return "https://calendar.google.com/calendar/render?" + q.toString();
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
  const mailFrom = env.MAIL_FROM || DEFAULT_FROM;
  const visitorTz = String(d.tz || "").slice(0, 60);
  const whenOwner = start ? start.toLocaleString("en-GB", { timeZone: "Asia/Manila", dateStyle: "full", timeStyle: "short" }) + " (Cebu, GMT+8)" : "";
  const whenVisitor = start && visitorTz ? start.toLocaleString("en-GB", { timeZone: visitorTz, dateStyle: "full", timeStyle: "short" }) + ` (${visitorTz})` : "";

  const gcal = isCall ? googleLink({ start, minutes: 30, name, email, company, topic, message }) : "";
  const subject = isCall ? `Intro call request: ${name}${company ? " (" + company + ")" : ""} — ${whenOwner}` : `Website message: ${name}${company ? " (" + company + ")" : ""} — ${topic}`;
  const rows = [["Type", isCall ? "Free 30-min intro call" : "Message"], ["Name", name], ["Email", email], ["Company", company || "—"], ["Topic", topic]];
  if (isCall) rows.push(["Time (your side)", whenOwner], ["Time (their side)", whenVisitor || "—"]);
  const html = `<h2 style="font-family:Arial">${esc(isCall ? "New intro call request" : "New website message")}</h2>
<table style="font-family:Arial;font-size:14px;border-collapse:collapse">${rows.map(([k, v]) => `<tr><td style="padding:4px 12px 4px 0;color:#666">${esc(k)}</td><td style="padding:4px 0"><b>${esc(v)}</b></td></tr>`).join("")}</table>
<p style="font-family:Arial;font-size:14px;white-space:pre-wrap;border-top:1px solid #ddd;padding-top:12px">${esc(message || "(no message)")}</p>
${isCall ? `<p style="font-family:Arial;font-size:14px;margin:18px 0"><a href="${esc(gcal)}" style="background:#c84b2f;color:#fff;padding:12px 18px;text-decoration:none;font-weight:bold;border-radius:4px">Add to Google Calendar and invite ${esc(name)}</a></p>
<p style="font-family:Arial;font-size:13px;color:#666">The button opens the event with ${esc(email)} already added as a guest. Add Google Meet if needed, press Save, then "Send" so the invitation goes out. Other calendars: open the attached invite.ics. To propose another time, just reply to this email.</p>` : ""}`;
  const text = rows.map(([k, v]) => `${k}: ${v}`).join("\n") + "\n\n" + (message || "(no message)") + (isCall ? "\n\nAdd to Google Calendar and invite: " + gcal : "");

  const payload = { from: mailFrom, to: [owner], reply_to: email, subject, html, text };
  if (isCall) {
    const ics = buildIcs({ start, minutes: 30, name, email, company, topic, message });
    payload.attachments = [{ filename: "invite.ics", content: btoa(unescape(encodeURIComponent(ics))) }];
  }

  const r = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!r.ok) return json({ ok: false, error: "Could not send right now. Please email directly." }, 502);

  { // visitor confirmation
    const vSubject = isCall ? "Your intro call request: Evgeny Maradin" : "Your message to Evgeny Maradin";
    const vText = `Hello ${name},\n\n` + (isCall
      ? `Thank you for requesting a free 30-min intro call for ${whenVisitor || whenOwner}. I will confirm by email within one working day and send a calendar invitation.`
      : "Thank you for your message. I will reply within one working day.") +
      "\n\nEvgeny Maradin\nhttps://evgenymaradin.com";
    await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, "Content-Type": "application/json" },
      body: JSON.stringify({ from: mailFrom, to: [email], reply_to: owner, subject: vSubject, text: vText }),
    }).catch(() => {});
  }
  return json({ ok: true });
}

export const onRequest = () => json({ ok: false, error: "Method not allowed" }, 405);
