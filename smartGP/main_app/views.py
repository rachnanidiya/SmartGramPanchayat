from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.hashers import make_password
from .models import *
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def schemes(request):
    return render(request, 'schemes.html')

def apply(request):
    # Get the scheme name from URL parameter (default to empty if not provided)
    scheme_name = request.GET.get('scheme', '')

    if request.method == 'POST':
        name = request.POST.get('name')
        aadhaar = request.POST.get('aadhaar')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        scheme = request.POST.get('scheme')  # Get scheme from form
        income = request.POST.get('income')
        description = request.POST.get('description')  # ✅ Get the new description field
        # Handle file upload
        document = request.FILES.get('documents')
        filename = None
        if document:
            fs = FileSystemStorage()
            filename = fs.save(document.name, document)

        # Save to database
        SchemeApplication.objects.create(
            user=request.user, 
            name=name,
            aadhaar=aadhaar,
            dob=dob,
            gender=gender,
            mobile=mobile,
            address=address,
            scheme=scheme,
            income=income,
            documents=filename,
            description=description  
        )

        return redirect('success')  # Redirect to success page

    return render(request, 'apply.html', {'scheme_name': scheme_name})  # Pass scheme to template

def digital_literacy(request):
    return render(request, 'digital-literacy.html')

def healthcare(request):
    return render(request, 'Healthcare_for_All.html')

def women(request):
    return render(request, 'Rural_Women.html')

def energy(request):
    return render(request, 'Renewable_Energy.html')

def agriculture(request):
    return render(request, 'Smart_Agriculture_Initiative.html')

def employment(request):
    return render(request, 'Employement_Skill.html')

def success(request):
    return render(request, 'success.html')

def complaint(request):
    if request.method == "POST":
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        complaint_type = request.POST.get('complaintType')
        description = request.POST.get('description')
        image = request.FILES.get('imageUpload')

        user = request.user if request.user.is_authenticated else None

        Complaint.objects.create(
            user=user,
            name=name,
            contact=contact,
            email=email,
            complaint_type=complaint_type,
            description=description,
            image=image
        )

        messages.success(request, "Your complaint has been submitted successfully!")
        return redirect('thanks')

    return render(request, 'complaint.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile_number = request.POST.get('mobile_number')
        password = request.POST.get('password')

        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists!'})

        if CustomUser.objects.filter(mobile_number=mobile_number).exists():
            return render(request, 'register.html', {'error': 'Mobile number already in use!'})

        user = CustomUser.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            mobile_number=mobile_number,
            password=password  # `create_user` hashes password automatically
        )

        # Authenticate and log in the user
        authenticated_user = authenticate(request, username=username, password=password)
        if authenticated_user:
            login(request, authenticated_user)  # ✅ Correct usage
            return redirect('home')

    return render(request, 'register.html')

def user_login(request):  # 🔹 Renamed from `login` to `user_login` to prevent conflicts
     if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("home")  # Redirect to home page on success
        else:
            return render(request, "login.html", {"error": "Invalid username or password!"})
    
     return render(request, "login.html")
def logout_user(request):
    logout(request)
    return redirect('/')

def thanks(request):
    return render(request, 'ty.html')
def news_list(request):
    news_items = News.objects.all().order_by('-created_at')  # Fetch all news items
    return render(request, 'news.html', {'news_items': news_items})  
# Admin-only access check
def admin_required(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(admin_required)
def admin_dashboard(request):
    complaints = Complaint.objects.all()
    applications = SchemeApplication.objects.all()
    news_items = News.objects.all()

    context = {
        'complaints': complaints,
        'applications': applications,
        'news_items': news_items
    }
    return render(request, 'admin_dashboard.html', context)

@user_passes_test(admin_required)
def approve_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    complaint.is_approved = True
    complaint.save()
    return redirect('admin_dashboard')
@user_passes_test(admin_required)
def delete_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    complaint.delete()
    return redirect('admin_dashboard')
@user_passes_test(admin_required)
def approve_scheme(request, scheme_id):
    scheme = get_object_or_404(SchemeApplication, id=scheme_id)
    scheme.is_approved = True
    scheme.save()
    return redirect('admin_dashboard')
@user_passes_test(admin_required)
def edit_news(request, news_id):
    news = get_object_or_404(News, id=news_id)
    if request.method == 'POST':
        news.title = request.POST['title']
        news.content = request.POST['content']
        news.date = request.POST['date']
    if 'image' in request.FILES:
        news.image = request.FILES['image']
        news.save()
        return redirect('admin_dashboard')
    return render(request, 'edit_news.html', {'news': news})

@user_passes_test(admin_required)
def delete_news(request, news_id):
    news = get_object_or_404(News, id=news_id)
    news.delete()
    return redirect('admin_dashboard')
def is_admin(user):
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(is_admin)
def add_news(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')  # File input

        if title and content:
            News.objects.create(title=title, content=content, image=image)
            return redirect('admin_dashboard')  # Redirect to your admin page
    return render(request, 'add_news.html')
@login_required
def user_profile(request):
    user = request.user
    complaints = Complaint.objects.filter(user=user)
    applications = SchemeApplication.objects.filter(user=user)

    return render(request, 'user_profile.html', {
        'user': user,
        'complaints': complaints,
        'applications': applications,
    })