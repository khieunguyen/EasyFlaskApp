# -*- coding: utf-8 -*-
# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

# Config for your site
SITE_NAME = "EasyFlaskApp"
SITE_TITLE = "EasyFlaskApp - A ready to use Flask App"
SITE_URL  = "localhost:8000"

# Support multi-languages
LANGUAGES = ["en", "vi"]

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Secret key for signing session data
CSRF_SESSION_KEY = os.environ.get("CSRF_SESSION_KEY", "MySecret-;)")

# Secret key for signing cookies
SECRET_KEY = os.environ.get("COOKIES_SECRET_KEY", "MySecretRecipe_:)")