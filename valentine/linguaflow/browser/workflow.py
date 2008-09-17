from zope.event import notify

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.CMFPlone import PloneMessageFactory as _

from valentine.linguaflow.events import TranslationObjectUpdate

class WorkflowHistory(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request
        
    def histories(self):
        """Return workflow history of this context.

        Taken from plone_scripts/getWorkflowHistory.py
        """
        context = self.context

        workflow = getToolByName(context, 'portal_workflow')
        membership = getToolByName(context, 'portal_membership')
        
        history = {}

        # check if the current user has the proper permissions
        if (membership.checkPermission('Request review', self.context) or
            membership.checkPermission('Review portal content', self.context) and
            getToolByName(context, 'portal_url').getPortalObject() != context):
            try:
                # get total history with old unused workflows too
                allWorkflows = getattr(context, 'workflow_history',{}).keys()
                for wfId in allWorkflows:
                    review_history = workflow.getInfoFor(self.context, 'review_history', [], wfId)

                    for r in review_history:
                        if r['action']:
                            r['transition_title'] = workflow.getTitleForTransitionOnType(r['action'],
                                                                                 self.context.portal_type)
                        else:
                            r['transition_title'] = ''
                        
                        actorid = r['actor']
                        r['actorid'] = actorid
                        if actorid is None:
                            # action performed by an anonymous user
                            r['actor'] = {'username': _(u'label_anonymous_user', default=u'Anonymous User')}
                            r['actor_home'] = ''
                        else:
                            r['actor'] = membership.getMemberInfo(actorid)
                            if r['actor'] is not None:
                                r['actor_home'] =  '/author/' + actorid
                            else:
                                # member info is not available
                                # the user was probably deleted
                                r['actor_home'] = ''
                    review_history.reverse()
                    history[wfId] = review_history
                    
            except WorkflowException:
                log( 'valentine.linguaflow: '
                     '%s has no associated workflow' % self.context.absolute_url(), severity=logging.DEBUG)

        return history


class LinguaflowInvalidateAll(object):
    """ Called by invalidate all transition in lingua flow. Here we redistribute
        invalidate translation to each translation. """
    
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        context = self.context
        comment = self.request.get('comment', 'Invalidate all translations initiated.')
        context.invalidateTranslations(comment)
        cUpdate = TranslationObjectUpdate(context, context,'nochange',
                                          comment=comment)
        notify(cUpdate)
        self.request.RESPONSE.redirect(context.absolute_url())

class LinguaflowValidateAll(object):
    """ Called by validate all transition in lingua flow. Here we redistribute
        validate translation to each translation. """
    
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        context = self.context
        comment = self.request.get('comment', 'Validate all translations initiated.')
        translations = context.getNonCanonicalTranslations()                                             
        for lang in translations.keys():
            translation = translations[lang][0]
            cUpdate = TranslationObjectUpdate(context, translation,'validate',comment=comment)
            notify(cUpdate)                       
        self.request.RESPONSE.redirect(context.absolute_url())

