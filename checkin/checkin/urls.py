"""checkin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from users import views as users_views
from django.urls import path
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', users_views.inicio, name='inicio'),
    path('inicio2', users_views.inicio2, name='inicio2'),
    path('eventos2/<int:id>/', users_views.eventos2, name='eventos2'),
    path('eventos/<int:id>/', users_views.eventos, name='eventos'),
    path('puntoventa/<int:id>/', users_views.puntoventa, name='puntoventa'),
    path('listaboleta', users_views.listaboleta, name='listaboleta'),
    path('carshop', users_views.carshop, name='carshop'),
    path('carshop2', users_views.carshop2, name='carshop2'),
    path('checkout/', users_views.checkout, name='checkout'),
    path('detalleboleta/<int:id>/', users_views.detalleboleta, name='detalleboleta'),
    path('process-payment/', users_views.process_payment, name='process_payment'),
    path('payment-done/', users_views.payment_done, name='payment_done'),
    path('payment-cancelled/', users_views.payment_canceled, name='payment_cancelled'),
    path('signup', users_views.signup, name='signup'),
    path('login', users_views.login_view, name='login'),
    path('boleta/<int:id>/delete', users_views.delete_boleta, name='delete_boleta'),
    path('api/',users_views.check.as_view(), name='check'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
