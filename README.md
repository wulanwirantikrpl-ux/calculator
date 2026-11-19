# Kalkulator Subnet & VLSM Web (SMK TKJ)

Aplikasi kalkulator subnetting IPv4 (FLSM/CIDR) dan VLSM berbasis web untuk guru dan siswa SMK Teknik Komputer dan Jaringan (TKJ).

## Docker

Aplikasi ini dapat dijalankan menggunakan Docker container:

### 1. Build Image
Jalankan perintah berikut di direktori root proyek untuk membangun image Docker:
```bash
docker build -t subnet-calculator .
```

### 2. Jalankan Container
Jalankan container di latar belakang (*detached mode*) dan petakan port 8000:
```bash
docker run -d --name subnet-app -p 8000:8000 subnet-calculator
```

Aplikasi dapat diakses melalui browser di `http://127.0.0.1:8000`.

### 3. Menjalankan Smoke Test
Untuk memastikan container berjalan dengan benar dan seluruh endpoint merespons dengan tepat, jalankan skrip smoke test:
```bash
uv run python scripts/smoke_test.py http://127.0.0.1:8000
```

### 4. Menghentikan & Menghapus Container
Setelah selesai pengujian, hentikan dan hapus container:
```bash
docker rm -f subnet-app
```

## Deploy

Aplikasi ini telah di-deploy ke Vercel dan dapat diakses secara publik melalui tautan berikut:
- **URL Produksi**: https://calculator-dusky-theta-87.vercel.app/

### Menjalankan Smoke Test di Lingkungan Produksi
Untuk memvalidasi bahwa seluruh fungsi API dan antarmuka web pada lingkungan produksi berjalan dengan baik, jalankan perintah berikut:
```bash
uv run python scripts/smoke_test.py https://calculator-dusky-theta-87.vercel.app/
```

