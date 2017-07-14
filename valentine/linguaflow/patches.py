""" Patches
"""
from hashlib import md5
from zope.event import notify
from valentine.linguaflow.events import TranslationObjectUpdate
from Products.Archetypes.atapi import BaseObject
from Products.Archetypes.utils import shasattr
from Products.LinguaPlone import config
from Acquisition import aq_inner
from Acquisition import aq_parent

def processForm(self, data=1, metadata=0, REQUEST=None, values=None):
    """ Find out what language dependent fields have changed. """
    request = REQUEST or self.REQUEST
    if values:
        form = values
    else:
        form = request.form

    fieldset = form.get('fieldset', None)
    schema = self.Schema()
    schemata = self.Schemata()
    fields = []

    if fieldset is not None:
        try:
            fields = schemata[fieldset].fields()
        except KeyError:
            if data:
                fields += schema.filterFields()
    else:
        if data:
            fields += schema.filterFields()

    form_keys = form.keys()
    oldValues = {}
    for field in fields:
        if not field.languageIndependent and field.getName() in form_keys:
            # we have a translatable field in the form
            # save a hash for old value
            accessor = field.getAccessor(self)
            oldValues[field.getName()] = md5(str(accessor())).hexdigest()

    translations = getattr(self, 'getTranslations', lambda: '')()
    has_translations = len(translations) > 1
    modified_independent_fields = []
    lang_independent_fields_old_values = {}
    if has_translations:
        lang_independent_fields = [i for i in fields if
                                   i.isLanguageIndependent(i)]
        for field in lang_independent_fields:
            fname = field.getName()
            if fname in form_keys:
                form_value = form.get(fname)
                if form_value:
                    accessor = field.getAccessor(self)
                    lang_independent_fields_old_values[field.getName()] = \
                        md5(str(accessor())).hexdigest()

    # START LinguaPlone.I18NBaseObject.processForm method
    is_new_object = self.checkCreationFlag()
    BaseObject.processForm(self, data, metadata, REQUEST, values)

    # EEA #71102 reindex translations if languageIndependent fields
    # are modified as right now as of Plone 4.3.x only the object
    # being modified is reindexed even though language independent
    # fields are set on all translations
    if has_translations:
        for fName, fValue in lang_independent_fields_old_values.items():
            schema_accessor = schema.getField(fName).getAccessor(self)()
            if fValue != md5(str(schema_accessor)).hexdigest():
                modified_independent_fields.append(fName)
        if modified_independent_fields:
            for translation in translations:
                obj = translations[translation][0]
                if obj.isCanonical():
                    continue
                obj.reindexObject()

    #
    # Translation invalidation moved to the end
    #

    if self._at_rename_after_creation and is_new_object:
        new_id = self._renameAfterCreation()
    else:
        new_id = self.getId()

    if shasattr(self, '_lp_default_page'):
        delattr(self, '_lp_default_page')
        if not self.isCanonical():
            language = self.getLanguage()
            canonical = self.getCanonical()
            canonical_parent = aq_parent(aq_inner(canonical))
            parent = aq_parent(aq_inner(self))
            if parent == canonical_parent and \
                         not parent.hasTranslation(language):
                parent.addTranslation(language)
                translation_parent = parent.getTranslation(language)
                values = {'title': self.Title()}
                translation_parent.processForm(values=values)
                translation_parent.setDescription(self.Description())
                parent = translation_parent
            if shasattr(parent, 'setDefaultPage'):
                parent.setDefaultPage(new_id)

    if shasattr(self, '_lp_outdated'):
        delattr(self, '_lp_outdated')
    # END - LinguaPlone.I18NBaseObject.processForm method

    changedFields = []
    for fName, md5Hex in oldValues.items():
        schema_accessor = schema.getField(fName).getAccessor(self)()
        if md5Hex != md5(str(schema_accessor)).hexdigest():
            # translatable field changed
            changedFields.append(fName)

    if config.AUTO_NOTIFY_CANONICAL_UPDATE:
        comment = 'Fields changed: %s' % ','.join(changedFields)
        if self.isCanonical() and changedFields:
            self.invalidateTranslations(comment)
            # mark canonical with the changes but no state change
            cUpdate = TranslationObjectUpdate(self,
                                              self,
                                              'nochange',
                                              comment=comment)
            notify(cUpdate)

def invalidateTranslations(self, comment=''):
    """ Marks the translation as outdated. """
    translations = self.getNonCanonicalTranslations()
    for lang in translations.keys():
        translation = translations[lang][0]
        translation.notifyCanonicalUpdate()
        if comment:
            cUpdate = TranslationObjectUpdate(self,
                                              translation,
                                              'invalidate',
                                              comment=comment)
            notify(cUpdate)
    if hasattr(self, 'invalidateTranslationCache'):
        self.invalidateTranslationCache()
