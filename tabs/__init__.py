from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from tabs.api import v0 as api
from tabs.views import general

app = Flask(__name__)
app.config.from_object('websiteconfig')

db = SQLAlchemy(app)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404 

app.register_blueprint(api.mod)
app.register_blueprint(general.mod)
