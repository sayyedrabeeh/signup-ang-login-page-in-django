from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.utils.cache import add_never_cache_headers
from django.views.decorators.cache import cache_control
from django.views.decorators.cache import never_cache
from django.contrib.auth.forms import AuthenticationForm  
from django.contrib.auth import login
from . models import Datastore

# @login_required

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    
    if 'username' not in request.session:
        return redirect('app1:login')
    # if not request.session.get('username'):
    #     return redirect('app1:login')
      
    return render(request, 'registration/home.html', {})



def custom_logout(request):
    logout(request)
    request.session.flush()
    response = redirect('app1:login')
    add_never_cache_headers(response) 
    
    def get_success_url(self):
        next = self.request.GET.get('next', '/')
        return next 
     
    return response
# @login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def authview(request):
    if 'username' in request.session:
        return redirect('app1:home') 
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            
            username = form.cleaned_data.get('username')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            if not (4 <= len(username) <= 6):
                form.add_error('username', 'Username must be between 4 and 6 characters long.')
            elif User.objects.filter(username=username).exists():
                form.add_error('username', 'This username already exists.')
            if len(password1) < 4:
                form.add_error('password1', 'Password must be at least 4 characters.')
            elif not any(char.isdigit() for char in password1):
                form.add_error('password1', 'Password must contain at least one positive integer.')
            elif password1 != password2:
                form.add_error('password2', 'Passwords do not match.')
            
            if not form.errors:
                form.save()
                ob=Datastore(name=username,password=password1)
                ob.save()
                return redirect('app1:login')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/signup.html', {'form': form})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_view(request):
    print('iam working outside of the post')
    
    if 'username' in  request.session:
        print("i  am workinggggg",request.session['username'])
        return redirect('app1:home')
    
    if request.method == 'POST':
        print('iam working')
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Log the user in
            print(form.get_user())
            print('type',type(form.get_user()))
            request.session['username'] = str(form.get_user())
            
            return redirect('app1:home')  # Redirect to a success page or the homepage after successful login
    else:
        form = AuthenticationForm()

    # Render the login form for GET requests or invalid POST requests
    return render(request, 'registration/login.html', {'form': form})