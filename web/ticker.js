// Market ticker at the top of every page. Data: /api/prices (Cloudflare Pages Function, cached 15 min).
// Refreshes every 15 minutes while the page is open; collapses quietly if prices are unavailable.
(function () {
  var bar = document.getElementById("ticker"), list = document.getElementById("ticker-items"), stamp = document.getElementById("ticker-time");
  if (!bar) return;
  var CUR = { "$": "$", "€": "€" };
  function fmt(i) {
    var cur = CUR[i.unit.charAt(0)] || "", unit = i.unit.slice(1);
    var ch = i.change === null || i.change === undefined ? "" :
      '<em class="' + (i.change > 0 ? "up" : i.change < 0 ? "dn" : "") + '">' + (i.change > 0 ? "▲" : i.change < 0 ? "▼" : "") +
      Math.abs(i.change).toFixed(1) + "%</em>";
    return '<span class="tk" title="' + i.label + ", " + i.unit + " · source: " + i.src + '"><i>' + i.label + "</i> " + cur +
      i.price.toFixed(2) + '<u>' + unit + "</u>" + ch + "</span>";
  }
  function load() {
    fetch("/api/prices", { cache: "no-cache" }).then(function (r) { return r.ok ? r.json() : null; }).then(function (d) {
      if (!d || !d.items || !d.items.length) { bar.classList.add("off"); return; }
      list.innerHTML = d.items.map(fmt).join("");
      var t = new Date(d.updated);
      stamp.textContent = "Delayed · " + t.toLocaleString(undefined, { day: "numeric", month: "short", hour: "2-digit", minute: "2-digit" });
      bar.classList.add("on");
    }).catch(function () { bar.classList.add("off"); });
  }
  load();
  setInterval(load, 15 * 60 * 1000);
})();
