from flask import Blueprint, flash, redirect, render_template, request
from sqlalchemy.exc import IntegrityError
from tabs import db
from tabs.database import News, Projects, Samples, Sequencing, Updates, Users
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
    project_list = Projects.query.all()
    if form.validate_on_submit():
        project = Projects.query.filter_by(name=form.project.data).first()
        if project:
            sample = Samples(form.name.data, project)
            db.session.add(sample)
            db.session.commit()
            flash("New Sample: '%s' - added successfully!" % form.name.data)
        elif not project:
            flash("New Sample: '%s' - not submitted. Invalid project" % \
                  form.name.data)
        return redirect('/tracker/samples')
    elif not project_list:
        flash("Unable to create sample without a project!  Please add project.")
        return redirect('/new/project')
    return render_template('forms/sample.html',
                           title='new sample',
                           form=form,
                           project_list=project_list)

@mod.route('/sequencing', methods=['GET', 'POST'])
def new_sequencing():
    form = SequencingForm()
    samples = Samples.query.all()
    if form.validate_on_submit():
        sample = Samples.query.filter_by(id=form.sample.data).first()
        sequencing = Sequencing(form.name.data, sample)
        db.session.add(sequencing)
        db.session.commit()
        flash("New Sequencing Method: '%s' add successfully to '%s'!" % \
              (form.name.data, sample.name))
        return redirect('/tracker/samples/%s' % str(sample.id))
    return render_template('forms/sequencing.html',
                           title='new sequencing',
                           form=form,
                           samples=samples)
