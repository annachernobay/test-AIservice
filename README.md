Інструкція із запуску

### 1. Клонування репозиторію та підготовка

bash
# Клонуйте репозиторій (замініть посилання на своє)
git clone [https://github.com/ваш_логін/назва_репозиторію.git](https://github.com/ваш_логін/назва_репозиторію.git)
cd назва_репозиторію

# Створіть віртуальне середовище
python -m venv venv

# Активуйте його:
# Linux / macOS:
source venv/bin/activate
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Windows (CMD):
venv\Scripts\activate.bat

# Встановіть необхідні залежності
pip install -r requirements.txt


### 2. Налаштування змінних оточення

Створіть файл `.env` на основі шаблону:

bash
cp .env.example .env


### 3. Запуск сервера

bash
uvicorn main:app --reload

### 4. Перевірка роботи

Після запуску відкрийте у браузері:

* **Веб-чат (UI):** [http://127.0.0.1:8000](http://127.0.0.1:8000)
* **Документація Swagger API:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
