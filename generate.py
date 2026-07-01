#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Static site generator for Samuel's Tree Service.
Assembles 11 pages from shared head / nav / footer templates.
Real data only — sourced from samuelstreeservice.com + Google profile."""

import json, os

OUT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- business facts
BIZ = {
    "name": "Samuel's Tree Service",
    "legal": "Samuel's Tree Service, LLC",
    "phone": "940-595-3335",
    "tel": "+19405953335",
    "addr": "405 S Elm St. Ste. 303",
    "city": "Denton, TX 76201",
    "area": "Denton, Corinth & surrounding areas",
    "founded": 2002,
    "google": "https://g.co/kgs/Qwg9jkr",
    "facebook": "https://www.facebook.com/SamuelsTreeService/",
}

# ---------------------------------------------------------------- icons (feather)
def ic(p):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + p + '</svg>')

ICONS = {
    "phone": ic('<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>'),
    "arrow": ic('<line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>'),
    "check": ic('<polyline points="20 6 9 17 4 12"/>'),
    "pin": ic('<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>'),
    "clock": ic('<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>'),
    "shield": ic('<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>'),
    "award": ic('<circle cx="12" cy="8" r="6"/><path d="M15.5 13.5L17 22l-5-3-5 3 1.5-8.5"/>'),
    "leaf": ic('<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10z"/><path d="M2 21c0-3 1.85-5.36 5.08-6"/>'),
    "axe": ic('<path d="M14 3l7 7-3 3-7-7z"/><path d="M11 6L3 14l4 4 8-8"/><line x1="7" y1="18" x2="3" y2="22"/>'),
    "crane": ic('<line x1="4" y1="21" x2="20" y2="21"/><line x1="6" y1="21" x2="6" y2="5"/><polyline points="6 5 20 5 20 9"/><line x1="14" y1="5" x2="14" y2="11"/><line x1="6" y1="5" x2="3" y2="8"/>'),
    "wind": ic('<path d="M9.59 4.59A2 2 0 1 1 11 8H2"/><path d="M12.59 19.41A2 2 0 1 0 14 16H2"/><path d="M17.73 7.73A2.5 2.5 0 1 1 19.5 12H2"/>'),
    "stump": ic('<ellipse cx="12" cy="7" rx="7" ry="3"/><path d="M5 7v6c0 1.66 3.13 3 7 3s7-1.34 7-3V7"/><path d="M12 10v8"/>'),
    "search": ic('<circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>'),
    "drop": ic('<path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/>'),
    "star": ic('<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>'),
    "mail": ic('<rect x="2" y="4" width="20" height="16" rx="2"/><polyline points="22 6 12 13 2 6"/>'),
    "fb": ic('<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>'),
    "chev": ic('<polyline points="6 9 12 15 18 9"/>'),
    "scissors": ic('<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><line x1="20" y1="4" x2="8.12" y2="15.88"/><line x1="14.47" y1="14.48" x2="20" y2="20"/><line x1="8.12" y1="8.12" x2="12" y2="12"/>'),
    "truck": ic('<rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/>'),
    "bolt": ic('<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>'),
    "users": ic('<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>'),
    "tag": ic('<path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/>'),
}

# ---------------------------------------------------------------- services
SERVICES = [
    {
        "slug": "tree-removal", "title": "Tree Removal", "icon": "crane",
        "img": "tree-removal.jpg",
        "tag": "Crane-assisted · fully insured",
        "short": "Safe felling, low-impact lowering, and complete debris haul-off for dead, hazardous, or unwanted trees.",
        "hero_sub": "Dead and structurally compromised trees don't wait for a convenient moment. Neither do we.",
        "lead": "For over two decades, Samuel's Tree Service has removed trees of every size and scope across Denton — from a single dead oak over a driveway to crane-assisted takedowns inches from a roofline.",
        "sections": [
            ("Three ways we remove a tree", [
                "<b>Standard removal.</b> Safe felling followed by meticulous debris clean-up, chipping, and haul-off. You get a detailed estimate before we start.",
                "<b>Down-only removal.</b> The budget option: we safely cut the tree down in one or several pieces, with no cleanup, firewood cutting, or limb removal.",
                "<b>Low-impact removal.</b> Worried about your lawn or beds? We carefully lower tree sections to the ground in small pieces — sometimes with a lift or crane — to minimize any damage.",
            ]),
        ],
        "body": [
            "Dead or dying trees lose the ability to support themselves and become liabilities that can damage your home, your property, or the people on it. When we take one down, we also assess the health of the trees left standing so we can flag the next risk before it becomes an emergency.",
            "We're locally owned and operated, but we work with the equipment and resources of a national operation — which is how clients get high-quality removals that are also fast and friendly. Free estimates, every time.",
        ],
        "reasons_title": "When a tree should come out",
        "reasons": [
            "It's diseased, damaged, or dead and likely to drop limbs or fall",
            "Pests or disease have made it unsalvageable and threaten nearby trees",
            "Invasive roots are reaching foundations, sidewalks, or sewer lines",
            "It blocks a view, crowds healthier trees, or sits where you're building",
            "Leaning trunks or heavy limbs overhang the house ahead of storm season",
        ],
    },
    {
        "slug": "tree-trimming", "title": "Tree Trimming & Pruning", "icon": "scissors",
        "img": "tree-trimming.jpg",
        "tag": "ISA-informed cuts",
        "short": "Pruning for health and structure — every cut made for a reason, never to a stub.",
        "hero_sub": "Pruning is the most common tree-care procedure, and the most misunderstood. We treat it like the science it is.",
        "lead": "Many companies prune by removing whatever's in reach. Because each cut changes how a tree grows, we don't take a branch off without a reason — structure, clearance, health, or safety.",
        "sections": [
            ("What good pruning does", [
                "<b>Protects the tree's health.</b> Removing dead, diseased, or crossing limbs stops decay from spreading and opens the canopy to light and air.",
                "<b>Reduces risk.</b> Thinning heavy, overextended limbs lowers the load that wind and ice can act on.",
                "<b>Improves the shape.</b> Thoughtful cuts guide growth and keep a mature tree balanced over your roof, drive, and walkways.",
            ]),
        ],
        "body": [
            "Our crews are trained to make proper pruning cuts at the right points — never the indiscriminate topping that leaves a tree weaker and uglier than they found it. The goal is a tree that's safer today and healthier for the next decade.",
            "Not sure whether a tree needs pruning or something more? Our ISA Certified Arborist can look at it and tell you straight.",
        ],
        "reasons_title": "Good candidates for pruning",
        "reasons": [
            "Limbs overhanging the roof, drive, or power service",
            "Dead, broken, or rubbing branches inside the canopy",
            "Young trees that need early structural training",
            "Dense crowns that should be thinned before storm season",
            "Trees that have outgrown their clearance from the house",
        ],
    },
    {
        "slug": "stump-grinding", "title": "Stump Grinding", "icon": "stump",
        "img": "stump-grinding.jpg",
        "tag": "Low site disturbance",
        "short": "Grind the stump below grade with minimal disruption — the cleanest way to reclaim the spot.",
        "hero_sub": "Two ways to deal with a stump: grind it, or dig it out. In most yards, grinding wins.",
        "lead": "To remove a stump there are two common options — grind it down or dig it out. Stump grinding is the preferred method in most situations because it limits the extent of site disturbance and impact on the surrounding lawn.",
        "sections": [
            ("Why grinding beats digging", [
                "<b>Less damage.</b> Digging a stump out tears up far more of your yard than grinding the same stump below the surface.",
                "<b>Faster reclaim.</b> A ground stump lets you replant, re-sod, or build over the spot without hauling out a massive root ball.",
                "<b>Cleaner finish.</b> We grind below grade and leave the area tidy — the grindings can even be left as mulch on request.",
            ]),
        ],
        "body": [
            "Stump grinding pairs naturally with a removal, but we're glad to come grind down stumps left behind by another company or a storm. Ask about it when you request your free estimate.",
        ],
        "reasons_title": "Reasons to grind a stump",
        "reasons": [
            "It's a trip hazard or in the way of the mower",
            "You want to replant or re-sod the spot",
            "The stump is sprouting or attracting pests",
            "You're reclaiming the space for a patio, bed, or build",
        ],
    },
    {
        "slug": "storm-cleanup", "title": "Storm Clean-Up & Emergency", "icon": "wind",
        "img": "storm-cleanup.jpg",
        "tag": "24/7 emergency response",
        "short": "Downed trees, hanging limbs, and storm debris cleared fast — day or night.",
        "hero_sub": "When a storm puts a tree on your roof or across your drive, the clock is the whole problem.",
        "lead": "Strong winds and rain scatter dead branches, leaves, and whole trees across your property. Most people don't have the skill, tools, or experience to clean it up safely — or to keep the house secure afterward. That's the call we take 24/7.",
        "sections": [
            ("What emergency response covers", [
                "<b>Hazard removal first.</b> We clear the limbs and trunks threatening people, vehicles, and the structure before anything else.",
                "<b>Full debris cleanup.</b> Downed trees, broken limbs, and scattered storm debris hauled away so you can get back to normal.",
                "<b>Standing-tree assessment.</b> After the cleanup we check what's left for cracks, leans, and damage that could fail in the next storm.",
            ]),
        ],
        "body": [
            "Storm work is dangerous — tensioned limbs, unstable trunks, and downed lines turn a cleanup into a serious risk for anyone without the right training and gear. Call the professionals and let us handle the part that hurts people.",
        ],
        "reasons_title": "Call us right away when",
        "reasons": [
            "A tree or large limb is on your roof, car, or fence",
            "A trunk is blocking the driveway or road",
            "A tree is leaning or partially uprooted after wind",
            "Hanging limbs are caught up over a walkway or entry",
        ],
        "emergency": True,
    },
    {
        "slug": "arborist", "title": "Certified Arborist", "icon": "search",
        "img": "tree-removal-2.jpg",
        "tag": "ISA Certified Arborist on staff",
        "short": "Diagnosis and honest recommendations from someone trained in the science of trees.",
        "hero_sub": "An arborist is trained in the art and science of caring for and maintaining trees. We keep one on the crew.",
        "lead": "Our ISA Certified Arborist can diagnose a wide range of tree problems — fungus, disease, structural defects, decline — and then recommend the right response, whether that's treatment, pruning, or removal.",
        "sections": [
            ("What an arborist visit gets you", [
                "<b>A real diagnosis.</b> We identify what's actually wrong instead of guessing, so you spend money on the problem and not the symptom.",
                "<b>Honest options.</b> Sometimes the answer is a treatment plan; sometimes it's removal. We'll tell you which, and why.",
                "<b>A plan for the whole property.</b> We look at the trees you keep, not just the one you called about, to head off the next issue.",
            ]),
        ],
        "body": [
            "Bringing in a certified arborist before you cut is the difference between saving a healthy tree and losing a salvageable one — or, just as often, removing a hazard before it removes itself onto your roof.",
        ],
        "reasons_title": "When to call the arborist",
        "reasons": [
            "Leaves, bark, or limbs that look diseased or off-color",
            "Mushrooms or fungus at the base or on the trunk",
            "A tree that's declining and you don't know why",
            "Before any major pruning or a removal decision",
        ],
    },
    {
        "slug": "plant-health", "title": "Plant & Tree Health Care", "icon": "drop",
        "img": "beforeafter-1.jpg",
        "tag": "Deep root fertilization",
        "short": "Deep root fertilization to restore struggling, stressed, or declining trees.",
        "hero_sub": "A struggling tree is usually a hungry one. Deep root fertilization feeds it where it counts.",
        "lead": "Deep root fertilization is a specialized method used to restore struggling or declining trees. Nutrients are injected directly into the root zone — below the competing turf — where the tree can actually use them.",
        "sections": [
            ("Why deep root feeding works", [
                "<b>Bypasses the lawn.</b> Surface fertilizer feeds your grass first. Deep injection puts nutrients down where tree roots take them up.",
                "<b>Targets stress.</b> Urban trees fight compacted soil, construction damage, and drought. Feeding the root zone helps them recover.",
                "<b>Pairs with care.</b> Combined with sound pruning and arborist diagnosis, it's one of the best ways to extend the life of a valued tree.",
            ]),
        ],
        "body": [
            "If a tree on your property is thinning out, dropping leaves early, or simply not thriving the way it used to, deep root fertilization is often the lowest-cost first step before you consider anything more drastic.",
        ],
        "reasons_title": "Signs a tree could use feeding",
        "reasons": [
            "Thinning canopy or smaller-than-normal leaves",
            "Early leaf drop or pale, off-color foliage",
            "Recent construction or soil compaction nearby",
            "A mature, high-value tree you want to protect",
        ],
    },
]
SVC_BY_SLUG = {s["slug"]: s for s in SERVICES}

REVIEWS = [
    ("Debra R.", "We had a great experience with Samuel's Tree Service. They came out on time, did the job efficiently and left our yard neat and tidy.", "Google Review"),
    ("Carolyn N.", "A very good experience. I highly recommend Samuel's Tree Service. They are prompt and efficient.", "Google Review"),
]

AWARDS = ["Best of Denton 2025", "Best of Denton 2024", "Best of Denton 2023",
          "Best of Denton 2022", "Best of Denton 2021", "Best of Denton 2020"]

# ---------------------------------------------------------------- shared chunks
def nav(active):
    def cur(slug): return ' aria-current="page"' if active == slug else ''
    svc_items = ""
    for s in SERVICES:
        svc_items += (
            f'<a href="service-{s["slug"]}.html"><span class="di">{ICONS[s["icon"]]}</span>'
            f'<span><b style="font-weight:600;color:var(--ink);display:block;font-family:var(--body);font-size:.92rem">{s["title"]}</b>'
            f'<small>{s["short"][:46]}…</small></span></a>'
        )
    mobile_svc = "".join(f'<a class="m-sub" href="service-{s["slug"]}.html">{s["title"]}</a>' for s in SERVICES)
    return f'''<header class="site-header">
  <nav class="nav" aria-label="Primary">
    <a class="brand" href="index.html" aria-label="Samuel's Tree Service home">
      <span class="mark">S</span>
      <span><b>Samuel's</b><span>Tree Service</span></span>
    </a>
    <ul class="nav-links">
      <li><a class="nav-link" href="index.html"{cur('home')}>Home</a></li>
      <li><a class="nav-link" href="about.html"{cur('about')}>About</a></li>
      <li class="has-menu">
        <a class="nav-link" href="services.html"{cur('services')}>Services <span class="caret">{ICONS['chev']}</span></a>
        <div class="dropdown" role="menu">{svc_items}</div>
      </li>
      <li><a class="nav-link" href="gallery.html"{cur('gallery')}>Past Work</a></li>
      <li><a class="nav-link" href="contact.html"{cur('contact')}>Contact</a></li>
    </ul>
    <div class="nav-cta">
      <a class="nav-phone" href="tel:{BIZ['tel']}">{ICONS['phone']}{BIZ['phone']}</a>
      <a class="btn btn-primary" href="contact.html">Get a Free Estimate {ICONS['arrow']}</a>
      <button class="hamburger" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-nav"><span></span><span></span><span></span></button>
    </div>
  </nav>
  <div class="mobile-nav" id="mobile-nav">
    <a href="index.html">Home <small>01</small></a>
    <a href="about.html">About <small>02</small></a>
    <a href="services.html">Services <small>03</small></a>
    {mobile_svc}
    <a href="gallery.html">Past Work <small>04</small></a>
    <a href="contact.html">Contact <small>05</small></a>
    <div class="m-cta">
      <a class="btn btn-primary btn-lg" href="contact.html">Get a Free Estimate {ICONS['arrow']}</a>
      <a class="btn btn-ghost btn-lg" href="tel:{BIZ['tel']}">{ICONS['phone']} {BIZ['phone']}</a>
    </div>
  </div>
</header>'''

def footer():
    svc_links = "".join(f'<a href="service-{s["slug"]}.html">{s["title"]}</a>' for s in SERVICES)
    return f'''<footer class="site-footer">
  <div class="wrap-wide">
    <div class="footer-top">
      <div class="footer-brand">
        <a class="brand" href="index.html"><span class="mark">S</span><span><b>Samuel's</b><span>Tree Service</span></span></a>
        <p>Locally owned, ISA Certified, and fully insured tree care serving {BIZ['area']} since {BIZ['founded']}.</p>
        <span class="status" data-status role="status" aria-live="polite"><span class="dot"></span><span data-status-text>Open now</span><small data-status-sub></small></span>
      </div>
      <div class="footer-col">
        <h5>Services</h5>
        {svc_links}
        <a href="services.html">All services</a>
      </div>
      <div class="footer-col">
        <h5>Company</h5>
        <a href="about.html">About Us</a>
        <a href="gallery.html">Past Work</a>
        <a href="contact.html">Free Estimates</a>
        <a href="contact.html">Specials &amp; Discounts</a>
        <a href="{BIZ['google']}" target="_blank" rel="noopener">Google Reviews</a>
      </div>
      <div class="footer-col footer-contact">
        <h5>Get in touch</h5>
        <a class="fc" href="tel:{BIZ['tel']}">{ICONS['phone']} {BIZ['phone']}</a>
        <span class="fc">{ICONS['pin']} {BIZ['addr']}, {BIZ['city']}</span>
        <span class="fc">{ICONS['clock']} Mon–Fri 8–7 · Sat 9–2 · 24/7 Emergency</span>
        <a class="fc" href="{BIZ['facebook']}" target="_blank" rel="noopener">{ICONS['fb']} Facebook</a>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© {2026} {BIZ['legal']}. All rights reserved.</span>
      <span class="fb-badges">
        <span>{ICONS['shield']} Licensed &amp; Insured</span>
        <span>{ICONS['award']} BBB A+ Rated</span>
        <span>{ICONS['leaf']} ISA Certified Arborist</span>
      </span>
    </div>
  </div>
</footer>'''

def head(title, desc, og_img="assets/img/tree-removal.jpg", canonical="", jsonld=None):
    fonts = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
             '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
             '<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..600;1,9..144,300..500&family=Inter:wght@400;500;600&family=Space+Grotesk:wght@400;500&display=swap" rel="stylesheet">')
    ld = f'<script type="application/ld+json">{json.dumps(jsonld)}</script>' if jsonld else ''
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0C110D">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{og_img}">
<meta property="og:site_name" content="Samuel's Tree Service">
<meta name="twitter:card" content="summary_large_image">
{fonts}
<link rel="stylesheet" href="assets/css/styles.css">
{ld}
</head>
<body>
'''

SCRIPTS = ('<script src="https://cdn.jsdelivr.net/npm/lenis@1.1.13/dist/lenis.min.js"></script>'
           '<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>'
           '<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js"></script>'
           '<script src="assets/js/main.js"></script>\n</body>\n</html>')

LOCAL_BIZ_LD = {
    "@context": "https://schema.org", "@type": "LocalBusiness",
    "name": BIZ["legal"], "image": "assets/img/tree-removal.jpg",
    "telephone": BIZ["phone"], "url": "https://samuelstreeservice.com/",
    "priceRange": "$$",
    "address": {"@type": "PostalAddress", "streetAddress": BIZ["addr"],
                "addressLocality": "Denton", "addressRegion": "TX", "postalCode": "76201", "addressCountry": "US"},
    "areaServed": ["Denton", "Corinth"],
    "aggregateRating": {"@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "950"},
    "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "08:00", "closes": "19:00"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Saturday"], "opens": "09:00", "closes": "14:00"},
    ],
}

def status_badge():
    return ('<span class="status" data-status role="status" aria-live="polite"><span class="dot"></span>'
            '<span data-status-text>Open now</span><small data-status-sub></small></span>')

def write(name, body):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(body)
    print("wrote", name)

def page_hero(crumbs, title, sub, img=None, alt="", tag="", eyebrow=""):
    """Dark header; optional contained photo card on the right (split)."""
    eb = f'<span class="eyebrow reveal" style="margin:1rem 0 .4rem">{eyebrow}</span>' if eyebrow else ''
    left = f'''<div>
        <div class="crumbs reveal">{crumbs}</div>
        {eb}
        <h1 class="reveal">{title}</h1>
        <p class="reveal">{sub}</p>
      </div>'''
    if img:
        card = f'''<div class="ph-card reveal">
        <img src="assets/img/{img}" alt="{alt}" loading="eager" width="1000" height="667">
        {f'<span class="tag">{tag}</span>' if tag else ''}
      </div>'''
        return f'''<section class="page-hero split">
    <div class="wrap-wide ph-grid">
      {left}
      {card}
    </div>
  </section>'''
    return f'''<section class="page-hero">
    <div class="wrap-wide">
      {left}
    </div>
  </section>'''

# ---------------------------------------------------------------- reusable sections
def cta_band():
    return f'''<section>
  <div class="wrap">
    <div class="cta-band reveal">
      <div class="bg"><img src="assets/img/tree-removal-2.jpg" alt="" loading="lazy"></div>
      <span class="eyebrow no-rule" style="justify-content:center;margin-bottom:1.2rem">Free estimates · {BIZ['area']}</span>
      <h2>The tree isn't going to<br>get smaller.</h2>
      <p>Tell us what you're looking at and we'll come give you a straight estimate — no pressure, no hidden fees, no charge for work you didn't authorize.</p>
      <div class="cta-actions">
        <a class="btn btn-primary btn-lg" href="contact.html">Get a Free Estimate {ICONS['arrow']}</a>
        <a class="btn btn-ghost btn-lg" href="tel:{BIZ['tel']}">{ICONS['phone']} {BIZ['phone']}</a>
      </div>
    </div>
  </div>
</section>'''

def reviews_section():
    cards = ""
    for who, text, src in REVIEWS:
        cards += f'''<div class="review reveal">
      <div class="stars" aria-label="5 out of 5 stars">★★★★★</div>
      <p>{text}</p>
      <div class="who"><span class="av">{who[0]}</span><span><b>{who}</b><span>{src}</span></span></div>
    </div>'''
    return f'''<section>
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">5.0 across 950+ reviews</span>
      <h2 class="section-title">Denton keeps<br>calling us back.</h2>
      <p>Five stars on Google across more than 950 reviews, an A+ with the BBB, and Best of Denton six years running. Here's a sample — read the rest on Google.</p>
    </div>
    <div class="reviews">{cards}</div>
    <div class="reveal" style="margin-top:2rem">
      <a class="textlink" href="{BIZ['google']}" target="_blank" rel="noopener">Read all reviews on Google {ICONS['arrow']}</a>
    </div>
  </div>
</section>'''

# ================================================================ HOME
def page_home():
    svc_cards = ""
    layout = ["span-3 tall", "span-3 tall", "span-2", "span-2", "span-2"]
    feature = SERVICES[:5]
    for i, s in enumerate(feature):
        cls = layout[i] if i < len(layout) else "span-2"
        svc_cards += f'''<article class="svc-card {cls} reveal">
        <div class="bg"><img src="assets/img/{s['img']}" alt="{s['title']} in Denton, TX" loading="lazy"></div>
        <div class="num">0{i+1}</div>
        <h3>{s['title']}</h3>
        <p>{s['short']}</p>
        <span class="textlink">Explore service {ICONS['arrow']}</span>
        <a class="full-link" href="service-{s['slug']}.html" aria-label="{s['title']}"></a>
      </article>'''

    props = [
        ("award", "Best of Denton, 6 years running", "Voted the area's best tree service 2020 through 2025 — and best specialty service on top of that."),
        ("shield", "Licensed, insured & A+ rated", "Fully licensed and insured with an A+ from the BBB, so the liability never lands on you."),
        ("leaf", "An ISA Certified Arborist on the crew", "Real diagnosis from someone trained in the science of trees — not a guess from a guy with a saw."),
        ("tag", "No hidden fees, ever", "We never charge for work you didn't authorize, and the bid you approve is the bid you pay."),
        ("users", "Military & senior discounts", "Real discounts for those who've served and for our senior neighbors across Denton County."),
        ("wind", "24/7 emergency response", "When a storm puts a tree on your roof at 2 a.m., the emergency line is answered."),
    ]
    prop_cards = ""
    for ic_name, h, p in props:
        prop_cards += f'''<div class="prop reveal"><div class="ico">{ICONS[ic_name]}</div><h3>{h}</h3><p>{p}</p></div>'''

    head_html = head(
        "Samuel's Tree Service | Denton Tree Removal, Trimming & Arborist — 940-595-3335",
        "Denton's Best of Denton tree service for 6 years running. ISA Certified Arborist, licensed & insured tree removal, trimming, stump grinding & 24/7 storm cleanup. Free estimates: 940-595-3335.",
        jsonld=LOCAL_BIZ_LD)

    return head_html + nav("home") + f'''
<main>
  <section class="hero">
    <div class="wrap-wide hero-inner">
      <div class="hero-grid">
        <div class="hero-copy">
          <span class="eyebrow no-rule lift">{ICONS['pin']} Denton + Corinth · Since {BIZ['founded']}</span>
          <h1 class="display"><span class="ln"><span class="l1">Climbed.</span></span><span class="ln"><span class="l2">Cut.</span></span><span class="ln"><span class="l3">Cleared.</span></span></h1>
          <p class="hero-sub lift s1">ISA Certified arborists, fully insured, and voted Best of Denton six years running. Free estimates, honest bids, and a 24/7 line when the storm doesn't wait.</p>
          <div class="hero-actions lift s2">
            <a class="btn btn-primary btn-lg" href="contact.html">Get a Free Estimate {ICONS['arrow']}</a>
            <a class="btn btn-ghost btn-lg" href="tel:{BIZ['tel']}">{ICONS['phone']} {BIZ['phone']}</a>
          </div>
          <div class="hero-meta lift s3">
            <div class="hm"><b><span data-years>24</span><span class="accent">+</span></b><span>Years in Denton</span></div>
            <div class="hm"><b>6<span class="accent">×</span></b><span>Best of Denton</span></div>
            <div class="hm">{status_badge()}</div>
          </div>
        </div>
        <div class="hero-figure lift s2">
          <div class="hero-card">
            <img src="assets/img/tree-removal.jpg" alt="Samuel's Tree Service crew performing a crane-assisted tree removal in Denton, Texas" fetchpriority="high" width="1000" height="739">
            <span class="hero-chip"><b>5.0 <span class="st">★</span></b><span>950+ Google reviews</span></span>
            <span class="tag">{ICONS['award']} Best of Denton · 6 years</span>
          </div>
        </div>
      </div>
    </div>
  </section>

  <div class="marquee" aria-hidden="true">
    <div class="marquee-track">
      {''.join(f'<span class="item">{ICONS["award"]} {a}</span>' for a in AWARDS)}
      <span class="item"><span class="star">{ICONS['star']}</span> 5.0 on Google</span>
      <span class="item">{ICONS['shield']} Licensed &amp; Insured</span>
      <span class="item">{ICONS['leaf']} ISA Certified Arborist</span>
      {''.join(f'<span class="item">{ICONS["award"]} {a}</span>' for a in AWARDS)}
      <span class="item"><span class="star">{ICONS['star']}</span> 5.0 on Google</span>
      <span class="item">{ICONS['shield']} Licensed &amp; Insured</span>
      <span class="item">{ICONS['leaf']} ISA Certified Arborist</span>
    </div>
  </div>

  <section>
    <div class="wrap">
      <div class="stats reveal">
        <div class="stat"><b data-count="24" data-years>24</b><div class="label">Years in business</div></div>
        <div class="stat"><b><span data-count="950">0</span><span class="accent">+</span></b><div class="label">Five-star reviews</div></div>
        <div class="stat"><b><span data-count="5" data-dec="1">0</span><span class="accent">★</span></b><div class="label">Average rating</div></div>
        <div class="stat"><b><span data-count="6">0</span><span class="accent">×</span></b><div class="label">Best of Denton '20–'25</div></div>
      </div>
    </div>
  </section>

  <section id="services">
    <div class="wrap">
      <div class="section-head reveal">
        <span class="eyebrow">What we do</span>
        <h2 class="section-title">Big trees, steady hands,<br>and the gear to match.</h2>
        <p>From a single hazardous limb to a crane-assisted takedown over your roofline — and everything a healthy landscape needs in between.</p>
      </div>
      <div class="svc-grid">{svc_cards}</div>
      <div class="reveal" style="margin-top:2rem"><a class="textlink" href="services.html">See all services {ICONS['arrow']}</a></div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="split">
        <div class="split-media reveal-clip">
          <img src="assets/img/team.jpg" alt="The Samuel's Tree Service team accepting a Best of Denton award" loading="lazy">
          <span class="tag">{ICONS['award']} Best of Denton 2024</span>
        </div>
        <div class="split-body">
          <span class="eyebrow reveal">Why Samuel's</span>
          <h2 class="reveal">Locally owned.<br>Nationally equipped.</h2>
          <p class="lead reveal">We've cared for Denton's trees since {BIZ['founded']} with one standard: complete honesty, integrity, and dependability — and a finished job site you'd never know we'd been on.</p>
          <ul class="checklist">
            <li class="reveal"><span class="ck">{ICONS['check']}</span><span><b>Quality, professional, affordable.</b> The three don't usually go together. We make them.</span></li>
            <li class="reveal"><span class="ck">{ICONS['check']}</span><span><b>No hidden fees.</b> We never charge for work you didn't authorize. The bid is the bill.</span></li>
            <li class="reveal"><span class="ck">{ICONS['check']}</span><span><b>We clean up like it's ours.</b> Debris chipped and hauled, yard left neat and tidy.</span></li>
          </ul>
          <div class="reveal"><a class="btn btn-ghost" href="about.html">More about us {ICONS['arrow']}</a></div>
        </div>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="section-head reveal">
        <span class="eyebrow">The difference</span>
        <h2 class="section-title">Six reasons Denton<br>keeps voting for us.</h2>
      </div>
      <div class="props">{prop_cards}</div>
    </div>
  </section>

  {reviews_section()}

  {cta_band()}
</main>
''' + footer() + SCRIPTS

# ================================================================ ABOUT
def page_about():
    head_html = head(
        "About Samuel's Tree Service | Denton's Best-of-Denton Tree Care Since 2002",
        "Locally owned and operated since 2002, Samuel's Tree Service brings ISA-certified, fully-insured tree care to Denton & Corinth — voted Best of Denton six years running. Honest bids, no hidden fees.",
        og_img="assets/img/team.jpg", jsonld=LOCAL_BIZ_LD)
    hero = page_hero(
        '<a href="index.html">Home</a><span class="sep">/</span><span>About</span>',
        "Two decades up<br>in Denton's trees.",
        f"Established in {BIZ['founded']}, locally owned and operated, and dedicated to one thing above all — our customers' satisfaction.",
        img="tree-trimming.jpg", alt="A Samuel's Tree Service climber working high in a tree canopy in Denton",
        tag=f"{ICONS['leaf']} ISA Certified")
    return head_html + nav("about") + f'''
<main>
  {hero}

  <section>
    <div class="wrap">
      <div class="split">
        <div class="split-body">
          <span class="eyebrow reveal">Our story</span>
          <h2 class="reveal">A standard we<br>won't cut.</h2>
          <p class="lead reveal">Samuel's Tree Service has served the greater Denton area for over <span data-years>24</span> years. In that time we've taken down trees of every size and scope — and built a reputation on doing it with complete honesty, integrity, and dependability.</p>
          <p class="reveal">Our promise is simple: quality, professional, affordable service with no surprises. We will never include hidden fees or charge you for work you did not authorize. That's why our customers have trusted us with their biggest, closest, most dangerous trees for two decades — and why Denton has voted us Best of Denton every year from 2020 through 2025.</p>
          <p class="reveal">We're locally owned and operated, but we carry the equipment and resources of a national operation. For you that means high-quality work that's also fast, friendly, and finished with a clean job site.</p>
        </div>
        <div class="split-media reveal-clip">
          <img src="assets/img/team.jpg" alt="The Samuel's Tree Service team with their Best of Denton 2024 award">
          <span class="tag">{ICONS['users']} The crew</span>
        </div>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="stats reveal">
        <div class="stat"><b data-years>24</b><div class="label">Years serving Denton</div></div>
        <div class="stat"><b><span data-count="950">0</span><span class="accent">+</span></b><div class="label">Five-star reviews</div></div>
        <div class="stat"><b>A<span class="accent">+</span></b><div class="label">BBB rating</div></div>
        <div class="stat"><b><span data-count="6">0</span><span class="accent">×</span></b><div class="label">Best of Denton</div></div>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="section-head reveal">
        <span class="eyebrow">What we stand on</span>
        <h2 class="section-title">Credentials you can<br>actually check.</h2>
      </div>
      <div class="props">
        <div class="prop reveal"><div class="ico">{ICONS['leaf']}</div><h3>ISA Certified Arborist</h3><p>Trained in the art and science of tree care — real diagnosis and honest recommendations, not guesswork.</p></div>
        <div class="prop reveal"><div class="ico">{ICONS['shield']}</div><h3>Fully Licensed &amp; Insured</h3><p>We take safety seriously and carry the coverage to back it, so your project is in capable hands.</p></div>
        <div class="prop reveal"><div class="ico">{ICONS['award']}</div><h3>BBB A+ &amp; Google Guaranteed</h3><p>An A+ rating with the Better Business Bureau and Google Guaranteed backing on the work we do.</p></div>
        <div class="prop reveal"><div class="ico">{ICONS['tag']}</div><h3>Competitive, Honest Pricing</h3><p>Free estimates, military and senior discounts, and a bid that never grows behind your back.</p></div>
        <div class="prop reveal"><div class="ico">{ICONS['wind']}</div><h3>24/7 Emergency Service</h3><p>Storms don't keep business hours. When a tree comes down on your property, we pick up.</p></div>
        <div class="prop reveal"><div class="ico">{ICONS['pin']}</div><h3>Local to Denton County</h3><p>Based in downtown Denton and serving Corinth and the surrounding communities we live in too.</p></div>
      </div>
    </div>
  </section>

  {reviews_section()}
  {cta_band()}
</main>
''' + footer() + SCRIPTS

# ================================================================ SERVICES HUB
def page_services():
    cards = ""
    for i, s in enumerate(SERVICES):
        cards += f'''<article class="svc-card span-2 reveal">
        <div class="bg"><img src="assets/img/{s['img']}" alt="{s['title']} in Denton, TX" loading="lazy"></div>
        <div class="num">0{i+1}</div>
        <h3>{s['title']}</h3>
        <p>{s['short']}</p>
        <span class="textlink">Explore service {ICONS['arrow']}</span>
        <a class="full-link" href="service-{s['slug']}.html" aria-label="{s['title']}"></a>
      </article>'''
    head_html = head(
        "Tree Services in Denton, TX | Removal, Trimming, Stump Grinding & More",
        "Full-service tree care in Denton & Corinth: tree removal, trimming & pruning, stump grinding, storm cleanup, certified arborist diagnosis, and deep root fertilization. Free estimates.",
        og_img="assets/img/tree-trimming.jpg", jsonld=LOCAL_BIZ_LD)
    hero = page_hero(
        '<a href="index.html">Home</a><span class="sep">/</span><span>Services</span>',
        "Everything a tree<br>could ask for.",
        "Six core services covering the whole life of your trees — from a careful pruning cut to a full crane-assisted removal and the cleanup after.",
        img="tree-removal-2.jpg", alt="Samuel's Tree Service truck and wood chipper on a Denton job site",
        tag=f"{ICONS['truck']} Locally owned fleet")
    return head_html + nav("services") + f'''
<main>
  {hero}

  <section>
    <div class="wrap">
      <div class="svc-grid">{cards}</div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="section-head reveal">
        <span class="eyebrow">How it goes</span>
        <h2 class="section-title">Four steps, no surprises.</h2>
        <p>The same straightforward process whether it's one limb or a whole stand of trees.</p>
      </div>
      <div class="steps">
        <div class="step reveal"><div class="n">01</div><h3>You call or request</h3><p>Tell us what you're looking at by phone or through the free-estimate form. Photos help.</p></div>
        <div class="step reveal d1"><div class="n">02</div><h3>We assess &amp; quote</h3><p>We look at the tree and the site, then give you a clear, written estimate — free, with no hidden fees.</p></div>
        <div class="step reveal d2"><div class="n">03</div><h3>We do the work</h3><p>Trained crews, proper gear, and respect for your property. We only do work you've authorized.</p></div>
        <div class="step reveal d3"><div class="n">04</div><h3>We clean up</h3><p>Debris chipped and hauled, the site left neat and tidy, and your remaining trees assessed.</p></div>
      </div>
    </div>
  </section>

  {cta_band()}
</main>
''' + footer() + SCRIPTS

# ================================================================ SERVICE DETAIL
def page_service(s):
    sections_html = ""
    for title, items in s["sections"]:
        lis = "".join(f'<li class="reveal">{it}</li>' for it in items)
        sections_html += f'<h2 class="reveal">{title}</h2><ul class="bullets">{lis}</ul>'
    reasons = "".join(f'<li class="reveal">{r}</li>' for r in s["reasons"])
    body = "".join(f'<p class="reveal">{p}</p>' for p in s["body"])
    others = [x for x in SERVICES if x["slug"] != s["slug"]][:3]
    other_cards = ""
    for o in others:
        other_cards += f'''<article class="svc-card span-2 reveal">
        <div class="bg"><img src="assets/img/{o['img']}" alt="{o['title']}" loading="lazy"></div>
        <h3>{o['title']}</h3><p>{o['short']}</p>
        <span class="textlink">Explore {ICONS['arrow']}</span>
        <a class="full-link" href="service-{o['slug']}.html" aria-label="{o['title']}"></a>
      </article>'''
    emergency = ""
    if s.get("emergency"):
        emergency = f'''<div class="aside-card" style="margin-top:1.2rem;border-color:rgba(143,209,79,.4)">
        <h4>{ICONS['bolt']} Storm emergency?</h4>
        <p style="font-size:.92rem;margin-bottom:1rem">Downed tree or hanging limb right now? Don't wait for a form.</p>
        <a class="btn btn-primary" href="tel:{BIZ['tel']}">{ICONS['phone']} Call {BIZ['phone']}</a>
      </div>'''

    svc_ld = {
        "@context": "https://schema.org", "@type": "Service",
        "serviceType": s["title"], "provider": {"@type": "LocalBusiness", "name": BIZ["legal"], "telephone": BIZ["phone"]},
        "areaServed": {"@type": "City", "name": "Denton"}, "description": s["short"],
    }
    head_html = head(
        f"{s['title']} in Denton, TX | Samuel's Tree Service — 940-595-3335",
        f"{s['short']} ISA Certified, licensed & insured, serving Denton & Corinth since 2002. Free estimates from Samuel's Tree Service.",
        og_img=f"assets/img/{s['img']}", jsonld=svc_ld)

    hero = page_hero(
        f'<a href="index.html">Home</a><span class="sep">/</span><a href="services.html">Services</a><span class="sep">/</span><span>{s["title"]}</span>',
        s['title'], s['hero_sub'],
        img=s['img'], alt=f"{s['title']} by Samuel's Tree Service in Denton, TX",
        tag=f"{ICONS[s['icon']]} {s['tag']}", eyebrow=s['tag'])
    return head_html + nav("services") + f'''
<main>
  {hero}

  <section>
    <div class="wrap layout-2col">
      <div class="prose">
        <p class="lead reveal">{s['lead']}</p>
        {sections_html}
        {body}
        <h2 class="reveal">{s['reasons_title']}</h2>
        <ul class="bullets">{reasons}</ul>
      </div>
      <div>
        <div class="aside-card reveal">
          <h4>Request this service</h4>
          <div class="ac-row"><span>Service area</span><b>{BIZ['area'].split(' & ')[0]}</b></div>
          <div class="ac-row"><span>Estimates</span><b>Free</b></div>
          <div class="ac-row"><span>Insured</span><b>Yes</b></div>
          <div class="ac-row"><span>Hours</span><b>Mon–Sat</b></div>
          {status_badge()}
          <a class="btn btn-primary" href="contact.html">Get a Free Estimate {ICONS['arrow']}</a>
          <a class="btn btn-ghost" style="width:100%;justify-content:center;margin-top:.6rem" href="tel:{BIZ['tel']}">{ICONS['phone']} {BIZ['phone']}</a>
        </div>
        {emergency}
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="section-head reveal"><span class="eyebrow">Keep exploring</span><h2 class="section-title">Other services</h2></div>
      <div class="svc-grid">{other_cards}</div>
    </div>
  </section>

  {cta_band()}
</main>
''' + footer() + SCRIPTS

# ================================================================ GALLERY
def page_gallery():
    photos = [
        ("beforeafter-1.jpg", "Crown thinning on a lakeside oak", "col-8", True),
        ("tree-removal.jpg", "Crane-assisted removal, Denton", "col-4 row-2", False),
        ("beforeafter-2.jpg", "Canopy raise over a two-story home", "col-4", True),
        ("storm-cleanup.jpg", "Storm-toppled oak across a driveway", "col-4", False),
        ("tree-trimming.jpg", "Climber pruning a mature canopy", "col-4", False),
        ("beforeafter-4.jpg", "Structural pruning, full property", "col-4", True),
        ("stump-grinding.jpg", "Stump ground below grade", "col-4", False),
        ("beforeafter-5.jpg", "Clearance pruning near the roofline", "col-4", True),
        ("tree-removal-2.jpg", "Removal & chipping in progress", "col-4", False),
        ("free-estimates.jpg", "On-site for a free estimate", "col-4", False),
        ("beforeafter-3.jpg", "Before & after on a backyard oak", "col-8", True),
        ("equipment.jpg", "The Samuel's Tree Service fleet", "col-4", False),
    ]
    items = ""
    for img, cap, cls, ba in photos:
        badge = f'<span class="ba">Before / After</span>' if ba else ''
        items += f'''<div class="gal-item {cls}" data-lightbox="assets/img/{img}" data-caption="{cap}" aria-label="View: {cap}">
        {badge}<img src="assets/img/{img}" alt="{cap}" loading="lazy"><span class="cap">{cap}</span>
      </div>'''
    head_html = head(
        "Past Work & Before/After Gallery | Samuel's Tree Service, Denton TX",
        "Real before-and-after photos and job sites from Samuel's Tree Service across Denton & Corinth — removals, crane work, pruning, stump grinding, and storm cleanup.",
        og_img="assets/img/beforeafter-1.jpg")
    return head_html + nav("gallery") + f'''
<main>
  <section class="page-hero">
    <div class="wrap-wide">
      <div class="crumbs reveal"><a href="index.html">Home</a><span class="sep">/</span><span>Past Work</span></div>
      <h1 class="reveal">The work speaks<br>for itself.</h1>
      <p class="reveal">Real trees, real Denton-area properties, real before-and-afters. Tap any photo to see it full size.</p>
    </div>
  </section>

  <section style="padding-top:0">
    <div class="wrap-wide">
      <div class="gallery-grid reveal">{items}</div>
    </div>
  </section>

  {reviews_section()}
  {cta_band()}
</main>
''' + footer() + SCRIPTS

# ================================================================ CONTACT
def page_contact():
    svc_options = "".join(f'<option value="{s["title"]}">{s["title"]}</option>' for s in SERVICES)
    head_html = head(
        "Contact & Free Estimates | Samuel's Tree Service, Denton TX — 940-595-3335",
        "Request a free tree-service estimate in Denton or Corinth. Call 940-595-3335, visit us at 405 S Elm St, or send the quick form. 24/7 emergency response available.",
        og_img="assets/img/free-estimates.jpg", jsonld=LOCAL_BIZ_LD)
    return head_html + nav("contact") + f'''
<main>
  <section class="page-hero">
    <div class="wrap-wide">
      <div class="crumbs reveal"><a href="index.html">Home</a><span class="sep">/</span><span>Contact</span></div>
      <h1 class="reveal">Get a free<br>estimate.</h1>
      <p class="reveal">Tell us what you're looking at. We'll come take a look and give you a straight, written bid — no pressure, no hidden fees.</p>
    </div>
  </section>

  <section style="padding-top:1rem">
    <div class="wrap layout-2col">
      <div class="form-card reveal">
        <form data-quote-form novalidate>
          <div class="field-row">
            <div class="field"><label for="name">Name</label><input id="name" name="name" type="text" required autocomplete="name"></div>
            <div class="field"><label for="phone">Phone</label><input id="phone" name="phone" type="tel" required autocomplete="tel"></div>
          </div>
          <div class="field-row">
            <div class="field"><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email"></div>
            <div class="field"><label for="zip">Property city / ZIP</label><input id="zip" name="zip" type="text" autocomplete="postal-code"></div>
          </div>
          <div class="field"><label for="service">What do you need?</label>
            <select id="service" name="service"><option value="">Select a service…</option>{svc_options}<option value="Not sure">Not sure — please advise</option></select>
          </div>
          <div class="field"><label for="message">Tell us about the tree(s)</label><textarea id="message" name="message" placeholder="Size, location, what you're seeing, anything urgent…"></textarea></div>
          <button class="btn btn-primary btn-lg" type="submit" style="width:100%;justify-content:center">Request my free estimate {ICONS['arrow']}</button>
          <p class="form-note">This form is for estimate requests only. For a tree down right now, call {BIZ['phone']} — our 24/7 emergency line.</p>
        </form>
        <div class="form-success">
          <div class="sc-ico">{ICONS['check']}</div>
          <h3>Request received.</h3>
          <p>Thanks — we'll be in touch shortly to set up your free estimate. For anything urgent, call {BIZ['phone']}.</p>
        </div>
      </div>

      <div>
        <div class="contact-rows">
          <div class="crow reveal"><div class="ci">{ICONS['phone']}</div><div><b>Call / Text</b><a href="tel:{BIZ['tel']}">{BIZ['phone']}</a></div></div>
          <div class="crow reveal"><div class="ci">{ICONS['pin']}</div><div><b>Visit</b><p>{BIZ['addr']}<br>{BIZ['city']}</p></div></div>
          <div class="crow reveal"><div class="ci">{ICONS['star']}</div><div><b>Reviews</b><a href="{BIZ['google']}" target="_blank" rel="noopener">Read 950+ on Google</a></div></div>
          <div class="crow reveal"><div class="ci">{ICONS['clock']}</div><div style="width:100%"><b>Hours</b>
            <table class="hours-table" data-hours>
              <tr data-day="1"><td>Monday</td><td>8:00 AM – 7:00 PM</td></tr>
              <tr data-day="2"><td>Tuesday</td><td>8:00 AM – 7:00 PM</td></tr>
              <tr data-day="3"><td>Wednesday</td><td>8:00 AM – 7:00 PM</td></tr>
              <tr data-day="4"><td>Thursday</td><td>8:00 AM – 7:00 PM</td></tr>
              <tr data-day="5"><td>Friday</td><td>8:00 AM – 7:00 PM</td></tr>
              <tr data-day="6"><td>Saturday</td><td>9:00 AM – 2:00 PM</td></tr>
              <tr data-day="0"><td>Sunday</td><td>Closed</td></tr>
            </table>
            <div style="margin-top:1rem">{status_badge()}</div>
            <p style="font-size:.85rem;color:var(--muted);margin-top:.8rem">24/7 emergency response available outside posted hours.</p>
          </div></div>
        </div>
      </div>
    </div>
  </section>
</main>
''' + footer() + SCRIPTS

# ---------------------------------------------------------------- build
write("index.html", page_home())
write("about.html", page_about())
write("services.html", page_services())
for s in SERVICES:
    write(f"service-{s['slug']}.html", page_service(s))
write("gallery.html", page_gallery())
write("contact.html", page_contact())
print("done.")
