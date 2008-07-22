from zope.interface import Attribute, implements
from zope.app.event.interfaces import IObjectEvent

from Products.CMFCore.utils import getToolByName

class ITranslationObjectUpdate(IObjectEvent):
    """ A canonical lingaua plone object has changed. """

    object = Attribute("The canonical object.")
    translation = Attribute("The translation target object.")
    action = Attribute("The workflow action to perform.")

class TranslationObjectUpdate(object):
    """Sent after an canonical object has been edited."""
    implements(ITranslationObjectUpdate)

    def __init__(self, context, target, action):
        self.object = context
        self.target = target
        self.action = action
    
def notifyCanonicalUpdate(obj, event):
    # catch all ITranslatable modified
    wt = getToolByName(obj, 'portal_workflow')
    wt.doActionFor(event.target, event.action)
