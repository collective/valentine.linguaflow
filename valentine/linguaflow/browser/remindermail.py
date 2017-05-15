""" Reminder email
"""
import logging
from Products.Five import BrowserView
from Products.CMFPlone.utils import getToolByName

logger = logging.getLogger('Plone')

class ReminderMail(BrowserView):
    """ View to update all feeds
    """

    def send(self):
        """ Send reminder mail
        """
        portal = self.context
        ct = getToolByName(portal, 'portal_catalog')
        wf = getToolByName(portal, 'portal_workflow')
        doActionFor = wf.doActionFor
        invalidTranslations = \
                   [b.getObject() for b in ct(Language='all',
                                              lingua_state='invalid')]
        for translation in invalidTranslations:
            doActionFor(translation, 'notify_editors')
        logger.info('valentine.linguaflow: Notified editors about %d '
                    'invalidated translations', len(invalidTranslations))
