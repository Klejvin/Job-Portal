from django.contrib import admin
from .models import*
from django.db.models import Q
# Register your models here.


admin.site.register(Partner)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title','author' ,'partner', 'created_at')

    # TI (Superuser) sheh gjithçka, PARTNERI sheh vetëm punët e tij
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Filtrojmë që partneri të shohë vetëm punët ku 'partner__user' është ai vetë
        return qs.filter(
            Q(author=request.user) | Q(partner__user=request.user)
        ).distinct()

    # Kur Partneri shton një punë, sistemi e lidh automatikisht me kompaninë e tij
    def save_model(self, request, obj, form, change):
        # Kur ruhet puna, vendosim automatikisht author-in
        if not obj.pk:  # Vetëm kur krijohet për herë të parë
            obj.author = request.user
            
        # Nëse ky user ka një profil partneri, e lidhim automatikisht
        partner_profile = getattr(request.user, 'partner_profile', None)
        if partner_profile and not request.user.is_superuser:
            obj.partner = partner_profile
            
        super().save_model(request, obj, form, change)

    
    def get_list_display(self, request):
        # Nëse përdoruesi NUK je ti, i shfaqim vetëm Titullin dhe Datën
        if not request.user.is_superuser:
            return ('title', 'created_at')
        return self.list_display

    # Partneri nuk ka pse ta zgjedhë kompaninë (sepse është e tij), ia fshehim si fushë
    def get_fields(self, request, obj=None):
        fields = list(super().get_fields(request, obj))
        if not request.user.is_superuser:
            # Fshehim fushat që plotësohen automatikisht që mos t'i ndryshojë useri
            if 'partner' in fields: fields.remove('partner')
            if 'author' in fields: fields.remove('author')
        return fields
    

@admin.register(Aplikim)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'get_job_title', 'get_partner', 'created_at')
    
    def get_job_title(self, obj):
        return obj.job.title
    get_job_title.short_description = "Pozicioni"

    def get_partner(self, obj):
        # 1. Provo të marrësh emrin nga modeli Partner
        if obj.job.partner:
            return obj.job.partner.emri_kompanise
        # 2. Nëse nuk ka Partner, provo fushën 'company' te modeli Job
        return getattr(obj.job, 'company', 'Pa Kompani')
    get_partner.short_description = "Kompania"
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        # Nëse është Superuser, i sheh të gjitha
        if request.user.is_superuser:
            return qs
        
        # Nëse është Partner, sheh aplikimet ku:
        # Puna -> ka si Partner -> profilin e këtij User-i
        return qs.filter(job__partner__user=request.user)