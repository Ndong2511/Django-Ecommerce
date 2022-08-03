from django.contrib import admin

from .models import *

admin.site.register(Pelanggan)
admin.site.register(Produk)
admin.site.register(Pesan)
admin.site.register(PesanBarang)
admin.site.register(AlamatPengirim)