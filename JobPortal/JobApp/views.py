from django.shortcuts import render, redirect , get_object_or_404
from .models import *
from django.core.mail import EmailMessage
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import re
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .forms import JobForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


# Create your views here.
def home(request):
    latest_jobs = Job.objects.all().order_by('-id')[:6] 
    return render(request, 'home.html', {'latest_jobs': latest_jobs})

def navbar(request):
    return render(request,"navbar.html")

def base(request):
    return render(request,"base.html")
    

def footer(request):
    return render(request,"footer.html")



def pune(request):
    jobs = Job.objects.all().order_by('-created_at') 
    return render(request, "pune.html", {'jobs': jobs})

def rrethnesh(request):
    return render(request,"rrethnesh.html")

def pyetje(request):
    return render(request,"pyetje.html")

def partneret(request):
    partneret_nga_db = Partner.objects.all().order_by('-id') 
    
    return render(request, 'partneret.html', {
        'partneret': partneret_nga_db  
    })

def behu_partner(request):
    if request.method == 'POST':
        emri_kompanise = request.POST.get('emri_kompanise')
        emer_mbiemer = request.POST.get('emer_mbiemer')
        email_klientit = request.POST.get('email')
        pershkrimi = request.POST.get('pershkrimi')
        logo_file = request.FILES.get('logo')
        subjekti = f"Aplikim i ri për Partneritet: {emri_kompanise}"
        permbajtja = (
            f"Detajet e Aplikimit:\n"
            f"--------------------------\n"
            f"Kompania: {emri_kompanise}\n"
            f"Personi Kontaktues: {emer_mbiemer}\n"
            f"Email: {email_klientit}\n\n"
            f"Përshkrimi:\n{pershkrimi}"
        )
        email = EmailMessage(
            subject=subjekti,
            body=permbajtja,
            from_email='noreply@jobportal.al', 
            to=['admin-email@email.com'], 
            reply_to=[email_klientit]
        )
        if logo_file:
            email.attach(logo_file.name, logo_file.read(), logo_file.content_type)
        try:
            email.send()
            messages.success(request, "Kërkesa u dërgua me sukses! Do t'ju kontaktojmë së shpejti.")
            return redirect('homePage') 
        except Exception as e:
            print(f"Gabimi: {e}")
            messages.error(request, "Pati një gabim gjatë dërgimit. Provoni përsëri.")

    return render(request, 'behu_partner.html')

def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(request, 'details.html', {'job': job})


