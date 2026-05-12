from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.

class Partner(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='partner_profile',
        verbose_name="Llogaria e Partnerit"
    )
    emri_kompanise = models.CharField(max_length=200, verbose_name="Emri i Kompanisë")
    logo = models.ImageField(upload_to='partners/', verbose_name="Logoja")
    website_url = models.URLField(blank=True, null=True, verbose_name="Linku i Website-it")
    data_shtimit = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Partner"
        verbose_name_plural = "Partnerët Tanë"

    def __str__(self):
        return self.emri_kompanise
    
    
class Job(models.Model):
    CITY_CHOICES = [
        ('Tiranë', 'Tiranë'),
        ('Durrës', 'Durrës'),
        ('Vlorë', 'Vlorë'),
        ('Shkodër', 'Shkodër'),
        ('Fier', 'Fier'),
        ('Korçë', 'Korçë'),
        ('Elbasan', 'Elbasan'),
        ('Berat', 'Berat'),
        ('Lushnjë', 'Lushnjë'),
        ('Kavajë', 'Kavajë'),
        ('Gjirokastër', 'Gjirokastër'),
        ('Sarandë', 'Sarandë'),
        ('Lezhë', 'Lezhë'),
        ('Kukës', 'Kukës'),
    ]

    # Shto fushat e punës këtu
    CATEGORY_CHOICES = [
        ('Informatikë', 'Informatikë / Teknologji'),
        ('Ekonomi', 'Ekonomi / Financë'),
        ('Marketing', 'Marketing / Shitje'),
        ('Administratë', 'Administratë / Zyrat'),
        ('Inxhinieri', 'Inxhinieri'),
        ('Mjekësi', 'Mjekësi / Shëndetësi'),
        ('Arsim', 'Arsim / Shkencë'),
        ('Turizëm', 'Turizëm / Hoteleri'),
        ('Ndërtim', 'Ndërtim'),
        ('Tjetër', 'Tjetër'),
    ]

    partner = models.ForeignKey('Partner', on_delete=models.CASCADE, related_name='jobs', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=100)
    salary = models.CharField(max_length=100)
    conditions = models.CharField(max_length=100)
    
    location = models.CharField(max_length=100, choices=CITY_CHOICES, default='Tiranë') 
    
    # Fusha e re për kategorinë
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='Informatikë')
    
    location_link = models.URLField(max_length=500, blank=True, null=True) 
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.category}) - {self.location}"
    

class Aplikim(models.Model):
    # Lidhja me punën
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    # Të dhënat personale (nga forma e aplikimit)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, null=True, blank=True) # E shtuar nga CV
    
    # Të dhënat e CV-së (të bashkuara këtu)
    skills = models.TextField(null=True, blank=True)
    experience = models.TextField(null=True, blank=True)
    education = models.TextField(null=True, blank=True)
    projects = models.TextField(null=True, blank=True)
    
    # Opsioni për të ngarkuar edhe një dokument fizik
    cv_file = models.FileField(upload_to='cv_uploads/', null=True, blank=True)
    
    description = models.TextField(verbose_name="Pse jeni ju kandidati i duhur?")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Aplikim"
        verbose_name_plural = "Aplikime"

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.job.title}"
    



class CV(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='cv', 
        verbose_name="Përdoruesi"
    )
    phone = models.CharField(max_length=20, null=True, blank=True)
    languages = models.CharField(max_length=200, null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    experience = models.TextField(null=True, blank=True)
    education = models.TextField(null=True, blank=True)
    projects = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "CV Përdoruesi"
        verbose_name_plural = "CV-të e Përdoruesve"

    def __str__(self):
        return f"CV e {self.user.username}"