from django.shortcuts import render, redirect, get_object_or_404
from .models import Member, MemberRelationship
from .forms import UserCreationForm, MemberRelationshipForm
import json
from django.http import JsonResponse

def homepage(request):
    members = Member.objects.all()
    return render(request, 'homepage.html', {'members':members})

def find_member(request):
    member_id = request.GET.get('member_id')
    member = get_object_or_404(Member, id=member_id)
    return redirect('member_detail', member_id=member.id)

def member_detail(request, member_id):
    member = Member.objects.get(id=member_id)
    members = Member.objects.all()

    def get_network_tree(member):
        # Recursive function to build the tree structure
        children = []
        for child_relationship in member.children.all():
            children.append(get_network_tree(child_relationship.child))
        
        return {
            'name': member.user.username,
            'children': children
        }

    network_data = get_network_tree(member)
    network_tree_html = render_network_tree(network_data)

    return render(request, 'member_detail.html', {'member': member, 'members': members, 'network_tree': network_tree_html})

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

def render_network_tree(node):
    # Recursive rendering of the tree structure
    html = f'<li><a href="javascript:void(0);"><div class="member-view-box"><div class="member-image"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512" class="icon"><!--!Font Awesome Free 6.5.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path d="M224 256A128 128 0 1 0 224 0a128 128 0 1 0 0 256zm-45.7 48C79.8 304 0 383.8 0 482.3C0 498.7 13.3 512 29.7 512H418.3c16.4 0 29.7-13.3 29.7-29.7C448 383.8 368.2 304 269.7 304H178.3z"/></svg><div class="member-details"><h3>{node["name"]}</h3></div></div></div></a>'
    
    if node.get('children'):
        html += '<ul>'
        for child in node['children']:
            html += render_network_tree(child)
        html += '</ul>'
    
    html += '</li>'
    return html

def establish_relationship(request):
    members = Member.objects.all()
    if request.method == 'POST':
        form = MemberRelationshipForm(request.POST)
        if form.is_valid():
            form.save()
            parent_id, child_id = form.get_selected_ids()
            parent = Member.objects.get(id=parent_id)
            child = Member.objects.get(id=child_id)
            return redirect('relation_established', parent=parent.user.username, child=child.user.username, member_id=parent.id)
    else:
        form = MemberRelationshipForm()
    
    return render(request, 'establish_relationship.html', {'form': form, 'members': members})

def relation_established(request, parent, child, member_id):
    member = Member.objects.get(id=member_id)
    return render(request, 'relation_established.html', {'parent': parent, 'child': child, 'member': member})