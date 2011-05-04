""" Doctest runner for 'valentine.linguaflow'
"""
import base
import doctest
from Testing.ZopeTestCase import ZopeDocFileSuite
from unittest import TestSuite

optionflags =  (doctest.ELLIPSIS |
                doctest.NORMALIZE_WHITESPACE |
                doctest.REPORT_ONLY_FIRST_FAILURE)

def setUp(root):
    portal = root.portal
    root.setRoles(['Manager'])
    ourId = portal.invokeFactory('Folder', id='folder')
    portal.portal_workflow.doActionFor(portal[ourId], 'publish')

def test_suite():
    suite = TestSuite()
    suite.addTest(ZopeDocFileSuite(
                'README.txt',
                setUp=setUp,
                package="valentine.linguaflow",
                test_class=base.ValentineLinguaflowFunctionalTestCase,
                optionflags=optionflags),
                )
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
