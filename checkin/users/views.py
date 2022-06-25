from django.shortcuts import render
from django.db.utils import IntegrityError
from django.views.decorators.csrf import csrf_exempt

from .models import Profile, Localidad, Boleta, CarShop, Check
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth import login as auth_login, login
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Eventos
from django.views.generic import FormView
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import CheckSerializer


@csrf_exempt
def payment_done(request):
    return render(request, 'payment_done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment_cancelled.html')

def process_payment(request):
    car = get_object_or_404(CarShop, id=5)
    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': 0.1,
        'item_name': 'Car {}'.format(car.id),
        'invoice': str(car.id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('payment_cancelled')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('payment_cancelled')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'process_payment.html', {'car': car, 'form': form})

def checkout(request):
    if request.method == 'POST':
        user = request.user
        profile = Profile.objects.get(user=user)
        cars = profile.car

        request.session['card_id'] = cars.id
        return redirect('process_payment')


    else:
        form = CheckoutForm()
        return render(request, 'ecommerce_app/checkout.html', locals())

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
@login_required
def carshop(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    cars = profile.car
    boletascars = cars.boleta.all()
    carid = profile.car.id
    carshop = CarShop.objects.filter(id=carid).order_by('-id')
    if request.method == 'POST':
        user = request.user
        profile = Profile.objects.get(user=user)
        cars = profile.car

        request.session['card_id'] = cars.id
        return redirect('process_payment')

    return render(request, 'user/carshop.html',{'carshop':carshop,'boletascars': boletascars, })

class check(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get_queryset(self):
        return Check.objects.all()

    def post(self, request, *args, **kwargs):
        check = request.data
        serializer = CheckSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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