SPEC.md — Kalkulator Subnet & VLSM Web (SMK TKJ)
1. Tujuan
Dokumen ini mendefinisikan spesifikasi teknis untuk aplikasi Kalkulator Subnet & VLSM berbasis web yang ditujukan bagi guru SMK Teknik Komputer dan Jaringan (TKJ). Aplikasi berfungsi sebagai alat bantu pengajaran dan verifikasi otomatis atas hasil perhitungan pengalamatan IPv4 (FLSM/CIDR dan VLSM) dengan aturan yang eksplisit, deterministik, dan dapat diuji secara otomatis.

Arsitektur & Struktur Berkas
Runtime: Python 3.12+

Framework Backend: FastAPI

Frontend: Satu halaman statis (index.html) tanpa dependensi framework eksternal yang rumit.

Struktur Direktori Minimal:

main.py — Seluruh logika validasi, perhitungan subnet/VLSM, dan definisi endpoint FastAPI.

test_main.py — Unit test dan integration test berbasis pytest.

index.html — Antarmuka pengguna satu halaman.

2. Aturan Validasi
Seluruh fungsi inti wajib memvalidasi input secara ketat sebelum melakukan operasi aritmetika biner. Setiap pelanggaran aturan berikut wajib melempar pengecualian ValueError dengan pesan deskriptif dalam bahasa Indonesia.

2.1. Validasi Alamat IPv4 (ip)
Tipe data harus berupa str.

Tidak boleh mengandung spasi di awal, tengah, maupun akhir string (tidak boleh di-trim diam-diam; " 192.168.1.1" dianggap tidak valid).

Harus terdiri dari tepat 4 oktet yang dipisahkan oleh karakter titik (.).

Setiap oktet hanya boleh berisi digit desimal (0–9), tidak boleh kosong, tidak boleh bertanda (+/-).

Nilai numerik setiap oktet berada pada rentang inklusif 0 hingga 255.

Larangan Leading Zero: Oktet yang memiliki panjang lebih dari 1 karakter tidak boleh diawali angka 0 (contoh: "0" valid, "00" atau "01" ditolak).

2.2. Validasi Prefix (prefix)
Tipe data harus berupa bilangan bulat (int), dan bukan tipe bool (True/False ditolak meskipun merupakan subclass int di Python).

Nilai berada pada rentang inklusif 0 hingga 32.

2.3. Validasi Input VLSM
network_cidr:

Harus berformat "<ip>/<prefix>" dengan tepat satu pemisah /, tanpa spasi.

Bagian <ip> wajib lolos aturan 2.1 dan <prefix> wajib lolos aturan 2.2.

Alamat IP yang diberikan wajib merupakan Network Address yang sah untuk prefix tersebut (hasil ip AND mask == ip). Contoh: "192.168.1.0/24" valid, sedangkan "192.168.1.5/24" wajib ditolak.

kebutuhan_host:

Harus berupa list yang tidak kosong (len(kebutuhan_host) >= 1).

Setiap elemen di dalam list harus berupa bilangan bulat (int, bukan bool) dengan nilai minimal 1 (kebutuhan >= 1).

Total alokasi blok seluruh kebutuhan tidak boleh melebihi kapasitas total alamat pada network_cidr induk.

3. Kontrak Fungsi (main.py)
3.1. hitung_subnet(ip: str, prefix: int) -> dict
Menghitung parameter jaringan IPv4 berdasarkan alamat IP dan panjang prefix.

Parameter:

ip (str): Alamat IPv4 dotted-decimal.

prefix (int): Panjang prefix CIDR (0–32).

Aturan Perhitungan:

mask: Subnet mask dalam format dotted-decimal hasil pergeseran bit 1 sebanyak prefix dari kiri (contoh /24 -> "255.255.255.0").

network: Hasil operasi bitwise IP_int & Mask_int dalam format dotted-decimal.

Kasus Umum (0 <= prefix <= 30):

broadcast: Hasil operasi bitwise Network_int | (~Mask_int & 0xFFFFFFFF) dalam format dotted-decimal.

first_host: Network_int + 1 dalam format dotted-decimal.

last_host: Broadcast_int - 1 dalam format dotted-decimal.

usable_hosts: 
2
(
32
−
prefix
)
−
2
2 
(32−prefix)
 −2 (int).

Kasus Khusus /31 (RFC 3021 — Point-to-Point Link):

