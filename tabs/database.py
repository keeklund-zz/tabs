from datetime import datetime
from tabs import db

class Base(object):

    __json_hidden__ = None

    def __init__(self):
        pass

    def __repr__(self):
        return '<%s %r>' % (type(self).__name__, self.name)
    
    def get_table_columns(self):
        for c in self.__mapper__.iterate_properties:
            yield c.key
            
    def serialize(self):
        """Return dictionary of key-value pairs based on table columns."""
        hidden = self.__json_hidden__ or []
        d = dict()
        for key in self.get_table_columns():
            if not key in hidden:
                value = getattr(self, key)
                d[key] = value
        return d

    
class UsersBase(Base):
    __json_hidden__ = []

    
class Users(UsersBase, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    timestamp = db.Column(db.DateTime)
    # samples?
    # data generated? might get out of hand here
    
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.timestamp = datetime.now()
        
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_annonymous(self):
        return False

    def get_it(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

    def __repr__(self):
        return '<User %r>' % self.name
    
    
class NewsBase(Base):
    __json_hidden__ = []

    
class News(NewsBase, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(140))
    body = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # user = ?
    timestamp = db.Column(db.DateTime)

    def __init__(self, title, body, user_id):
        self.title = title
        self.body = body
        self.user_id = user_id
        self.timestamp = datetime.now()

class UpdatesBase(Base):
    __json_hidden__ = []

    
class Updates(UpdatesBase, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(140))
    body = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    #user = ?
    timestamp = db.Column(db.DateTime)

    def __init__(self, title, body, user_id):
        self.title = title
        self.body = body
        self.user_id = user_id
        self.timestamp = datetime.now()

        
class ProjectsBase(Base):
    __json_hidden__ = []

    
class Projects(ProjectsBase, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    samples = db.relationship('Samples', backref='projects', lazy='select')
    timestamp = db.Column(db.DateTime)
    
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id
        self.timestamp = datetime.now()


class SamplesBase(Base):
    __json_hidden__ = []


class Samples(SamplesBase, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(140))
    strain = db.Column(db.String(16))
    sex = db.Column(db.String(8))
    exposure = db.Column(db.Integer)
    date_sacrificed = db.Column(db.DateTime)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    preparations = db.relationship('Preparation', backref='samples', lazy='select')
    timestamp = db.Column(db.DateTime)

    def __init__(self, form_data, project_id):
        for key, value in form_data.items():
            if key != 'project':
                setattr(self, key, value)
        self.project_id = project_id
        self.timestamp = datetime.now()


class PreparationBase(Base):
    __json_hidden__ = []


class Preparation(PreparationBase, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    antibody = db.Column(db.String(64))
    cell_line = db.Column(db.String(16))
    bioanalyzer_shearing = db.Column(db.String(1024))
    library_yield = db.Column(db.Float)
    adaptor = db.Column(db.String(16))
    bioanalyzer_library = db.Column(db.String(1024))
    amount_submitted = db.Column(db.Integer)
    concentration = db.Column(db.Float)
    fedex_tracking_number = db.Column(db.String(64))
    comments = db.Column(db.String(2048))
    sample_id = db.Column(db.Integer, db.ForeignKey('samples.id'))
    sequencing = db.relationship('Sequencing',
                                 backref='preparation', lazy='select')
    timestamp = db.Column(db.DateTime)

    def __init__(self, form_data, sample_id, timestamp=None):
        for key, value in form_data.items():
            if key != 'sample':
                setattr(self, key, value)
        self.sample_id = sample_id
        if not timestamp:
            timestamp = datetime.now()
        self.timestamp = timestamp


class SequencingBase(Base):
    __json_hidden__ = []


class Sequencing(SequencingBase, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    preparation_id = db.Column(db.Integer, db.ForeignKey('preparation.id'))
    processing = db.relationship('Processing', 
                                 backref='sequencing', lazy='select')
    timestamp = db.Column(db.DateTime)

    def __init__(self, name, preparation_id, timestamp=None):
        self.name = name
        self.preparation_id = preparation_id
        if not timestamp:
            timestamp = datetime.now()
        self.timestamp = timestamp


class ProcessingBase(Base):
    __json_hidden__ = []


class Processing(ProcessingBase, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    host = db.Column(db.String(80))
    cmd = db.Column(db.String(1024))
    output_dir = db.Column(db.String(1024))
    sequencing_id = db.Column(db.Integer, db.ForeignKey('sequencing.id'))
    timestamp = db.Column(db.DateTime)

    def __init__(self, name, host, cmd, output_dir, sequencing_id, timestamp=None):
        self.name = name
        self.host = host
        self.cmd = cmd
        self.output_dir = output_dir
        self.sequencing_id = sequencing_id
        if not timestamp:
            timestamp = datetime.now()
        self.timestamp = timestamp


