from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView

class InvalidTranslations(BrowserView):
    """ View to find invalid translations and group them for nice display in a
        listing or portlet.

    """
    
    def __call__(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        query = {'lingua_state' : 'invalid',
                 'Language' : 'all'}
        result = catalog(query)
        
        return result
