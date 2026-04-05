### INF601 - Advanced Programming in Python
### Jace Hesford
### Mini Project 4

# Kansas Bill Tracker
## Description

A Django web application that pulls live bill data from the Kansas Legislature KLISS REST API. Users can browse current session bills, leave comments, and upvote or downvote bills. Admins can remove comments and attach written analysis summaries to bills via the Django admin panel.

## Getting Started
This project uses [uv package manager](https://docs.astral.sh/uv/getting-started/installation/) but it is not required to run this project. Any Python installation >= 3.13 will work fine and instructions reflect both ways to install and run the program using regular Python or uv package manager respectively.

### Dependencies
* No specific OS is required
* See Installing for obtaining dependencies

Main dependencies in requirements.txt:
```
django
requests
django-crispy-forms
crispy-bootstrap5
```

### Installing

```
# pull the repository and enter the directory
git clone https://github.com/FloorIsGround/miniproject4JaceHesford.git
cd miniproject4JaceHesford

# create your virtual environment
# For Python
python -m venv .venv

# For uv package manager (what I use)
uv venv

# activate the virtual environment
# on linux/wsl
source .venv/bin/activate

# on windows
.venv\Scripts\activate

# install dependencies
# For Python
pip install -r requirements.txt

# For uv package manager (what I use)
uv pip install -r requirements.txt
```

### Executing program

#### 1. Initialize the database

```
# Python
python manage.py makemigrations
python manage.py migrate

# uv package manager
uv run manage.py makemigrations
uv run manage.py migrate
```

#### 2. (Optional) Create a superuser for the admin panel

```
# Python
python manage.py createsuperuser

# uv package manager
uv run manage.py createsuperuser
```

#### 3. Start the development server

```
# Python
python manage.py runserver

# uv package manager
uv run manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

#### 4. Using the app

| Page | URL |
|------|-----|
| Home | `/` |
| Bill list | `/bills/` |
| Bill detail | `/bills/<bill_number>/` |
| Register | `/accounts/register/` |
| Login | `/accounts/login/` |
| Profile | `/accounts/profile/` |
| Admin panel | `/admin/` |

## Authors

Jace Hesford

## Version History

* 0.1
    * Initial Release

## Acknowledgments

* [Django](https://www.djangoproject.com/) - Web framework
* [Bootstrap](https://getbootstrap.com/) - Frontend styling
* [django-crispy-forms](https://django-crispy-forms.readthedocs.io/) - Form rendering
* [Kansas Legislature KLISS API](https://www.kslegislature.gov/li/api/v10/rev-1/) - Bill data source
* [Claude](https://claude.ai) by [Anthropic](https://www.anthropic.com) - AI assistant used during development
