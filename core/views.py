from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth import authenticate , login , logout
from .models import *
from django.db.models import Count, Q
from django.contrib import messages
from django.views.decorators.cache import never_cache


# Create your views here.

# ===============================================
# authenticate Register page
# =============================================== 
def register_view(request):

    if request.user.is_authenticated:

        return redirect('citizen_dashboard')


    if request.method == 'POST':

        first_name = request.POST.get('first_name')

        last_name = request.POST.get('last_name')

        username = request.POST.get('username')

        email = request.POST.get('email')

        mobile_number = request.POST.get('mobile_number')

        password = request.POST.get('password')

        confirm_password = request.POST.get('confirm_password')


        # Username already exists
        if User.objects.filter(username=username).exists():

            return render(request, 'auth/register.html', {

                'error': 'Username already exists'

            })


        # Email already exists
        if User.objects.filter(email=email).exists():

            return render(request, 'auth/register.html', {

                'error': 'Email already exists'

            })


        # Mobile validation
        if len(mobile_number) != 10 or not mobile_number.isdigit():

            return render(request, 'auth/register.html', {

                'error': 'Enter valid 10 digit mobile number'

            })


        # Password validation
        if len(password) < 6:

            return render(request, 'auth/register.html', {

                'error': 'Password must be at least 6 characters'

            })


        # Password match validation
        if password != confirm_password:

            return render(request, 'auth/register.html', {

                'error': 'Passwords do not match'

            })


        # Create User
        User.objects.create_user(

            first_name=first_name,

            last_name=last_name,

            username=username,

            email=email,

            mobile_number=mobile_number,

            role='citizen',

            password=password

        )


        return redirect('login')


    return render(request, 'auth/register.html')


# ===============================================
# authenticate Login page
# ===============================================
def login_view(request):

    if request.user.is_authenticated: 

        if request.user.role == 'citizen': 
            return redirect('citizen_dashboard') 
        elif request.user.role == 'staff': 
            return redirect('staff_dashboard') 
        elif request.user.role == 'admin': 
            return redirect('admin_dashboard')
        
    if request.method == 'POST':

        username = request.POST.get('username')

        password = request.POST.get('password')


        # Empty field validation
        if not username or not password:

            return render(request, 'auth/login.html', {

                'error': 'Please fill all fields'

            })


        user = authenticate(

            request,

            username=username,

            password=password

        )


        # Invalid credentials
        if user is None:

            return render(request, 'auth/login.html', {

                'error': 'Invalid username or password'

            })


        login(request, user)


        # Role-based redirect
        if user.role == 'citizen':

            return redirect('citizen_dashboard')


        elif user.role == 'volunteer':

            return redirect('volunteer_dashboard')


        elif user.role == 'staff':

            return redirect('staff_dashboard')


        elif user.role == 'admin':

            return redirect('admin_dashboard')


    return render(request, 'auth/login.html')


# =================================================
# Log-out View
# =================================================

def logout_view(request):
    logout(request)
    
    return redirect('login')


# ===============================================
# Issue_Detail and My_issue pages View
# ===============================================
@never_cache
def my_issues(request):

    if not request.user.is_authenticated: 
        return redirect('login')

    if request.user.role != 'citizen': 
        return redirect('login')
    
    issues = Issue.objects.filter(

        user=request.user

    ).order_by('-created_at')

    total_issues = issues.count()

    in_progress_count = issues.filter(
        status='in_progress'
    ).count()

    pending_count = issues.filter(
        status='pending'
    ).count()

    resolved_count = issues.filter(
        status='resolved'
    ).count()

    return render(

        request,

        'dashboard/myissue.html',

        {
            'issues': issues , 
            'total_issues': total_issues,

            'in_progress_count': in_progress_count,

            'pending_count': pending_count,

            'resolved_count': resolved_count,
        }

    )