def loginPage(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('/admin/')
        return redirect('homePage')
    
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        
        user = authenticate(request, username=u, password=p)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Mirëseerdhe, {user.username}!")
            
            if user.is_superuser:
                return redirect('/admin/') 
            else:
                return redirect('homePage') 
        else:
            messages.error(request, "Username ose Password i pasaktë.")
            
    return render(request, 'login.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('homePage')

    if request.method == 'POST':
        fname = request.POST.get('firstName')
        lname = request.POST.get('lastName')
        uname = request.POST.get('username')
        email = request.POST.get('email')
        p1 = request.POST.get('password')
        p2 = request.POST.get('confirm_password')

       
        context = {
            'fname': fname,
            'lname': lname,
            'uname': uname,
            'email': email,
        }

        
        if len(p1) < 8:
            messages.error(request, "Fjalëkalimi duhet të jetë të paktën 8 karaktere.")
            return render(request, 'register.html', context)
        
        
        elif not re.search(r'[A-Z]', p1):
            messages.error(request, "Fjalëkalimi duhet të përmbajë të paktën një shkronjë të madhe.")
            return render(request, 'register.html', context)
        
        
        elif not re.search(r'[0-9]', p1):
            messages.error(request, "Fjalëkalimi duhet të përmbajë të paktën një numër.")
            return render(request, 'register.html', context)
        
        
        elif p1 != p2:
            messages.error(request, "Fjalëkalimet nuk përputhen!")
            return render(request, 'register.html', context)
        
        
        elif User.objects.filter(username=uname).exists():
            messages.error(request, "Ky username është i zënë.")
            return render(request, 'register.html', context)

       
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Ky email është përdorur njëherë.")
            return render(request, 'register.html', context)
            
        else:
            
            user = User.objects.create_user(uname, email, p1)
            user.first_name = fname
            user.last_name = lname
            user.save()
            messages.success(request, "Llogaria u krijua! Po ju ridrejtojmë...")
            return render(request, 'login.html', {'registration_success': True})

    return render(request, 'register.html')


def logoutUser(request):
    storage = messages.get_messages(request)
    for message in storage:
        pass
    
    logout(request)
    messages.success(request, "U çloguat me sukses.") 
    return redirect('loginPage')



@login_required
def my_jobs(request):
    jobs = Job.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'my_jobs.html', {'jobs': jobs})

@login_required
def add_job_custom(request):
    
    my_jobs = Job.objects.filter(author=request.user).order_by('-created_at')
    
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.author = request.user  
            job.save()
            messages.success(request, "Puna u publikua me sukses!")
            return redirect('add_job_custom')
    else:
        form = JobForm()
    
    return render(request, 'add_job.html', {
        'form': form, 
        'jobs': my_jobs 
    })

def edit_job(request, pk):
    job = get_object_or_404(Job, pk=pk, author=request.user)
    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            
            
            return redirect('add_job_custom') 
    else:
        form = JobForm(instance=job)
    
    return render(request, 'add_job.html', {
        'form': form, 
        'edit_mode': True 
    })

@login_required
def delete_job(request, pk):
    job = get_object_or_404(Job, pk=pk) 
    
    
    if job.author != request.user and not request.user.is_superuser:
        messages.error(request, "Nuk keni leje të fshini këtë njoftim!")
        return redirect('add_job_custom')

    if request.method == "POST":
        job.delete()
        messages.success(request, "Puna u fshi me sukses!")
        return redirect('add_job_custom')
    
    return render(request, 'delete_confirm.html', {'job': job})


def aplikim(request, pk):
    job = get_object_or_404(Job, pk=pk)
    
    # Nëse përdoruesi ka një CV të ruajtur, i marrim të dhënat paraprakisht
    user_cv = None
    if request.user.is_authenticated:
        user_cv = getattr(request.user, 'cv', None)

    if request.method == "POST":
        Aplikim.objects.create(
            job=job,
            applicant=request.user if request.user.is_authenticated else None,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            # Marrim të dhënat e CV-së nga forma
            skills=request.POST.get('skills'),
            experience=request.POST.get('experience'),
            education=request.POST.get('education'),
            projects=request.POST.get('projects'),
            description=request.POST.get('description'),
            cv_file=request.FILES.get('cv_file')
        )
        messages.success(request, "Aplikimi u dërgua me sukses!")
        return redirect('detailsPage', pk=pk)

    return render(request, 'aplikim.html', {'job': job, 'user_cv': user_cv})


@login_required
def cv_view(request):
    from .models import CV, Aplikim, Job
    user_cv, created = CV.objects.get_or_create(user=request.user)
    
    # Marrim ID-në e punës nga URL-ja (psh: ?job_id=5)
    job_id = request.GET.get('job_id')

    if request.method == "POST":
        # HAPI 1: Ruajmë të dhënat te Profili i CV-së
        user_cv.phone = request.POST.get('phone')
        user_cv.languages = request.POST.get('languages')
        user_cv.skills = request.POST.get('skills')
        user_cv.experience = request.POST.get('experience')
        user_cv.education = request.POST.get('education')
        user_cv.projects = request.POST.get('projects')
        user_cv.save()

        # HAPI 2: Nëse përdoruesi erdhi nga një punë specifike, krijo Aplikimin
        if job_id:
            try:
                job = Job.objects.get(id=job_id)
                # Krijojmë aplikimin direkt në databazë
                Aplikim.objects.create(
                    job=job,
                    applicant=request.user,
                    first_name=request.user.first_name,
                    last_name=request.user.last_name,
                    email=request.user.email,
                    phone=user_cv.phone,
                    skills=user_cv.skills,
                    experience=user_cv.experience,
                    education=user_cv.education,
                    projects=user_cv.projects,
                    description="Aplikim i dërguar automatikisht pas plotësimit të CV-së."
                )
                messages.success(request, "Aplikimi u krye me sukses!")
            except Job.DoesNotExist:
                messages.error(request, "Puna nuk u gjet.")
        else:
            messages.success(request, "CV-ja u ruajt, por nuk kishte aplikim aktiv.")

        # HAPI 3: Redirect në Home Page
        return redirect('homePage')

    return render(request, 'cv.html', {'cv': user_cv})



@login_required
def aplikimet_e_mia(request):
    # Marrim aplikimet ku 'applicant' është përdoruesi aktual
    aplikimet = Aplikim.objects.filter(applicant=request.user).order_by('-created_at')
    return render(request, 'aplikimet_e_mia.html', {'aplikimet': aplikimet})


def custom_password_reset(request):
    if request.method == 'POST':
        email_input = request.POST.get('email')
        # Përdorim filter().first() për të marrë vetëm një përdorues
        user = User.objects.filter(email=email_input).first()
        
        if user:
            # 1. Gjenerojmë UID dhe e kthejmë në string të pastër
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # 2. Gjenerojmë Token-in
            token = default_token_generator.make_token(user)
            
            # 3. Ndërtojmë linkun (Sigurohu që porta është 8000)
            link = f"http://127.0.0.1:8000/reset/{uid}/{token}/"
            
            # PRINTIMI PER DEBUG (Kopjo këtë link fiks siç del)
            print("\n" + "="*60)
            print(f"LINKU I RI: {link}")
            print("="*60 + "\n")
            
            send_mail(
                "Rivendos Fjalekalimin",
                f"Kliko ketu per fjalekalimin e ri: {link}",
                "noreply@jobportal.al",
                [user.email],
                fail_silently=False,
            )
            return redirect('password_reset_done')
        else:
            messages.error(request, "Ky email nuk ekziston në sistem.")
            
    return render(request, 'password_reset.html')


def pune(request):
    # 1. Merri të gjitha punët fillimisht
    jobs = Job.objects.all().order_by('-created_at')

    # 2. Merri vlerat nga URL dhe pastroji nga hapësirat
    qyteti_query = request.GET.get('qyteti', '').strip()
    kategoria_query = request.GET.get('kategoria', '').strip()

    # 3. Logjika e filtrimit (iexact është më i sigurt për krahasime tekstesh)
    if qyteti_query:
        jobs = jobs.filter(location__iexact=qyteti_query)

    if kategoria_query:
        jobs = jobs.filter(category__iexact=kategoria_query)

    # 4. Paketimi i të dhënave për HTML
    context = {
        'jobs': jobs,
        'city_choices': Job.CITY_CHOICES,    # Merren direkt nga modeli Job
        'category_choices': Job.CATEGORY_CHOICES, # Merren direkt nga modeli Job
    }
    
    return render(request, 'pune.html', context)

