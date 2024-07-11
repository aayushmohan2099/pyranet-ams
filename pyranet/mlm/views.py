from django.shortcuts import render, redirect, get_object_or_404
from .models import Member, MemberRelationship, Company, Product
from .forms import UserCreationForm, MemberRelationshipForm, UpdateUserForm, EditMemberRelationshipForm, CompanyForm, ProductForm
import json
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse

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
    relationships = MemberRelationship.objects.all()
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
    
    return render(request, 'establish_relationship.html', {'form': form, 'members': members, 'relationships': relationships})

def relation_established(request, parent, child, member_id):
    member = Member.objects.get(id=member_id)
    return render(request, 'relation_established.html', {'parent': parent, 'child': child, 'member': member})

def update_user(request, username):
    user = get_object_or_404(User, username=username)
    try:
        member = Member.objects.get(user=user)
    except Member.DoesNotExist:
        member = None
    
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_updated', username=user.username)
    else:
        form = UpdateUserForm(instance=user)
        if member:
            form.fields['sponsor'].initial = member.sponsor  # Set initial value if member exists
    
    return render(request, 'update_user.html', {'form': form, 'user': user})
def user_updated(request, username):
    members=Member.objects.all()
    user = get_object_or_404(User, username=username)
    return render(request, 'user_updated.html', {'user': user, 'members': members})

def edit_member_relationship(request, relationship_id):
    relationship = get_object_or_404(MemberRelationship, id=relationship_id)
    
    if request.method == 'POST':
        form = EditMemberRelationshipForm(request.POST, instance=relationship)
        if form.is_valid():
            form.save()
            return redirect('relationship_updated', relationship_id=relationship.id)
    else:
        form = EditMemberRelationshipForm(instance=relationship)
    
    return render(request, 'edit_member_relationship.html', {'form': form, 'relationship': relationship})

def relationship_updated(request, relationship_id):
    relationship = get_object_or_404(MemberRelationship, id=relationship_id)
    return render(request, 'relationship_updated.html', {'relationship': relationship})


# View to show, update, or add new products under any company
def manage_products(request):
    Products = Product.objects.all()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage_products')
    else:
        form = ProductForm()
    
    return render(request, 'manage_products.html', {'Products': Products, 'form': form})

# View to show, update, or add new companies and the products they offer
def manage_companies(request):
    companies = Company.objects.all()
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage_companies')
    else:
        form = CompanyForm()
    
    return render(request, 'manage_companies.html', {'companies': companies, 'form': form})

# View to browse the products of any company with their name, price, and description only
def browse_products(request):
    companies = Company.objects.all()
    return render(request, 'browse_products.html', {'companies': companies})

def user_login(request):
    if request.method == 'POST':
        email_or_username = request.POST['email_or_username']
        password = request.POST['password']

        user = authenticate(request, username=email_or_username, password=password)
        
        if user is None:
            # Try to authenticate using email
            try:
                user_obj = User.objects.get(email=email_or_username)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                messages.error(request, 'User does not exist')

        if user is not None:
            login(request, user)
            try:
                member = Member.objects.get(user=user)
                request.session['member_id'] = member.id  # Store member ID in session
            except Member.DoesNotExist:
                messages.error(request, 'Member associated with user does not exist')
                return redirect('user_login')  # Redirect back to login if no member is found
            
            return redirect('user_dashboard', member.id)
        else:
            messages.error(request, 'Invalid login credentials')

    return render(request, 'user_login.html')

def user_dashboard(request, member_id):
    members = Member.objects.all()
    member_id = request.session.get('member_id')
    if member_id:
        member = get_object_or_404(Member, id=member_id)
    else:
        member = None
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

    return render(request, 'dashboard.html', {'member': member, 'members': members, 'network_tree': network_tree_html})