from flask import Blueprint, render_template
from tabs.database import Projects#, Samples

mod = Blueprint('tracker', __name__, url_prefix='/tracker')

@mod.route('/')
def index():
    projects = Projects.query.order_by(Projects.timestamp.desc()).limit(5).all()
    samples = []
    return render_template('tracker/index.html',
                           title='tracker home',
                           projects=projects,
                           samples=samples,)

@mod.route('/projects')
def projects():
    projects = Projects.query.order_by(Projects.timestamp.desc()).all()
    return render_template('tracker/projects.html',
                           title='projects',
                           projects=projects)

@mod.route('/samples')
def samples():
    return render_template('tracker/samples.html',
                           title='samples',
                           samples=None)
