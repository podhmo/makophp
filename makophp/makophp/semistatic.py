import os
import os.path
import logging
from pyramid.path import AssetResolver
from pyramid.exceptions import ConfigurationError
from pyramid.httpexceptions import HTTPNotFound
from pyramid.renderers import render
from pyramid.interfaces import IRendererFactory
from pyramid.response import FileResponse, Response

logger = logging.getLogger(__name__)

def has_renderer(request, path):
    ext = os.path.splitext(path)[1]
    return bool(request.registry.queryUtility(IRendererFactory, name=ext))

class SemiStaticRenderer(object):
    def __init__(self, prefix):
        self.prefix_original = prefix
        self.prefix = AssetResolver().resolve(prefix).abspath()

    def validate(self):
        if not os.path.exists(self.prefix):
            os.mkdirs(self.prefix)
        if not os.path.exists(self.prefix):
            raise ConfigurationError("{0} is not readable".format(self.prefix))
            
    def is_static(self, request, fullname):
        return not has_renderer(request, fullname)

    def static_render(self, request, fullpath):
        if os.path.isdir(fullpath):
            return directory_response(request, fullpath)
        elif os.path.exists(fullpath):
            return FileResponse(fullpath)
        else:
            return HTTPNotFound("file {0} is not found".format(fullpath))

    def render(self,  request,  path,  value,  package=None):
        fullname = os.path.join(self.prefix_original, path)
        if self.is_static(request, fullname):
            return self.static_render(request, os.path.join(self.prefix, path))
        try:
            return Response(render(fullname, value, request=request, package=path))
        except Exception:
            #this is bad.
            logger.info("{0} is not found".format(fullname))
            raise HTTPNotFound("{0} is not found".format(fullname))

def directory_response(request, path):
    return Response(u"{0} is directory".format(path))
