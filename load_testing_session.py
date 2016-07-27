#NOTE: untested as for now

import load_testing_page_response

# to use static_vars functionality
import helpers

# to print out error
import traceback

# Human readable print functions
import pprint

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

# to use PCRE in this module
import re

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

    # Load Resources flag
    LOAD_RESOURCES = 0x00000001

    # Verbose flag
    VERBOSE = 0x00000002

    # File output format
    FILE_OUT_FORMAT = "%s%stest%i-rawData%i-%s.txt" % (self.__output_dir, os.pathsep, \
                self.__test_num, fetchRawDataFromUrl.page_num, "info")

    # TODO: docstringify
	# /**
	#  * Constructor
	#  * @param int $testNum Test number
	#  * @param string $rand Random token for test
	#  * @param string $cookieDir Cookie directory (default: 'cookies')
	#  * @param string $outputDir Output directory (default: 'output')
	#  */
    def __init__(self, test_num, rand, cookie_dir = 'cookies', output_dir = 'output'):

        # Flags
        __flags = None

        # Test Number
        self.__test_num = test_num

        # Random token for test
        self.__rand = rand

        # Cookie directory
        self.__cookie_dir = cookie_dir

        # Output directory
        self.__output_dir = output_dir

        # Last response headers
        self.__last_resp_headers = []

        # Last URL
        self.__last_url = None

        # Min. delay (in ms) after fetching page
        self.__min_delay = 0
        # Max. delay (in ms) after fetching page
        self.__max_delay = 0
        # Track last used delay
        self.__delay = None

        # Resource cache
        self.__resource_cache = [] # NOTE: array or map?

        # Resource data
        self.__resource_data = [] # NOTE: array or map?

        # Base url that resources will be loaded for
        self.loadable_resource_base_url = None

        # Seed random number generate
        random.seed(test_num * time.time())

        # Set up curl handle
        self.__ch = pycurl.Curl()

        # TODO: UNFINISHED

        # NOTE: no need as pycurl should store
        # the output in the StringIO buffer
        # and it's the only choice
        # "Setup curl_exec to return output"

        # Don't include HTTP headers in output
        self.__ch.setopt(pycurl.HEADER, 0)

        # Set up function to get headers
        self.__ch.setopt(pycurl.HEADERFUNCTION, self.getLastCurlRespHeaders)

        # Include request header in curl info
        # http://stackoverflow.com/questions/11280684/what-is-the-use-of-pycurl-infotype-header-out
        # NOTE: CURLINFO_HEADER_OUT can't be specified as an option

        # Follow redirects
        self.__ch.setopt(pycurl.FOLLOWLOCATION, 1)

        # Don't use persist connection
        self.__ch.setopt(pycurl.FRESH_CONNECT, 1)

        # Enable compression
        self.__ch.setopt(pycurl.ENCODING, '')

        # Timeouts
        self.__ch.setopt(pycurl.CONNECTTIMEOUT, 30)
        self.__ch.setopt(pycurl.TIMEOUT, 120)

        # Set cookie jar (i.e. filename)
        self.__cookie_jar = os.tempnam(self.__cookie_dir, 'cookie-')
        self.__ch.setopt(pycurl.COOKIEJAR, self.__cookie_jar)

        # Don't check SSL
        self.__ch.setopt(pycurl.SSL_VERIFYPEER, 0)


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
    @helpers.static_vars(page_num=0)
    def fetchRawDataFromUrl(self, url, post = None, headers = [], `save_data` = False):
        # Set referer
        if self.__last_url:
            self.__ch.setopt(pycurl.REFERER, self.__last_url)
        self.__last_url = url

        # Set post info
        if post:
            self.__ch.setopt(pycurl.POST, 1)
            self.__ch.setopt(pycurl.POSTFIELDS, post)
        else:
            self.__ch.setopt(pycurl.POST, 0)

        # Set up headers
        self.__ch.setopt(HTTPHEADER, headers)

        # Get page
        self.__ch.setopt(pycurl.URL, url)
        self.__last_resp_headers = [] # Clear last response headers

        # Setting up a buffer to write out response
        content = StringIO()
        self.__ch.setopt(pycurl.WRITEDATA, content)
        self.__ch.perform() # throws Error upon failure

        # Save data
        if save_data:
            fetchRawDataFromUrl.page_num += 1
            # NOTE: INFINISHED INFO OUT
            with open(FILE_OUT_FORMAT % (self.__output_dir, os.pathsep, \
                        self.__test_num, fetchRawDataFromUrl.page_num, "info"), "w") as f:
                f.write(pprint.pprint(<>)+pprint.pprint(self.__last_resp_headers))
            with open(FILE_OUT_FORMAT % (self.__output_dir, os.pathsep, \
                        self.__test_num, fetchRawDataFromUrl.page_num, "content"), "w") as f:
                f.write(content)

        return content


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
        # Add slight delay to simulate user delay
        if self.__min_delay or self.__max_delay:
            delay = random.randrange(self.__min_delay*1000, self.__max_delay*1000)
            self.__delay = (delay/1000000)
            if self.__flags & self.VERBOSE:
                echo 'Delay: %is' % (delay/1000000)
            time.sleep(delay/1000000)

        # Set referer
        if self.__last_url:
            self.__ch.setopt(pycurl.REFERER, self.__last_url)
        self.__last_url = url

        rtn = LoadTestingPageResponse()

        # Set post info
        if post:
            self.__ch.setopt(pycurl.POST, 1)
            self.__ch.setopt(pycurl.POSTFIELDS, post)
        else:
            self.__ch.setopt(pycurl.POST, 0)

        # Set up headers
        self.__ch.setopt(HTTPHEADER, headers)

        # Get page
        if self.__flags & self.VERBOSE:
            print(datetime.date.today().strftime("%m/%d/%Y %-H:%M:%S"))
        self.__ch.setopt(pycurl.URL, url)
        self.__last_resp_headers = [] # Clear last response headers
        start_time = time.time()
        try:
            content = self.__ch.perform()
        except pycurl.error:
            end_time = time.time()
            total_time = end_time - start_time
            if is_user:
                recordPageTime(end_time, total_time, True, 0) # NOTE: located in run_load_test.py
            recordURLPageLoad(self.removeQueryStringAndFragmentFromUrl(url),end_time, total_time, True, 0)
            traceback.print_exc() # throw last error
        curl_info = # NOTE: CAN'T FIGURE OUT HOW TO GET IT
        rtn.setContent(content, curl_info['content_type'])

        # Get info
        rtn.setInfo(curl_info)
        if self.__flags & self.VERBOSE:
            print(datetime.date.today().strftime("%m/%d/%Y %-H:%M:%S"))

        # Record bandwidth
        info = rtn.getInfo()
        kb = 0
        if info['download_content_length'] > 0:
            kb = int(info['download_content_length'])/1024
        elif info['size_download'] > 0:
            kb = int(infp['size_download'])/1024

        # Check response code
        resp_code = rtn.getHttpStatus()
        resp_error = False
        if not (resp_code >= 200 && resp_code <= 399):
            resp_error = True

        # Record info
        end_time = time.time()
        total_time = rtn.getTotalTime()
        if is_user:
            recordPageTime(end_time, total_time, resp_error, 0)
        recordURLPageLoad(self.removeQueryStringAndFragmentFromUrl(url), end_time, total_time, resp_error, kb)

        # Save files
        if save_data:
            # TODO: unfinished
            # TODO: revise code formatting (is it too long sometimes?)


    # TODO: docstringify
	# /**
	#  * Parse page and request other resources
	#  * @param LoadTestingPageResponse $page Page object
	#  */
    def loadResources(page):
        if self.loadable_resource_base_url:
            resources = [] # TODO: assuming it's list

            # Get CSS hrefs
            for href in page.getCssHrefs():
                if href.find(self.loadable_resource_base_url) == 0:
                    resources.append(href)

            # Get image hrefs
            for href in page.getImageHrefs():
                if href.find(self.loadable_resource_base_url) == 0:
                    resources.append(href)

            # Get javascript srcs
            for src in page.getJavascriptSrcs():
                if src.find(self.loadable_resource_base_url) == 0:
                    resources.append(src)

            # Set up new curl object
            ch = pycurl.Curl()
            if resources and ch:
                # Set options


    # TODO: docstringify
	# /**
	#  * Get automatic value for form field
	#  * @param string $name Field name
	#  * @return string Value, or null
	#  */
    def getFormAutoValue(name):
        lower_alpha = 'abcdefghijklmnopqrstuvwxyz'

        # Names
        if re.match('.*first.*name', name, re.IGNORECASE):
            return 'Load'
        elif re.match('.*last.*name', name, re.IGNORECASE):
            return 'Test%s' % self.__test_num
        # E-mails
        elif re.match('.*email', name, re.IGNORECASE):
            return lower_alpha[random.randrange(25)] + lower_alpha[random.randrange(25)] +
                    '-LoadTest' + self.__test_num + '-' + time.time() + '@example.com'
        # Passwords
        elif re.match('.*password', name, re.IGNORECASE):
            return 'password'
        # Address
        elif re.match('.*address', name, re.IGNORECASE):
            return self.test_num + ' Load Test Ave.'
        # City
        elif re.match('.*city', name, re.IGNORECASE):
            return 'Moorestown'
        # Country
        elif re.match('.*country', name, re.IGNORECASE):
            return 'US'
        # State
        elif re.match('.*state', name, re.IGNORECASE):
            return 'NJ'
        # Zip code
        elif re.match('.*zipcode', name, re.IGNORECASE):
            return '08057'
        # Dob (Random)
        elif re.match('.*dob', name, re.IGNORECASE):
            return "%i/%i/%i" % (random.randrange(1,12), random.randrange(2,28), \
                                                random.randrange(1950, 2005))
        # Phone (Random)
        elif re.match('.*phone', name, re.IGNORECASE):
            return "%i-555-%04d" % (random.randrange(100, 999), random.randrange(0, 9999))
        # Gender (Random)
        elif re.match('.*gender', name, re.IGNORECASE):
            return 'M' if random.getrandbits(1) else 'F'
        # Credit card info
        elif re.match('.*cardNumber', name, re.IGNORECASE):
            return '4111111111111111'
        elif re.match('.*cvv', name, re.IGNORECASE):
            return '123'
        elif re.match('.*cardExpiresMonth', name, re.IGNORECASE):
            return random.randrange(1,12)
        elif re.match('.*cardExpiresYear', name, re.IGNORECASE):
            return 2050

        return None
