from django.shortcuts import render,redirect
from .forms import RegistrationForm
from .models import Accounts
from django.contrib import  messages,auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from carts.views import _cart_id
from carts.models import Cart
from carts.models import Cart_item
from orders.models import Order
import requests


#verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage 


def register(request):
    if request.method=='POST':
        form= RegistrationForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            phone_number=form.cleaned_data['phone_number']
            password=form.cleaned_data['password']
            username=email.split("@")[0]
            
            user = Accounts.object.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.phone_number=phone_number
            user.save()
            
            #USER ACTIVATION
            
            current_site=get_current_site(request)
            mail_subject='Please activate your account'
            message=render_to_string('accounts/activation.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
                
            })
            to_email=email
            send_email= EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            #messages.success(request,'Thank you for registering with us we have sent you a verification email to your email address please verify it.')
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form=RegistrationForm()
    context={
        'form': form,
    }
    return render(request,'accounts/register.html',context)

def login(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        
        user=auth.authenticate(email=email,password=password)
        
        if user is not None:
            try:
                cart=Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exist=Cart_item.objects.filter(cart=cart).exists()
                if is_cart_item_exist:
                    cart_item=Cart_item.objects.filter(cart=cart)
                    
                    for item in cart_item:
                        item.user=user
                        item.save()
                
            except:
                pass
            auth.login(request,user)
            messages.success(request,"You are now logged in")
            url=request.META.get('HTTP_REFERER')
            try:
                query=requests.utils.urlparse(url).query
                
                #next=cart/checkout
                params= dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage=params['next']
                    return redirect(nextPage)
               
            except:
                return redirect('dashboard')
        else:
            messages.error(request,'Invalid Credentials')
            return redirect('login')
    return render(request,'accounts/login.html')



@login_required(login_url='login')
def logout(request):
    
    auth.logout(request)
    messages.success(request,"You have Logged out")
    return redirect('login')

def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Accounts._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Accounts.DoesNotExist):
        user=None
        
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        
        messages.error(request,'Invalid activation link')
        return redirec('register')
    
@login_required(login_url='login')
def dashboard(request):
    orders=Order.objects.order_by('-created_at').filter(user_id=request.user.id,is_ordered=True)
    orders_count=orders.count()
    context={
        'orders_count':orders_count,
    }
    return render(request,'accounts/dashboard.html',context)
        
   
