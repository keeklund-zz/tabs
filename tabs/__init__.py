from flask import Flask, render_template
from flask.ext.login import LoginManager
from flask.ext.restful import Api
from flask.ext.sqlalchemy import SQLAlchemy
from flask.json import JSONEncoder

app = Flask(__name__)
app.config.from_object('websiteconfig')
app.json_encoder = JSONEncoder
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)

restful_api = Api(app)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404 

# does this HAVE to be this way?
# separate app into app.py? then import here - then all imports at top?
#from tabs.api import v1 
import tabs.api.v1
from tabs.views import general, forms, tracker
#app.register_blueprint(v1.mod)
app.register_blueprint(general.mod)
app.register_blueprint(forms.mod)
app.register_blueprint(tracker.mod)
