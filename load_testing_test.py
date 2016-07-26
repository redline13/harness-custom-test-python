#NOTE: untested as for now

import load_testing_session

# to add the support for an abstract class definition
from abs import ABCMeta, abstractmethod

# Load Testing Test Exception
class LoadTestingTestException(Exception):
    pass

class LoadTestingTest:
    __metaclass__ = ABCMeta

    # TODO: docstringify
    # /** @var LoadTestingSession Access to object to invoke requests to pages and wrap CURL. */
    __session = None

    # Verbose mode
    __verbose = False

    # Ini settings
    __ini_settings = {} # NOTE: my guess it's a map

    # Test Number
    __test_num = None

    # TODO: docstringify
    # /**
	#  * Constructor
	#  * @param int $testNum Test Number
	#  * @param string $rand Random token for test
	#  * @param string $resourceUrl Optional URL specifying host that resources will
	#  * 	be loaded for.  The hostname is grabbed from this URL.
	#  */
    def __init__(self, test_num, rand, resource_url = None):

        # Set up sessoin
        self.__session = LoadTestingSession(test_num, rand)

        # Save test number
        self.__test_num = test_num

        # Load resourse only from base url
