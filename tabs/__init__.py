from flask import flash, Flask, render_template
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.json import JSONEncoder

app = Flask(__name__, static_url_path='/static')
app.config.from_object('websiteconfig')
app.json_encoder = JSONEncoder
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)

@app.errorhandler(400)
def bad_request(error):
    return render_template('errors/errors.html', error_number=error)
                           

@app.errorhandler(404)
def page_not_found(error):
    flash("This page doesn't exist")
    return render_template('errors/errors.html', error_number=error)

# does this HAVE to be this way?
# separate app into app.py? then import here - then all imports at top?
#from tabs.api import v1 as api
from tabs.views import docs, general, forms, tracker
#app.register_blueprint(api.mod)
app.register_blueprint(docs.mod)
app.register_blueprint(general.mod)
app.register_blueprint(forms.mod)
app.register_blueprint(tracker.mod)
