# backend-swaranava

Backend dari aplikasi Swaranava menggunakan library Flask (Python).

## Struktur Proyek
```
backend-swaranava/
├── server.py          # File utama untuk server Flask
├── router/            # Direktori untuk modul API routes
│   ├── __init__.py    # Inisialisasi router dan registrasi routes
│   └── example.py     # Contoh modul router (template)
├── requirements.txt   # Dependencies Python
└── README.md
```

## Setup 

### Prerequisites

- Python 3.8 atau lebih baru
- [uv](https://github.com/astral-sh/uv) - Package manager Python

### Install uv

```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Atau menggunakan pip
pip install uv
```

### Install Dependencies

```bash
uv pip install -r requirements.txt
```

## Menjalankan Server

```bash
uv run python server.py
```

Server akan berjalan di `http://localhost:5000` secara default.

## API Routes

Semua API routes diorganisir dalam direktori `router/` dan dipecah menjadi beberapa modul sesuai kebutuhan.

### Menambahkan Route Baru

1. Buat folder baru di direktori `router/` (contoh: `router/auth/login.py`)
2. Buat kode di file tersebut
3. Import dan register Blueprint di `router/__init__.py`