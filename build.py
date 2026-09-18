# -*- coding: utf-8 -*-
"""Baut site/index.html (fuer chinawokdao.com) und build/artifact.html (Vorschau)."""
import html, os, sys, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from menu import RESTAURANT, HOURS, ADDITIVES, SECTIONS

R = RESTAURANT
BASE = os.path.dirname(os.path.abspath(__file__))
e = lambda s: html.escape(s, quote=True)

HAS_PRICES = any(it[3] for sec in SECTIONS for it in sec[3])


def heat(text):
    """0 = mild, 1 = scharf, 2 = sehr scharf. Nur aus dem Text des Gerichts."""
    t = text.lower()
    if "sehr scharf" in t:
        return 2
    if "scharf" in t:
        return 1
    return 0

# ---------------------------------------------------------------- Bausteine

def additive_marks(codes):
    if not codes:
        return ""
    inner = ",".join(codes)
    label = "Zusatzstoffe " + ", ".join(codes)
    return ('<a class="add" href="#zusatzstoffe" title="%s" aria-label="%s">%s</a>'
            % (e(label), e(label), e(inner)))


def heat_mark(level):
    if not level:
        return ""
    word = "sehr scharf" if level == 2 else "scharf"
    dots = "".join('<span class="chili-dot"></span>' for _ in range(level))
    # &#8288; (word joiner) verhindert, dass die Schaerfe-Markierung allein
    # in die naechste Zeile rutscht.
    return ('&#8288;<span class="heat" role="img" aria-label="%s" title="%s">%s</span>'
            % (word, word, dots))


def item_row(num, name, codes, price):
    h = heat(name)
    num_cell = ('<span class="num">%s</span>' % e(num)) if num else '<span class="num num-empty" aria-hidden="true">&bull;</span>'
    price_cell = ('<span class="price">%s</span>' % e(price)) if (HAS_PRICES and price) else ""
    return (
        '<li class="item"%s>'
        '%s'
        '<span class="body"><span class="name">%s</span>%s%s</span>'
        '%s'
        '</li>'
    ) % (
        (' id="nr-%s"' % e(num)) if num else "",
        num_cell,
        e(name),
        additive_marks(codes),
        heat_mark(h),
        price_cell,
    )


def section_block(slug, title, note, items):
    note_html = ('<span class="sec-note">%s</span>' % e(note)) if note else ""
    rows = "\n        ".join(item_row(*it) for it in items)
    first = items[0][0]
    last = items[-1][0]
    range_html = ""
    if first and last and first != last:
        range_html = '<span class="sec-range">%s&thinsp;&ndash;&thinsp;%s</span>' % (e(first), e(last))
    return """
    <section class="sec" id="%s" aria-labelledby="h-%s">
      <h2 class="sec-head" id="h-%s"><span class="sec-title">%s</span>%s%s</h2>
      <ul class="items">
        %s
      </ul>
    </section>""" % (slug, slug, slug, e(title), note_html, range_html, rows)


NAV = "\n".join(
    '        <li><a href="#%s">%s</a></li>' % (s[0], e(s[1])) for s in SECTIONS
)
MENU = "\n".join(section_block(*s) for s in SECTIONS)

HOURS_ROWS = "\n".join(
    '          <tr%s><th scope="row">%s</th><td>%s</td></tr>' % (
        ' class="today" data-day="%d"' % i,
        e(day),
        e(" &amp; ".join("%s bis %s Uhr" % (a, b) for a, b in slots)).replace("&amp;amp;", "&amp;"),
    )
    for i, (day, slots) in enumerate(HOURS)
)

LEGEND = "\n".join(
    '          <li><span class="lg-code">%s</span><span class="lg-text">%s</span></li>' % (e(c), e(t))
    for c, t in ADDITIVES
)

# Oeffnungszeiten als JSON fuer die Live-Anzeige (Mo=0 ... So=6)
HOURS_JSON = json.dumps([[[a, b] for a, b in slots] for _, slots in HOURS], ensure_ascii=False)

