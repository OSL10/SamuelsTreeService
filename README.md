# Samuel's Tree Service

Multi-page marketing site for Samuel's Tree Service, LLC — Denton, TX.

Static HTML/CSS/JS. All 11 pages are generated from `generate.py` using shared
head/nav/footer templates and a real-data-only Client Brief (no invented
statistics, testimonials, or years-in-business — sourced from the live site,
Google Business Profile, and the client's own photo library).

## Structure

```
.
├── index.html               # home
├── about.html
├── services.html            # services hub
├── service-*.html           # 6 dedicated service pages
├── gallery.html             # past work / before-and-after
├── contact.html             # free-estimate form
├── generate.py              # site generator
└── assets/
    ├── css/styles.css
    ├── js/main.js
    └── img/                 # real client photos
```

## Regenerate

```bash
python3 generate.py
```

Overwrites the HTML files from `generate.py`. Edit templates there, not the
compiled pages.

## Local preview

```bash
npx serve . -l 5196
# then open http://localhost:5196
```

## Design signature

One cohesive motion system across the whole site:

- Native View Transitions API for cross-page fades
- Lenis smooth scroll, synced to
- GSAP ScrollTrigger for reveal batches + subtle hero-card parallax
- Live Open/Closed badge driven from real business hours (`aria-live="polite"`)
- Years-in-business counter auto-computed from founding year (2002), so it
  never goes stale

## Real-business facts (do not edit without source)

- Phone: 940-595-3335
- Address: 405 S Elm St. Ste. 303, Denton, TX 76201
- Hours: Mon–Fri 8–7, Sat 9–2, 24/7 emergency
- Founded: 2002
- Reviews: 950+ / 5.0★ Google
- Awards: Best of Denton 2020–2025
