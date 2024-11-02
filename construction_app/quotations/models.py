from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    description = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('DECLINED', 'Declined'),
        ('COMPLETED', 'Completed'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Project {self.id}: {self.description}"


class ProjectElement(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Material(models.Model):
    element = models.ForeignKey(ProjectElement, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    unit = models.CharField(max_length=50)
    price_per_qty = models.DecimalField(max_digits=10, decimal_places=2)
    markup_percent = models.DecimalField(max_digits=5, decimal_places=2)

    def total_cost(self):
        return self.quantity * self.price_per_qty * (1 + self.markup_percent / 100)

    def __str__(self):
        return f"{self.name} - {self.quantity} {self.unit}"


class Quotation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    area_size = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Quotation for {self.project.description} by {self.user.username}"


from django.db import models

# Create your models here.
