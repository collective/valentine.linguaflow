from Products.CMFCore.utils import getToolByName

def setupVarious(context):

    if context.readDataFile('valentine.linguaflow_various.txt') is None:
        return

    logger = context.getLogger('valentine.linguaflow')

    # Add linguaflow workflow as parallel default workflow
    portal = context.getSite()
    wf = getToolByName(portal, 'portal_workflow')
    default_chain = list(wf._default_chain)
    if 'linguaflow' not in default_chain:
        default_chain.append('linguaflow')
        wf.setDefaultChain(' '.join(default_chain))
        logger.info("Valentine Linguaflow: add linguaflow workflow as parallel default workflow")

    # Add linguaflow for folder workflow too if it doesn't use the default
    folder_chain = list(wf.getChainForPortalType('Folder'))
    if 'linguaflow' not in folder_chain:
        folder_chain.append('linguaflow')
        wf.setChainForPortalTypes(('Folder',), folder_chain)
        logger.info("Valentine Linguaflow: add linguaflow for folder workflow")

    logger.info("Valentine Linguaflow: done setting import steps")
