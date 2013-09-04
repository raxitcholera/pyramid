from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from sqlalchemy import func 
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from users.security import groupfinder


from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    authn_policy = AuthTktAuthenticationPolicy(
        'sosecret', callback=groupfinder)
    authz_policy = ACLAuthorizationPolicy()
    session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')
    Base.metadata.bind = engine
    config = Configurator(settings=settings, session_factory=session_factory,root_factory='users.models.RootFactory')
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/home')
    config.add_route('login','/')
    config.add_route('logout','/logout')
    config.add_route('list', '/list')
    config.add_route('new', '/new')
    config.scan()
    return config.make_wsgi_app()
