from flask import Blueprint, render_template
from tabs.database import Preparation, Processing, Projects, Samples, Sequencing

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
        query = Projects.query.order_by(Projects.timestamp.desc()).all()
        projects = [i.serialize() for i in query]
    else:
        try:
            projects = Projects.query.get(id)
            samples = Samples.query.filter_by(project_id=projects.id).all()
        except:
            projects, samples = None, None
    return render_template('tracker/layout.html',
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
    return render_template('tracker/layout.html',
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
    return render_template('tracker/layout.html',
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
    return render_template('tracker/layout.html',
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
    return render_template('tracker/layout.html',
                           data_type='processing',
                           data=processing,
                           subdata_type=None,
                           subdata=None)
