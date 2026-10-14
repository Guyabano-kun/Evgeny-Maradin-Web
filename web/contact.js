(function () {
  var form = document.getElementById('enquiry');
  if (!form) return;
  var tz = Intl.DateTimeFormat().resolvedOptions().timeZone || 'UTC';
  var callBlock = document.getElementById('call-fields');
  var msg = form.elements.message;
  var dateIn = form.elements.date, timeIn = form.elements.time, hint = document.getElementById('time-hint');
  var status = document.getElementById('form-status'), btn = form.querySelector('button[type=submit]');
  document.getElementById('tz-label').textContent = tz;

  // earliest date: tomorrow
  var t = new Date(); t.setDate(t.getDate() + 1);
  dateIn.min = t.toISOString().slice(0, 10);

  function mode() { return form.elements.type.value; }
  function setMode(m) {
    var call = m === 'call';
    callBlock.hidden = !call;
    dateIn.required = timeIn.required = call;
    msg.required = !call;
    msg.placeholder = call ? 'What would you like to discuss? (optional)' : 'Your message';
    btn.textContent = call ? 'Request the call' : 'Send message';
    document.querySelectorAll('.mode label').forEach(function (l) { l.classList.toggle('on', l.querySelector('input').value === m); });
  }
  form.querySelectorAll('input[name=type]').forEach(function (r) { r.addEventListener('change', function () { setMode(mode()); }); });
  var qs = new URLSearchParams(location.search).get('type');
  if (qs === 'call' || qs === 'message') form.elements.type.value = qs;
  setMode(mode());

  function startDate() {
    if (!dateIn.value || !timeIn.value) return null;
    var d = new Date(dateIn.value + 'T' + timeIn.value);
    return isNaN(d) ? null : d;
  }
  function updateHint() {
    var d = startDate();
    hint.textContent = d ? 'That is ' + d.toLocaleString('en-GB', { timeZone: 'Asia/Manila', weekday: 'short', day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' }) + ' in Cebu (GMT+8). I will confirm or suggest another time.' : '';
  }
  dateIn.addEventListener('change', updateHint); timeIn.addEventListener('change', updateHint);

  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function icsDate(d) { return d.getUTCFullYear() + pad(d.getUTCMonth() + 1) + pad(d.getUTCDate()) + 'T' + pad(d.getUTCHours()) + pad(d.getUTCMinutes()) + '00Z'; }
  function visitorLinks(start) {
    var end = new Date(start.getTime() + 30 * 60000);
    var title = 'Intro call with Evgeny Maradin';
    var details = 'Free 30-min intro call (tentative until confirmed by email). Contact: enmaradin@gmail.com';
    var ics = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Evgeny Maradin//Website booking//EN', 'BEGIN:VEVENT',
      'UID:' + start.getTime() + '@evgeny-maradin.pages.dev', 'DTSTAMP:' + icsDate(new Date()), 'DTSTART:' + icsDate(start), 'DTEND:' + icsDate(end),
      'SUMMARY:' + title, 'DESCRIPTION:' + details, 'STATUS:TENTATIVE', 'END:VEVENT', 'END:VCALENDAR'].join('\r\n');
    var file = URL.createObjectURL(new Blob([ics], { type: 'text/calendar' }));
    var g = 'https://calendar.google.com/calendar/render?action=TEMPLATE&text=' + encodeURIComponent(title) +
      '&dates=' + icsDate(start) + '/' + icsDate(end) + '&details=' + encodeURIComponent(details) + '&add=enmaradin@gmail.com';
    return '<div class="actions"><a class="button primary" href="' + file + '" download="intro-call.ics">Add to calendar (.ics)</a>' +
      '<a class="button secondary" href="' + g + '" target="_blank" rel="noopener">Google Calendar ↗</a></div>';
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    status.className = 'form-status'; status.textContent = '';
    var call = mode() === 'call', start = call ? startDate() : null;
    if (call && (!start || start < new Date())) { status.className = 'form-status err'; status.textContent = 'Please choose a future date and time.'; return; }
    var data = {
      type: mode(), name: form.elements.name.value, email: form.elements.email.value, company: form.elements.company.value,
      topic: form.elements.topic.value, message: msg.value, website: form.elements.website.value,
      start: start ? start.toISOString() : null, tz: tz
    };
    btn.disabled = true; btn.textContent = 'Sending…';
    fetch('/api/contact', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
      .then(function (r) { return r.json().catch(function () { return { ok: false }; }); })
      .then(function (res) {
        if (!res.ok) throw new Error(res.error || 'Could not send right now.');
        var done = document.getElementById('form-done');
        done.querySelector('h3').textContent = call ? 'Call requested.' : 'Message sent.';
        done.querySelector('p:not(.eyebrow)').textContent = call
          ? 'I will confirm the time by email within one working day. You can already add the slot to your calendar:'
          : 'Thank you. I will reply by email within one working day.';
        if (call) done.insertAdjacentHTML('beforeend', visitorLinks(start));
        form.hidden = true; done.hidden = false; done.scrollIntoView({ behavior: 'smooth', block: 'center' });
      })
      .catch(function (err) {
        status.className = 'form-status err';
        status.innerHTML = (err.message || 'Could not send right now.') + ' Email <a href="mailto:enmaradin@gmail.com">enmaradin@gmail.com</a> or message on <a href="https://wa.me/639669813383" target="_blank" rel="noopener">WhatsApp</a>.';
        btn.disabled = false; setMode(mode());
      });
  });
})();
