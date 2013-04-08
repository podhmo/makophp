from .interfaces import ISemiStaticRenderer

def get_semistatic_renderer(request):
    return request.registry.getUtility(ISemiStaticRenderer)
