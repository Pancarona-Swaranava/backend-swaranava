# backend-swaranava

Backend dari aplikasi Swaranava menggunakan library Flask (Python).

## Struktur Proyek
```
backend-swaranava/
├── server.py          # File utama untuk server Flask
├── database.py        # Konfigurasi dan setup database
├── router/            # Direktori untuk modul API routes
│   ├── __init__.py    # Inisialisasi router dan registrasi routes
│   └── example.py     # Contoh modul router (template)
├── models/            # Direktori untuk database models
│   ├── __init__.py    # Inisialisasi models
│   └── example.py     # Contoh model database
├── requirements.txt   # Dependencies Python
└── README.md
```

## Setup 

### Prerequisites

- Python 3.8 atau lebih baru
- [uv](https://github.com/astral-sh/uv) - Package manager Python
- MySQL Server (versi 5.7 atau lebih baru)

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

### Setup Database

1. **Install MySQL Server** (jika belum terinstall):
   ```bash
   # Ubuntu/Debian
   sudo apt-get install mysql-server
   
   # macOS (dengan Homebrew)
   brew install mysql
   
   # Atau download dari https://dev.mysql.com/downloads/mysql/
   ```

2. **Buat Database**:
   ```bash
   # Login ke MySQL
   mysql -u root -p
   
   # Buat database
   CREATE DATABASE swaranava_db;
   
   # Buat user (opsional)
   CREATE USER 'swaranava_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON swaranava_db.* TO 'swaranava_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

3. **Konfigurasi Database Connection**:
   
   Set environment variable `DATABASE_URI` dengan format:
   ```
   mysql+pymysql://username:password@host:port/database_name
   ```
   
   Contoh:
   ```bash
   export DATABASE_URI="mysql+pymysql://root:password@localhost:3306/swaranava_db"
   ```
   
   Atau untuk development, bisa langsung edit di `database.py` (tidak disarankan untuk production).

4. **Inisialisasi Database Tables**:
   
   Tables akan otomatis dibuat saat pertama kali menjalankan server. Pastikan database sudah dibuat terlebih dahulu.

## Menjalankan Server

```bash
uv run python server.py
```

Server akan berjalan di `http://localhost:5000` secara default.

## Database & ORM

Aplikasi menggunakan **SQLAlchemy** sebagai ORM dan **MySQL** sebagai database.

### Struktur Models

Semua model database didefinisikan di direktori `models/`. Setiap model adalah class yang inherit dari `db.Model`.

### Membuat Model Baru

1. Buat file baru di direktori `models/` (contoh: `models/user.py`)
2. Import `db` dari `database`:
   ```python
   from database import db
   ```
3. Buat class model yang inherit dari `db.Model`
4. Import model di `models/__init__.py` jika diperlukan

Contoh dapat dilihat di `models/example.py`.

### Menggunakan Database di Routes

```python
from database import db
from models.example import Example

# Query data
examples = Example.query.all()

# Create data
new_example = Example(name="Test", description="Description")
db.session.add(new_example)
db.session.commit()
```

## API Routes

Semua API routes diorganisir dalam direktori `router/` dan dipecah menjadi beberapa modul sesuai kebutuhan.

### Menambahkan Route Baru

1. Buat file baru di direktori `router/` (contoh: `router/auth.py`)
2. Buat Blueprint di file tersebut
3. Import dan register Blueprint di `router/__init__.py`

Contoh dapat dilihat di `router/example.py`.