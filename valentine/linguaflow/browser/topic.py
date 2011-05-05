""" Topic
"""
from Products.CMFCore.utils import getToolByName

def syncTopicCriteria(canonical, translation):
    """ Sync topic criteria """
    portal_types = getToolByName(canonical, 'portal_types')

    # get the translated object by taking the first part of the url
    for obj in canonical.objectValues():
        if obj.getId().startswith('crit_'):
            # copy the criteria over to the new translated smart folder

            # save content type restrictions and change them temporarily
            # so we are allowed to add criteria objects to the smart folder
            # by default only smart folders can be added to smart folders

            crit_type = getattr(portal_types, obj.portal_type)
            topic_type = getattr(portal_types, translation.portal_type)
            global_allow = crit_type.global_allow
            filter_content = topic_type.filter_content_types

            crit_type.global_allow = True
            topic_type.filter_content_types = False
            if hasattr(translation, obj.getId()):
                translation.manage_delObjects([obj.getId()])
            copy = canonical.manage_copyObjects([obj.getId()])
            translation.manage_pasteObjects(copy)

            # restore the original restrictions
            crit_type.global_allow = global_allow
            topic_type.filter_content_types = filter_content
