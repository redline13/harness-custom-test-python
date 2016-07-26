#NOTE: untested as for now

import load_testing_page_response

# to use seed() function
import random

# to use time() function
import time

# python cURL binders
import pycurl

# to unlink (delete) variables
import os

# to store the output of cURL execution
from StringIO import StringIO

# TODO: docstringify
# /**
#  * Load Testing Session is the CURL wrapper.  This is not required but does provide some easy calling and managing of web requests.
#  *
#  * CURL Options Set by Default include
#  * CURLOPT_RETURNTRANSFER (1)
#  * CURLOPT_HEADER (0) - Do not include headers in output
#  * CURLOPT_FOLLOWLOCATION (1) - Follow Redirects
#  * CURLOPT_FRESH_CONNECT (0) - Do not use persist connections.
#  * CURLOPT_ENCODING ('') - Enable compression
#  * CURLOPT_CONNECTTIMEOUT (30) - 30 second time out
#  * CURLOPT_TIMEOUT (120) - Overall timeout
#  * CURLOPT_COOKIEJAR - Setup location for cookie jar.
#  * CURLOPT_SSL_VERIFYPEER (0) - Don't validate SSL
#  */
class LoadTestingSession(object):

    # Test Number
    __test_num = None

    # Random token for test
    __rand = None

    # Cookie directory
    __cookie_dir = None

    # Output directory
    __output_dir = None

    # Flags
    __flags = None

    # Load Resources flag
    LOAD_RESOURCES = 0x00000001

    # Verbose flag
    VERBOSE = 0x00000002

    # Curl handle
    __ch = None

    # Cookie jar (i.e. filename)
    __cookie_jar = None

    # Last response headers
    __last_resp_headers = []

    # Last URL
    __last_url = None

    # Min. delay (in ms) after fetching page
    __min_delay = 0
    # Max. delay (in ms) after fetching page
    __max_delay = 0
    # Track last used delay
    __delay = None

    # Resource cache
    __resource_cache = [] # NOTE: array or map?

    # Resource data
    __resource_data = [] # NOTE: array or map?

    # Base url that resources will be loaded for
    loadable_resource_base_url = None

    # TODO: docstringify
	# /**
	#  * Constructor
	#  * @param int $testNum Test number
	#  * @param string $rand Random token for test
	#  * @param string $cookieDir Cookie directory (default: 'cookies')
	#  * @param string $outputDir Output directory (default: 'output')
	#  */
    def __init__(self, test_num, rand, cookie_dir = 'cookies', output_dir = 'output'):
        self.__test_num = test_num
        self.__rand = rand
        self.__cookie_dir = cookie_dir
        self.__output_dir = output_dir

        # Seed random number generate
        random.seed(test_num * time.time())

        # Set up curl
        self.__ch = pycurl.Curl()

        # TODO: UNFINISHED

        # NOTE: no need as pycurl should store
        # the output in the StringIO buffer
        # and it's the only choice
        # "Setup curl_exec to return output"

        # Don't include HTTP headers in output
        self.__ch.setopt()

        # Set up function to get headers
        self.__ch.setopt()

        # Include request header in curl info
        self.__ch.setopt()

        # Follow redirects
        self.__ch.setopt()

        # Don't use persist connection
        self.__ch.setopt()

        # Enable compression
        self.__ch.setopt()

        # Timeouts
        self.__ch.setopt()
        self.__ch.setopt()

        # Set cookie jar
        self.__cookie_jar = ##
        self.__ch.setopt()

        # Don't check SSL
        self.__ch.setopt()


    # NOTE: no need in __get func as
    # __* vars can be accessed directly?


    # Enable resource loading
    def enableResourceLoading(self):
        self.__flags |= self.LOAD_RESOURCES


    # Disable resource loading
    def disableResourceLoading(self):
        self.__flags |= ~self.LOAD_RESOURCES


    # Verbose
    def verbose(self):
        self.__flags = self.VERBOSE

        # Output cookie jar file
        print('Cookie jar: %s') % self.__cookie_jar


    # Non-verbose
    def nonVerbose(self):
        self.__flags &= ~self.VERBOSE


    # TODO: docstringify
	# /**
	#  * Set delay (in ms) on page load.
	#  * @param int $minDelay Min. artificial delay (in ms) on page load.
	#  * @param int $maxDelay Max. artificial delay (in ms) on page load.
	#  */
    def setDelay(self, min_delay, max_delay):
        if min_delay > max_delay:
            swap = min_delay
            min_delay = max_delay
            max_delay = swap
        self.__min_delay = min_delay
        self.__max_delay = max_delay
        if not self.__max_delay:
            self.__max_delay = self.__min_delay


    # TODO: docstringify
	# /**
	#  * Send back recently used delay value.
	#  */
    def getDelay(self):
        return self.__delay


    # Cleanup
    def cleanup(self):
        # Close curl
        self.__ch.close()

        # Delete cookie file
        if self.__cookie_jar:
            os.unlink(self.__cookie_jar)


    # TODO: docstringify
    # /**
	#  * Set last curl response headers
	#  */
    def getLastCurlRespHeaders(self, ch, header):
        self.__last_resp_headers.append(header.strip())
        return len(header)


    # TODO: docstringify
	# /**
	#  * Fetch raw data form a URL with no delays or output
	#  * @param string $url URL to go to
	#  * @param mixed $post POST data, or null
	#  * @param array $headers HTTP headers to send
	#  * @param bool $saveData True to save data to file system
	#  * @return string Raw response
	#  * @throws Exception
	#  */
    def fetchRawDataFromUrl(self, url, post = None, headers = [], saveData = False):
        # Set referer
        if self.__last_url:
            ### TODO: NOT FINISHED


    # TODO: docstringify
	# /**
	#  * Remove query string and fragment from URL
	#  *
	#  * @param string $url URL
	#  *
	#  * @return string URL without query string and fragment
	#  */
    def removeQueryStringAndFragmentFromUrl(url):
        pos = url.find('?')
        if not pos == -1:
            return url[0:pos]
        pos = url.find('#')
        if not pos == -1:
            return url[0:pos]
        return url


    # TODO: docstringify
    # /**
	#  * Go to a url.
	#  * @param string $url URL to go to
	#  * @param mixed $post POST data, or null
	#  * @param array $headers HTTP headers to send
	#  * @param boolean $saveData writing it to file.
	#  * @return LoadTestingPageResponse
	#  * @throws Exception
	#  */
    def goToUrl(self, url, post = None, headers = [], saveData = False, is_user = True):
        # TODO: UNFINISHED


    # TODO: docstringify
	# /**
	#  * Parse page and request other resources
	#  * @param LoadTestingPageResponse $page Page object
	#  */
    def loadResources(page):
        # TODO: UNFINISHED


    # TODO: docstringify
	# /**
	#  * Get automatic value for form field
	#  * @param string $name Field name
	#  * @return string Value, or null
	#  */
    def getFormAutoValue(name):
        # TODO: UNFINISHED
