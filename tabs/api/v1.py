from os.path import basename, splitext
from flask import Blueprint
from flask.ext.restful import Api, marshal_with, Resource
from tabs import api, db
from tabs.database import News, Updates, Users
from tabs.forms import NewsForm, UpdateForm, UserForm
from tabs.serializers import news_fields, update_fields, user_fields

__version__ = splitext(basename(__file__))[0]
mod = Blueprint('api', __name__, url_prefix='/api/%s' % __version__)
api = Api(mod)

# NEED TO GENERALIZE THIS STUFF



# # working?
# class AddProject(Resource):
#     form = ProjectForm()
#     if not form.validate_on_submit():
#         return form.errors, 422

#     project = Projects(form.name.data, form.user_id.data)
#     db.session.add(project)
#     db.session.commit()
#     return ProjectSerializer(project).data


# # working?
# class AddSample(Resource):
#     form = SampleForm()
#     if not form.validate_on_submit():
#         return form.errors, 422

#     sample = Samples(form.name.data, project)
#     db.session.add(sample)
#     db.session.commit()
#     return SampleSerializer(sample).data


# # working?
# class AddSequencing(Resource):
#     form = SequengingForm()
#     if not form.validate_on_submit():
#         return form.errors, 422

#     sequencing = Sequencing()
#     db.session.add(sequencing)
#     db.session.commit()
#     return SequencingSerializer(sequencing).data


# working?
class UpdateEndpoint(Resource):
    @marshal_with(update_fields)
    def get(self):
        updates = Updates.query.all()
        return updates

    @marshal_with(update_fields)
    def post(self):
        form = UpdateForm()
        if not form.validate_on_submit():
            return form.errors, 422

        update = Updates(form.title.data, form.body.data, form.user_id.data)
        db.session.add(update)
        db.session.commit()
        return update


class UserEndpoint(Resource):
    @marshal_with(user_fields)
    def get(self):
        users = Users.query.all()
        return users

    @marshal_with(user_fields)    
    def post(self):
        form = UserForm()
        if not form.validate_on_submit():
            return form.errors, 422

        user = Users(form.name.data, form.email.data)
        db.session.add(user)
        db.session.commit()
        return user


# combined?
# working?
class NewsEndpoint(Resource):
    @marshal_with(news_fields)
    def get(self):
        news = News.query.all()
        return news

    @marshal_with(news_fields)
    def post(self):
        form = NewsForm()
        if not form.validate_on_submit():
            return form.errors, 422

        news = News(form.title.data, form.body.data, form.user_id.data)
        db.session.add(news)
        db.session.commit()
        return news


api.add_resource(UserEndpoint, "/users")
api.add_resource(NewsEndpoint, "/news")
api.add_resource(UpdateEndpoint, "/updates")
