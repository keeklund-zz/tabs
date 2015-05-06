from flask import Blueprint, flash, redirect, render_template, request
from tabs.forms import NewsForm, UserForm

mod = Blueprint('forms', __name__, url_prefix='/new')

@mod.route('/news', methods=['GET', 'POST'])
def new_news():
    form = NewsForm()
    if form.validate_on_submit():
        flash("News: '%s' - posted successfully!" % form.title.data)
        return redirect('/news')
    return render_template('forms/news.html',
                           title='new news',
                           form=form)

@mod.route('/update', methods=['GET', 'POST'])
def new_update():
    form = NewsForm()
    if form.validate_on_submit():
        flash("Update: '%s' - posted successfully!" % form.title.data)
        return redirect('/updates')
    return render_template('forms/update.html',
                           title='new updates',
                           form=form)

@mod.route('/user')
def new_user():
    form = UserForm()
    if form.validate_on_submit():
        flash("New user: '%s' - added successfully!" % form.name.data)
        return redirect('/')
    return render_template('general/index.html')
    
