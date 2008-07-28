from zope.interface import Attribute, implements
from zope.app.event.interfaces import IObjectEvent

from Products.CMFCore.utils import getToolByName

class ITranslationObjectUpdate(IObjectEvent):
    """ A canonical lingaua plone object has changed or a translation has
        been updated. . """

    object = Attribute("The canonical object.")
    translation = Attribute("The translation target object.")
    action = Attribute("The workflow action to perform.")

class TranslationObjectUpdate(object):
    """Sent after an canonical or translation object has been edited.
       When a canonical is edited the action is 'invalidate' and if
       a translation is edited the action is 'validate'. Both actions
       are performed on the translation."""
    implements(ITranslationObjectUpdate)

    def __init__(self, context, translation, action, changedFields=[]):
        self.object = context
        self.translation = translation
        self.action = action
        self.changedFields = changedFields
    
def notifyCanonicalUpdate(obj, event):
    # catch all ITranslatable modified
    wt = getToolByName(obj, 'portal_workflow')
    if event.changedFields:
        comment = 'Fields changed: %s' % ','.join(event.changedFields)
        wt.doActionFor(event.translation, event.action, comment=comment )
