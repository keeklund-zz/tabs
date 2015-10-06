from os import walk
from os.path import dirname, exists, join, normpath, relpath
from flask import abort, Blueprint, render_template, request

mod = Blueprint('docs', __name__, url_prefix='/docs')
doc_path = normpath(join(dirname(__file__), '../../docs'))

@mod.route('/')
def index():
    data = []
    for root, dnames, filenames in walk(doc_path):
        if isinstance(filenames, list):
            for f in filenames:
                if 'swp' not in f and '~' not in f:
                    data.append(join(relpath(root, doc_path), f))
    return render_template('docs/index.html', data=data) 

@mod.route('/<doc>')
@mod.route('/researcher/<doc>')
@mod.route('/supervisor/<doc>')
def serve_doc(doc=None):
    url = request.url
    if 'researcher' in url:
        subdir = 'researcher'
    elif 'supervisor' in url:
        subdir = 'supervisor'
    else:
        subdir = ''

    documentation = join(doc_path, subdir, doc)
    if exists(documentation):
        with open(documentation, 'r') as f:
            data = f.read()
    else:
        abort(404)
    return render_template('docs/docs.html', doc=doc, data=data)
