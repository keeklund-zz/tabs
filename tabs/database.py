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

    
class UserBase(Base):
    __json_hidden__ = []

    
class User(UserBase, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    
    def __init__(self, name, email):
        self.name = name
        self.email = email

    
class NewsBase(Base):
    __json_hidden__ = []

    
class News(NewsBase, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(140))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    

class UpdatesBase(Base):
    __json_hidden__ = []

    
class Updates(UpdatesBase, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(140))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # title?
    # be able to reference sample, artifacts, process, or generic?
    # body the right name for it?
    # what exactly do I mean by updates?


class ProjectBase(Base):
    __json_hidden__ = []

    
class Project(ProjectBase, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
