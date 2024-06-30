from django.shortcuts import render
from django.shortcuts import render
from .models import Member

def member_detail(request, member_id):
    member = Member.objects.get(id=member_id)
    return render(request, 'member_detail.html', {'member': member})
