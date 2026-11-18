"""
sitemap.xml and robots.txt for echoesofnature.co.in

Place at: eon/eonapp/seo.py
No settings.py change needed (does not use django.contrib.sitemaps).
"""
from datetime import date

from xml.sax.saxutils import escape

from django.apps import apps
from django.http import HttpResponse
from django.urls import NoReverseMatch, reverse

SITE = "https://echoesofnature.co.in"

# url name -> (priority, changefreq)
PAGES = {
    "home": ("1.0", "monthly"),
    "Deepdive": ("0.9", "monthly"),
    "birds_list": ("0.9", "monthly"),
    "butterfly_list": ("0.9", "monthly"),
    "flora_list": ("0.9", "monthly"),
    "Naturetrail": ("0.8", "monthly"),
    "Birdwatching": ("0.8", "monthly"),
    "Urbanlegends": ("0.8", "monthly"),
    "Disclaimer": ("0.2", "yearly"),
    "Terms": ("0.2", "yearly"),
    "Privacy": ("0.2", "yearly"),
    "Credits": ("0.2", "yearly"),
}


# Species detail pages: (field that identifies the model, url name, attribute used in the url)
SPECIES = [
    ("Bird_Name", "bird_detail", "slug"),
    ("Butterfly_Name", "butterfly_detail", "slug"),
    ("Flora_Name", "flora_detail", "id"),
]


def _url_entry(path, today, freq, priority):
    return (
        f"  <url>\n"
        f"    <loc>{SITE}{escape(path)}</loc>\n"
        f"    <lastmod>{today}</lastmod>\n"
        f"    <changefreq>{freq}</changefreq>\n"
        f"    <priority>{priority}</priority>\n"
        f"  </url>"
    )


def _species_paths():
    """Yield detail-page paths for every bird, butterfly and plant in the database.
    Models are found by their field names, so no model imports are needed."""
    try:
        models = list(apps.get_app_config("eonapp").get_models())
    except LookupError:
        return
    for field, url_name, attr in SPECIES:
        for model in models:
            if field not in {f.name for f in model._meta.get_fields()}:
                continue
            try:
                for obj in model.objects.all().only("pk", *([attr] if attr != "id" else [])):
                    value = getattr(obj, attr, None)
                    if value:
                        try:
                            yield reverse(url_name, args=[value])
                        except NoReverseMatch:
                            break
            except Exception:
                pass  # never let one bad table break the sitemap


def sitemap_xml(request):
    today = date.today().isoformat()
    urls = []
    for name, (priority, freq) in PAGES.items():
        try:
            path = reverse(name)
        except NoReverseMatch:
            continue  # skip any name that doesn't exist instead of crashing
        urls.append(_url_entry(path, today, freq, priority))
    for path in _species_paths():
        urls.append(_url_entry(path, today, "monthly", "0.7"))
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )
    return HttpResponse(xml, content_type="application/xml")


def robots_txt(request):
    body = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /admin/\n"
        "\n"
        f"Sitemap: {SITE}/sitemap.xml\n"
    )
    return HttpResponse(body, content_type="text/plain")
