from flask import Blueprint, render_template
from tabs.database import Informatics, Projects, Samples, Sequencing

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
    projects, samples = None, None
    if not id:
        projects = Projects.query.order_by(Projects.timestamp.desc()).all()
    else:
        projects = Projects.query.get(id)
        samples = Samples.query.filter_by(project_id=projects.id).all()
    return render_template('tracker/projects.html',
                           data_type='projects',
                           data=projects,
                           subdata_type='samples',
                           subdata=samples)

@mod.route('/samples/')
@mod.route('/samples/<int:id>')
def samples(id=None):
    if not id:
        samples = Samples.query.order_by(Samples.timestamp.desc()).all()
    else:
        samples = Samples.query.get(id)

    sequencing = None
    if not isinstance(samples, list):
        sequencing = Sequencing.query.filter(Sequencing.sample_id==samples.id).all()
    return render_template('tracker/samples.html',
                           data_type='samples',
                           data=samples,
                           subdata_type='sequencing',
                           subdata=sequencing)

@mod.route('/sequencing/')
@mod.route('/sequencing/<int:id>')
def sequencing(id=None):
    if not id:
        # group by type or sequencing methodology?
        sequencing = Sequencing.query.join(Samples).group_by(Sequencing.name, Samples.name).all()
    else:
        sequencing = Sequencing.query.get(id)
    return render_template('tracker/sequencing.html',
                           data_type='sequencing',
                           data=sequencing,)

@mod.route('/informatics/')
@mod.route('/informatics/<int:id>')
def informatics(id=None):
    if not id:
        info = Informatics.query.all()
    else:
        info = Informatics.query.get(id)
    return render_template('tracker/informatics.html',
                           data_type='informatics',
                           data=info)