SCHEMA = {
    "@context": "https://schema.org",
    "@type": "Restaurant",
    "name": R["name"],
    "servesCuisine": ["Chinesisch", "Thailändisch"],
    "telephone": R["phone_tel"],
    "url": "https://%s/" % R["domain"],
    "address": {
        "@type": "PostalAddress",
        "streetAddress": R["street"],
        "postalCode": R["zip"],
        "addressLocality": R["city"],
        "addressCountry": R["country"],
    },
    "hasMap": R["maps"],
    "acceptsReservations": "True",
    "menu": "https://%s/#speisekarte" % R["domain"],
    "openingHoursSpecification": [
        {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": "https://schema.org/" + en,
            "opens": a,
            "closes": b,
        }
        for (de, slots), en in zip(HOURS, ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        for a, b in slots
    ],
}
if R["email"]:
    SCHEMA["email"] = R["email"]

CSS = r"""
:root{
  --paper:#FBFAF8; --surface:#FFFFFF; --sunken:#F2EEE8;
  --ink:#1A1512; --ink-soft:#4A423C; --ash:#7C736C; --rule:#E2DCD3;
  --chili:#BF3A2B; --jade:#16685A; --wok:#241E1B; --wok-ink:#EDE6DE; --wok-ash:#A0958C;
  --shadow:0 1px 2px rgba(26,21,18,.05), 0 8px 24px -12px rgba(26,21,18,.18);
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --paper:#141110; --surface:#1C1817; --sunken:#221D1B;
    --ink:#EDE6DE; --ink-soft:#BDB3AA; --ash:#968B83; --rule:#302927;
    --chili:#E8604F; --jade:#45AF97; --wok:#0E0C0B; --wok-ink:#EDE6DE; --wok-ash:#A0958C;
    --shadow:0 1px 2px rgba(0,0,0,.4), 0 8px 24px -12px rgba(0,0,0,.6);
  }
}
:root[data-theme="dark"]{
  --paper:#141110; --surface:#1C1817; --sunken:#221D1B;
  --ink:#EDE6DE; --ink-soft:#BDB3AA; --ash:#968B83; --rule:#302927;
  --chili:#E8604F; --jade:#45AF97; --wok:#0E0C0B; --wok-ink:#EDE6DE; --wok-ash:#A0958C;
  --shadow:0 1px 2px rgba(0,0,0,.4), 0 8px 24px -12px rgba(0,0,0,.6);
}

*,*::before,*::after{ box-sizing:border-box; }
body{
  margin:0; background:var(--paper); color:var(--ink);
  font-family:"Public Sans","Helvetica Neue",Arial,sans-serif;
  font-size:16px; line-height:1.55; -webkit-text-size-adjust:100%;
  font-feature-settings:"kern" 1;
}
img{ max-width:100%; }
[hidden]{ display:none !important; }
a{ color:inherit; }
:where(a,button,[tabindex]):focus-visible{
  outline:2px solid var(--jade); outline-offset:3px; border-radius:3px;
}
.skip{
  position:absolute; left:-9999px; top:0; z-index:99;
  background:var(--jade); color:#fff; padding:.6rem 1rem; border-radius:0 0 6px 0;
}
.skip:focus{ left:0; }
.wrap{ width:100%; max-width:1180px; margin-inline:auto; padding-inline:20px; }

/* ---------- Hero: die dunkle Wok-Flaeche ---------- */
.hero{
  background:var(--wok); color:var(--wok-ink);
  padding-block:clamp(2.5rem,7vw,4.5rem) clamp(2.25rem,6vw,3.5rem);
  position:relative; overflow:hidden;
}
.hero::after{
  content:""; position:absolute; inset:auto 0 0 0; height:3px;
  background:linear-gradient(90deg,var(--chili) 0 38%,var(--jade) 38% 100%);
}
.hero-grid{ display:grid; gap:clamp(1.75rem,4vw,3rem); grid-template-columns:1fr; }
@media (min-width:860px){ .hero-grid{ grid-template-columns:1.25fr .85fr; align-items:end; } }

.eyebrow{
  font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace;
  font-size:.7rem; letter-spacing:.18em; text-transform:uppercase;
  color:var(--wok-ash); margin:0 0 1rem;
}
.wordmark{
  font-family:"Big Shoulders Display","Haettenschweiler","Arial Narrow",sans-serif;
  font-weight:800; font-size:clamp(3.6rem,15vw,8.5rem); line-height:.84;
  letter-spacing:-.005em; margin:0; text-wrap:balance; text-transform:uppercase;
}
.wordmark .dao{ color:var(--chili); }
.tagline{
  margin:1.1rem 0 0; max-width:34ch; color:var(--wok-ash);
  font-size:clamp(1rem,2.4vw,1.15rem);
}
.status{
  display:inline-flex; align-items:center; gap:.5rem; margin-top:1.6rem;
  font-family:"IBM Plex Mono",ui-monospace,monospace; font-size:.78rem;
  letter-spacing:.06em; text-transform:uppercase;
  border:1px solid rgba(255,255,255,.18); border-radius:100px; padding:.4rem .85rem;
}
.status .dot{ width:8px; height:8px; border-radius:50%; background:var(--wok-ash); flex:none; }
.status.open .dot{ background:var(--jade); box-shadow:0 0 0 4px rgba(69,175,151,.18); }
.status.shut .dot{ background:var(--chili); }

.call{
  display:flex; flex-direction:column; gap:.2rem;
  background:rgba(255,255,255,.05); border:1px solid rgba(255,255,255,.14);
  border-radius:4px; padding:1.1rem 1.25rem; text-decoration:none;
  transition:background .18s ease, border-color .18s ease;
}
.call:hover{ background:rgba(255,255,255,.09); border-color:rgba(255,255,255,.3); }
.call-label{
  font-family:"IBM Plex Mono",ui-monospace,monospace; font-size:.68rem;
  letter-spacing:.18em; text-transform:uppercase; color:var(--wok-ash);
}
.call-num{
  font-family:"Big Shoulders Display","Arial Narrow",sans-serif; font-weight:700;
  font-size:clamp(2rem,6vw,2.9rem); line-height:1; letter-spacing:.01em;
  font-variant-numeric:tabular-nums;
}
.hero-hours{ margin-top:1.4rem; }
.hours-table{ width:100%; border-collapse:collapse; font-size:.9rem; }
.hours-table th, .hours-table td{
  text-align:left; padding:.42rem 0; border-bottom:1px solid rgba(255,255,255,.09);
  font-weight:400; vertical-align:baseline;
}
.hours-table th{ color:var(--wok-ash); width:8.5em; font-weight:400; }
.hours-table td{ font-variant-numeric:tabular-nums; }
.hours-table tr[data-today] th, .hours-table tr[data-today] td{ color:var(--wok-ink); font-weight:600; }
.hours-table tr[data-today] th::after{ content:" ·"; color:var(--jade); }

/* ---------- Beilagen-Hinweis ---------- */
.rice-note{
  background:var(--sunken); border-block:1px solid var(--rule);
  padding-block:1.1rem; font-size:.95rem;
}
.rice-note p{ margin:0; max-width:62ch; }
.rice-note strong{ font-weight:600; }
.rice-note .plus{ color:var(--jade); font-weight:600; font-variant-numeric:tabular-nums; }

/* ---------- Layout Karte + Index ---------- */
.karte{ padding-block:clamp(2.25rem,5vw,3.5rem) 0; }
.karte-grid{ display:grid; gap:2.5rem; grid-template-columns:1fr; align-items:start; }
@media (min-width:1000px){
  .karte-grid{ grid-template-columns:230px minmax(0,1fr); gap:3.5rem; }
}

.index{ display:none; }
@media (min-width:1000px){
  .index{
    display:block; position:sticky; top:1.5rem; max-height:calc(100dvh - 3rem);
    overflow-y:auto; overscroll-behavior:contain;
  }
}
.index h2{
  font-family:"IBM Plex Mono",ui-monospace,monospace; font-size:.68rem;
  letter-spacing:.18em; text-transform:uppercase; color:var(--ash);
  margin:0 0 .85rem; font-weight:500;
}
.index ol{ list-style:none; margin:0; padding:0; display:flex; flex-direction:column; gap:1px; }
.index a{
  display:block; padding:.34rem .6rem; text-decoration:none; font-size:.875rem;
  color:var(--ink-soft); border-left:2px solid transparent; border-radius:0 3px 3px 0;
  transition:color .15s ease, border-color .15s ease, background .15s ease;
}
.index a:hover{ color:var(--ink); background:var(--sunken); }
.index a[aria-current="true"]{ color:var(--chili); border-left-color:var(--chili); font-weight:600; }

/* Chip-Leiste fuer schmale Displays */
.chips{
  position:sticky; top:env(safe-area-inset-top,0px); z-index:20;
  background:color-mix(in srgb, var(--paper) 92%, transparent);
  -webkit-backdrop-filter:blur(10px); backdrop-filter:blur(10px);
  border-bottom:1px solid var(--rule); margin-bottom:1.75rem;
}
@media (min-width:1000px){ .chips{ display:none; } }
.chips ul{
  list-style:none; margin:0; padding:.6rem 20px; display:flex; gap:.4rem;
  overflow-x:auto; scrollbar-width:none; -webkit-overflow-scrolling:touch;
}
.chips ul::-webkit-scrollbar{ display:none; }
.chips a{
  display:block; white-space:nowrap; text-decoration:none; font-size:.8rem;
  padding:.35rem .75rem; border:1px solid var(--rule); border-radius:100px;
  color:var(--ink-soft); background:var(--surface);
}
.chips a[aria-current="true"]{ background:var(--chili); border-color:var(--chili); color:#fff; }

/* ---------- Gerichte ---------- */
.sec{ margin:0 0 2.75rem; scroll-margin-top:5rem; }
@media (min-width:1000px){ .sec{ scroll-margin-top:1.5rem; } }
.sec-head{
  display:flex; align-items:baseline; gap:.65rem; flex-wrap:wrap;
  margin:0 0 .9rem; padding-bottom:.5rem; border-bottom:2px solid var(--ink);
}
.sec-title{
  font-family:"Big Shoulders Display","Arial Narrow",sans-serif; font-weight:700;
  font-size:clamp(1.65rem,4.5vw,2.3rem); line-height:1; text-transform:uppercase;
  letter-spacing:.005em;
}
.sec-note{
  font-family:"Public Sans",sans-serif; font-size:.78rem; font-weight:400;
  color:var(--jade); border:1px solid currentColor; border-radius:100px;
  padding:.1rem .55rem; line-height:1.5; white-space:nowrap;
}
.sec-range{
  margin-left:auto; font-family:"IBM Plex Mono",ui-monospace,monospace;
  font-size:.75rem; color:var(--ash); font-variant-numeric:tabular-nums;
}
.items{ list-style:none; margin:0; padding:0; }
.item{
  display:grid; grid-template-columns:3.1rem minmax(0,1fr); gap:0 .85rem;
  align-items:baseline; padding:.62rem 0; border-bottom:1px solid var(--rule);
}
.item:last-child{ border-bottom:0; }
.item:target{ background:var(--sunken); }
.num{
  font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace; font-weight:500;
  font-size:1rem; font-variant-numeric:tabular-nums; color:var(--chili);
  letter-spacing:-.02em;
}
.num-empty{ color:var(--rule); }
.body{ display:block; }
.name{ }
.add{
  font-family:"IBM Plex Mono",ui-monospace,monospace; font-size:.62rem;
  vertical-align:super; margin-left:.22em; color:var(--ash);
  text-decoration:none; border-bottom:1px dotted currentColor;
}
.add:hover{ color:var(--ink); }
.heat{ display:inline-flex; gap:2px; margin-left:.45em; vertical-align:middle; white-space:nowrap; }
.chili-dot{
  width:6px; height:6px; border-radius:50% 50% 50% 0; background:var(--chili);
  transform:rotate(-45deg); display:inline-block;
}
.price{
  font-family:"IBM Plex Mono",ui-monospace,monospace; font-variant-numeric:tabular-nums;
  text-align:right; white-space:nowrap;
}

/* ---------- Zusatzstoffe ---------- */
.legend{ background:var(--sunken); border-top:1px solid var(--rule); padding-block:2.5rem; margin-top:1rem; }
.legend h2{
  font-family:"IBM Plex Mono",ui-monospace,monospace; font-size:.68rem;
  letter-spacing:.18em; text-transform:uppercase; color:var(--ash);
  margin:0 0 1rem; font-weight:500;
}
.legend ul{
  list-style:none; margin:0; padding:0; display:grid; gap:.45rem .5rem;
  grid-template-columns:1fr; font-size:.875rem;
}
@media (min-width:640px){ .legend ul{ grid-template-columns:repeat(2,minmax(0,1fr)); column-gap:2.5rem; } }
.legend li{ display:grid; grid-template-columns:2.1rem minmax(0,1fr); gap:.5rem; align-items:baseline; }
.lg-code{
  font-family:"IBM Plex Mono",ui-monospace,monospace; font-size:.8rem;
  color:var(--chili); font-variant-numeric:tabular-nums;
}
.lg-text{ color:var(--ink-soft); }

/* ---------- Kontakt / Fuss ---------- */
.foot{ background:var(--wok); color:var(--wok-ink); padding-block:clamp(2.5rem,6vw,3.75rem); }
.foot-grid{ display:grid; gap:2rem; grid-template-columns:1fr; }
@media (min-width:760px){ .foot-grid{ grid-template-columns:repeat(2,minmax(0,1fr)); gap:3rem; } }
.foot h2{
  font-family:"IBM Plex Mono",ui-monospace,monospace; font-size:.68rem;
  letter-spacing:.18em; text-transform:uppercase; color:var(--wok-ash);
  margin:0 0 .85rem; font-weight:500;
}
.foot p{ margin:0 0 .3rem; }
.foot a{ color:var(--wok-ink); text-decoration-color:var(--wok-ash); text-underline-offset:3px; }
.foot a:hover{ text-decoration-color:var(--wok-ink); }
.foot .maps{
  display:inline-block; margin-top:.7rem; font-size:.85rem;
  color:var(--jade); text-decoration:none; border-bottom:1px solid currentColor;
}
.foot .imp p{ margin-bottom:.85rem; font-size:.9rem; }
.foot .imp p:first-of-type{ color:var(--wok-ash); font-size:.8rem; }
.foot .imp strong{ font-weight:600; }
.colophon{
  margin-top:2.5rem; padding-top:1.25rem; border-top:1px solid rgba(255,255,255,.1);
  font-size:.78rem; color:var(--wok-ash);
  display:flex; flex-wrap:wrap; gap:.4rem 1.25rem; align-items:baseline;
}

/* ---------- Anruf-Leiste (Handy) ---------- */
.callbar{
  position:fixed; left:0; right:0; bottom:0; z-index:30;
  background:var(--chili); color:#fff; text-decoration:none;
  display:flex; align-items:center; justify-content:center; gap:.6rem;
  padding:.85rem 1rem calc(.85rem + env(safe-area-inset-bottom,0px));
  font-weight:600; font-size:1rem; letter-spacing:.01em;
  box-shadow:0 -6px 20px -10px rgba(0,0,0,.5);
}
.callbar .tel{ font-family:"IBM Plex Mono",ui-monospace,monospace; font-variant-numeric:tabular-nums; }
@media (min-width:1000px){ .callbar{ display:none; } }
@media (max-width:999px){ .foot{ padding-bottom:calc(4.5rem + env(safe-area-inset-bottom,0px)); } }

@media (prefers-reduced-motion:reduce){
  *,*::before,*::after{ animation-duration:.01ms !important; transition-duration:.01ms !important; scroll-behavior:auto !important; }
}
html{ scroll-behavior:smooth; }
"""

JS = r"""
(function(){
  var HOURS = __HOURS__;
  function mins(s){ var p = s.split(":"); return (+p[0])*60 + (+p[1]); }

  // Immer nach Uhrzeit in Deutschland rechnen, nicht nach der Uhr des Besuchers.
  var WD = { Mo:0, Di:1, Mi:2, Do:3, Fr:4, Sa:5, So:6 };
  function berlinNow(){
    try {
      var parts = {};
      new Intl.DateTimeFormat("de-DE", {
        timeZone: "Europe/Berlin", weekday: "short",
        hour: "2-digit", minute: "2-digit", hour12: false
      }).formatToParts(new Date()).forEach(function(p){ parts[p.type] = p.value; });
      var d = WD[(parts.weekday || "").slice(0, 2)];
      var h = parseInt(parts.hour, 10), m = parseInt(parts.minute, 10);
      if(d !== undefined && !isNaN(h) && !isNaN(m)) return { day: d, minutes: h*60 + m };
    } catch(err){ /* faellt unten auf die lokale Uhr zurueck */ }
    var now = new Date();
    return { day: (now.getDay() + 6) % 7, minutes: now.getHours()*60 + now.getMinutes() };
  }

  function refreshStatus(){
    var el = document.getElementById("status");
    if(!el) return;
    var t = berlinNow();
    var day = t.day;
    var nowM = t.minutes;
    var slots = HOURS[day] || [];
    var open = null, next = null;
    for(var i=0;i<slots.length;i++){
      var a = mins(slots[i][0]), b = mins(slots[i][1]);
      if(nowM >= a && nowM < b){ open = slots[i]; break; }
      if(nowM < a && next === null){ next = slots[i]; }
    }
    el.classList.remove("open","shut");
    var label = el.querySelector(".status-text");
    if(open){
      el.classList.add("open");
      label.textContent = "Jetzt geöffnet bis " + open[1] + " Uhr";
    } else if(next){
      el.classList.add("shut");
      label.textContent = "Geschlossen, ab " + next[0] + " Uhr geöffnet";
    } else {
      el.classList.add("shut");
      var d = (day + 1) % 7, guard = 0;
      while((!HOURS[d] || !HOURS[d].length) && guard++ < 7){ d = (d+1) % 7; }
      var names = ["morgen","Dienstag","Mittwoch","Donnerstag","Freitag","Samstag","Sonntag","Montag"];
      label.textContent = "Heute geschlossen, morgen ab " + (HOURS[d] && HOURS[d][0] ? HOURS[d][0][0] : "17:00") + " Uhr";
    }
    var rows = document.querySelectorAll(".hours-table tr[data-day]");
    for(var r=0;r<rows.length;r++){
      if(+rows[r].getAttribute("data-day") === day){ rows[r].setAttribute("data-today",""); }
      else { rows[r].removeAttribute("data-today"); }
    }
  }
  refreshStatus();
  setInterval(refreshStatus, 60000);

  // Aktiven Abschnitt in Index und Chip-Leiste markieren
  var secs = [].slice.call(document.querySelectorAll(".sec"));
  var links = {};
  [].forEach.call(document.querySelectorAll('.index a, .chips a'), function(a){
    var id = a.getAttribute("href").slice(1);
    (links[id] = links[id] || []).push(a);
  });
  if(secs.length && "IntersectionObserver" in window){
    var current = null;
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(en){ en.target.__vis = en.isIntersecting; });
      var top = null;
      for(var i=0;i<secs.length;i++){ if(secs[i].__vis){ top = secs[i].id; break; } }
      if(!top || top === current) return;
      if(current && links[current]) links[current].forEach(function(a){ a.removeAttribute("aria-current"); });
      current = top;
      if(links[current]) links[current].forEach(function(a){
        a.setAttribute("aria-current","true");
        var bar = a.closest(".chips ul");
        if(bar){ bar.scrollTo({ left: a.offsetLeft - 20, behavior: "smooth" }); }
      });
    }, { rootMargin: "-72px 0px -65% 0px", threshold: 0 });
    secs.forEach(function(s){ io.observe(s); });
  }
})();
"""

TITLE = "China Wok Dao"
DESC = ("China Wok Dao in Rodalben: chinesische und thailändische Küche zum Abholen "
        "und im Restaurant. Speisekarte, Öffnungszeiten und Telefonnummer 06331 / 140888.")

BODY = """<a class="skip" href="#speisekarte">Direkt zur Speisekarte</a>

<header class="hero">
  <div class="wrap hero-grid">
    <div>
      <p class="eyebrow">Rodalben &middot; Chinesisch &amp; Thai</p>
      <h1 class="wordmark">China<br>Wok <span class="dao">Dao</span></h1>
      <p class="tagline">Frisch aus dem Wok, zum Mitnehmen oder bei uns im Haus. Bestellt wird nach Nummer.</p>
      <p class="status" id="status"><span class="dot"></span><span class="status-text">Öffnungszeiten</span></p>
    </div>
    <div>
      <a class="call" href="tel:__TEL__">
        <span class="call-label">Bestellung &amp; Reservierung</span>
        <span class="call-num">__PHONE__</span>
      </a>
      <div class="hero-hours">
        <table class="hours-table">
          <caption class="eyebrow" style="margin:0 0 .5rem; text-align:left;">Öffnungszeiten</caption>
          <tbody>
__HOURS_ROWS__
          </tbody>
        </table>
      </div>
    </div>
  </div>
</header>

<div class="rice-note">
  <div class="wrap">
    <p><strong>Alle Hauptgerichte kommen mit Reis als Beilage.</strong>
    Stattdessen gebratener Reis oder gebratene Nudeln: <span class="plus">+2,50 €</span></p>
  </div>
</div>

<nav class="chips" aria-label="Abschnitte der Speisekarte">
  <ul>
__CHIPS__
  </ul>
</nav>

<main class="karte" id="speisekarte">
  <div class="wrap karte-grid">
    <nav class="index" aria-label="Speisekarte">
      <h2>Speisekarte</h2>
      <ol>
__NAV__
      </ol>
    </nav>
    <div>
__MENU__
    </div>
  </div>
</main>

<section class="legend" id="zusatzstoffe" aria-labelledby="h-zus">
  <div class="wrap">
    <h2 id="h-zus">Kennzeichnung der Zusatzstoffe</h2>
    <ul>
__LEGEND__
    </ul>
  </div>
</section>

<footer class="foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <h2>Anschrift</h2>
        <p>__NAME__</p>
        <p>__STREET__</p>
        <p>__ZIP__ __CITY__</p>
        <a class="maps" href="__MAPS__" target="_blank" rel="noopener">Route in Google Maps</a>
      </div>
      <div class="imp">
        <h2>Impressum</h2>
        <p>Angaben gemäß § 5 DDG</p>
        <p><strong>__NAME__</strong><br>Inhaber: __OWNER__<br>__STREET__<br>__ZIP__ __CITY__</p>
        <p>Telefon: __PHONE__<br>E-Mail: <a href="mailto:__EMAIL__">__EMAIL__</a></p>
      </div>
    </div>
    <p class="colophon">
      <span>&copy; __YEAR__ __NAME__</span>
      <span>Alle Preise in Euro, inklusive Mehrwertsteuer</span>
      <span>Änderungen und Irrtümer vorbehalten</span>
    </p>
  </div>
</footer>

<a class="callbar" href="tel:__TEL__">Jetzt bestellen <span class="tel">__PHONE__</span></a>"""

CHIPS = "\n".join('    <li><a href="#%s">%s</a></li>' % (s[0], e(s[1])) for s in SECTIONS)

body = (BODY
        .replace("__HOURS_ROWS__", HOURS_ROWS)
        .replace("__CHIPS__", CHIPS)
        .replace("__NAV__", NAV)
        .replace("__MENU__", MENU)
        .replace("__LEGEND__", LEGEND)
        .replace("__TEL__", R["phone_tel"])
        .replace("__PHONE__", e(R["phone_display"]))
        .replace("__NAME__", e(R["name"]))
        .replace("__STREET__", e(R["street"]))
        .replace("__ZIP__", e(R["zip"]))
        .replace("__CITY__", e(R["city"]))
        .replace("__MAPS__", e(R["maps"]))
        .replace("__OWNER__", e(R["owner"]))
        .replace("__EMAIL__", e(R["email"]))
        .replace("__YEAR__", "2026"))

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=Big+Shoulders+Display:wght@700;800&'
         'family=IBM+Plex+Mono:wght@400;500&'
         'family=Public+Sans:ital,wght@0,400;0,600;1,400&display=swap">')