@never_cache
def issue_detail(request, issue_id):

    # Login protection
    if not request.user.is_authenticated:

        return redirect('login')


    # ==============================
    # ADMIN CAN VIEW ALL ISSUES
    # ==============================
    if request.user.role == 'admin':

        issue = get_object_or_404(

            Issue,

            id=issue_id

        )


    # ==============================
    # CITIZEN CAN VIEW OWN ISSUES
    # ==============================
    elif request.user.role == 'citizen':

        issue = get_object_or_404(

            Issue,

            id=issue_id,

            user=request.user

        )


    # ==============================
    # STAFF CAN VIEW ASSIGNED ISSUES
    # ==============================
    elif request.user.role == 'staff':

        issue = get_object_or_404(

            Issue,

            id=issue_id,

            assigned_staff__user=request.user

        )


    else:

        return redirect('login')


    return render(

        request,

        'dashboard/issueDetailPage.html',

        {

            'issue': issue

        }

    )

# ===============================================
# Dashboard pages
# ===============================================


# ============Citizen-Dashboard====================
@never_cache
def citizen_dashboard(request):


    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.user.role != 'citizen': 
        return redirect('login')
    
    if request.method == "POST":
        category = request.POST.get('category')
        description = request.POST.get('description')
        address = request.POST.get('address')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        images = request.FILES.getlist('images')

        issue = Issue.objects.create(

           
            user=request.user,

            category=category,

            description=description,

            address=address,

            latitude=latitude,

            longitude=longitude,

        )

        for image in images:

            IssueImage.objects.create(

                issue=issue,

                image=image

            )

    return render(request , 'dashboard/citizenHome.html')



# ============volunteer-Dashboard====================

def volunteer_dashboard(request):
    return render(request,'dashboard/volunteer_dashboard.html')



