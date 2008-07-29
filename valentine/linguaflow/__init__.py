import patches

from Products.CMFCore import DirectoryView
DirectoryView.registerDirectory('skins/linguaflow_templates',
                                    globals())

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
