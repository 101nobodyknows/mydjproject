from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth.models import auth
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import re


def sign(request):
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
                    auth.login(request, user)
                    return redirect('home')
            else:
                messages.error(request, 'Both passwords do not match')
        else:
            messages.error(request, 'Password must match required format')
    return render(request, 'member/sign.html')

def log(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid Username or Password')
            return redirect('log')
    else:
        return render(request, 'member/log.html')

@login_required
def account_details(request):
    return render(request, 'member/account.html')

@login_required
def logout_user(request):
    logout(request)
    return redirect('log')

@login_required
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.phone_number = request.POST['phone_number']
        user.username = request.POST['username']
        #to check if new profile image is provided
        new_profile_img = request.FILES.get('profile_img')
        if new_profile_img:
            user.profile_img = new_profile_img
            
        user.save()
        messages.success(request, 'Personal details have been updated successfully')
        return redirect('account_details')
    return render(request, 'member/account.html')

@login_required
def edit_email(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        user.email = request.POST['email']    
        user.save()
        return redirect('account_details')
    return render(request, 'member/account.html')

@login_required
def edit_user_psw(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        current_password = request.POST['password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        # Check if the current password matches the hashed password in the database
        if not check_password(current_password, user.password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('account_details')

        # Check if new password and confirm password match
        if new_password != confirm_password:
            messages.error(request, 'New password and confirm password do not match.')
            return redirect('account_details')

        # Set the new password
        user.set_password(new_password)
        user.save()

        # Update session auth hash to prevent the user from being logged out
        update_session_auth_hash(request, user)

        messages.success(request, 'Password updated successfully.')
        return redirect('account_details')

    return render(request, 'member/account.html')


def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    return redirect('home')