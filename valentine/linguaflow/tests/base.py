""" Base module
"""
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import onsetup
import valentine.linguaflow

PloneTestCase.installProduct('LinguaPlone')

@onsetup
def setup_valentine_linguaflow():
    """ Setup """
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', valentine.linguaflow)
    zcml.load_config('testing.zcml', valentine.linguaflow.tests)
    fiveconfigure.debug_mode = False

setup_valentine_linguaflow()
PloneTestCase.setupPloneSite(
                 extension_profiles=('valentine.linguaflow:default',
                                     'valentine.linguaflow.tests:testing'))

class ValentineLinguaflowTestCase(PloneTestCase.PloneTestCase):
    """ Valentine Linguaflow Test Case """

class ValentineLinguaflowFunctionalTestCase(PloneTestCase.FunctionalTestCase):
    """ Valentine Linguaflow Functional Test Case """
