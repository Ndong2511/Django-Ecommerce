import json
from .models import *

def cookieKeranjang(request):

	#Create empty keranjang for now for non-logged in user
	try:
		keranjang = json.loads(request.COOKIES['keranjang'])
	except:
		keranjang = {}
		print('keranjang:', keranjang)

	barangs = []
	pesan = {'get_keranjang_total':0, 'get_keranjang_barangs':0, 'pengiriman':False}
	keranjangBarangs = pesan['get_keranjang_barangs']

	for i in keranjang:
		#We use try block to prevent barangs in keranjang that may have been removed from causing error
		try:	
			if(keranjang[i]['jumlah']>0): #barangs with negative jumlah = lot of freebies  
				keranjangBarangs += keranjang[i]['jumlah']

				produk = Produk.objects.get(id=i)
				total = (produk.harga * keranjang[i]['jumlah'])

				pesan['get_keranjang_total'] += total
				pesan['get_keranjang_barangs'] += keranjang[i]['jumlah']

				barang = {
				'id':produk.id,
				'produk':{'id':produk.id,'nama':produk.nama, 'harga':produk.harga, 
				'imageURL':produk.imageURL}, 'jumlah':keranjang[i]['jumlah'],
				'digital':produk.digital,'get_total':total,
				}
				barangs.append(barang)

				if produk.digital == False:
					pesan['pengiriman'] = True
		except:
			pass
			
	return {'keranjangBarangs':keranjangBarangs ,'pesan':pesan, 'barangs':barangs}

def keranjangData(request):
	if request.user.is_authenticated:
		pelanggan = request.user.pelanggan
		pesan, created = Pesan.objects.get_or_create(pelanggan=pelanggan, pesanselesai=False)
		barangs = pesan.pesanbarang_set.all()
		keranjangBarangs = pesan.get_keranjang_barangs
	else:
		cookieData = cookieKeranjang(request)
		keranjangBarangs = cookieData['keranjangBarangs']
		pesan = cookieData['pesan']
		barangs = cookieData['barangs']

	return {'keranjangBarangs':keranjangBarangs ,'pesan':pesan, 'barangs':barangs}

	
def tamuPesan(request, data):
	nama = data['form']['nama']
	email = data['form']['email']

	cookieData = cookieKeranjang(request)
	barangs = cookieData['barangs']

	pelanggan, created = Pelanggan.objects.get_or_create(
			email=email,
			)
	pelanggan.nama = nama
	pelanggan.save()

	pesan = Pesan.objects.create(
		pelanggan=pelanggan,
		pesanselesai=False,
		)

	for barang in barangs:
		produk = Produk.objects.get(id=barang['id'])
		pesanBarang = PesanBarang.objects.create(
			produk=produk,
			pesan=pesan,
			jumlah=(barang['jumlah'] if barang['jumlah']>0 else -1*barang['jumlah']), # negative jumlah = freebies
		)
	return pelanggan, pesan

