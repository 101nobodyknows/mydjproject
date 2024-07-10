from django.shortcuts import render, redirect
from .models import user_contact_review
from admins.models import team
from products.models import CartProduct
from django.views.decorators.csrf import csrf_protect
# from django.contrib import messages

#my views
def home(request):
    return render(request, 'nobodyknows/index.html')

def about(request):
    Team = team.objects.all()
    return render(request, 'nobodyknows/about.html', {'Team':Team})

def blog(request):
    return render(request, 'nobodyknows/blog.html')

@csrf_protect
def contact(request):
    if request.method == "POST":
        y_name = request.POST['name']
        y_email = request.POST['email']
        y_subject = request.POST['subject']
        y_message = request.POST['message']
        
        UserConRev = user_contact_review(name=y_name, email=y_email, subject=y_subject, message=y_message)
        UserConRev.save()
        return redirect('contact')
    return render(request, 'nobodyknows/contact.html')