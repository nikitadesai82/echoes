"""
sitemap.xml and robots.txt for echoesofnature.co.in

Place at: eon/eonapp/seo.py
No settings.py change needed (does not use django.contrib.sitemaps).
"""
from datetime import date

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


def sitemap_xml(request):
    today = date.today().isoformat()
    urls = []
    for name, (priority, freq) in PAGES.items():
        try:
            path = reverse(name)
        except NoReverseMatch:
            continue  # skip any name that doesn't exist instead of crashing
        urls.append(
            f"  <url>\n"
            f"    <loc>{SITE}{path}</loc>\n"
            f"    <lastmod>{today}</lastmod>\n"
            f"    <changefreq>{freq}</changefreq>\n"
            f"    <priority>{priority}</priority>\n"
            f"  </url>"
        )
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
