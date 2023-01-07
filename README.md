# Easy Flask App
A ready to use boilerplate Flask App built on top of an [AdminLTE v3.2](https://adminlte.io/) and [Awesome icons v6.2.1](https://fontawesome.com/icons). 
FYI, AdminLTE is an open-source dashboard built on top of Bootstrap 4. 


## 🔥Let's get started

### Preparation - Install `poetry`
> Linux, macOS, Windows
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

> Windows (Powershell)
```PowerShell 
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

More information about `poetry` can be found [here](https://python-poetry.org/docs/#installing-with-the-official-installer)


**Optional:** enable tab completion when using poetry:
> Bash
```bash
poetry completions bash >> ~/.bash_completion
```

> Fish
```bash 
poetry completions fish > ~/.config/fish/completions/poetry.fish
```

> Zsh
```bash
poetry completions zsh > ~/.zfunc/_poetry
```

### Set up the environment
On your terminal, let's `cd` to your project folder (e.g `EasyFlaskApp`) and run the following command to initialize a new environment and install all dependencies:
```bash
poetry install
```

If you prefer to create a new virtual environment within the current project folder, you can run the following command before running `poetry install`:
```bash
poetry config virtualenvs.in-project true
```

**Activate environment**
```bash
poetry shell
```

**Deactivate environment**
```bash 
exit
```

### 🚀 Start the app
After activating the virtual environment, you can start the app:
```bash
flask run
```

> ✨ In windows, you might need to run the app by adding `python -m` before the command: 
```bash 
python -m flask run
```

You can also start the app using `gunicorn`, for example
```bash 
gunicorn app:app -b 0.0.0.0:5000 --workers=1 --threads=2
```

> More usefull `gunicorn` parameters can be found [here](https://docs.gunicorn.org/en/latest/run.html) 


## Enable authentication module
### Prerequirements
The authentication module require a DB schema which contains a `User` table. You can use whatever DB management system you like such as MySQL, SQLite, MSSQL, ...
In this example I use MySQL.
- Make sure you have a `.env` file in the root project folder to store all sensitive secret environment variables. (See example `.env.sample`)
- Create a schema name, for example `easyflaskapp`
- Create `User` table using a provided script `mysql_scripts.sql`
- Update the DB connection information in `.env` file

### Enable authentication module
By default, the authentication module will be disabled. 
If you want to use the authentication module, feel free to add the authentication module `mod_auth` at line `43` in `app/__init__.py` file.

```python
def register_blueprints(app):
    for module_name in ('home',
                        'mod_auth'
                    ):
```

> You might also need to add `@login_required` protection to the `index` route in the main module `app/home/controllers.py` as well. 
```python 
@blueprint.route('/')
@login_required
def index():
    return render_template('home/index.html', config=app.config)
```


### Create new user
By default, the app will redirect guest users to the login page. If you don't have any account, feel free to click to the registration link and create new account as well as set up two-steps authentication. No worries, it can be done in 3 simple steps. 

🎉 🎉 🎉 

## Code-base structure
```bash
<PROJECT DIR>
|--- app                                  #
|     |--- __init__.py                    # Initialize the app
|     |
|     |--- home                           # App main module - home blueprints
|     |     |--- controllers.py           # Define main app routes (index)
|     |     |--- __init__.py              # Init for home blueprints
|     |
|     |--- mod_auth                       # Authentication module - auth blueprints
|     |     |--- controllers.py           # Define authentication routes
|     |     |--- __init__.py              # Init for authentiation module
|     |
|     |--- static                         # Assest resources
|     |     |--- <css, js, img>           # CSS, Javascript, image files
|     |
|     |--- db                             # Database Management
|     |     |--- models.py                # Database Models (SQLAlchemy)
|     |     |--- database.py              # Database connection
|     |
|     |--- templates                      # HTML pages template used to render pages
|     |     |--- home                     # HTML pages template for main module
|     |     |     |--- index.html         # Default index page
|     |     |     |--- *.html             # Other pages as needed
|     |     |
|     |     |--- auth                     # Authentication pages
|     |     |     |--- login.html         # Login page
|     |     |     |--- login-2fa.html     # Two step verification page
|     |     |     |--- setup-2fa.html     # Setup two step verification page
|     |     |     |--- signup.html        # Register new account page
|     |     |
|     |     |--- includes                 #
|     |     |     |--- footer.html        # App footer
|     |     |     |--- sidebar.html       # App side bar
|     |     |     |--- navigation.html    # App navigation 
|     |     |
|     |     |--- layouts                  # App layouts (master) pages
|     |     |     |--- base.html          # base layout used by common pages
|     |     |
|     |     |--- 500.html                 # 500-page
|     |     |--- 404.html                 # 404-page
|     |
|--- utils                                # Common helper classes
|     |--- two_factors.py                 # Two factor authenticator helper class
|
|--- config.py                            # App configuration
|--- .env.sample                          # Environment sample for .env file
|--- pyproject.toml                       # App dependencies management by Poetry
|--- poetry.lock                          # Dependencies info generated by Poetry
|--- README.md                            # Project info
|--- changelog.md                         # Changelogs
|--- mysql_scripts.sql                    # SQL script: Create User table for auth module
```


## Todo:
- [ ] Dockerfile
- [ ] Forgot password
- [ ] Reset password
- [ ] Login with Google
- [ ] Login with Facebook

