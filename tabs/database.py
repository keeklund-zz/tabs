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
    # user = ?
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
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    project = db.relationship('Projects', 
            backref = db.backref('projects', lazy = 'dynamic'))
    timestamp = db.Column(db.DateTime)

    def __init__(self, name, project):
        self.name = name
        self.project = project
        self.timestamp = datetime.now()


class PreparationBase(Base):
    __json_hidden__ = []


class Preparation(PreparationBase, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    timestamp = db.Column(db.DateTime)
    sample_id = db.Column(db.Integer, db.ForeignKey('samples.id'))
    sample = db.relationship('Samples', 
            backref = db.backref('samples', lazy = 'dynamic'))

    def __init__(self, name, sample, timestamp=None):
        self.name = name
        self.sample = sample
        if not timestamp:
            timestamp = datetime.now()
        self.timestamp = timestamp


class SequencingBase(Base):
    __json_hidden__ = []


class Sequencing(SequencingBase, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    timestamp = db.Column(db.DateTime)
    preparation_id = db.Column(db.Integer, db.ForeignKey('preparation.id'))
    preparation = db.relationship('Preparation', 
            backref = db.backref('preparation', lazy = 'dynamic'))

    def __init__(self, name, preparation, timestamp=None):
        self.name = name
        self.preparation = preparation
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
    timestamp = db.Column(db.DateTime)
    sequencing_id = db.Column(db.Integer, db.ForeignKey('sequencing.id'))
    sequencing = db.relationship('Sequencing', 
            backref = db.backref('sequencing', lazy = 'dynamic'))

    def __init__(self, name, host, cmd, output_dir, sequencing, timestamp=None):
        self.name = name
        self.host = host
        self.cmd = cmd
        self.output_dir = output_dir
        self.sequencing = sequencing
        if not timestamp:
            timestamp = datetime.now()
        self.timestamp = timestamp


