from flask import Blueprint, render_template

mod = Blueprint('tracker', __name__, url_prefix='/tracker')

@mod.route('/', methods=['GET'])
def index():
    # get users projects
    # collect meta data on said project
    return render_template('tracker/index.html',
                           title='tracker home',
                           projects=[])
