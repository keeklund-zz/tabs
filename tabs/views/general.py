from flask import Blueprint, render_template
from tabs.database import News
from tabs.forms import NewsForm, UserForm

mod = Blueprint('general', __name__)

@mod.route('/')
def index():
    # api access, separate library that api and web access, or comp separate
    return render_template('general/index.html',
                           title='home',
                           news=[])

@mod.route('/admin')
def admin():
    return render_template('general/admin.html',
                           title='admin')

@mod.route('/news')
def news():
    news = News.query.all()
    return render_template('general/news.html',
                           title='news',
                           news=news)

@mod.route('/updates')
def updates():
    return render_template('general/updates.html',
                           title='updates')


# pagination on news
