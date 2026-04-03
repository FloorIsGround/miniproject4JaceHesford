### INF601 - Advanced Programming in Python
### Jace Hesford
### Mini Project 3

# CRUD app - with admin panel
## Description


## Getting Started
This project uses [uv package manager](https://docs.astral.sh/uv/getting-started/installation/) but it is not required to run this script. Any python installation >= 3.13 will work fine and instructions reflect both ways to install and run the program using regular python or uv package manager respectively.
 
### Dependencies
* No specific OS is required
* See Installing for obtaining dependencies
Main dependencies in requirements.txt:
```

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

#### 2. Start the development server

Run `main.py` from the root of the project directory:

```
# Python
python main.py

# uv package manager
uv run main.py
```

Flask will start a local development server. You should see output similar to:

```
 * Running on http://127.0.0.1:5000
```

Open that URL in your browser.

#### 3. Using the app


 
## Authors
 
Jace Hesford
 
## Version History

* 0.1
    * Initial Release
 
## Acknowledgments

* [Flask](https://flask.palletsprojects.com/) - Web framework
* [Flask-Login](https://flask-login.readthedocs.io/en/latest/) - User session management
* [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) - SQLite ORM integration