from zope.event import notify

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.CMFPlone import PloneMessageFactory as _

from valentine.linguaflow.events import TranslationObjectUpdate
from DateTime import DateTime

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
                    review_history = list(workflow.getInfoFor(self.context, 'review_history', [], wfId))

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
        self.context = context.getCanonical()
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


class SyncWorkflow(object):
    """ """
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.languages = request.get('languages')        
        
    def __call__(self):
        context = self.context.getCanonical()
        wf = getToolByName(context, 'portal_workflow')
        wf_id = wf.getChainFor(context)[0]
        canonical_state = wf.getInfoFor(context, 'review_state')
        last_transition = wf.getHistoryOf(wf_id, context)[-1]
        last_transition['comments'] = self.request.get('comment', 'Sync workflow state')
        last_transition['actor'] = getToolByName(context, 'portal_membership').getAuthenticatedMember()
        last_transition['time'] = DateTime()
        translations = context.getNonCanonicalTranslations()
        expirationDate = self.request.get('syncExpirationDate', None) and context.getExpirationDate()
        effectiveDate = self.request.get('syncEffectiveDate', None) and context.getEffectiveDate()
        syncLocalRoles = self.request.get('syncLocalRoles', False)
        local_roles = context.get_local_roles()
        for lang in self.languages:
            translation = translations[lang][0]
            translation_state = wf.getInfoFor(translation, 'review_state')
            if canonical_state != translation_state:
                translation_history = list(translation.workflow_history[wf_id])
                translation_history.append(last_transition)
                translation.workflow_history[wf_id] = tuple(translation_history)
                if effectiveDate is not None:
                    print effectiveDate
                    translation.setEffectiveDate(effectiveDate)
                    
                if expirationDate is not None:
                    print expirationDate
                    translation.setExpirationDate(expirationDate)                    

            if syncLocalRoles:
                for userid, roles in local_roles:
                    translation.manage_setLocalRoles(userid, roles)
                     
        self.request.RESPONSE.redirect(self.context.absolute_url() + '/manage_translations_form')

