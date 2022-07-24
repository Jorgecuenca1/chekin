from django.shortcuts import render
from django.db.utils import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum

from .forms import EventosForm
from .models import Profile, Localidad, Boleta, CarShop, Check, Category, Blog
from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Q
import qrcode
from io import BytesIO
from django.db.models import Count
import barcode
from barcode.writer import ImageWriter

from django.core.files.base import ContentFile

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

@login_required(login_url='/login')
def gestioneventos(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    eventos = profile.eventos.all()

    return render(request, 'ticket/gestioneventos.html', { 'eventos': eventos })
def faq(request):
    return render(request, 'ticket/faq.html',)

def terminosycondiciones(request):
    return render(request, 'ticket/term-condition.html',)

def politicas(request):
    return render(request, 'ticket/privacy-policy.html',)

def contactanos(request):
    return render(request, 'ticket/contact.html',)

def nosotros(request):
    return render(request, 'ticket/about.html',)
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

@login_required(login_url='/login')
def agregareventos(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    profiles = Profile.objects.filter(id=profile.id,created__lte=timezone.now()).order_by('created')
    if request.method == "POST":
        form = EventosForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.created = timezone.now()
            profile=Profile.objects.get(user=user)

            post.save()
            profile.eventos.add(post)
            return redirect('perfil')
    else:
        form = EventosForm()

    return render(request, 'ticket/agregarevento.html',{'profiles': profiles,'form': form})
@login_required(login_url='/login')
def perfil(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    profiles = Profile.objects.filter(id=profile.id,created__lte=timezone.now()).order_by('created')

    eventos = profile.eventos.all()

    return render(request, 'ticket/perfil.html',{ 'eventos': eventos,'profiles': profiles,})
@login_required(login_url='/login')
def listaboleta(request):
    user = request.user
    profile = get_object_or_404(Profile,user=user)
    boletas = profile.boleta.all()
    return render(request, 'ticket/event-ticket.html', { 'boletas': boletas, })

@login_required(login_url='/login')
def reporte(request,id):
    user = request.user
    profile = get_object_or_404(Profile,user=user)
    evento = Eventos.objects.get(id=id)
    boletas = Boleta.objects.filter(evento=evento,comprada='SI')
    return render(request, 'ticket/reporte.html', { 'boletas': boletas, })
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

@login_required(login_url='/login')
def carshop2(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    cars = profile.car
    boletascars = cars.boleta.all()
    carid = profile.car.id
    carshop = CarShop.objects.filter(id=carid).order_by('-id')
    cars = profile.car
    boletascars = cars.boleta.all()
    suma = 0
    for element in boletascars:
        print(element.id)
        suma = suma + int(element.localidad.price)
    suma = str(suma)
    if request.method == 'POST':
        profile = Profile()
        user = request.user
        profile = Profile.objects.get(user=user)
        user = request.user

        if profile.car == None:
            car = CarShop.objects.create()
        else:
            car = profile.car
        cantidad = int(request.POST['cantidad'])
        for x in range(cantidad):
            localidad = localidad = Localidad.objects.get(id=request.POST['localidad'])
            boleta = Boleta.objects.create(
                localidad=Localidad.objects.get(id=request.POST['localidad'], price=localidad.price), price=localidad.price, comprada = 'NO')
            car.boleta.add(boleta)
        Profile.objects.filter(user=user).update(car=car)
        return redirect(f"/carshop2")

    return render(request, 'ticket/event-checkout.html',{'carshop':carshop,'boletascars': boletascars, 'suma': suma,  })

@login_required(login_url='/login')
def carshop(request):
    user = request.user
    if user == None:
        return redirect('/')
    else:
        profile = Profile.objects.get(user=user)
        cars = profile.car

        carid = profile.car.id
        carshop = CarShop.objects.filter(id=carid).order_by('-id')
        cars = profile.car
        boletascars = cars.boleta.all()
        suma = 0
        for element in boletascars:
            print(element.id)
            suma = suma + int(element.localidad.price)
        suma = str(suma)
        if request.method == 'POST':
            profile = Profile()
            user = request.user
            profile = Profile.objects.get(user=user)
            user = request.user

            if profile.car == None:
                car = CarShop.objects.create()
            else:
                car = profile.car
            cantidad = int(request.POST['cantidad'])
            for x in range(cantidad):
                localidad = localidad = Localidad.objects.get(id=request.POST['localidad'])
                boletas = Boleta.objects.filter(localidad=localidad.id,comprada='SI')
                suma2=0
                for element in boletascars:
                    suma2 = suma2 + 1
                suma2 = suma2 + cantidad
                if int(localidad.capacity) < suma2:
                    return redirect('/')
                else:
                    boleta = Boleta.objects.create(
                    localidad=Localidad.objects.get(id=request.POST['localidad'], price=localidad.price), price=localidad.price, comprada = 'NO',evento=localidad.evento)
                    car.boleta.add(boleta)
            Profile.objects.filter(user=user).update(car=car)
            return redirect(f"/carshop")

    return render(request, 'ticket/event-checkout.html',{'carshop':carshop,'boletascars': boletascars, 'suma': suma,  })

class check(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get_queryset(self):
        return Check.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = CheckSerializer(data=request.data)
        general_data = request.data
        if serializer.is_valid():
            serializer.save()
            if serializer.data['sucess'] == 'COMPLETED':
                user = request.user
                profile = Profile.objects.get(user=user)
                cars = profile.car
                boletascars = cars.boleta.all()
                for element in boletascars:
                    print(element.id)
                    profile.boleta.add(element.id)
                    Boleta.objects.filter(id=element.id).update(comprada='SI')
                carnew = CarShop.objects.create()
                profile.historialcar.add(cars)
                Profile.objects.filter(id=profile.id).update(car=carnew)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def eventos2(request, id):

    eventos = Eventos.objects.filter(id=id,created__lte=timezone.now()).order_by('created')
    evento = Eventos.objects.get(pk=id)
    localidades = evento.localidad.all()
    evento = Eventos.objects.get(pk=id)
    boletas = evento.boleta.all()
    participantes = evento.participante.all()
    sponsors = evento.sponsor.all()

    if request.method == 'POST':
        profile = Profile()
        user = request.user
        profile = Profile.objects.get(user=user)
        user = request.user

        if profile.car == None:
            car = CarShop.objects.create()
        else:
            car = profile.car
        cantidad = int(request.POST['cantidad'])
        for x in range(cantidad):
            localidad = localidad=Localidad.objects.get(id=request.POST['localidad'])
            boleta = Boleta.objects.create(
                localidad=Localidad.objects.get(id=request.POST['localidad'],price= localidad.price))
            car.boleta.add(boleta)
        Profile.objects.filter(user=user).update(car=car)
        return redirect(f"/eventos/{id}")
    return render(request, 'ticket/event-details.html',{ 'eventos': eventos,'boletas':boletas,'localidades':localidades})

def eventos(request, id):

    eventos = Eventos.objects.filter(id=id,created__lte=timezone.now()).order_by('created')
    evento = Eventos.objects.get(pk=id)
    localidades = Localidad.objects.filter(evento=evento,created__lte=timezone.now()).order_by('created')
    evento = Eventos.objects.get(pk=id)
    participantes = evento.participante.all()
    sponsors = evento.sponsor.all()
    if request.method == 'POST':
        localidad = localidad = Localidad.objects.get(id=request.POST['localidad'])
        boletas = Boleta.objects.filter(localidad=localidad, created__lte=timezone.now()).order_by('created')
        suma = 0
        for element in boletas:
            suma = suma + 1
        suma = str(suma)
        queryset = Boleta.objects.annotate(number_of_localidads=Count('localidad'))
        profile = Profile()
        user = request.user
        profile = Profile.objects.get(user=user)
        user = request.user

        if profile.car == None:
            car = CarShop.objects.create()
        else:
            car = profile.car
        cantidad = int(request.POST['cantidad'])
        for x in range(cantidad):
            localidad = localidad=Localidad.objects.get(id=request.POST['localidad'])
            boleta = Boleta.objects.create(
                localidad=Localidad.objects.get(id=request.POST['localidad'],price= localidad.price))
            car.boleta.add(boleta)
        Profile.objects.filter(user=user).update(car=car)
        return redirect(f"/eventos/{id}")
    return render(request, 'ticket/event-details.html',{ 'eventos': eventos,'localidades':localidades,'participantes':participantes,'sponsors':sponsors,})
def inicio(request):
    eventos = Eventos.objects.filter(created__lte=timezone.now()).order_by('created')
    blogs = Blog.objects.filter(created__lte=timezone.now()).order_by('created')
    categorias = Category.objects.filter(created__lte=timezone.now()).order_by('created')
    query = request.GET.get('search_box')
    pais = request.GET.get('filter1')

    if query:
        eventos = Eventos.objects.all()
        query = query.split()
        q_obj = Q(
            *[Q(('title__icontains', item)) for item in query],
            _connector=Q.OR
        )
        eventos = Eventos.objects.filter(q_obj)
    return render(request, 'ticket/index.html', { 'eventos': eventos,'categorias': categorias, 'blogs': blogs, })
def inicio2(request):
    eventos = Eventos.objects.filter(created__lte=timezone.now()).order_by('created')
    categorias = Category.objects.filter(created__lte=timezone.now()).order_by('created')
    query = request.GET.get('search_box')
    pais = request.GET.get('filter1')

    if query:
        eventos = Eventos.objects.all()
        query = query.split()
        q_obj = Q(
            *[Q(('title__icontains', item)) for item in query],
            _connector=Q.OR
        )
        eventos = Eventos.objects.filter(q_obj)
    return render(request, 'ticket/index.html', {'eventos': eventos, 'categorias': categorias, })

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
        car = CarShop.objects.create()
        profile = Profile(user=user,car=car)
        profile.first_name = request.POST['name']
        profile.email = request.POST['email']
        profile.last_name = request.POST['last_name']
        profile.save()

        return redirect('login')

    return render(request, 'ticket/register.html')
def signupEnterprise(request):
    """Sign up view."""
    if request.method == 'POST':
        username = request.POST['username']
        passwd = request.POST['passwd']
        passwd_confirmation = request.POST['passwd_confirmation']

        if passwd != passwd_confirmation:
            return render(request, 'ticket/registerempresa.html', {'error': 'Password confirmation does not match'})

        try:
            user = User.objects.create_user(username=username, password=passwd)
        except IntegrityError:
            return render(request, 'ticket/registerempresa.html', {'error': 'Username is already in user'})
        user.first_name = request.POST['name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()

        profile = Profile(user=user)
        profile.first_name = request.POST['name']
        profile.last_name = request.POST['last_name']
        profile.nit = request.POST['nit']
        profile.email = request.POST['email']
        profile.tipo = 'Persona Juridica'
        profile.razon_social = request.POST['razon']
        profile.save()

        return redirect('login')

    return render(request, 'ticket/registerempresa.html', )

def login_view(request):
    """Login view."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.profile.tipo == 'Persona Juridica':
                return redirect('perfil')
            else:
                return redirect('inicio')
        else:
            return render(request, 'user/login.html', {'error': 'Invalid username and password'})

    return render(request, 'ticket/login.html')

def detalleboleta(request, id):
    user = request.user

    bc = Boleta(id=id)

    upc = barcode.get('upc', '12345678901', writer=ImageWriter())

    i = upc.render()  # <PIL.Image.Image image mode=RGB size=523x280 at 0x7FAE2B471320>

    image_io = BytesIO()

    i.save(image_io, format='PNG')

    image_name = 'test.png'

    bc.code = i
    profiles = Profile.objects.filter(user=user, created__lte=timezone.now()).order_by('created')
    boletas = Boleta.objects.filter(id=id).order_by('created')
    return render(request, 'user/detalleboleta.html', {'boletas': boletas, 'profiles': profiles, })
