from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .utils import cookieKeranjang, keranjangData, tamuPesan
from django.views.decorators.csrf import csrf_exempt


def toko(request):
	data = keranjangData(request)

	keranjangBarangs = data['keranjangBarangs']
	pesan = data['pesan']
	barangs = data['barangs']

	produks = Produk.objects.all()
	context = {'produks':produks, 'keranjangBarangs':keranjangBarangs}
	return render(request, 'toko/toko.html', context)


def keranjang(request):
	data = keranjangData(request)

	keranjangBarangs = data['keranjangBarangs']
	pesan = data['pesan']
	barangs = data['barangs']

	context = {'barangs':barangs, 'pesan':pesan, 'keranjangBarangs':keranjangBarangs}
	return render(request, 'toko/keranjang.html', context)

def checkout(request):
	data = keranjangData(request)
	
	keranjangBarangs = data['keranjangBarangs']
	pesan = data['pesan']
	barangs = data['barangs']

	context = {'barangs':barangs, 'pesan':pesan, 'keranjangBarangs':keranjangBarangs}
	return render(request, 'toko/checkout.html', context)

def lihat(request):
	data = keranjangData(request)

	keranjangBarangs = data['keranjangBarangs']
	pesan = data['pesan']
	barangs = data['barangs']

	context = {'barangs':barangs, 'pesan':pesan, 'keranjangBarangs':keranjangBarangs}
	return render(request, 'toko/lihat.html', context)

@csrf_exempt
def updateBarang(request):
	data = json.loads(request.body)
	produkid = data['produkid']
	action = data['action']
	print('Action:', action)
	print('Produk:', produkid)

	pelanggan = request.user.pelanggan
	produk = Produk.objects.get(id=produkid)
	pesan, created = Pesan.objects.get_or_create(pelanggan=pelanggan, pesanselesai=False)

	pesanBarang, created = PesanBarang.objects.get_or_create(pesan=pesan, produk=produk)

	if action == 'add':
		pesanBarang.jumlah = (pesanBarang.jumlah + 1)
	elif action == 'remove':
		pesanBarang.jumlah = (pesanBarang.jumlah - 1)

	pesanBarang.save()

	if pesanBarang.jumlah <= 0:
		pesanBarang.delete()

	return JsonResponse('Barang ditambahkan', safe=False)

def prosesPesan(request):
	transaksi_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		pelanggan = request.user.pelanggan
		pesan, created = Pesan.objects.get_or_create(pelanggan=pelanggan, pesanselesai=False)
	else:
		pelanggan, pesan = tamuPesan(request, data)

	total = float(data['form']['total'])
	pesan.transaksi_id = transaksi_id

	if total == pesan.get_keranjang_total:
		pesan.pesanselesai = True
	pesan.save()

	if pesan.pengiriman == True:
		AlamatPengirim.objects.create(
		pelanggan=pelanggan,
		pesan=pesan,
		alamat=data['pengiriman']['alamat'],
		kota=data['pengiriman']['kota'],
		negara=data['pengiriman']['negara'],
		kodepos=data['pengiriman']['kodepos'],
		)

	return JsonResponse('Pembayaran Masuk..', safe=False)