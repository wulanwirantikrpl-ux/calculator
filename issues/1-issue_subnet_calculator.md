# [Feature] Kalkulator Subnet & VLSM Web (SMK TKJ)

## 1. Deskripsi
Aplikasi Kalkulator Subnet & VLSM berbasis web ini dirancang sebagai alat bantu pengajaran dan verifikasi otomatis atas hasil perhitungan pengalamatan IPv4 (FLSM/CIDR dan VLSM) untuk guru serta siswa SMK Teknik Komputer dan Jaringan (TKJ).

Fitur ini menyediakan:
- Perhitungan parameter subnet IPv4 tunggal (`hitung_subnet`), mendukung kasus standar, /31 (RFC 3021), dan /32 (Host Route).
- Alokasi Variable Length Subnet Mask (`alokasi_vlsm`) dari blok induk secara deterministik terurut dari kebutuhan terbesar.
- Validasi input ketat (mencegah spasi liar, leading zero, oktet > 255, prefix di luar 0–32, dan blok subnet tidak valid).
- Backend berbasis FastAPI (Python 3.12+) dengan endpoint `GET /`, `GET /api/subnet`, dan `POST /api/vlsm`.
- Antarmuka web satu halaman (`index.html`) yang responsif, bersih, dan sesuai dengan panduan visual `DESIGN.md`.

---

## 2. Tugas
- [ ] **Persiapan & Arsitektur Proyek**
  - [ ] Pastikan runtime Python 3.12+ dan dependensi FastAPI, Uvicorn, Pytest terkonfigurasi.
  - [ ] Siapkan struktur proyek (`main.py`, `test_main.py`, `index.html`).
- [ ] **Implementasi Validasi Ketat**
  - [ ] Validasi format IPv4 (4 oktet, tanpa leading zero, rentang 0–255, tanpa spasi).
  - [ ] Validasi prefix (integer 0–32, menolak tipe boolean).
  - [ ] Validasi input VLSM (network CIDR harus Network Address yang valid, list kebutuhan host >= 1).
- [ ] **Implementasi Logika Inti Subnetting**
  - [ ] Fungsi `hitung_subnet(ip: str, prefix: int) -> dict`:
    - Perhitungan mask, network, broadcast, first_host, last_host, usable_hosts.
    - Penanganan kasus khusus /31 (RFC 3021) dan /32 (Host Route).
- [ ] **Implementasi Logika Alokasi VLSM**
  - [ ] Fungsi `alokasi_vlsm(network_cidr: str, kebutuhan_host: list[int]) -> list[dict]`:
    - Pengurutan kebutuhan descending.
    - Penentuan ukuran blok minimum 4 IP (/30).
    - Validasi kapasitas blok induk agar tidak overflow.
- [ ] **Implementasi Endpoint FastAPI**
  - [ ] `GET /`: Menyajikan `index.html`.
  - [ ] `GET /api/subnet`: Query params `ip` & `prefix`, merespons format JSON atau 400 Bad Request jika input invalid.
  - [ ] `POST /api/vlsm`: Request body JSON `{ network, kebutuhan_host }`, merespons array JSON atau 400 Bad Request jika kapasitas/input invalid.
  - [ ] Handler exception agar mengembalikan HTTP 400 dengan payload `{"detail": "<pesan error>"}` (termasuk validasi query integer).
- [ ] **Pengujian Berbasis Pytest**
  - [ ] Buat unit test dan endpoint test di `test_main.py` yang mencakup seluruh skenario TC-01 hingga TC-19.
- [ ] **Integrasi Antarmuka Web (Frontend)**
  - [ ] Mode Subnet (CIDR) dan Mode VLSM.
  - [ ] Tampilan hasil perhitungan terstruktur dan ramah pengguna.
  - [ ] Penanganan visual error (alert box merah lembut dan menyembunyikan hasil lama saat error).

---

## 3. Kriteria Penerimaan
Implementasi dianggap selesai dan diterima jika seluruh skenario pengujian berikut (merujuk pada Bagian 6 SPEC.md) berhasil diuji dan lolos 100% pada `test_main.py`:

