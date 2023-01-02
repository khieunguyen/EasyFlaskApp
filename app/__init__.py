# -*- coding: utf-8 -*-

from datetime import datetime
from os.path import join, dirname

from flask import Flask, render_template
#from flask_babel import Babel # support for multilingual web app 

from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

#------------------------------------------------
# App config
#------------------------------------------------

app = Flask(__name__, static_folder='static') 
# Load app configurations from config file
app.config.from_object('config')

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

#------------------------------------------------
# Error handlers
#------------------------------------------------

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500

#------------------------------------------------
# Register all blueprints modules
#------------------------------------------------
from importlib import import_module

def register_blueprints(app):
    for module_name in ('home','mod_auth'
                        ):
        module = import_module('app.{}.controllers'.format(module_name))
        app.register_blueprint(module.blueprint)

register_blueprints(app)

# enable following rule if the exeption still appeared in console
# app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='img/favicon.ico'))

if __name__ == "__main__":
    with app.app_context():
        app.run(
            host='0.0.0.0', 
            port=80, 
            threaded=True, 
            #ssl_context=('local_ssl/localhost.crt', 'local_ssl/localhost.key')
        )

