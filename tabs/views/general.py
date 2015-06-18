from flask import Blueprint, g, render_template
from tabs import lm
from tabs.database import News, Updates
from tabs.forms import NewsForm, UserForm

mod = Blueprint('general', __name__)

@mod.route('/')
def index():
    # api access, separate library that api and web access, or comp separate
    updates = Updates.query.order_by(Updates.timestamp.desc()).limit(5).all()
    news = News.query.order_by(News.timestamp.desc()).limit(5).all()
    return render_template('general/index.html',
                           title='home',
                           news=news,
                           updates=updates,)

@mod.route('/admin')
def admin():
    return render_template('general/admin.html',
                           title='admin')

@mod.route('/news')
def news():
    news = News.query.order_by(News.timestamp.desc()).all()
    return render_template('general/news.html',
                           title='news',
                           news=news)

@mod.route('/updates')
def updates():
    updates = Updates.query.order_by(Updates.timestamp.desc()).all()
    return render_template('general/updates.html',
                           title='updates',
                           updates=updates,)


# pagination on news
