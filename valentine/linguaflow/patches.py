from zope.event import notify

from collective.monkey.monkey import Patcher
from valentine.linguaflow.events import TranslationObjectUpdate

linguaPatcher = Patcher('LinguaPlone')

#LinguaPlone patches
from Products.LinguaPlone.I18NBaseObject import I18NBaseObject

def processForm(self, data=1, metadata=0, REQUEST=None, values=None):
    """ Find out what language dependent fields have changed. """
    outdated = self.isOutdated()
    orig_name = getattr(processForm, linguaPatcher.ORIG_NAME)
    origProcessForm = getattr(self, orig_name)
    origProcessForm(data, metadata, REQUEST, values)
    if not self.isCanonical() and outdated:
        tUpdate = TranslationObjectUpdate(self.getCanonical(), self, 'validate')
        notify(tUpdate)
    
def invalidateTranslations(self):
    """Marks the translation as outdated."""
    translations = self.getNonCanonicalTranslations()
    for lang in translations.keys():
        translation = translations[lang][0]
        translation.notifyCanonicalUpdate()
        cUpdate = TranslationObjectUpdate(self, translation,'invalidate')
        notify(cUpdate)
    self.invalidateTranslationCache()


linguaPatcher.wrap_method(I18NBaseObject, 'invalidateTranslations', invalidateTranslations)
linguaPatcher.wrap_method(I18NBaseObject, 'processForm', processForm)

