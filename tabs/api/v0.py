from os.path import basename, splitext
from flask import abort, make_response
from flask import Blueprint, jsonify, request
from tabs import db
from tabs.database import User, News, Updates, Project

__version__ = splitext(basename(__file__))[0]

mod = Blueprint('api', __name__, url_prefix='/api/%s' % __version__)

# @mod.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify(error=error.description), error.code)

@mod.errorhandler(400)
def bad_request(error):
    return make_response(jsonify(error=error.description), error.code)

@mod.route('/', methods=['GET'])
def index():
    # meta data?
    return jsonify(version=__version__)

@mod.route('/users/', methods=['GET'])
def get_users():
    user_list = [user.serialize() for user in User.query.all()]
    return jsonify(version=__version__,
                   users=user_list,
                   num_users=len(user_list),)

@mod.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user_query = User.query.get(id)
    user_len = 1 if user_query else 0
    user = user_query.serialize() if user_query else {}
    return jsonify(version=__version__,
                   users=user,
                   num_users=user_len,)

@mod.route('/users/', methods=['POST'])
def add_user():
    if not request.json or \
       not 'name' in request.json or \
       not 'email' in request.json:
        abort(400)
    new_user = User(name=request.json['name'], email=request.json['email'])
    db.session.add(new_user)
    db.session.commit()
    user_list = [user.serialize() for user in User.query.all()]    
    return jsonify(version=__version__,
                   users=user_list,
                   num_users=len(user_list),)

@mod.route('/news/', methods=['GET'])
def get_news():
    news_list = [new.serialize() for new in News.query.all()]
    return jsonify(version=__version__,
                   news=news_list,
                   num_news=len(news_list),)

@mod.route('/news/<int:id>', methods=['GET'])
def get_new(id):
    new_query = News.query.get(id)
    new_len = 1 if new_query else 0
    new = new_query.serialize() if new_query else {}
    return jsonify(version=__version__,
                   news=new,
                   num_news=new_len,)

# @mod.route('/news/', methods=['POST'])
# def add_news():
#     new_new = News()
#     print dir(new_new)
#     return jsonify(version=__version__,
#                    news=[],
#                    num_news=1)
    
@mod.route('/news/recent/<int:num>', methods=['GET'])
def get_recent_news(num):
    news_query = News.query.order_by(News.timestamp.desc()).limit(num).all() 
    news_list = [new.serialize() for new in news_query]
    return jsonify(version=__version__,
                   news=news_list,
                   num_news=len(news_list),)
    
@mod.route('/updates/', methods=['GET'])
def get_updates():
    update_list = [update.serialize() for update in Updates.query.all()]
    return jsonify(version=__version__,
                   updates=update_list,
                   num_updates=len(update_list),)

@mod.route('/updates/<int:id>', methods=['GET'])
def get_update(id):
    update_query = Updates.query.get(id)
    update_len = 1 if update_query else 0
    update = update_query.serialize() if update_query else {}
    return jsonify(version=__version__,
                   updates=update,
                   num_updates=update_len,)

@mod.route('/projects/', methods=['GET'])
def get_projects():
    project_list = [project.serialize() for project in Project.query.all()]
    return jsonify(version=__version__,
                   projects=project_list,
                   num_projects=len(project_list),)

@mod.route('/projects/<int:id>', methods=['GET'])
def get_project(id):
    project_query = Project.query.get(id)
    project_len = 1 if project_query else 0
    project = project_query.serialize() if project_query else {}
    return jsonify(version=__version__,
                   projects=project,
                   num_projects=project_len,)

# /something/<int:datum>/<int:datum>/
# should really split this file into a subfolder and logical partitions
# when unset value, error?  /user/3 where 3 doesn't exist - fail vs empty
# data validation
# declarative_base()? better sessions?
# should use aborts?
