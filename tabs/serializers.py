from flask.ext.restful import fields

news_fields = {
    "id": fields.Integer,
    "title": fields.String,
    "body": fields.String,
    "user_id": fields.Integer,
    "timestamp": fields.DateTime(),
}

update_fields = {
    "id": fields.Integer,
    "title": fields.String,
    "body": fields.String,
    "user_id": fields.Integer,
    "timestamp": fields.DateTime(),
}

user_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
    "timestamp": fields.DateTime(),
}
