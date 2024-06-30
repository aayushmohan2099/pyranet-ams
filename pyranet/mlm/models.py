from django.db import models
from django.contrib.auth.models import User

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sponsor = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

class MemberRelationship(models.Model):
    parent = models.ForeignKey(Member, related_name='children', on_delete=models.CASCADE)
    child = models.ForeignKey(Member, related_name='parents', on_delete=models.CASCADE)