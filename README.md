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
