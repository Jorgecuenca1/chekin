from django.shortcuts import render
from django.db.utils import IntegrityError
from .models import Profile, Localidad, Boleta, CarShop
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth import login as auth_login, login
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Eventos
# Create your views here.
def listaboleta(request):
    user = request.user
    profile = get_object_or_404(Profile,user=user)
    boletas = profile.boleta.all()
    return render(request, 'user/listaboleta.html', { 'boletas': boletas, })
def delete_boleta(request, id):
    boleta = get_object_or_404(Boleta, id=id)
    boleta.delete()
    return redirect('/carshop')
def compra(request, id):
    carshop = get_object_or_404(CarShop, id=id)
    carshop.delete()
    return redirect('/')
def puntoventa(request, id):
    eventos = Eventos.objects.filter(id=id,created__lte=timezone.now()).order_by('created')
    evento = Eventos.objects.get(pk=id)
    puntoventas = evento.puntosventa.all()

    return render(request, 'user/puntoventa.html',{ 'eventos': eventos,'puntoventas':puntoventas, })

def carshop(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    cars = profile.car
    boletascars = cars.boleta.all()
    carshop = profile.car.id
    return render(request, 'user/carshop.html',{'carshop':carshop,'boletascars': boletascars, })
def eventos(request, id):
    eventos = Eventos.objects.filter(id=id,created__lte=timezone.now()).order_by('created')
    evento = Eventos.objects.get(pk=id)
    localidades = evento.localidad.all()
    evento = Eventos.objects.get(pk=id)
    boletas = evento.boleta.all()
    if request.method == 'POST':
        profile = Profile()
        user = request.user
        profile = Profile.objects.get(user=user)
        if profile.car == None:
            car = CarShop.objects.create()
        else:
            car = profile.car
        cantidad = int(request.POST['cantidad'])
        for x in range(cantidad):
            boleta = Boleta.objects.create(
                localidad=Localidad.objects.get(id=request.POST['localidad']))
            car.boleta.add(boleta)
        Profile.objects.filter(user=user).update(car=car)
        return redirect(f"/eventos/{id}")
    return render(request, 'user/eventos.html',{ 'eventos': eventos,'boletas':boletas,'localidades':localidades,})
def inicio(request):
    eventos = Eventos.objects.filter(created__lte=timezone.now()).order_by('created')

    return render(request, 'user/inicio.html', { 'eventos': eventos, })

def signup(request):
    """Sign up view."""
    if request.method == 'POST':
        username = request.POST['username']
        passwd = request.POST['passwd']
        passwd_confirmation = request.POST['passwd_confirmation']

        if passwd != passwd_confirmation:
            return render(request, 'users/signup.html', {'error': 'Password confirmation does not match'})

        try:
            user = User.objects.create_user(username=username, password=passwd)
        except IntegrityError:
            return render(request, 'signup.html', {'error': 'Username is already in user'})

        user.first_name = request.POST['name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()

        profile = Profile(user=user)
        profile.first_name = request.POST['name']
        profile.last_name = request.POST['name']
        profile.email = request.POST['email']
        profile.identification = request.POST['username']
        profile.last_name = request.POST['last_name']
        profile.save()

        return redirect('login')

    return render(request, 'user/signup.html')


def login_view(request):
    """Login view."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('inicio')
        else:
            return render(request, 'user/login.html', {'error': 'Invalid username and password'})

    return render(request, 'user/login.html')