broadcast: None

first_host: Network_int dalam format dotted-decimal.

last_host: Network_int + 1 dalam format dotted-decimal.

usable_hosts: 2 (int).

Kasus Khusus /32 (Host Route):

broadcast: None

first_host: ip (sama dengan network).

last_host: ip (sama dengan network).

usable_hosts: 1 (int).

Nilai Kembalian (dict):

JSON
{
  "mask": "str",
  "network": "str",
  "broadcast": "str | None",
  "first_host": "str",
  "last_host": "str",
  "usable_hosts": "int"
}
Pengecualian: Melempar ValueError jika input tidak valid.

3.2. alokasi_vlsm(network_cidr: str, kebutuhan_host: list[int]) -> list[dict]
Melakukan alokasi blok subnet dengan metode Variable Length Subnet Mask (VLSM).

Parameter:

network_cidr (str): Blok jaringan induk dalam notasi CIDR (misal "192.168.1.0/24").

kebutuhan_host (list[int]): Daftar jumlah host yang dibutuhkan untuk setiap segmen/subnet.

Aturan Algoritma:

Validasi network_cidr dan kebutuhan_host sesuai Bagian 2.3.

Urutkan daftar kebutuhan_host secara menurun (descending, dari kebutuhan terbesar ke terkecil).

Mulai pointer alamat saat ini (current_ip) dari alamat jaringan network_cidr.

Untuk setiap nilai kebutuhan:

Tentukan ukuran blok (jumlah total IP) sebagai pangkat 2 terkecil yang memenuhi syarat 
ukuran_blok
≥
kebutuhan
+
2
ukuran_blok≥kebutuhan+2, dengan ukuran blok minimal 4 (setara prefix maksimal /30).

Hitung prefix baru: 
prefix_baru
=
32
−
log
⁡
2
(
ukuran_blok
)
prefix_baru=32−log 
2
​
 (ukuran_blok).

Pastikan current_ip + ukuran_blok - 1 tidak melampaui alamat broadcast dari network_cidr induk. Jika melampaui, segera lempar ValueError.

Panggil hitung_subnet(current_ip_str, prefix_baru) untuk mendapatkan detail subnet.

Susun kamus hasil yang menggabungkan kebutuhan, network_cidr (format "{network}/{prefix_baru}"), dan seluruh kunci hasil dari hitung_subnet.

Majukan current_ip sebesar ukuran_blok untuk alokasi berikutnya.

Nilai Kembalian (list[dict]):
Setiap elemen dalam list berurutan dari blok terbesar dan memiliki struktur kunci:

JSON
{
  "kebutuhan": "int",
  "network_cidr": "str",
  "mask": "str",
  "network": "str",
  "broadcast": "str",
  "first_host": "str",
  "last_host": "str",
  "usable_hosts": "int"
}
Pengecualian: Melempar ValueError jika format salah, network_cidr bukan Network Address valid, daftar kosong/berisi nilai < 1, atau kapasitas blok induk tidak mencukupi.

4. Kontrak API (FastAPI)
Seluruh respons JSON menggunakan encoding UTF-8. Apabila terjadi ValueError pada logika domain atau kegagalan validasi parameter input, API wajib mengembalikan status HTTP 400 Bad Request dengan payload JSON: {"detail": "<pesan error>"}.

4.1. GET /
Deskripsi: Menyajikan halaman antarmuka web utama.

Respons Sukses (200 OK): Konten HTML dari berkas index.html (Content-Type: text/html).

4.2. GET /api/subnet
Deskripsi: Menghitung informasi subnet tunggal.

Query Parameters:

ip (str, wajib): Alamat IPv4 (contoh: 172.16.5.130).

prefix (int, wajib): Prefix jaringan (contoh: 25).(Catatan: Jika parameter prefix tidak dapat dikonversi menjadi integer, misal "abc" atau kosong, endpoint harus tetap mengembalikan HTTP 400 dengan field "detail", bukan HTTP 422 bawaan FastAPI).

Respons Sukses (200 OK):

JSON
{
  "mask": "255.255.255.128",
  "network": "172.16.5.128",
  "broadcast": "172.16.5.255",
  "first_host": "172.16.5.129",
  "last_host": "172.16.5.254",
  "usable_hosts": 126
}
Respons Error (400 Bad Request):

