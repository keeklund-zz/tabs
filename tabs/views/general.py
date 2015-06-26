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


@mod.route('/news/') 
@mod.route('/news/<int:id>')
def news(id=None):
    if not id:
        news = News.query.order_by(News.timestamp.desc()).all()
    else:
        news = News.query.get(id)
    return render_template('general/generic.html',
            data_type='news',
            data=news)

@mod.route('/updates/')
@mod.route('/updates/<int:id>')
def updates(id=None):
    if not id:
        updates = Updates.query.order_by(Updates.timestamp.desc()).all()
    else:
        updates = Updates.query.get(id)
    return render_template('general/generic.html',
            data_type='updates',
            data=updates)

# pagination on news