| ID | Kategori | Kasus Uji | Input | Hasil yang Diharapkan | Tipe |
|---|---|---|---|---|---|
| **TC-01** | Subnet | Subnetting Kelas B lintas batas | `ip="172.16.5.130"`, `prefix=25` | `mask="255.255.255.128"`, `network="172.16.5.128"`, `broadcast="172.16.5.255"`, `first_host="172.16.5.129"`, `last_host="172.16.5.254"`, `usable_hosts=126` | Sukses |
| **TC-02** | Subnet | Subnetting terkecil standar (/30) | `ip="10.0.0.0"`, `prefix=30` | `mask="255.255.255.252"`, `network="10.0.0.0"`, `broadcast="10.0.0.3"`, `first_host="10.0.0.1"`, `last_host="10.0.0.2"`, `usable_hosts=2` | Sukses |
| **TC-03** | Subnet | Point-to-Point RFC 3021 (/31) | `ip="192.168.1.0"`, `prefix=31` | `mask="255.255.255.254"`, `network="192.168.1.0"`, `broadcast=None`, `first_host="192.168.1.0"`, `last_host="192.168.1.1"`, `usable_hosts=2` | Sukses |
| **TC-04** | Subnet | Host Route tunggal (/32) | `ip="192.168.1.5"`, `prefix=32` | `mask="255.255.255.255"`, `network="192.168.1.5"`, `broadcast=None`, `first_host="192.168.1.5"`, `last_host="192.168.1.5"`, `usable_hosts=1` | Sukses |
| **TC-05** | Subnet | Default Route (/0) | `ip="0.0.0.0"`, `prefix=0` | `mask="0.0.0.0"`, `network="0.0.0.0"`, `broadcast="255.255.255.255"`, `first_host="0.0.0.1"`, `last_host="255.255.255.254"`, `usable_hosts=4294967294` | Sukses |
| **TC-06** | Validasi | Oktet IP melebihi 255 | `ip="256.1.1.1"`, `prefix=24` | `ValueError` / HTTP 400 dengan `detail` | Error |
| **TC-07** | Validasi | Oktet mengandung leading zero | `ip="192.168.01.1"`, `prefix=24` | `ValueError` / HTTP 400 dengan `detail` | Error |
| **TC-08** | Validasi | Oktet kurang dari 4 bagian | `ip="192.168.1"`, `prefix=24` | `ValueError` / HTTP 400 dengan `detail` | Error |
| **TC-09** | Validasi | Input bukan angka / huruf | `ip="abc"`, `prefix=24` | `ValueError` / HTTP 400 dengan `detail` | Error |
| **TC-10** | Validasi | Input string kosong atau spasi | `ip=""` atau `ip=" 192.168.1.1"`, `prefix=24` | `ValueError` / HTTP 400 dengan `detail` | Error |
| **TC-11** | Validasi | Prefix di atas batas maksimum | `ip="192.168.1.1"`, `prefix=33` | `ValueError` / HTTP 400 dengan `detail` | Error |
| **TC-12** | Validasi | Prefix bernilai negatif | `ip="192.168.1.1"`, `prefix=-1` | `ValueError` / HTTP 400 dengan `detail` | Error |
| **TC-13** | VLSM | Alokasi multi-subnet berurutan & pengurutan | `network="192.168.1.0/24"`, `kebutuhan=[20, 100, 2, 50]` | 4 blok terurut:<br>1. `192.168.1.0/25` (req 100, host 126)<br>2. `192.168.1.128/26` (req 50, host 62)<br>3. `192.168.1.192/27` (req 20, host 30)<br>4. `192.168.1.224/30` (req 2, host 2) | Sukses |
| **TC-14** | VLSM | Batas tepat kapasitas blok (Exact Boundary) | `network="192.168.1.0/24"`, `kebutuhan=[30]` | Dialokasikan ke `192.168.1.0/27` (`usable_hosts=30`), tidak naik ke /26 | Sukses |
| **TC-15** | VLSM | Batas tepat + 1 (terkena overhead Net & Bcast) | `network="192.168.1.0/24"`, `kebutuhan=[63]` | Dialokasikan ke `192.168.1.0/25` (`usable_hosts=126`), bukan /26 | Sukses |
| **TC-16** | VLSM | Kebutuhan 1 host tetap minimal /30 | `network="192.168.1.0/24"`, `kebutuhan=[1]` | Dialokasikan ke `192.168.1.0/30` (`usable_hosts=2`), tidak memakai /31 atau /32 | Sukses |
| **TC-17** | VLSM | Kapasitas jaringan induk tidak mencukupi | `network="192.168.1.0/24"`, `kebutuhan=[200, 100]` | `ValueError` / HTTP 400 dengan `detail` | Error |
| **TC-18** | VLSM | Input network_cidr bukan Network Address | `network="192.168.1.10/24"`, `kebutuhan=[10]` | `ValueError` / HTTP 400 dengan `detail` | Error |
| **TC-19** | VLSM | Daftar kebutuhan kosong atau bernilai <= 0 | `network="192.168.1.0/24"`, `kebutuhan=[]` atau `[10, 0]` | `ValueError` / HTTP 400 dengan `detail` | Error |

### Kriteria Tambahan
- Format respons error API wajib konsisten mengembalikan HTTP 400 dengan payload: `{"detail": "<pesan deskriptif bahasa indonesia>"}`.
- Tampilan UI `index.html` sesuai spesifikasi palet warna, tipografi, dan komponen di `DESIGN.md`.

---

## 4. Alur Kerja (Workflow)
Siklus pengembangan mengikuti alur disiplin rekayasa perangkat lunak:
```text
issue -> branch -> test dulu -> implementasi -> commit -> pull request -> CI -> merge
```

1. **Issue**
   - Mendefinisikan kebutuhan, tugas, dan kriteria penerimaan secara transparan di GitHub Issue.
2. **Branch**
   - Membuat branch baru yang dicabangkan dari branch `main` dengan format penamaan:
     `feature/issue-<nomor>-subnet-calculator`
3. **Test Dulu (Test-Driven Development)**
   - Menulis test suite di `test_main.py` terlebih dahulu berdasarkan tabel test case di SPEC.md (TC-01 sampai TC-19).
   - Memastikan test dieksekusi dan berada pada status *fail/red* sebelum kode implementasi ditulis.
4. **Implementasi**
   - Mengembangkan kode backend di `main.py` dan frontend di `index.html` hingga seluruh test berhasil lolos (*pass/green*).
   - Menjaga kebersihan dan keterbacaan kode (*refactor*).
5. **Commit**
   - Menyimpan progres kerja dengan pesan commit yang jelas mengikuti konvensi (*conventional commits*), contoh:
     `test: tambahkan pengujian tc-01 hingga tc-19`
     `feat: implementasi kalkulator subnet dan vlsm`
6. **Pull Request (PR)**
   - Membuka PR dari branch fitur menuju `main` dengan deskripsi jelas dan merujuk issue terkait (`Closes #<nomor>`).
7. **CI (Continuous Integration)**
   - Memastikan pipeline GitHub Actions (linter, unit test, integration test) berjalan otomatis dan lolos (*green build*).
8. **Merge**
   - Melakukan penggabungan (*merge*) branch fitur ke `main` setelah review dan CI dinyatakan sukses.
