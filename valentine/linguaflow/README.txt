Demo
----

We prepare languages, we will have english as default and swedish and
polish as available languages for translation.

  >>> from Products.CMFCore.utils import getToolByName
  >>> lt = getToolByName(portal, 'portal_languages')
  >>> lt.manage_setLanguageSettings('en', ('en','sv','pl'))

Now we create some content and translations.
 
  >>> portal = self.portal
  >>> folder = portal.folder
  >>> did = folder.invokeFactory('Document', id='doc1', title="Doc one", text='Some doc one text')
  >>> did = folder.invokeFactory('Document', id='doc2', title="Doc two", text='Some doc two text')
  >>> doc1 = folder.doc1
  >>> doc2 = folder.doc2
  
  >>> doc1.addTranslation('sv')
  >>> doc1.addTranslation('pl')

  >>> doc2.addTranslation('sv')  
  >>> doc1_sv = doc1.getTranslation('sv')
  >>> doc1_sv.setTitle('Dok ett')
  >>> doc1_sv.setText('Lite dok ett text')

valentine.linguaflow provides a new workflow which installs as a second default workflow so all
content types that use the default one will automaticall have it.

  >>> wf = getToolByName(portal, 'portal_workflow')
  >>> linguaflow = wf.linguaflow
 
Let check status on our fresh content.

  >>> hist = wf.getHistoryOf(linguaflow.getId(), doc1)
  >>> hist[0]['review_state']
  'valid'

  >>> hist = wf.getHistoryOf(linguaflow.getId(), doc1_sv)
  >>> hist[0]['review_state']
  'valid'

Now if we edit the canonical we can invalidate all translations.

  >>> doc1.processForm(values={'text':'Changed text of doc one'})
  >>> wf.doActionFor(doc1_sv, 'invalidate', comment='Fields changed: text')
  >>> hist = wf.getHistoryOf(linguaflow.getId(), doc1_sv)
  >>> hist[1]['review_state']
  'invalid'

  >>> hist[1]['comments']
  'Fields changed: text'

  >>> doc1_sv.processForm(values={'text':'Translation updated'})
  >>> hist = wf.getHistoryOf(linguaflow.getId(), doc1_sv)
  >>> hist[1]['review_state']
  'invalid'

The translation is still invalid even if we have edited and that is because a
validation has to be manually invoked when editing is done through plone since
we don't know if our changes are small corrections or retranslation of changes
in canonical.

  >>> wf.doActionFor(doc1_sv, 'validate')
  >>> hist = wf.getHistoryOf(linguaflow.getId(), doc1_sv)
  >>> hist[2]['review_state']
  'valid'

  >>> wf.getInfoFor(doc1_sv, 'review_state', None, linguaflow.getId())
  'valid'

  
