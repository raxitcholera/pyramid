import re
from docutils.core import publish_parts

from pyramid.httpexceptions import(
    HTTPFound,
    HTTPNotFound,
    )

from pyramid.response import Response

from .security import USERS

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    MyModel,
    Users,
    )

from pyramid.view import (
    view_config,
    forbidden_view_config,
    )

from pyramid.security import (
    remember,
    forget,
    authenticated_userid,
    )

@view_config(route_name='list', renderer='list.mako',permission='edit')
def list_view(request):
    try:
        users = DBSession.query(Users).all()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'users': users, 'project': 'users','logged_in':authenticated_userid(request)}


@view_config(route_name='new', renderer='new.mako',permission='edit')
def new_view(request):
    if request.method == 'POST':
        if request.POST.get('UserName') and request.POST.get('Password'):
            newUserObj = Users(name=request.POST.get('UserName'),password=request.POST.get('Password'),group='viewer')
            
            DBSession.add(newUserObj)

            request.session.flash('New User was successfully added!')
            return HTTPFound(location=request.route_url('list'))
        else:
            request.session.flash('Please enter a name for the User!')
    return {}


@view_config(route_name='login', renderer='login.mako')
@forbidden_view_config(renderer='login.mako')
def login_view(request):
    if request.method == 'POST':
        if request.POST.get('UserName') and request.POST.get('Password'):
            usr=DBSession.query(Users).filter_by(name=request.POST['UserName'],password=request.POST['Password']).first()
            if usr:
                request.session.flash('Welcome!')
                headers = remember(request, request.params['UserName'])
                response = Response()
                #response.set_cookie('user', value = request,POST.get('UserName') , max_age = 30)
                return HTTPFound(location=request.route_url('list'))
            else:
                request.session.flash('Please enter a valid User Name or Password!')
                return HTTPFound(location=request.route_url('login'))
        else:
            request.session.flash('Please enter a User Name or Password!')
            return HTTPFound(location=request.route_url('login'))
    return {}
'''
@view_config(route_name='login', renderer='templates/login.pt')
@forbidden_view_config(renderer='templates/login.pt')
def login(request):
    login_url = request.route_url('login')
    referrer = request.url
    if referrer == login_url:
        referrer = '/' # never use the login form itself as came_from
    came_from = request.params.get('came_from', referrer)
    message = ''
    login = ''
    password = ''
    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']
        if USERS.get(login) == password:
            headers = remember(request, login)
            return HTTPFound(location = came_from,
                             headers = headers)
        message = 'Failed login'

    return dict(
        message = message,
        url = request.application_url + '/login',
        came_from = came_from,
        login = login,
        password = password,
        )
'''

@view_config(context='pyramid.exceptions.NotFound', renderer='notfound.mako')
def notfound_view(request):
    request.response.status = '404 Not Found'
    return {}

@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location = request.route_url('login'),
                     headers = headers)
    

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    try:
        one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'users'}

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_users_db" script
    to initialize your database tables.  Check your virtual 
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

