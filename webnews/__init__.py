from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.view import view_config

from webnews.views.security import groupfinder

from .models.mymodel import (
    DBSession,
    Base,
    News)

from pyramid_sacrud import PYRAMID_SACRUD_HOME, PYRAMID_SACRUD_VIEW

authn_policy = AuthTktAuthenticationPolicy('seekrit', callback=groupfinder, hashalg='sha512')
authz_policy = ACLAuthorizationPolicy()

def sacrud_settings(config):
    config.include('pyramid_sacrud', route_prefix='admin')
    config.registry.settings['pyramid_sacrud.models'] = (('WebNews', [News]),)

@view_config(
    context=News,
    renderer='templates/news_sacrud.jinja2',
    route_name=PYRAMID_SACRUD_VIEW
)
def admin_news_view(context, request):
    return {}


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    #authn_policy = AuthTktAuthenticationPolicy(
    #    'sosecret', callback=groupfinder, hashalg='sha512')
    #authz_policy = ACLAuthorizationPolicy()

    config = Configurator(settings=settings, root_factory='webnews.models.mymodel.Accesses')
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)    

    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.routes')
    	
    config.include('ps_alchemy')

    config.include(sacrud_settings)
    settings = config.registry.settings

    
    config.scan()
    return config.make_wsgi_app()
