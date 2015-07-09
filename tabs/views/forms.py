from flask import Blueprint, flash, redirect, render_template, request
from sqlalchemy.exc import IntegrityError
from tabs import db
from tabs.database import News, Projects, Samples, Updates, Users
from tabs.forms import NewsForm, ProjectForm, SampleForm, SequencingForm
from tabs.forms import UpdateForm, UserForm

mod = Blueprint('forms', __name__, url_prefix='/new')

@mod.route('/news', methods=['GET', 'POST'])
def new_news():
    form = NewsForm()
    if form.validate_on_submit():
        news = News(form.title.data, form.body.data, form.user_id.data)
        db.session.add(news)
        db.session.commit()
        flash("News: '%s' - posted successfully!" % form.title.data)
        return redirect('/news')
    return render_template('forms/news.html',
                           title='new news',
                           form=form)

@mod.route('/update', methods=['GET', 'POST'])
def new_update():
    form = UpdateForm()
    if form.validate_on_submit():
        updates = Updates(form.title.data, form.body.data, form.user_id.data)
        db.session.add(updates)
        db.session.commit()
        flash("Update: '%s' - posted successfully!" % form.title.data)
        return redirect('/updates')
    return render_template('forms/update.html',
                           title='new updates',
                           form=form)

@mod.route('/user', methods=['GET', 'POST'])
def new_user():
    form = UserForm()
    if form.validate_on_submit():
        user = Users(form.name.data, form.email.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash("New user: '%s' - added successfully!" % form.name.data)
        except IntegrityError:
            flash("New user: '%s' - already exists!" % form.name.data)
        return redirect('/') # CORRECT LOCATION?
    return render_template('forms/user.html',
            title='new user',
            form=form)
    
@mod.route('/project', methods=['GET', 'POST'])
def new_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Projects(form.name.data, form.user_id.data)
        db.session.add(project)
        db.session.commit()
        flash("New Project: '%s' - added successfully!" % form.name.data)
        return redirect('/tracker/projects') 
    return render_template('forms/project.html',
                           title='new project',
                           form=form,)

@mod.route('/sample', methods=['GET', 'POST'])
def new_sample():
    form = SampleForm()
    if form.validate_on_submit():
        project = Projects.query.filter_by(name=form.project.data).first()
        if project:
            sample = Samples(form.name.data, project)
            db.session.add(sample)
            db.session.commit()
            flash("New Sample: '%s' - added successfully!" % form.name.data)
        flash("New Sample: '%s' - not submitted. Invalid project" % \
                form.name.data)
        return redirect('/tracker/samples')
    return render_template('forms/sample.html',
            title='new sample',
            form=form)

@mod.route('/sample/<int:id>/sequencing', methods=['GET', 'POST'])
def new_sequencing(id):
    form = SequencingForm()
    sample = Samples.query.get(id)
    if form.validate_on_submit():
        pass
    return render_template('forms/sequencing.html',
            title='new sequencing',
            form=form,
            sample=sample)
    # project? Filter by project, get sample list?
