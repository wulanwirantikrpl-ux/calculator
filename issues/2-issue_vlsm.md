# [Feature] Alokasi Subnet VLSM (Variable Length Subnet Mask)

## 1. Deskripsi
Fitur alokasi Variable Length Subnet Mask (VLSM) dirancang untuk membagi satu blok jaringan induk (major network) menjadi beberapa subnet dengan ukuran bervariasi sesuai kebutuhan host riil di laboratorium SMK TKJ.

Fitur ini menyediakan:
- Algoritma alokasi VLSM deterministik terurut dari kebutuhan terbesar (`alokasi_vlsm`).
- Pembatasan ukuran blok subnet terkecil pada /30 (blok minimal 4 IP: 2 host usable, 1 network, 1 broadcast) guna menjamin standar jaringan LAN SMK.
- Validasi ketat bahwa blok induk harus merupakan *Network Address* yang sah dan total alokasi tidak melebihi kapasitas blok induk.
- Endpoint API `POST /api/vlsm` berbasis FastAPI yang menerima JSON `{ "network": "...", "kebutuhan_host": [...] }` dan mengembalikan daftar subnet terurut.
- Integrasi antarmuka tab VLSM pada `index.html` dengan form builder dinamis dan tabel hasil alokasi multi-kolom beserta penanganan error (HTTP 400).

---

## 2. Tugas
- [ ] **Validasi Input VLSM**
  - [ ] Validasi format `network_cidr` (`<ip>/<prefix>`), memastikan alamat IP adalah Network Address valid (ip AND mask == ip).
  - [ ] Validasi list `kebutuhan_host` (tidak kosong, nilai int bukan bool, setiap elemen >= 1).
- [ ] **Implementasi Logika Alokasi VLSM**
  - [ ] Pengurutan kebutuhan descending (dari terbesar ke terkecil).
  - [ ] Perhitungan ukuran blok: pangkat 2 terkecil yang memenuhi `ukuran_blok >= kebutuhan + 2`, minimal 4 IP (prefix maksimal /30).
  - [ ] Pengecekan batas kapasitas alamat blok induk (*overflow detection*).
  - [ ] Pemanggilan `hitung_subnet` per segmen dan penyusunan output list of dict.
- [ ] **Implementasi Endpoint FastAPI**
  - [ ] `POST /api/vlsm`: Menerima payload JSON, memproses alokasi, mengembalikan 200 OK dengan list alokasi atau 400 Bad Request jika input/kapasitas tidak valid.
- [ ] **Pengujian Pytest**
  - [ ] Menulis unit test dan API integration test untuk TC-13 s.d. TC-19 di `test_main.py`.
- [ ] **Integrasi Antarmuka Web (Frontend)**
  - [ ] Menghubungkan tombol "Calculate VLSM Allocation" ke endpoint `POST /api/vlsm`.
  - [ ] Menampilkan tabel alokasi lengkap (No, Kebutuhan Host, Network/Prefix, Subnet Mask, Network Address, Range Host, Broadcast, Host Tersedia).
  - [ ] Menampilkan alert error merah lembut jika terjadi kesalahan API (HTTP 400) dan menyembunyikan hasil lama.

---

## 3. Kriteria Penerimaan
Merujuk pada tabel test di Bagian 6 SPEC.md:

| ID | Kategori | Kasus Uji | Input | Hasil yang Diharapkan | Tipe |
|---|---|---|---|---|---|
| **TC-13** | VLSM | Alokasi multi-subnet berurutan & pengurutan | `network="192.168.1.0/24"`, `kebutuhan=[20, 100, 2, 50]` | 4 blok terurut:<br>1. `192.168.1.0/25` (req 100, host 126)<br>2. `192.168.1.128/26` (req 50, host 62)<br>3. `192.168.1.192/27` (req 20, host 30)<br>4. `192.168.1.224/30` (req 2, host 2) | Sukses |
| **TC-14** | VLSM | Batas tepat kapasitas blok (Exact Boundary) | `network="192.168.1.0/24"`, `kebutuhan=[30]` | Dialokasikan ke `192.168.1.0/27` (`usable_hosts=30`), tidak naik ke /26 | Sukses |
| **TC-15** | VLSM | Batas tepat + 1 (terkena overhead Net & Bcast) | `network="192.168.1.0/24"`, `kebutuhan=[63]` | Dialokasikan ke `192.168.1.0/25` (`usable_hosts=126`), bukan /26 | Sukses |
| **TC-16** | VLSM | Kebutuhan 1 host tetap minimal /30 | `network="192.168.1.0/24"`, `kebutuhan=[1]` | Dialokasikan ke `192.168.1.0/30` (`usable_hosts=2`), tidak memakai /31 atau /32 | Sukses |
| **TC-17** | VLSM | Kapasitas jaringan induk tidak mencukupi | `network="192.168.1.0/24"`, `kebutuhan=[200, 100]` | `ValueError` / HTTP 400 dengan pesan `detail` | Error |
| **TC-18** | VLSM | Input network_cidr bukan Network Address | `network="192.168.1.10/24"`, `kebutuhan=[10]` | `ValueError` / HTTP 400 dengan pesan `detail` | Error |
| **TC-19** | VLSM | Daftar kebutuhan kosong atau bernilai <= 0 | `network="192.168.1.0/24"`, `kebutuhan=[]` atau `[10, 0]` | `ValueError` / HTTP 400 dengan pesan `detail` | Error |

---

## 4. Alur Kerja (Workflow)
```text
issue -> branch -> test dulu -> implementasi -> commit -> pull request -> CI -> merge
```

1. **Issue**: Mendefinisikan kebutuhan fitur VLSM di GitHub Issue.
2. **Branch**: Membuat branch fitur `feature/issue-<nomor>-vlsm` dari `main` terbaru.
3. **Test Dulu**: Menulis test case VLSM di `test_main.py` dan memastikan test gagal (Red).
4. **Implementasi**: Mengembangkan `alokasi_vlsm` di `main.py` dan menghubungkan UI `index.html` hingga seluruh test berhasil lolos (Green).
5. **Commit**: Menyimpan pekerjaan dengan commit terstruktur.
6. **Pull Request**: Membuka PR ke `main` dengan deskripsi `Closes #<nomor>`.
7. **CI**: Memantau verifikasi pipeline GitHub Actions hingga sukses.
8. **Merge**: Menggabungkan PR ke `main`.
