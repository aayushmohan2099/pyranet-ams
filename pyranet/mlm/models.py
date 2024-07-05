from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    name = models.CharField(max_length=255)
    license_number = models.CharField(max_length=255)
    description = models.TextField()
    logo = models.ImageField(upload_to='media/company_logos/')
    base_profit_per_member = models.DecimalField(max_digits=10, decimal_places=2)
    Products_offered = models.ManyToManyField('Product', related_name='offering_companies')

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='media/Product_images/')

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sponsor = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    component = models.TextField(blank=True, null=True)
    base_sale_profit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    personal_profit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    profit_from_members = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    profit_to_head = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    Products_bought = models.ManyToManyField(Product, related_name='buyers', blank=True)

class MemberRelationship(models.Model):
    parent = models.ForeignKey(Member, related_name='children', on_delete=models.CASCADE)
    child = models.ForeignKey(Member, related_name='parents', on_delete=models.CASCADE)