js = JS.replace("__HOURS__", HOURS_JSON)

# ---- 1) Eigenstaendige Seite fuer chinawokdao.com -------------------------
standalone = """<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>%(title)s | Chinesisch &amp; Thai in %(city)s</title>
<meta name="description" content="%(desc)s">
<link rel="canonical" href="https://%(domain)s/">
<meta property="og:type" content="website">
<meta property="og:locale" content="de_DE">
<meta property="og:site_name" content="%(title)s">
<meta property="og:title" content="%(title)s | Chinesisch &amp; Thai in %(city)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:url" content="https://%(domain)s/">
<meta name="twitter:card" content="summary">
<meta name="theme-color" content="#241E1B">
<link rel="icon" href="data:image/svg+xml,%%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%%3E%%3Crect width='64' height='64' rx='12' fill='%%23241E1B'/%%3E%%3Cpath d='M26.8 3.5L29.2 3.4L31.7 3.6L34.1 3.9L36.4 4.4L38.6 5.2L40.8 6.1L42.9 7.1L44.8 8.4L46.6 9.7L48.3 11.2L49.9 12.8L51.3 14.6L52.5 16.4L53.5 18.3L54.4 20.2L55.2 22.2L55.7 24.2L56.1 26.3L56.3 28.3L56.3 30.3L56.2 32.3L55.8 34.3L55.4 36.2L54.8 38.0L54.0 39.8L53.1 41.5L52.1 43.1L51.0 44.5L49.8 45.9L48.4 47.1L47.0 48.2L45.6 49.2L44.0 50.0L42.5 50.7L40.9 51.2L39.2 51.6L37.6 51.9L36.0 52.0L34.4 52.0L32.8 51.9L31.3 51.6L29.8 51.2L28.4 50.7L27.0 50.1L25.8 49.3L24.6 48.5L23.5 47.6L22.4 46.6L21.5 45.6L20.7 44.5L20.1 43.4L19.5 42.2L19.0 41.0L18.6 39.8L18.4 38.6L18.2 37.3L18.2 36.1L18.3 35.0L18.4 33.8L18.7 32.7L19.0 31.7L19.5 30.6L20.0 29.7L20.5 28.8L24.7 30.3L24.4 30.9L24.1 31.5L24.0 32.2L23.8 32.8L23.7 33.5L23.7 34.2L23.7 34.9L23.8 35.6L24.0 36.3L24.2 37.0L24.4 37.6L24.8 38.3L25.2 38.9L25.6 39.5L26.1 40.1L26.6 40.7L27.2 41.2L27.9 41.6L28.6 42.0L29.3 42.3L30.0 42.6L30.8 42.9L31.6 43.0L32.4 43.1L33.3 43.1L34.1 43.1L35.0 43.0L35.8 42.8L36.6 42.5L37.5 42.2L38.2 41.8L39.0 41.3L39.7 40.8L40.4 40.2L41.1 39.6L41.6 38.9L42.2 38.1L42.7 37.3L43.1 36.4L43.4 35.5L43.7 34.6L43.9 33.6L44.0 32.7L44.0 31.7L43.9 30.7L43.8 29.7L43.6 28.7L43.3 27.7L42.9 26.8L42.4 25.9L41.9 25.0L41.3 24.1L40.6 23.3L39.8 22.6L39.0 21.9L38.1 21.3L37.2 20.7L36.2 20.2L35.1 19.9L34.1 19.5L33.0 19.3L31.8 19.2L30.7 19.2L29.6 19.2Z' fill='%%23F2714F'/%%3E%%3Cpath d='M22.6 29.6 l-2 -8 l5 3 l5 -4 l-1 8 z' fill='%%23F2714F'/%%3E%%3Ccircle cx='29.2' cy='12.3' r='2.6' fill='%%23241E1B'/%%3E%%3C/svg%%3E">
%(fonts)s
<style>
:root{ color-scheme:light dark; padding-top:env(safe-area-inset-top,0px); padding-bottom:env(safe-area-inset-bottom,0px); }
%(css)s
</style>
<script type="application/ld+json">%(schema)s</script>
</head>
<body>
%(body)s
<script>%(js)s</script>
</body>
</html>
""" % {
    "title": e(TITLE), "city": e(R["city"]), "desc": e(DESC), "domain": e(R["domain"]),
    "fonts": FONTS, "css": CSS, "schema": json.dumps(SCHEMA, ensure_ascii=False, indent=1),
    "body": body, "js": js,
}

