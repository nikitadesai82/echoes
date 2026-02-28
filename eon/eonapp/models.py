from django.db import models
from django.utils.text import slugify


class Bird(models.Model):
    Bird_Scientific_Name = models.CharField(max_length=255)
    Bird_Name = models.CharField(max_length=255)
    Bird_AKA = models.TextField()
    Bird_Sub_Species = models.TextField()
    Bird_Sub_Species_Details = models.TextField()
    Bird_Family = models.CharField(max_length=255)
    Bird_Wingspan = models.CharField(max_length=50)
    Bird_Wingspan_Details = models.TextField(blank=True, null=True)
    Bird_Length = models.CharField(max_length=50)
    Bird_Length_Details = models.TextField(blank=True, null=True)
    Bird_Weight = models.CharField(max_length=50)
    Bird_Weight_Details = models.TextField(blank=True, null=True)
    Bird_Lifespan = models.CharField(max_length=50)
    Bird_Lifespan_Details = models.TextField(blank=True, null=True)
    Bird_Geographic_Range = models.TextField()
    Bird_Zones = models.TextField()
    Bird_Animation = models.FileField(upload_to="Animations/Birds/Single Birds/",blank=True, null=True)
    Bird_Conservation_Status = models.CharField(max_length=20)
    Bird_Conservation_Status_SVGKey = models.CharField(max_length=255)
    Bird_Call = models.FileField(upload_to="Audio/Bird_Calls/",blank=True,null=True)
    Bird_Image1 = models.ImageField(upload_to="Images/Birds/", blank=True, null=True)
    Bird_Video  = models.FileField(upload_to="Videos/Birds/", blank=True, null=True)
    Bird_Poster = models.ImageField(upload_to="Videos/Posters", blank=True, null=True)
    Bird_Sighting_Area = models.TextField()
    Bird_Active_Time = models.TextField()
    Bird_Fun_Facts = models.TextField()
    
    Bird_Migration = models.TextField()
    Bird_Habitat = models.TextField()
    Bird_Nesting = models.TextField()
    Bird_Feeding_Behaviour = models.TextField()
    Bird_Plumange = models.TextField()
    Bird_Diet_Key = models.CharField(max_length=100)
    Bird_Active_Time_Key = models.CharField(max_length=100)
    Bird_Migration_Key = models.CharField(max_length=100)
    BirdAt_HoHStatus = models.CharField(max_length=100)
    Bird_Button_Media = models.FileField(upload_to="Animations/Birds/Buttons/",blank=True, null=True)
    Bird_Button_Thumb = models.FileField(upload_to="Animations/Birds/Single Birds/",blank=True, null=True)
    Bird_Videolink = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
		
    Bird_Quiz_Question = models.TextField(null=True, blank=True)
    Bird_Quiz_OptionA = models.CharField(max_length=255, null=True, blank=True)
    Bird_Quiz_OptionB = models.CharField(max_length=255, null=True, blank=True)
    Bird_Quiz_OptionC = models.CharField(max_length=255, null=True, blank=True)
    Bird_Quiz_OptionD = models.CharField(max_length=255, null=True, blank=True)
    Bird_Quiz_Correct = models.CharField(max_length=1, choices=[
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ], null=True, blank=True)
    
    slug = models.SlugField(blank=True, null=True)

    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.Bird_Name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.Bird_Name


class Flora(models.Model):
    Flora_Botanical_Name = models.CharField(max_length=200)
    Flora_Name = models.CharField(max_length=200)
    Flora_AKA = models.CharField(max_length=300, blank=True, null=True)
    Flora_Family = models.CharField(max_length=200, blank=True, null=True)
    Flora_Origin = models.CharField(max_length=200, blank=True, null=True)
    Flora_Geo_Range = models.TextField(blank=True, null=True)
    Flora_Zones = models.CharField(max_length=200, blank=True, null=True)
    Flora_Habitat = models.TextField(blank=True, null=True)

    Flora_Media_1 = models.FileField(upload_to="Animations/Flora/Single Plants/",blank=True, null=True)
    Flora_Media_2 = models.ImageField(upload_to="Images/Illustrations/Trees/", blank=True, null=True)

    Flora_Height = models.CharField(max_length=50, blank=True, null=True)
    Flora_Height_Details = models.TextField(blank=True, null=True)

    Flora_Image_1 = models.ImageField(upload_to="Images/Flora/", blank=True, null=True)
    Flora_Image_2 = models.ImageField(upload_to="Images/Flora/", blank=True, null=True)
    Flora_Image_3 = models.ImageField(upload_to="Images/Flora/", blank=True, null=True)



    Flora_Conservation_Status = models.CharField(max_length=100, blank=True, null=True)
    Flora_Conservation_Status_SVGKey = models.CharField(max_length=100, blank=True, null=True)

    Flora_Description = models.TextField(blank=True, null=True)
    Flora_Fun_Facts = models.TextField(blank=True, null=True)
    Flora_Ecological = models.TextField(blank=True, null=True)
    Flora_Medicinal = models.TextField(blank=True, null=True)
    Flora_Culinary = models.TextField(blank=True, null=True)
    Flora_Cultural = models.TextField(blank=True, null=True)
    Flora_Parts = models.TextField(blank=True, null=True)
    Flora_Question = models.TextField(blank=True, null=True)

    Flora_Button_Media = models.FileField(upload_to="Animations/Flora/Buttons/",blank=True, null=True)

    Flora_Flowering_Key = models.CharField(max_length=100, blank=True, null=True)
    Flora_Type_Key = models.CharField(max_length=100, blank=True, null=True)
    Flora_HoHLocation = models.CharField(max_length=100, blank=True, null=True)
    Flora_Marathi_name = models.CharField(max_length=200, blank=True, null=True)

    Flora_Quiz_Question = models.TextField(null=True, blank=True)
    Flora_Quiz_OptionA = models.CharField(max_length=255, null=True, blank=True)
    Flora_Quiz_OptionB = models.CharField(max_length=255, null=True, blank=True)
    Flora_Quiz_OptionC = models.CharField(max_length=255, null=True, blank=True)
    Flora_Quiz_OptionD = models.CharField(max_length=255, null=True, blank=True)
    Flora_Quiz_Correct = models.CharField(max_length=1, choices=[
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ], null=True, blank=True)

    def __str__(self):
        return self.Flora_Name


class Story(models.Model):
    Story_Title = models.CharField(max_length=200)
    Story_text = models.TextField()
    Story_Audio = models.FileField(upload_to='story_audio/', blank=True, null=True)
    Story_Image = models.ImageField(upload_to='story_images/', blank=True, null=True)

    def __str__(self):
        return self.Story_Title

class NatureTrailSchedule(models.Model):
    day = models.CharField(max_length=10, blank=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ['date', 'start_time']

    def save(self, *args, **kwargs):
        if self.date:
            self.day = self.date.strftime("%A")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.day} - {self.date}"

class NatureTrailMedia(models.Model):
    IMAGE = 'image'
    VIDEO = 'video'

    MEDIA_TYPE_CHOICES = [
        (IMAGE, 'Image'),
        (VIDEO, 'Video'),
    ]

    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    file = models.FileField(upload_to='nature_trails/media/')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
