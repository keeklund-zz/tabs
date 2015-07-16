from flask.ext.wtf import Form
from wtforms import SelectField, StringField
from wtforms.validators import DataRequired

class NewsForm(Form):

    title = StringField('title', validators=[DataRequired()])
    body = StringField('body', validators=[DataRequired()])
    user_id = StringField('user_id', validators=[DataRequired()])
    

class UpdateForm(Form):

    title = StringField('title', validators=[DataRequired()])
    body = StringField('body', validators=[DataRequired()])
    user_id = StringField('user_id', validators=[DataRequired()])
    

class UserForm(Form):

    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])


class ProjectForm(Form):

    name = StringField('name', validators=[DataRequired()])
    user_id = StringField('user_id', validators=[DataRequired()])


class SampleForm(Form):
    name = StringField('name', validators=[DataRequired()])
    project = StringField('project', validators=[DataRequired()])


class SequencingForm(Form):
    name = SelectField('name', 
            choices=[('atac','ATACSeq'), 
                ('chip', 'ChipSeq'),
                ('dnase', 'DNASeq'),
                ('rna', 'RNASeq'),],
            validators=[DataRequired()])
    sample = StringField('sample', validators=[DataRequired()])


class InformaticsForm(Form):
    name = StringField('name', validators=[DataRequired()])
    host_name = SelectField('host_name',
                            choices=[('kure', 'Kure'),
                                     ('cerberus', 'Cerberus'),],
                            validators=[DataRequired()])
    file_location = StringField('file_location', validators=[DataRequired()])
    pipeline_cmd = StringField('pipeline_cmd', validators=[DataRequired()])
    sequencing = StringField('sequencing', validators=[DataRequired()])
