""" Check validation
"""
from plone.app.layout.viewlets.common import ViewletBase
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class CheckValidation(ViewletBase):
    """ Check validation """
    #TODO: in-place invalidation doesn't show this vielet
    index = ViewPageTemplateFile('checkvalidation.pt')

    def update(self):
        """
        Checker if viewlet should be rendered or not
        """
        context = self.context
        wf = getToolByName(context, 'portal_workflow')
        if 'linguaflow' not in wf.getChainFor(context):
            self.invalid = False
            return
        linguaflow = wf.linguaflow
        linguaState = wf.getInfoFor(context,
                                    'review_state',
                                    None,
                                    linguaflow.getId())
        self.invalid = invalid = linguaState == 'invalid'
        if not invalid:
            return
        history = wf.getHistoryOf(linguaflow.getId(), context)
        invalidationTime = history and history[-1]['time'] or None
        modificationTime = context.modified()
        # Invalidation changes modification time so I subtract 2 seconds
        #   just in case.
        modificationTime = modificationTime - (1.0 / 24 / 3600 * 2)
        self.uptodate = modificationTime > invalidationTime


