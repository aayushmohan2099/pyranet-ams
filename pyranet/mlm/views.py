from django.shortcuts import render, redirect
from .models import Member
from .forms import UserCreationForm

def member_detail(request, member_id):
    member = Member.objects.get(id=member_id)
    return render(request, 'member_detail.html', {'member': member})

def create_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user=form.save()
            member = Member.objects.get(user=new_user)
            return redirect('user_created', username=new_user.username, member_id=member.id)
    else:
        form = UserCreationForm()
    
    return render(request, 'create_user.html', {'form': form})

def user_created(request, username, member_id):
    member = Member.objects.get(id=member_id)
    return render(request, 'user_created.html', {'username': username, 'member': member})