JSON
{
  "detail": "Oktet IP harus berada dalam rentang 0-255."
}
4.3. POST /api/vlsm
Deskripsi: Menghitung pembagian subnet VLSM dari satu blok induk.

Request Body (application/json):

JSON
{
  "network": "192.168.1.0/24",
  "kebutuhan_host": [100, 50, 20, 2]
}
Respons Sukses (200 OK): Array JSON berisi objek hasil alokasi_vlsm yang telah terurut dari kebutuhan terbesar.

JSON
[
  {
    "kebutuhan": 100,
    "network_cidr": "192.168.1.0/25",
    "mask": "255.255.255.128",
    "network": "192.168.1.0",
    "broadcast": "192.168.1.127",
    "first_host": "192.168.1.1",
    "last_host": "192.168.1.126",
    "usable_hosts": 126
  }
]
Respons Error (400 Bad Request):

JSON
{
  "detail": "Kapasitas jaringan induk tidak mencukupi untuk seluruh kebutuhan host."
}
5. Halaman Web (index.html)
Antarmuka pengguna berupa satu halaman web tunggal yang bersih, responsif, dan mudah dibaca oleh guru maupun siswa saat praktik di kelas.

5.1. Struktur & Navigasi Mode
Header: Judul aplikasi (Kalkulator Subnet & VLSM — TKJ) dan deskripsi singkat.

Switcher Tab/Mode: Dua tombol tab untuk berpindah tampilan tanpa memuat ulang halaman:

Mode Subnet (CIDR)

Mode VLSM

5.2. Komponen Mode Subnet
Form Input:

Input teks untuk Alamat IPv4 (placeholder: 192.168.1.10).

Input angka/dropdown untuk Prefix (0 sampai 32, default 24).

Tombol Hitung Subnet.

Area Hasil:

Tabel ringkasan menampilkan label yang jelas: Subnet Mask, Network Address, Broadcast Address (tampilkan "- (Point-to-Point)" atau "-" jika bernilai null), Range Host (first_host - last_host), dan Jumlah Host Usable.

5.3. Komponen Mode VLSM
Form Input:

Input teks untuk Network Induk (CIDR) (placeholder: 192.168.1.0/24).

Daftar input Kebutuhan Host dinamis (mendukung tombol "+ Tambah Subnet" dan tombol hapus per baris, atau input dipisahkan koma).

Tombol Hitung VLSM.

Area Hasil:

Tabel multi-kolom yang menampilkan seluruh hasil alokasi terurut dari kebutuhan terbesar: No, Kebutuhan Host, Network/Prefix, Subnet Mask, Network Address, Range Host, Broadcast Address, dan Host Tersedia.

5.4. Penanganan Error UI
Setiap kegagalan dari API (HTTP 400) wajib ditampilkan dalam kotak peringatan visual yang mencolok (berwarna merah lembut) tepat di atas area hasil, menampilkan teks persis dari properti detail.

Saat error terjadi, hasil perhitungan sebelumnya harus disembunyikan agar tidak membingungkan pengguna.

6. Tabel Test Case (test_main.py)
Daftar berikut menjadi acuan wajib pengujian unit (pemanggilan fungsi langsung) dan pengujian endpoint API menggunakan pytest.

