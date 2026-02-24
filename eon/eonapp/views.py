from django.shortcuts import render, get_object_or_404
from django.db.models import FloatField, Value
from django.db.models import F
from django.utils.timezone import localdate
from django.db.models.functions import Cast, Substr, StrIndex, Trim
from .models import Bird,Flora,Story,NatureTrailSchedule, NatureTrailMedia

def home(request):
    return render(request, "home.html")

def birds_list(request):
    birds = Bird.objects.all()

    active_time = request.GET.get('activeTime')
    diet = request.GET.get('diet')
    migration = request.GET.get('migration')
    sort = request.GET.get('sort') or "az"

    if active_time:
        birds = birds.filter(Bird_Active_Time_Key__icontains=active_time)

    if diet:
        birds = birds.filter(Bird_Diet_Key__icontains=diet)

    if migration:
        birds = birds.filter(Bird_Migration_Key__iexact=migration)


    if sort == "az":
        birds = birds.order_by("Bird_Name")

    elif sort == "za":
        birds = birds.order_by("-Bird_Name")

    elif sort in ["small", "large"]:
        birds = birds.annotate(
            dash_pos=StrIndex('Bird_Weight', Value('-'))
        ).annotate(
            weight_text=Substr('Bird_Weight', 1, F('dash_pos') - 1)
        ).annotate(
            weight_clean=Trim('weight_text')
        ).annotate(
            weight_num=Cast('weight_clean', FloatField())
        )

        birds = birds.order_by(
            'weight_num' if sort == "small" else '-weight_num'
        )

    return render(request, "Birds_list.html", {"birds": birds})



def bird_detail(request, slug):
    bird = get_object_or_404(Bird, slug=slug)
    return render(request, "Bird_Main.html", {
        "bird": bird,
        "svg_status": bird.Bird_Conservation_Status_SVGKey,
        "geo_range": bird.Bird_Zones,
    })



def flora_list(request):
    floras = Flora.objects.all()

    flora_type = request.GET.get('flora_type')      # ✅ FIXED
    flora_origin = request.GET.get('flora_origin')  # ✅ ADD THIS
    sort = request.GET.get('sort')

    # FILTERS
    if flora_type:
        floras = floras.filter(Flora_Type_Key=flora_type)

    if flora_origin:
        floras = floras.filter(Flora_Origin=flora_origin)

    # SORT
    if sort == "za":
        floras = floras.order_by("-Flora_Name")
        active_sort = "za"
    else:
        floras = floras.order_by("Flora_Name")
        active_sort = "az"

    return render(request, "flora_list.html", {
        "floras": floras,
        "active_sort": active_sort
    })



def flora_detail(request, flora_id):
    flora = get_object_or_404(Flora, id=flora_id)
    return render(request, "flora_detail.html", {
        "flora": flora,
        "svg_status": flora.Flora_Conservation_Status_SVGKey,  # <-- IMPORTANT
        "geo_range": flora.Flora_Zones,
    })

def Deepdive(request):
    return render(request, "Deepdive.html")

def bird_gallery(request, bird_id):
    bird = get_object_or_404(Bird, id=bird_id)
    return render(request, 'gallery.html', {'bird': bird})


def flora_gallery(request, flora_id):
    flora = get_object_or_404(Flora, id=flora_id)
    return render(request, 'gallery.html', {'flora': flora})

from collections import defaultdict

def Birdwatching(request):
    birds = Bird.objects.all()
    birds_by_area = defaultdict(list)

    for bird in birds:
        if not bird.Bird_Sighting_Area:
            continue

        # Split multiple areas
        areas = bird.Bird_Sighting_Area.split(",")

        for area in areas:
            normalized_area = area.strip().upper()
            birds_by_area[normalized_area].append(bird)

    spots = [
        {"id": 1, "name": "KAVESAR LAKE", "image": "img/Spot1.png"},
        {"id": 2, "name": "CENTRAL PARK", "image": "img/Spot2.png"},
        {"id": 3, "name": "NURSERY", "image": "img/Spot3.png"},
        {"id": 4, "name": "GARDEN", "image": "img/Spot4.png"},
    ]

    return render(request, "Birdwatching.html", {
        "spots": spots,
        "birds_by_area": birds_by_area
    })





from django.utils.timezone import localdate

def Naturetrail(request):
    schedules = NatureTrailSchedule.objects.filter(
        date__gte=localdate()
    )

    media = NatureTrailMedia.objects.filter(is_active=True)

    return render(request, "Naturetrail.html", {
        "schedules": schedules,
        "media": media,
    })
def MDGallery(request):
    return render(request, 'gallery2.html')


def Urbanlegends(request):
    stories = Story.objects.all()
    return render(request, 'Urbanlegends.html', {"stories": stories})

def Gallery(request):
    return render(request,'gallery.html')

def Credits(request):
    return render(request,'Credits.html')

def Disclaimer(request):
    return render(request,'Disclaimer.html')

def Privacy(request):
    return render(request,'Privacy.html')
def Terms(request):
    return render(request,'Terms.html')

from django.http import HttpResponse
import subprocess
import os
import sys

def exit_kiosk(request):
    # Kill Chrome
    subprocess.run(['taskkill', '/IM', 'chrome.exe', '/F'], 
                   stdout=subprocess.DEVNULL, 
                   stderr=subprocess.DEVNULL)
    
    # Return response first
    response = HttpResponse("""
        <html><body style='background:#000;color:#0f0;font-family:monospace;
        display:flex;align-items:center;justify-content:center;height:100vh;
        font-size:48px'>
        KIOSK EXITING...
        </body></html>
    """)
    
    # Kill Django server after short delay (in a thread)
    import threading
    def shutdown():
        import time
        time.sleep(1)
        subprocess.run(['taskkill', '/IM', 'python.exe', '/F'],
                       stdout=subprocess.DEVNULL, 
                       stderr=subprocess.DEVNULL)
    
    threading.Thread(target=shutdown, daemon=True).start()
    
    return response 


