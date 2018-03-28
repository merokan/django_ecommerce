from django.shortcuts import render, HttpResponse, redirect 
from django.contrib import messages
from models import *
import bcrypt
import math

def index(request):
    request.session.clear()
    
    return render(request, 'drinksrus/index.html')

def register(request):
    errors = User.objects.register(request.POST)
    if len(errors):
        for error in errors.itervalues():
            messages.error(request, error)
        return redirect('/')
    else:
        hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(first_name= request.POST['first_name'], last_name= request.POST['last_name'], email = request.POST['email'], password = hash1)
        users = User.objects.all()
        if len(users) == 1:
            user.user_level = 3
            user.save()
        return redirect('/home/1')

def login(request):
    if request.method == "POST":
        userList=User.objects.filter(email=request.POST['email'])
        errors = User.objects.login(request.POST)

        if len(errors)> 0: # if invalid credentials
            for error in errors.itervalues():
                messages.error(request, error)
            return redirect('/')
        else: # if no error
            user = userList[0]
            cart = {}
            request.session['id'] = user.id
            request.session['cart'] = cart
            return redirect('/home/1')
    else:
        return redirect('/')

def admin_login(request):
    request.session.clear()

    if request.method == "POST":
        userList=User.objects.filter(email=request.POST['email'])
        errors = User.objects.admin_login(request.POST)

        if len(errors)> 0: # if invalid credentials
            for error in errors.itervalues():
                messages.error(request, error)
            return redirect('/admin_login')
        else: # if no error
            user = userList[0]
            request.session['id'] = user.id
            return render(request, 'drinksrus/admin_login.html')
    else:
        return render(request, 'drinksrus/admin_login.html')
    

def admindashboard(request):
    return render(request, "drinksrus/admin_dashboard.html")

def home(request, pagenum):
    if not 'id' in request.session:
        return redirect('/')
    else:
        #finding how many pages necessery
        totalpages = int(math.ceil(Product.objects.all().count()/15))
        pagelist = [0] * totalpages
        for i in range (totalpages):
            pagelist[i] = i+1
        
        #populating dictionary
        context = {
            "categories": Category.objects.all(),
            "products": Product.objects.all(),#.order_by("-created_at") [ (((int(pagenum)-1)) * 15 )  :(((int(pagenum)-1)) * 15 ) +15],
            "pagenum": pagenum,
            "pagelist": pagelist,
            "cart": request.session['cart']
        }
        return render(request, 'drinksrus/home.html', context)
def search (request):
    if request.method =="POST":
        context ={
            "products": Product.objects.filter(item__contains = request.POST['searchName']),
            "categories": Category.objects.all(),
            "cart": request.session['cart']
        }
        return render(request, 'drinksrus/home.html', context)
    else:
        return redirect('/')
def product(request, prodnum):
    context ={

    }
    return render (request,'drinksrus/product.html',context)
def logout(request):
    del request.session['id']
    del request.session['cart']
    return redirect('/')