import re
from docutils.core import publish_parts
import hashlib

from pyramid.httpexceptions import(
    HTTPFound,
    HTTPNotFound,
    )

from pyramid.response import Response

from .security import USERS

from sqlalchemy.exc import DBAPIError
from datetime import *

from .models import (
    DBSession,
    MyModel,
    Users,
    Login_Session,
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

def set_password(password):
    hashed_password = password
    salt ='testsaltstringwouldbeplacedhere'
    hashed_password=hashlib.sha224(password + salt ).hexdigest()
    return hashed_password

def check_session(sessionid):
    return_var = DBSession.query(Login_Session).filter_by(id=sessionid).first()
    allowed_time = datetime.strptime(return_var.timeout, "%Y-%m-%d %H:%M:%S.%f")

    if allowed_time > datetime.now():
        return True
    else:
        return False



@view_config(route_name='list', renderer='list.mako',permission='view')
def list_view(request):
    try:
        users = DBSession.query(Users).all()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'users': users, 'project': 'users'}


@view_config(route_name='new', renderer='new.mako',permission='edit')
def new_view(request):
    if request.method == 'POST':
        if request.POST.get('UserName') and request.POST.get('Password'):
            passw=set_password(request.POST.get('Password'))
            newUserObj = Users(name=request.POST.get('UserName'),password=passw,group='viewer')
            
            DBSession.add(newUserObj)

            request.session.flash('New User was successfully added!')
            return HTTPFound(location=request.route_url('list'))
        else:
            request.session.flash('Please enter a name for the User!')
    return {}


@view_config(route_name='login', renderer='login.mako')
@forbidden_view_config(renderer='login.mako')
def login_view(request):
    if request.method == 'POST' or 'logged_session_id' in request.session:
        if request.POST.get('UserName') and request.POST.get('Password'):
            passw=set_password(request.POST.get('Password'))
            usr=DBSession.query(Users).filter_by(name=request.POST['UserName'],password=passw).first()
            if usr:
                request.session.flash('Welcome!')
                
                request.session['logged_in']='yes'
                #request.session['logged_in_id']=usr.id
                #request.session['logged_in_group']=usr.group
                
                
                Sessiontimeoutime=datetime.now() + timedelta(minutes = 10)
                newSessionObj = Login_Session(userid=usr.id,group=usr.group,timeout=Sessiontimeoutime)
                DBSession.add(newSessionObj)
                
                log=DBSession.query(Login_Session).filter_by(userid=usr.id).order_by(Login_Session.id.desc()).first()
                request.session['logged_session_id']=log.id
                headers = remember(request,usr.group)
                return HTTPFound(location=request.route_url('list'),headers=headers)
            else:
                request.session.flash('Please enter a valid User Name or Password!')
                return HTTPFound(location=request.route_url('login'))
        elif 'logged_session_id' in request.session and check_session(request.session['logged_session_id']): 
            session_login =DBSession.query(Login_Session).filter_by(id=request.session['logged_session_id'])
            headers = remember(request,session_login.group)
            request.session.flash('Welcome Back !')    
            return HTTPFound(location=request.route_url('list'),headers=headers)
        else:
            request.session.flash('Please enter a User Name or Password!')
            return HTTPFound(location=request.route_url('login'))
    return {}

@view_config(route_name='cooky_check', renderer='coky_check.mako')
def cooky_check(request):
    if 'logged_session_id' in request.session and check_session(request.session['logged_session_id']):
        data_exists = request.session['logged_session_id']
    else:
        data_exists ='no'  
    return {'data_exists' : data_exists}


@view_config(context='pyramid.exceptions.NotFound', renderer='notfound.mako')
def notfound_view(request):
    request.response.status = '404 Not Found'
    return {}

@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    response = Response()
    request.session.invalidate()
    
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

