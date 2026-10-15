// Crude oil production by country (JODI, monthly). Data: /data/production.json, refreshed monthly by a GitHub Action.
// Stacked area: top-N countries of the selected region + "Others" as one sum; filters for period, region and top-N;
// a table of every country in the region; click a row to pin countries instead of top-N.
(function () {
  var root = document.getElementById("prod");
  if (!root) return;
  var COLORS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"];
  var OTHER = "#c9c2b5";
  var REGIONS = ["All", "Middle East", "CIS & Caspian", "Africa", "North America", "Latin America", "Europe", "Asia-Pacific"];
  var PERIODS = [["1Y", 12], ["3Y", 36], ["5Y", 60], ["All", 0]];
  var st = { period: 60, region: "All", top: 5, pinned: [] };
  var D, M;
  var $ = function (s) { return root.querySelector(s); };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  var mlabel = function (m) { var p = m.split("-"); return MON[+p[1] - 1] + " " + p[0]; };
  var fmt = function (v) { return v >= 1000 ? (v / 1000).toFixed(2) + " mb/d" : Math.round(v) + " kb/d"; };

  // fill reporting gaps of up to 3 months with the last reported value (marked as estimates)
  function filled(v) {
    var out = [], est = [], last = null, gap = 0;
    for (var i = 0; i < v.length; i++) {
      if (v[i] !== null) { last = v[i]; gap = 0; out.push(v[i]); est.push(false); }
      else if (last !== null && gap < 3) { gap++; out.push(last); est.push(true); }
      else { out.push(0); est.push(false); }
    }
    return { v: out, est: est };
  }

  function codes() {
    return Object.keys(D.countries).filter(function (c) { return st.region === "All" || D.countries[c].r === st.region; });
  }
  function win() { var n = M.length; return st.period ? [Math.max(0, n - st.period), n - 1] : [0, n - 1]; }
  function avg(c, a, b) { var v = D.countries[c].f.v, s = 0; for (var i = a; i <= b; i++) s += v[i]; return s / (b - a + 1); }

  function series() {
    var cs = codes(), w = win(), n = M.length;
    // rank on the last 12 months so the colour of a country does not change with the period filter
    var rank = cs.slice().sort(function (x, y) { return avg(y, n - 12, n - 1) - avg(x, n - 12, n - 1); });
    var shown = st.pinned.length ? st.pinned.filter(function (c) { return cs.indexOf(c) >= 0; }) : rank.slice(0, st.top);
    var rest = cs.filter(function (c) { return shown.indexOf(c) < 0; });
    var out = shown.map(function (c) {
      var k = (st.pinned.length ? st.pinned.indexOf(c) : rank.indexOf(c));
      return { code: c, name: D.countries[c].n, color: COLORS[k % COLORS.length], v: D.countries[c].f.v, est: D.countries[c].f.est };
    });
    if (rest.length) {
      var v = M.map(function (_, i) { var s = 0; rest.forEach(function (c) { s += D.countries[c].f.v[i]; }); return s; });
      out.push({ code: "_other", name: "Others (" + rest.length + ")", color: OTHER, v: v, est: [] });
    }
    return { s: out, w: w, rank: rank };
  }

  function chart() {
    var S = series(), s = S.s, a = S.w[0], b = S.w[1];
    var W = Math.max(320, Math.round($(".prod-chart").clientWidth || 900)), H = W < 640 ? 300 : 380, L = W < 640 ? 46 : 64, R = 12, T = 26, B = 34, iw = W - L - R, ih = H - T - B;
    var tot = []; for (var i = a; i <= b; i++) { var t = 0; s.forEach(function (x) { t += x.v[i]; }); tot.push(t); }
    var max = Math.max.apply(null, tot) || 1, step = niceStep(max / 5), top = Math.ceil(max / step) * step;
    var x = function (i) { return L + (b === a ? 0 : (i - a) / (b - a) * iw); };
    var y = function (v) { return T + ih - v / top * ih; };
    var g = "";
    for (var gv = 0; gv <= top + 1e-9; gv += step) g += '<line x1="' + L + '" x2="' + (W - R) + '" y1="' + y(gv) + '" y2="' + y(gv) + '" class="gl"/><text x="' + (L - 8) + '" y="' + (y(gv) + 4) + '" class="ax" text-anchor="end">' + (top >= 1000 ? (gv / 1000).toFixed(step % 1000 ? 1 : 0) : Math.round(gv)) + "</text>";
    g += '<text x="' + (L - 8) + '" y="12" class="ax" text-anchor="start">' + (top >= 1000 ? "million barrels per day" : "thousand barrels per day") + "</text>";
    var span = b - a;
    for (var j = a; j <= b; j++) {
      var mm = +M[j].split("-")[1], yr = M[j].slice(0, 4), lab = null;
      var narrow = W < 640;
      if (span > 36) { if (mm === 1 && (span <= (narrow ? 48 : 84) || +yr % 2 === 0)) lab = yr; }
      else if (span > 12) { if ((mm - 1) % (narrow ? 12 : 6) === 0) lab = mlabel(M[j]); }
      else if ((mm - 1) % (narrow ? 4 : 3) === 0) lab = mlabel(M[j]);
      if (lab) g += '<text x="' + x(j) + '" y="' + (H - 10) + '" class="ax" text-anchor="middle">' + lab + "</text>";
    }
    var base = M.map(function () { return 0; }), areas = "";
    s.forEach(function (ser) {
      var up = [], dn = [];
      for (var i = a; i <= b; i++) { up.push(x(i) + "," + y(base[i] + ser.v[i])); dn.unshift(x(i) + "," + y(base[i])); }
      areas += '<polygon points="' + up.concat(dn).join(" ") + '" fill="' + ser.color + '" stroke="#f4f1ea" stroke-width="1.5" stroke-linejoin="round"/>';
      for (var k = a; k <= b; k++) base[k] += ser.v[k];
    });
    var svg = '<svg viewBox="0 0 ' + W + " " + H + '" role="img" aria-label="Crude oil production, stacked by country">' + g +
      '<line x1="' + L + '" x2="' + (W - R) + '" y1="' + y(0) + '" y2="' + y(0) + '" class="bl"/>' + areas +
      '<line class="xh" x1="0" x2="0" y1="' + T + '" y2="' + (T + ih) + '" visibility="hidden"/><rect class="hit" x="' + L + '" y="' + T + '" width="' + iw + '" height="' + ih + '"/></svg>';
    $(".prod-chart").innerHTML = svg + '<div class="prod-tip" hidden></div>';
    $(".prod-legend").innerHTML = s.map(function (ser) { return '<span><i style="background:' + ser.color + '"></i>' + esc(ser.name) + "</span>"; }).join("");
    $(".prod-total").textContent = "Total " + (st.region === "All" ? "reported" : st.region) + ", " + mlabel(M[b]) + ": " + fmt(tot[tot.length - 1]);
    hover(s, a, b, x, W, L, iw);
    table(S);
  }
  function niceStep(r) { var p = Math.pow(10, Math.floor(Math.log10(r))), n = r / p; return (n < 1.5 ? 1 : n < 3 ? 2 : n < 7 ? 5 : 10) * p; }

  function hover(s, a, b, x, W, L, iw) {
    var svg = $(".prod-chart svg"), hit = svg.querySelector(".hit"), xh = svg.querySelector(".xh"), tip = $(".prod-tip");
    function show(ev) {
      var r = svg.getBoundingClientRect(), px = (ev.clientX - r.left) / r.width * W;
      var i = Math.round(a + (px - L) / iw * (b - a)); i = Math.max(a, Math.min(b, i));
      xh.setAttribute("x1", x(i)); xh.setAttribute("x2", x(i)); xh.setAttribute("visibility", "visible");
      var t = 0, rows = s.slice().reverse().map(function (ser) { t += ser.v[i]; return '<div><i style="background:' + ser.color + '"></i>' + esc(ser.name) + "<b>" + fmt(ser.v[i]) + (ser.est[i] ? "*" : "") + "</b></div>"; });
      tip.innerHTML = "<strong>" + mlabel(M[i]) + "</strong>" + rows.join("") + '<div class="tt"><i></i>Total<b>' + fmt(t) + "</b></div>";
      tip.hidden = false;
      var left = (x(i) / W) * r.width, tw = tip.offsetWidth;
      tip.style.left = (left + 14 + tw > r.width ? left - tw - 14 : left + 14) + "px";
    }
    hit.addEventListener("pointermove", show);
    hit.addEventListener("pointerdown", show);
    hit.addEventListener("pointerleave", function () { tip.hidden = true; xh.setAttribute("visibility", "hidden"); });
  }

  function table(S) {
    var n = M.length, rows = S.rank.map(function (c, k) {
      var d = D.countries[c], v = d.v[n - 1], last12 = avg(c, n - 12, n - 1), prev12 = n >= 24 ? avg(c, n - 24, n - 13) : null;
      var yoy = prev12 ? (last12 / prev12 - 1) * 100 : null;
      var ser = S.s.filter(function (x) { return x.code === c; })[0];
      return '<tr data-c="' + c + '" class="' + (ser ? "on" : "") + '"><td>' + (k + 1) + '</td><td><i style="background:' + (ser ? ser.color : "transparent") + '"></i>' + esc(d.n) + "</td><td>" + esc(d.r) +
        "</td><td>" + (v === null ? "–" : fmt(v)) + "</td><td>" + fmt(last12) + "</td><td class=\"" + (yoy > 0 ? "up" : yoy < 0 ? "dn" : "") + "\">" + (yoy === null ? "–" : (yoy > 0 ? "+" : "") + yoy.toFixed(1) + "%") + "</td></tr>";
    });
    $(".prod-table tbody").innerHTML = rows.join("");
    $(".prod-mode").textContent = st.pinned.length ? "Showing your selection (" + st.pinned.length + "). " : "Showing top " + st.top + " by last 12 months. ";
    $(".prod-reset").hidden = !st.pinned.length;
  }

  function controls() {
    $(".prod-period").innerHTML = PERIODS.map(function (p) { return '<button type="button" data-p="' + p[1] + '"' + (st.period === p[1] ? ' aria-pressed="true"' : "") + ">" + p[0] + "</button>"; }).join("");
    $(".prod-region").innerHTML = REGIONS.map(function (r) { return "<option" + (r === st.region ? " selected" : "") + ">" + r + "</option>"; }).join("");
    $(".prod-top").innerHTML = [3, 5, 8].map(function (t) { return "<option value=\"" + t + "\"" + (t === st.top ? " selected" : "") + ">Top " + t + "</option>"; }).join("");
  }

  function bind() {
    $(".prod-period").addEventListener("click", function (e) { var b = e.target.closest("button"); if (!b) return; st.period = +b.dataset.p; controls(); chart(); });
    $(".prod-region").addEventListener("change", function (e) { st.region = e.target.value; st.pinned = []; chart(); });
    $(".prod-top").addEventListener("change", function (e) { st.top = +e.target.value; st.pinned = []; chart(); });
    $(".prod-reset").addEventListener("click", function () { st.pinned = []; chart(); });
    $(".prod-table tbody").addEventListener("click", function (e) {
      var tr = e.target.closest("tr"); if (!tr) return;
      var c = tr.dataset.c, cur = st.pinned.length ? st.pinned.slice() : series().s.filter(function (x) { return x.code !== "_other"; }).map(function (x) { return x.code; });
      var i = cur.indexOf(c); if (i >= 0) cur.splice(i, 1); else if (cur.length < COLORS.length) cur.push(c);
      st.pinned = cur.length ? cur : []; chart();
    });
  }

  fetch("/data/production.json").then(function (r) { if (!r.ok) throw 0; return r.json(); }).then(function (d) {
    D = d; M = d.months;
    Object.keys(D.countries).forEach(function (c) { D.countries[c].f = filled(D.countries[c].v); });
    $(".prod-src").innerHTML = "Source: <a href=\"" + esc(d.source_url) + "\" target=\"_blank\" rel=\"noopener\">" + esc(d.source) + "</a> · " + esc(d.series) + " · data to " + mlabel(M[M.length - 1]) +
      " · " + Object.keys(D.countries).length + " countries · refreshed " + esc(d.updated) + ". Latest months are EIA estimates and may be revised. * = gap filled with the last reported month.";
    controls(); bind(); chart(); root.classList.add("ready");
    var rw = 0; window.addEventListener("resize", function () { clearTimeout(rw); rw = setTimeout(chart, 150); });
  }).catch(function () { $(".prod-chart").innerHTML = '<p class="prod-err">Production data is temporarily unavailable.</p>'; });
})();
