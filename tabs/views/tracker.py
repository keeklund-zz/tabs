from flask import Blueprint, render_template
from tabs.database import Projects, Samples

mod = Blueprint('tracker', __name__, url_prefix='/tracker')

@mod.route('/')
def index():
    projects = Projects.query.order_by(Projects.timestamp.desc()).limit(5).all()
    samples = Samples.query.order_by(Samples.timestamp.desc()).limit(5).all() 
    return render_template('tracker/index.html',
                           title='tracker home',
                           projects=projects,
                           samples=samples,)

@mod.route('/projects/')
@mod.route('/projects/<int:id>')
def projects(id=None):
    if not id:
        projects = Projects.query.order_by(Projects.timestamp.desc()).all()
    else:
        projects = Projects.query.get(id)
    return render_template('tracker/layout.html',
                           data_type='projects',
                           data=projects)

@mod.route('/samples/')
@mod.route('/samples/<int:id>')
def samples(id=None):
    if not id:
        samples = Samples.query.order_by(Samples.timestamp.desc()).all()
    else:
        samples = Samples.query.get(id)
    return render_template('tracker/layout.html',
                           data_type='samples',
                           data=samples)

