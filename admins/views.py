from django.shortcuts import render, redirect, get_object_or_404
from .models import new_product, team, New_task
from member.models import CustomUser
from products.models import Order
from nobodyknows.models import user_contact_review
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import re
from django.db.models import Q

#Dashboard
@login_required
def dashboard(request):
    num_product = new_product.objects.all()
    num_user = CustomUser.objects.all()
    num_message = user_contact_review.objects.all()
    num_order = Order.objects.all()
    
    product_num = len(num_product)
    user_num = len(num_user)
    message_num = len(num_message)
    order_num = len(num_order)
    
    context = {
        'product_num': product_num,
        'user_num': user_num,
        'order_num': order_num,
        'message_num': message_num
    }
    return render(request, 'admins/dashboard.html', context)

#Users
@login_required
def add_member(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        phone_number = request.POST['phone_number']
        profile_img = request.FILES.get('profile_img')
        
        if (
            len(password) >= 8 and
            re.search(r"[A-Z]", password) and
            re.search(r"[a-z]", password) and
            re.search(r"\d", password) and
            re.search(r"[@$!%*?&#]", password)
        ):
            if password == confirm_password:
                if CustomUser.objects.filter(email=email).exists():
                    messages.error(request, f'"{email}" email already exists')
                elif CustomUser.objects.filter(username=username).exists():
                    messages.error(request, f'"{username}" username already exists')
                else:
                    user = CustomUser.objects.create_user(
                        email=email, 
                        password=password, 
                        username=username, 
                        first_name=first_name, 
                        last_name=last_name, 
                        phone_number=phone_number, 
                        profile_img=profile_img
                    )
                    user.save()
                    messages.success(request, f'{username} - Account Created Successfully')
                    return redirect('add_member')
            else:
                messages.error(request, 'Both passwords do not match')
        else:
            messages.error(request, 'Password must match required format')
    return render(request, 'admins/add_member.html')

@login_required
def manage_member(request):
    member_list = CustomUser.objects.all()
    query = request.GET.get('query', '')
    results = []
    if (query != ''):
        results = CustomUser.objects.filter(
            Q(id__icontains = query)
        )
        context = {
            'member_list': results,
            'query': query
        }
    else:
        context = {
            'member_list': member_list
        }
    return render(request, 'admins/manage_members.html', context)

@login_required
def view_member(request, member_id):
    member = get_object_or_404(CustomUser, id=member_id)
    return render(request, 'admins/member_detail.html', {'member':member})

@login_required
def delete_member_alt(request, member_id):
    member = get_object_or_404(CustomUser, id=member_id)
    return render(request, 'admins/delete_member.html', {'member':member})

@login_required
def delete_member(request, member_id):
    member = get_object_or_404(CustomUser, id=member_id)
    member.delete()
    messages.success(request, f"User {member.username}'s account has been deleted successfully.")
    return redirect('manage_member')

#Team
@login_required
def add_team(request):
    if request.method == "POST":
        name = request.POST['name']
        position = request.POST['position']
        email = request.POST['email']
        whatsapp = request.POST['whatsapp']
        instagram = request.POST['instagram']
        twitter = request.POST['twitter']
        phone_number = request.POST['phone_number']
        user_img = request.FILES.get('user_img')
        user_cover = request.FILES.get('user_cover')
        
        TeamMember = team(
            name=name,
            position=position,
            email=email,
            whatsapp=whatsapp,
            instagram=instagram,
            twitter=twitter,
            phone_number=phone_number,
            user_img=user_img,
            user_cover=user_cover
        )
        TeamMember.save()
        messages.success(request, f'"{name}" has been added as team member')
        return redirect('add_team')
    return render(request, 'admins/add_team.html')

@login_required
def manage_team(request):
    team_members = team.objects.all()
    query = request.GET.get('query', '')
    results = []
    if (query != ''):
        results = CustomUser.objects.filter(
            Q(id__icontains = query) |
            Q(name__icontains = query)
        )
        context = {
            'team_members': results,
            'query': query
        }
    else:
        context = {
            'team_members': team_members
        }
    return render(request, 'admins/manage_team.html', context)

@login_required
def edit_team(request, team_id):
    team_member = get_object_or_404(team, id=team_id)
    if request.method == 'POST':
        team_member.name = request.POST['name']
        team_member.position = request.POST['position']
        team_member.email = request.POST['email']
        team_member.whatsapp = request.POST['whatsapp']
        team_member.instagram = request.POST['instagram']
        team_member.twitter = request.POST['twitter']
        team_member.phone_number = request.POST['phone_number']
        
        new_user_img = request.FILES.get('user_img')
        if new_user_img:
            team_member.user_img = new_user_img
        team_member.save()
        messages.success(request, f'Product "{team_member.name}" has been updated successfully')
        return redirect('edit_team', team_member.id)
    return render(request, 'admins/edit_team.html', {'team_member':team_member})

@login_required
def delete_team_member(request, team_id):
    team_member = get_object_or_404(team, id=team_id)
    team_member.delete()
    messages.success(request, f'"{team_member.name}" has been deleted successfully')
    return redirect('manage_team')

@login_required
def delete_team(request):
    team_members = team.objects.all()
    team_members.delete()
    messages.success(request, 'All team members have been deleted successfully')
    return redirect('manage_team')

#Products
@login_required
def add_product(request):
    if request.method == "POST":
        product_name = request.POST['product_name']
        product_price = request.POST['product_price']
        product_desc = request.POST['product_desc']
        product_rating = request.POST['product_rating']
        product_quantity = request.POST['product_quantity']
        product_img = request.FILES.get('product_img')
        product_category = request.POST['product_category']
        
        NewProduct = new_product(
            product_name=product_name, 
            product_price=product_price,
            product_desc=product_desc, 
            product_quantity=product_quantity,
            product_rating=product_rating,
            product_img=product_img,
            product_category=product_category
            )
        NewProduct.save()
        messages.success(request, f'"{product_name}" has been added successfully')
        return redirect('add_product')
    return render(request, 'admins/add_products.html')

@login_required
def manage_product(request):
    product_list = new_product.objects.all()
    query = request.GET.get('query', '')
    results = []
    if (query != ''):
        results = new_product.objects.filter(
            Q(id__icontains = query) | 
            Q(product_name__icontains = query) | 
            Q(product_category__icontains = query)
        )
        context = {
            'product_list': results,
            'query': query
        }
    else:
        context = {
            'product_list': product_list
        }
    return render(request, 'admins/manage_products.html', context)

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(new_product, id=product_id)
    if request.method == 'POST':
        product.product_name = request.POST['product_name']
        product.product_price = request.POST['product_price']
        product.product_desc = request.POST['product_desc']
        product.product_rating = request.POST['product_rating']
        product.product_quantity = request.POST['product_quantity']
        product.product_category = request.POST['product_category']
        
        new_product_img = request.FILES.get('product_img')
        if new_product_img:
            product.product_img = new_product_img
        product.save()
        messages.success(request, f'Product "{product.product_name}" has been updated successfully')
        return redirect('edit_product', product.id)
    return render(request, 'admins/edit_product.html', {'product':product})

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(new_product, id=product_id)
    product.delete()
    messages.success(request, f'"{product.product_name}" has been deleted successfully')
    return redirect('manage_product')

@login_required
def delete_all_products(request):
    all_products = new_product.objects.all()
    all_products.delete()
    messages.success(request, 'All products have been deleted successfully')
    return redirect('manage_product')

#User messages
@login_required
def user_message(request):
    user_messages = user_contact_review.objects.all()
    query = request.GET.get('query', '')
    results = []
    if (query != ''):
        results = user_contact_review.objects.filter(
            Q(name__icontains = query) | 
            Q(subject__icontains = query) | 
            Q(message__icontains = query)
        )
        context = {
            'user_messages': results,
            'query': query
        }
    else:
        context = {
            'user_messages': user_messages
        }
    return render(request, 'admins/contact_messages.html', context)

@login_required
def message_detail(request, message_id):
    message_detail = get_object_or_404(user_contact_review, id=message_id)
    return render(request, 'admins/message_detail.html', {'message_detail': message_detail})

@login_required
def delete_message(request, message_id):
    users_message = get_object_or_404(user_contact_review, id=message_id)
    users_message.delete()
    messages.success(request, f"{users_message.name}'s message has been deleted successfully")
    return redirect('user_messages')

@login_required
def delete_all_messages(request):
    all_messages = user_contact_review.objects.all()
    all_messages.delete()
    messages.success(request, 'All messages have been deleted successfully')
    return redirect('user_messages')

#Tasks
def tasks(request):
    if request.method == "POST":
        new_task = request.POST['new_task']
        
        NewTask = New_task(
            new_task=new_task
        )
        
        NewTask.save()
        return redirect('dashboard')
    
    all_tasks = New_task.objects.all()
    print(all_tasks)
    return render(request, 'admins/includes/tasks.html', {'all_tasks':all_tasks})