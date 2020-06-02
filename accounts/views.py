from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from shop.models import Profile
from django.contrib import messages
# Create your views here.

def register(request):

    if (request.method == "POST"):
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        username=request.POST['username']
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']

        if(password==confirm_password):

            if User.objects.filter(username=username).exists():
                messages.info(request, "This username is already taken!")
                return render(request, 'register.html')

            elif User.objects.filter(email=email).exists():
                messages.info(request, "This email ID is already registered!!")
                return render(request, 'register.html')

            else:
                user = User.objects.create_user(first_name=first_name, last_name=last_name,email=email,username=username,password=password)

                user.save()
                Profile.objects.create(user=user,pr='C')
                print("user is hereeeeeeeeeeeeeeee")
                return render(request, 'login.html')
        else:
            messages.info(request, "The two passwords don't match! Please enter correct password.")
            return render(request, 'register.html' )


    else:

        return render(request, 'register.html')#, {'form': form})
    #return render(request, 'SignUp.html')

def login(request):
        if(request.method=="POST"):

            username=request.POST['username']
            password=request.POST['password']

            user =  auth.authenticate(username=username,password=password)

            if(user.profile.pr=='C'):
                auth.login(request, user)
                return redirect('/')
            else:
                messages.info(request, "Incorrect Credentials. Please enter the correct ones!")
                return render(request, 'login.html')


        else:

            return render(request, 'login.html')

def landing(request):
#    form = SignupForm()
    return render(request, 'index.html')#, {'form': form})
    #return render(request, 'SignUp.html')

def logout(request):
    auth.logout(request)
    return render(request, 'index.html')#, {'form': form})
    #return render(request, 'SignUp.html')