ID	Kategori	Kasus Uji	Input	Hasil yang Diharapkan	Tipe
TC-01	Subnet	Subnetting Kelas B lintas batas	ip="172.16.5.130", prefix=25	mask="255.255.255.128", network="172.16.5.128", broadcast="172.16.5.255", first_host="172.16.5.129", last_host="172.16.5.254", usable_hosts=126	Sukses
TC-02	Subnet	Subnetting terkecil standar (/30)	ip="10.0.0.0", prefix=30	mask="255.255.255.252", network="10.0.0.0", broadcast="10.0.0.3", first_host="10.0.0.1", last_host="10.0.0.2", usable_hosts=2	Sukses
TC-03	Subnet	Point-to-Point RFC 3021 (/31)	ip="192.168.1.0", prefix=31	mask="255.255.255.254", network="192.168.1.0", broadcast=None, first_host="192.168.1.0", last_host="192.168.1.1", usable_hosts=2	Sukses
TC-04	Subnet	Host Route tunggal (/32)	ip="192.168.1.5", prefix=32	mask="255.255.255.255", network="192.168.1.5", broadcast=None, first_host="192.168.1.5", last_host="192.168.1.5", usable_hosts=1	Sukses
TC-05	Subnet	Default Route (/0)	ip="0.0.0.0", prefix=0	mask="0.0.0.0", network="0.0.0.0", broadcast="255.255.255.255", first_host="0.0.0.1", last_host="255.255.255.254", usable_hosts=4294967294	Sukses
TC-06	Validasi	Oktet IP melebihi 255	ip="256.1.1.1", prefix=24	ValueError / HTTP 400 dengan detail	Error
TC-07	Validasi	Oktet mengandung leading zero	ip="192.168.01.1", prefix=24	ValueError / HTTP 400 dengan detail	Error
TC-08	Validasi	Oktet kurang dari 4 bagian	ip="192.168.1", prefix=24	ValueError / HTTP 400 dengan detail	Error
TC-09	Validasi	Input bukan angka / huruf	ip="abc", prefix=24	ValueError / HTTP 400 dengan detail	Error
TC-10	Validasi	Input string kosong atau spasi	ip="" atau ip=" 192.168.1.1", prefix=24	ValueError / HTTP 400 dengan detail	Error
TC-11	Validasi	Prefix di atas batas maksimum	ip="192.168.1.1", prefix=33	ValueError / HTTP 400 dengan detail	Error
TC-12	Validasi	Prefix bernilai negatif	ip="192.168.1.1", prefix=-1	ValueError / HTTP 400 dengan detail	Error
TC-13	VLSM	Alokasi multi-subnet berurutan & pengurutan	network="192.168.1.0/24", kebutuhan=[20, 100, 2, 50]	
4 blok terurut:


1. 192.168.1.0/25 (req 100, host 126)


2. 192.168.1.128/26 (req 50, host 62)


3. 192.168.1.192/27 (req 20, host 30)


4. 192.168.1.224/30 (req 2, host 2)

Sukses
TC-14	VLSM	Batas tepat kapasitas blok (Exact Boundary)	network="192.168.1.0/24", kebutuhan=[30]	Dialokasikan ke 192.168.1.0/27 (usable_hosts=30), tidak naik ke /26	Sukses
TC-15	VLSM	Batas tepat + 1 (terkena overhead Net & Bcast)	network="192.168.1.0/24", kebutuhan=[63]	Dialokasikan ke 192.168.1.0/25 (usable_hosts=126), bukan /26	Sukses
TC-16	VLSM	Kebutuhan 1 host tetap minimal /30	network="192.168.1.0/24", kebutuhan=[1]	Dialokasikan ke 192.168.1.0/30 (usable_hosts=2), tidak memakai /31 atau /32	Sukses
TC-17	VLSM	Kapasitas jaringan induk tidak mencukupi	network="192.168.1.0/24", kebutuhan=[200, 100]	ValueError / HTTP 400 dengan detail	Error
TC-18	VLSM	Input network_cidr bukan Network Address	network="192.168.1.10/24", kebutuhan=[10]	ValueError / HTTP 400 dengan detail	Error
TC-19	VLSM	Daftar kebutuhan kosong atau bernilai <= 0	network="192.168.1.0/24", kebutuhan=[] atau [10, 0]	ValueError / HTTP 400 dengan detail	Error
7. Di Luar Cakupan (Out of Scope)
Untuk menjaga fokus aplikasi sebagai alat evaluasi perhitungan subnetting dasar dan VLSM, fitur-fitur berikut tidak termasuk dalam versi ini:

Dukungan IPv6: Aplikasi hanya memproses pengalamatan IPv4 32-bit.

Validasi Kelas IPv4 Klasik (Classful Rules): Aplikasi tidak memblokir atau memberi peringatan khusus untuk alamat Loopback (127.0.0.0/8), Link-Local (169.254.0.0/16), Multicast (224.0.0.0/4), maupun Experimental (240.0.0.0/4); seluruh IPv4 dihitung secara matematis biner.

Alokasi /31 dan /32 Otomatis pada Mode VLSM: Mode VLSM secara ketat membatasi ukuran subnet terkecil pada /30 (blok 4 IP) sesuai standar kebutuhan host LAN umum di kurikulum SMK.

Penyimpanan Riwayat & Autentikasi Pengguna: Tidak ada database, sistem login guru/siswa, maupun fitur ekspor ke PDF/Excel.

Visualisasi Topologi Jaringan: Tidak menyertakan diagram jaringan otomatis maupun generator konfigurasi CLI router (Cisco IOS/MikroTik).