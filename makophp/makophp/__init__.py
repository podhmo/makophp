from pyramid.config import Configurator

def install_html_mako(config):
    from .semistatic import SemiStaticRenderer
    from .interfaces import ISemiStaticRenderer
    semistatic = SemiStaticRenderer(config.registry.settings["makophp.mako.directory"])
    semistatic.validate()
    config.registry.registerUtility(semistatic, ISemiStaticRenderer) #todo:introspection

    config.add_renderer('.html' , 'pyramid.mako_templating.renderer_factory')
    config.add_renderer('.htm' , 'pyramid.mako_templating.renderer_factory')
    config.add_route("html.mako", "/{path:.*}")    
    config.add_view(".views.rendering_view", route_name="html.mako")

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.include(install_html_mako)
    return config.make_wsgi_app()
