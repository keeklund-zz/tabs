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
    timestamp = db.Column(db.DateTime)
    
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id
        self.timestamp = datetime.now()
