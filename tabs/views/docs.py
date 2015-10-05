from os import listdir
from os.path import dirname, join, normpath
from flask import Blueprint, render_template

mod = Blueprint('docs', __name__, url_prefix='/docs')

@mod.route('/')
def index():
    doc_path = normpath(join(dirname(__file__), '../../docs'))
    return render_template('docs/index.html', data=listdir(doc_path))
