from django.shortcuts import render, HttpResponse, redirect 
from django.contrib import messages
from models import *
import bcrypt

def index(request):
    request.session.clear()
    
    return render(request, 'drinksrus/index.html')

def register(request):
    errors = User.objects.register(request.POST)
    if len(errors):
        for key, error in errors.iteritems():
            messages.error(request, error)
        return redirect('/')
    else:
        hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(first_name= request.POST['first_name'], last_name= request.POST['last_name'], email = request.POST['email'], password = hash1)
        return redirect('/')

def login(request):
    if request.method == "POST":
        errors = User.objects.login(request.POST)
        if len(errors) >0:
            return redirect('/')
        else:
            user= User.objects.get(email =request.POST['email'])
            request.session['id'] = user.id
            request.session['cart'] = {}
            return redirect('/home/'+str(1))
    else:
        return redirect('/')

def home(request, pagenum):
    if not 'id' in request.session:
        return redirect('/')
    else:
        context = {
            "categories": Category.objects.all(),
            "products": Product.objects.all().order_by("-created_at") [ (((int(pagenum)-1)) * 15 )  :(((int(pagenum)-1)) * 15 ) +15],
            "pagenum": pagenum,
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

def logout(request):
    del request.session['id']
    del request.session['cart']
    return redirect('/')