""" Doctest runner for 'valentine.linguaflow'
"""
from valentine.linguaflow.tests.base import (
    ValentineLinguaflowFunctionalTestCase,
)
import doctest
from unittest import TestSuite
from Testing.ZopeTestCase import ZopeDocFileSuite

optionflags =  (doctest.ELLIPSIS |
                doctest.NORMALIZE_WHITESPACE |
                doctest.REPORT_ONLY_FIRST_FAILURE)

def setUp(root):
    """ Setup """
    portal = root.portal
    root.setRoles(['Manager'])
    ourId = portal.invokeFactory('Folder', id='folder')
    portal.portal_workflow.doActionFor(portal[ourId], 'publish')

def test_suite():
    """ Test suite """
    suite = TestSuite()
    suite.addTest(ZopeDocFileSuite('README.txt',
                            setUp=setUp,
                            package="valentine.linguaflow",
                            test_class=ValentineLinguaflowFunctionalTestCase,
                            optionflags=optionflags),)
    return suite
