from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

from django.urls import path

from . import views

urlpatterns = [
	path('', views.toko, name="toko"),
	path('keranjang/', views.keranjang, name="keranjang"),
	path('checkout/', views.checkout, name="checkout"),
	path('lihat/', views.lihat, name="lihat"),

	path('update_barang/', views.updateBarang, name="update_barang"),
	path('proses_pesan/', views.prosesPesan, name="proses_pesan"),
 	path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('images/favicon.ico')))

]