# ============Staff-Dashboard====================
@never_cache
def staff_dashboard(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.role != 'staff':

        return redirect('login')


    # ==================================
    # SAVE STAFF UPDATE
    # ==================================
    if request.method == 'POST':

        issue_id = request.POST.get('issue_id')

        note = request.POST.get('note')

        status = request.POST.get('status')

        image = request.FILES.get('image')


        issue = Issue.objects.get(

            id=issue_id

        )


        # Create new update entry
        IssueUpdate.objects.create(

            issue=issue,

            updated_by=request.user.staff,

            note=note,

            image=image

        )


        # Update issue status
        # issue.status = status

        # issue.save()


        messages.success(

            request,

            'Work update submitted successfully.'

        )


        return redirect('staff_dashboard')


    # ==================================
    # FETCH ASSIGNED ISSUES
    # ==================================
    issues = Issue.objects.filter(

        assigned_staff__user=request.user

    ).order_by('-created_at')


    total_issues = issues.count()


    in_progress_count = issues.filter(

        status='in_progress'

    ).count()


    resolved_count = issues.filter(

        status='resolved'

    ).count()


    context = {

        'issues': issues,

        'total_issues': total_issues,

        'in_progress_count': in_progress_count,

        'resolved_count': resolved_count,

    }


    return render(

        request,

        'dashboard/staff_dashboard.html',

        context

    )

# ============Admin-Dashboard====================

@never_cache
def admin_dashboard(request):

    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.user.role != 'admin': 
        return redirect('login')

    total_issues = Issue.objects.count()

    pending_count = Issue.objects.filter(
        status='pending'
    ).count()

    in_progress_count = Issue.objects.filter(
        status='in_progress'
    ).count()

    resolved_count = Issue.objects.filter(
        status='resolved'
    ).count()

    total_staff = Staff.objects.count()

    issues = Issue.objects.select_related(
        'user',
        'assigned_staff'
    ).prefetch_related(
        'images'
    ).order_by('-created_at')

    status_filter = request.GET.get('status')

    if status_filter: 
        issues = issues.filter( status=status_filter )

    staff_list = Staff.objects.annotate(

        assigned_count=Count(

            'issue',

            filter=Q(issue__status='in_progress')
        ),
        resolved_count=Count(

            'issue',

            filter=Q(issue__status='resolved')
        )
    )


    updates = IssueUpdate.objects.select_related(

        'issue',
        'updated_by',
        'updated_by__user'

    ).order_by('-created_at')

    # -------Added-Newthing_part-------
    category_data = Issue.objects.values(

        'category'

    ).annotate(

        count=Count('id')

    )


    total_category_issues = Issue.objects.count()


    category_stats = []


    for item in category_data:

        percent = 0

        if total_category_issues > 0:

            percent = (item['count'] / total_category_issues) * 100


        category_stats.append({

            'label': item['category'].title(),

            'count': item['count'],

            'percent': percent

        })

    recent_issues = Issue.objects.select_related(

        'user'

    ).prefetch_related(

        'images'

    ).order_by('-created_at')[:5]


    busy_staff_count = staff_list.filter(

        assigned_count__gt=0

    ).count()


    available_staff_count = staff_list.filter(

        assigned_count=0

    ).count()


    department_count = len(

        Staff.DEPARTMENT_CHOICES

    )

  


    # ------Ensit here-----------------------


    context = {

        'total_issues': total_issues,

        'pending_count': pending_count,

        'in_progress_count': in_progress_count,

        'resolved_count': resolved_count,

        'total_staff': total_staff,

        'issues': issues,

        'staff_list': staff_list,

        'updates': updates,

        'status_choices': Issue.STATUS_CHOICES,

        'department_choices': Staff.DEPARTMENT_CHOICES,

        'category_stats': category_stats,

        'recent_issues': recent_issues,

    'busy_staff_count': busy_staff_count,

    'available_staff_count': available_staff_count,

    'department_count': department_count,


    }

    return render(

        request,

        'dashboard/admin_dashboard.html',

        context

    )

@never_cache
def assign_staff(request):

    if request.user.role != 'admin':

        return redirect('login')



    if request.method == 'POST':

        issue_id = request.POST.get('issue_id')

        staff_id = request.POST.get('staff_id')

        status = request.POST.get('status')

        issue = Issue.objects.get(id=issue_id)

        staff = Staff.objects.get(id=staff_id)

        issue.assigned_staff = staff

        issue.status = status

        issue.save()

        messages.success(
            request,
            'Issue assigned successfully.'
        )

    return redirect('/admin-dashboard/?section=issues') 


from django.contrib import messages
@never_cache
def create_staff(request):

    if request.user.role != 'admin':

        return redirect('login')


    if request.method == 'POST':

        first_name = request.POST.get('first_name')

        last_name = request.POST.get('last_name')

        username = request.POST.get('username')

        mobile_number = request.POST.get('mobile_number')

        email = request.POST.get('email')

        department = request.POST.get('department')

        address = request.POST.get('address')

        password = request.POST.get('password')


        # Prevent duplicate username
        if User.objects.filter(username=username).exists():

            messages.error(

                request,

                'Username already exists.'

            )

            return redirect('admin_dashboard')


        # Create User
        user = User.objects.create_user(

            first_name=first_name,

            last_name=last_name,

            username=username,

            mobile_number=mobile_number,

            email=email,

            password=password,

            role='staff'

        )


        # Create Staff
        Staff.objects.create(

            user=user,

            department=department,

            address=address

        )


        messages.success(

            request,

            'Staff leader created successfully.'

        )

    return redirect('/admin-dashboard/?section=staff')


def change_status(request, issue_id):

    if not request.user.is_authenticated:

        return redirect('login')


    if request.user.role != 'admin':

        return redirect('login')


    if request.method == 'POST':

        issue = get_object_or_404(

            Issue,

            id=issue_id

        )

        status = request.POST.get('status')

        issue.status = status

        issue.save()


    return redirect('/admin-dashboard/?section=updates')