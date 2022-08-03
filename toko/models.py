from django.db import models
from django.contrib.auth.models import User

class Pelanggan(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	nama = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200)

	def __str__(self):
		return self.nama


class Produk(models.Model):
	nama = models.CharField(max_length=200)
	harga = models.FloatField()
	digital = models.BooleanField(default=False, null=True, blank=True)
	image = models.ImageField(null=True, blank=True)

	def __str__(self):
		return self.nama

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url


class Pesan(models.Model):
	pelanggan = models.ForeignKey(Pelanggan, on_delete=models.SET_NULL, null=True, blank=True)
	tanggal_pesan = models.DateTimeField(auto_now_add=True)
	pesanselesai = models.BooleanField(default=False)
	transaksi_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)

	@property
	def pengiriman(self):
		pengiriman = False
		pesanbarangs = self.pesanbarang_set.all()
		for i in pesanbarangs:
			if i.produk.digital == False:
				pengiriman = True
		return pengiriman

	@property
	def get_keranjang_total(self):
		pesanbarangs = self.pesanbarang_set.all()
		total = sum([barang.get_total for barang in pesanbarangs])
		return total

	@property
	def get_keranjang_barangs(self):
		pesanbarangs = self.pesanbarang_set.all()
		total = sum([barang.jumlah for barang in pesanbarangs])
		return total


class PesanBarang(models.Model):
	produk = models.ForeignKey(Produk, on_delete=models.SET_NULL, null=True)
	harga = models.ForeignKey(Pesan, on_delete=models.SET_NULL, null=True)
	jumlah = models.IntegerField(default=0, null=True, blank=True)
	tanggaltambah = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.produk.harga * self.jumlah
		return total


class AlamatPengirim(models.Model):
	pelanggan = models.ForeignKey(Pelanggan, on_delete=models.SET_NULL, null=True)
	harga = models.ForeignKey(Pesan, on_delete=models.SET_NULL, null=True)
	alamat = models.CharField(max_length=200, null=False)
	kota = models.CharField(max_length=200, null=False)
	negara = models.CharField(max_length=200, null=False)
	kodepos = models.CharField(max_length=200, null=False)
	tanggaltambah = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.alamat
