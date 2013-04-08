from zope.interface import Interface

class ISemiStaticRenderer(Interface):
    def renderer(request,  path,  parms):
        pass
