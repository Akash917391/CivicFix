from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = (
        ('citizen' , 'Citizen'),
        ('volunteer' , 'Volunteer'),
        ('staff' , 'Staff'),
        ('admin' , 'Admin'),
    )

    mobile_number = models.CharField(
        max_length=10
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='citizen'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.username
        

# ====================================================
# STAFF MODEL 
# ====================================================

class Staff(models.Model):
    DEPARTMENT_CHOICES = (
        ('garbage' , 'Garbage Department'),
        ('electricity' , 'Electricity Department'),
        ('roads' , 'Road Maintenance Department'),
        ('water' , 'Water Supply Department'),
        ('drainage' , 'Drainage Department'),
        ('sanitation' , 'Sanitation Department'),
        ('traffic' , 'Traffic Management Department'),
    )


    user = models.OneToOneField(
        User, 
        
        on_delete=models.CASCADE
    )

    department = models.CharField(
        max_length=30,
        choices=DEPARTMENT_CHOICES
    )

    address = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.department}"
    

# ==========================================
# VOLUNTEER GROUP MODEL 
# ==========================================

class VolunteerGroup(models.Model):
    created_by = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    group_name = models.CharField(max_length=25)

    contact_number = models.CharField(max_length=10)

    address = models.TextField()

    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.group_name
    

# =========================================
# ISSUE MODEL 
# =========================================

class Issue(models.Model):
    CATEGORY_CHOICES = (
        ('garbage', 'Garbage'),
        ('pothole', 'Pothole'),
        ('street_light', 'Street Light'),
        ('electricity', 'Electricity Issue'),
        ('water_leakage', 'Water Leakage'),
        ('drainage', 'Drainage Problem'),
        ('road_damage', 'Road Damage'),
        ('traffic_signal', 'Traffic Signal Issue'),
        ('illegal_dumping', 'Illegal Garbage Dumping'),
        ('public_toilet', 'Public Toilet Issue'),
        ('water_supply', 'Water Supply Problem'),
        ('tree_fallen', 'Fallen Tree'),
        ('dead_animal', 'Dead Animal'),
        ('sewage', 'Sewage Overflow'),
        ('encroachment', 'Illegal Encroachment'),
        ('other', 'Other'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    description = models.TextField()

    latitude = models.DecimalField(
        max_digits= 9 ,
        decimal_places=6
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6
    )

    address = models.TextField()

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='pending'
    )

    assigned_staff = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Issue #{self.id} - {self.category}"
    
# =========================================================
# ISSUE IMAGE MODEL
# =========================================================

class IssueImage(models.Model):

    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE , 
        related_name='images'
    )

    image = models.ImageField(
        upload_to='issue_images/'
    )

    def __str__(self):
        return f"Issue Image {self.id}"
    
# =========================================================
# ISSUE UPDATE MODEL
# =========================================================

class IssueUpdate(models.Model):

    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE
    )

    updated_by = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE
    )

    note = models.TextField()

    image = models.ImageField(
        upload_to='issue_updates/',
        null=True, 
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Update for Issue {self.issue.id}"


# =========================================================
# ISSUE SUPPORT MODEL
# =========================================================


class IssueSupport(models.Model):
    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} supported Issue {self.issue.id}"
    
    
# =========================================================
# NOTIFICATION MODEL
# =========================================================

class Notification(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    message = models.TextField()

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"