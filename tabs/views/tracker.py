from flask import Blueprint, render_template
import flask.ext.sqlalchemy
from tabs.database import Preparation, Processing, Projects, Samples, Sequencing

mod = Blueprint('tracker', __name__, url_prefix='/tracker')

fs = flask.ext.sqlalchemy
def r(model):
    """Experimenting with creating some sort of recursive walking of db.

    Will want to yield information during walk. Will need to evaluate or something.

    """
    for attr in dir(model):
        attr_class = getattr(type(model), attr, None)
        if isinstance(attr_class, fs.orm.attributes.InstrumentedAttribute):
            if isinstance(getattr(model, attr, None), list):
                print attr, getattr(model, attr, None)
                for i in getattr(model, attr, None):
                    r(i)

@mod.route('/')
def index():
    projects = Projects.query.order_by(Projects.timestamp.desc()).all()
    counts = dict()
    for project in projects:
        r(project)
        preps = []
        for sample in project.samples:
            preps.append(len(sample.preparations))
        
    return render_template('tracker/index.html',
                           title='tracker home',
                           projects=projects,)

@mod.route('/projects/')
@mod.route('/projects/<int:id>')
def projects(id=None):
    projects, samples = None, None
    if not id:
        projects = Projects.query.order_by(Projects.timestamp.desc()).all()
    else:
        try:
            projects = Projects.query.get(id)
            samples = Samples.query.filter_by(project_id=projects.id).all()
        except:
            projects, samples = None, None
    return render_template('tracker/projects.html',
                           data_type='projects',
                           data=projects,
                           subdata_type='samples',
                           subdata=samples)

@mod.route('/samples/')
@mod.route('/samples/<int:id>')
def samples(id=None):
    samples, preparation = None, None
    if not id:
        samples = Samples.query.order_by(Samples.timestamp.desc()).all()
    else:
        samples = Samples.query.get(id)

    if not isinstance(samples, list):
        try:
            preparation = Preparation.query.\
                         filter(Preparation.sample_id==samples.id).all()
        except:
            samples, preparation = None, None
    return render_template('tracker/samples.html',
                           data_type='samples',
                           data=samples,
                           subdata_type='preparation',
                           subdata=preparation)

@mod.route('/sequencing/')
@mod.route('/sequencing/<int:id>')
def sequencing(id=None):
    # if not id:
    #     # group by type or sequencing methodology?
    #     # group by samples?
    #     sequencing = Sequencing.query.join(Preparation).group_by(Preparation.name, Preparation.name).all()
    #     for seq in sequencing:
    #         print dir(seq)
    #         print seq.name, seq.preparation.name
    # else:
    #     sequencing = Sequencing.query.get(id)
    sequencing, processing = None, None
    if not id:
        sequencing = Sequencing.query.all()
    else:
        sequencing = Sequencing.query.get(id)

    if not isinstance(sequencing, list):
        try:
            processing = Processing.query.\
                         filter(Processing.sequencing_id==sequencing.id).all()
        except:
            sequencing, processing = None, None
    return render_template('tracker/sequencing.html',
                           data_type='sequencing',
                           data=sequencing,
                           subdata_type='processing',
                           subdata=processing)

@mod.route('/preparation/')
@mod.route('/preparation/<int:id>')
def preparation(id=None):
    preparation, sequencing = None, None
    if not id:
        preparation = Preparation.query.all()
    else:
        preparation = Preparation.query.get(id)

    if not isinstance(preparation, list):
        try:
            sequencing = Sequencing.query.\
                         filter(Sequencing.preparation_id==preparation.id).all()
        except:
            preparation, sequencing = None, None
    return render_template('tracker/preparation.html',
                           data_type='preparation',
                           data=preparation,
                           subdata_type='sequencing',
                           subdata=sequencing)

@mod.route('/processing/')
@mod.route('/processing/<int:id>')
def processing(id=None):
    if not id:
        processing = Processing.query.all()
    else:
        processing = Processing.query.get(id)
    return render_template('tracker/processing.html',
                           data_type='processing',
                           data=processing,
                           subdata_type=None,
                           subdata=None)
