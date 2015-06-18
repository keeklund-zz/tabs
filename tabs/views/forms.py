from flask import Blueprint, flash, redirect, render_template, request
from tabs import db
from tabs.database import News, Projects, Updates
from tabs.forms import NewsForm, ProjectForm, UpdateForm, UserForm

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
        flash("New user: '%s' - added successfully!" % form.name.data)
        return redirect('/') # CORRECT LOCATION?
    return render_template('general/index.html')
    
@mod.route('/project', methods=['GET', 'POST'])
def new_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Projects(form.name.data, form.user_id.data)
        db.session.add(project)
        db.session.commit()
        flash("New Project: '%s' - added successfully!" % form.name.data)
        return redirect('/projects') 
    return render_template('forms/project.html',
                           tilte='new project',
                           form=form,)

@mod.route('/sample', methods=['GET', 'POST'])
def new_sample():
    pass
