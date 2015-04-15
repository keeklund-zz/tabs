from flask import Blueprint, jsonify

mod = Blueprint('api', __name__, url_prefix='/api')

d= {'hello': 'world', 'foo': 'bar'}

@mod.route('/')
def index():
    return jsonify((k, [p for p in v]) for k,v in d.items())