# ---- 2) Fragment fuer die Artifact-Vorschau -------------------------------
artifact = """<title>%(title)s</title>
%(fonts)s
<style>
:root{ color-scheme:light dark; }
%(css)s
</style>
<script type="application/ld+json">%(schema)s</script>
%(body)s
<script>%(js)s</script>
""" % {
    "title": e(TITLE), "fonts": FONTS, "css": CSS,
    "schema": json.dumps(SCHEMA, ensure_ascii=False, indent=1), "body": body, "js": js,
}

# ---- 3) Beiwerk fuer Cloudflare Pages ------------------------------------
ROBOTS = """User-agent: *
Allow: /

Sitemap: https://%(domain)s/sitemap.xml
""" % {"domain": R["domain"]}

SITEMAP = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
 <url>
  <loc>https://%(domain)s/</loc>
  <changefreq>monthly</changefreq>
  <priority>1.0</priority>
 </url>
</urlset>
""" % {"domain": R["domain"]}

# GitHub Pages: CNAME bindet die eigene Domain, .nojekyll schaltet Jekyll ab.
CNAME = "%s\n" % R["domain"]
NOJEKYLL = ""

os.makedirs(os.path.join(BASE, "docs"), exist_ok=True)
os.makedirs(os.path.join(BASE, "build"), exist_ok=True)
open(os.path.join(BASE, "docs", "index.html"), "w", encoding="utf-8").write(standalone)
open(os.path.join(BASE, "build", "artifact.html"), "w", encoding="utf-8").write(artifact)
for fname, text in (("robots.txt", ROBOTS), ("sitemap.xml", SITEMAP),
                    ("CNAME", CNAME), (".nojekyll", NOJEKYLL)):
    open(os.path.join(BASE, "docs", fname), "w", encoding="utf-8").write(text)

n = sum(len(s[3]) for s in SECTIONS)
print("docs/index.html      %7d Bytes" % len(standalone.encode("utf-8")))
print("build/artifact.html  %7d Bytes" % len(artifact.encode("utf-8")))
print("docs/robots.txt, docs/sitemap.xml, docs/CNAME, docs/.nojekyll geschrieben")
print("%d Abschnitte, %d Gerichte, Preise: %s" % (len(SECTIONS), n, "ja" if HAS_PRICES else "noch keine"))
