from .api import get_semistatic_renderer

def rendering_view(context, request):
    renderer = get_semistatic_renderer(request)
    return renderer.render(request, request.matchdict["path"],  {})
