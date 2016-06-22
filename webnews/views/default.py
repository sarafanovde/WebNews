import os

from pyramid.response import Response
from pyramid.view import (
    view_config,
    forbidden_view_config)

from sqlalchemy.exc import DBAPIError

from sqlalchemy import desc

from ..models.mymodel import (
    User,
    DBSession,
    News
    )
from .security import USERS

from pyramid.security import (
    remember,
    forget)

from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound)
import time

@view_config(route_name='root', renderer='templates/page.jinja2')
def root_view(request):
    news = DBSession.query(News).order_by(desc(News.id))
    users = DBSession.query(User).all()
    users = map(lambda x:x.Name, users)
    return {'news': news,
            'username': request.authenticated_userid,
            'users': users,
            'project': 'WebNews' 
            }

db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_WebNews_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

@view_config(route_name='login', renderer='templates/login.jinja2')
@forbidden_view_config(renderer='templates/login.jinja2')
def login(request):
    login_url = request.route_url('login')
    users = DBSession.query(User).all()
    referrer = request.url
    if referrer == login_url:
        referrer = '/'
    came_from = request.params.get('came_from', referrer)
    message = ''
    login = ''
    password = ''
    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']
        for x in users:
            if (x.Name == login):
                user = x
        try:
            if user.Password == password:
                headers = remember(request, login)
                return HTTPFound(location = came_from, headers = headers)
        except:
            message = 'Неверный логин/пароль'

    return dict(
        message = message,
        url = request.application_url + '/login',
        came_from = came_from,
        login = login,
        password = password,
        )

@view_config(route_name='news_item', renderer='templates/news_item.jinja2')
def news_view(request):
    news_id = request.matchdict['id']
    news_item = DBSession.query(News).filter_by(id=news_id).first()
    users = DBSession.query(User).all()
    users = map(lambda x:x.Name, users)
    return {'news_item': news_item,
            'username': request.authenticated_userid,
            'users': users,
            'project': 'WebNews'
    }

@view_config(route_name='news_edit', renderer='templates/news_edit.jinja2')
def news_edit(request):
    users = DBSession.query(User).all()
    users = map(lambda x:x.Name, users)
    publishers = ['admin','root']
    if 'form.submitted' in request.params:
        try:
            img = request.POST['img']
            readFile(img)
            name = img
        except:
            name = 'noPhoto.png'
        topic = request.params['topic']
        short_info = request.params['short_info']
        data = request.params['data']
        news = News(Topic=topic, ShortInfo = short_info, Data = data, image_name = name)
        DBSession.add(news)

    return {
        'username': request.authenticated_userid,
	'users': users,
        'publishers': publishers,
        'project': 'WebNews'
        }
def readFile(image):
    path=os.path.join('/home/dima/WebNews/webnews/static/images/NewsPhotos',(image))
    file = open(path, 'rb')
    return file

@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location = request.route_url('root'),
                     headers = headers)

