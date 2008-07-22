from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

@onsetup
def setup_valentine_linguaflow():

    fiveconfigure.debug_mode = True
    import Products.Five
    import valentine.linguaflow
    zcml.load_config('meta.zcml', Products.Five)
    zcml.load_config('configure.zcml', valentine.linguaflow)
    fiveconfigure.debug_mode = False

    ptc.installProduct('PloneLanguageTool')
    ptc.installProduct('LinguaPlone')


setup_valentine_linguaflow()

ptc.setupPloneSite(products=['PloneLanguageTool', 'LinguaPlone'], extension_profiles=('valentine.linguaflow:default',))

class ValentineLinguaflowTestCase(ptc.PloneTestCase):
    """ """

class ValentineLinguaflowFunctionalTestCase(ptc.FunctionalTestCase):
    """ """
