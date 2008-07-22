from Products.CMFCore.utils import getToolByName

def setupVarious(context):
    
    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a 
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.
    
    if context.readDataFile('valentine.linguaflow_various.txt') is None:
        return
        
    # Add linguaflow workflow as parallel default workflow
    portal = context.getSite()
    wf = getToolByName(portal, 'portal_workflow')
    default_chain = list(wf._default_chain)
    default_chain.append('linguaflow')
    wf.setDefaultChain(' '.join(default_chain))

    
