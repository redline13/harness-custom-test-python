from load_testing_page_response import LoadTestingPageResponse

# to use static_vars functionality
import helpers

# Human readable print functions
import pprint

# to use seed() function
import random

# to use time() function
import time

# to cast string to time
import datetime

# python cURL binders
import pycurl

# to unlink (delete) variables
import os

# to store the output of cURL execution
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

# to use PCRE in this module
import re

# to be able to encode into json
import json


class LoadTestingSession(object):
    """Load Testing Session is the CURL wrapper.
    This is not required but does provide some easy calling and managing of web requests.

    CURL Options Set by Default include (libcurl constant names):
    CURLOPT_HEADER (0) - Do not include headers in output
    CURLOPT_FOLLOWLOCATION (1) - Follow Redirects
    CURLOPT_FRESH_CONNECT (0) - Do not use persist connections.
    CURLOPT_ENCODING ('') - Enable compression
    CURLOPT_CONNECTTIMEOUT (30) - 30 second time out
    CURLOPT_TIMEOUT (120) - Overall timeout
    CURLOPT_COOKIEJAR - Setup location for cookie jar.
    CURLOPT_SSL_VERIFYPEER (0) - Don't validate SSL
    """
    # Load Resources flag
    LOAD_RESOURCES = 0x00000001

    # Verbose flag
    VERBOSE = 0x00000002

    # File output format
    FILE_OUT_FORMAT = "%s%stest%i-%s%i-%s.txt"

    def collect_headers(self, debug_type, debug_msg):
        """Debug function for a curl object to capture and save request headers information

        :param debug_type: pycurl constant that specifies type of the information passed
        :param debug_msg: string debug information passed to a function
        """
        if debug_type == pycurl.INFOTYPE_HEADER_OUT:
            self.__sent_headers = debug_msg

    def __init__(self, test_num, rand, cookie_dir='cookies', output_dir='output'):
        """Constructor

        :param test_num: integer Test number
        :param rand: string Random token for test
        :param cookie_dir: string Cookie directory (default: 'cookies')
        :param output_dir: string Output directory (default: 'output')
        """
        # Flags
        self.__flags = None

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
        self.__resource_cache = {}

        # Resource data
        self.__resource_data = {}

        # Base url that resources will be loaded for
        self.loadable_resource_base_url = None

        # Seed random number generate
        random.seed(test_num * time.time())

        # Set up curl handle
        self.__ch = pycurl.Curl()

        # Don't include HTTP headers in output
        self.__ch.setopt(pycurl.HEADER, 0)

        # Set up function to get headers
        self.__ch.setopt(pycurl.HEADERFUNCTION, self.get_last_curl_resp_headers)

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

        # Verbose to be able to access headers out info
        self.__ch.setopt(pycurl.VERBOSE, 1)

        # Define debug function to capture request headers
        self.__ch.setopt(pycurl.DEBUGFUNCTION, self.collect_headers)

        # variable to hold out headers of a request
        self.__sent_headers = None

    def enable_resource_loading(self):
        """ Enable resource loading """
        self.__flags |= self.LOAD_RESOURCES

    def disable_resource_loading(self):
        """ Disable resource loading """
        self.__flags |= ~self.LOAD_RESOURCES

    def verbose(self):
        """ Verbose """
        self.__flags = self.VERBOSE

        # Output cookie jar file
        print('Cookie jar: %s') % self.__cookie_jar

    def non_verbose(self):
        """ Non-verbose """
        self.__flags &= ~self.VERBOSE

    def set_delay(self, min_delay, max_delay):
        """Set delay (in ms) on page load

        :param min_delay: int Min. artificial delay (in ms) on page load
        :param max_delay: int Max. artificial delay (in ms) on page load
        """
        if min_delay > max_delay:
            swap = min_delay
            min_delay = max_delay
            max_delay = swap
        self.__min_delay = min_delay
        self.__max_delay = max_delay
        if not self.__max_delay:
            self.__max_delay = self.__min_delay

    def get_delay(self):
        """ Send back recently used delay value """
        return self.__delay

    def cleanup(self):
        """ Cleanup """
        # Close curl
        self.__ch.close()

        # Delete cookie file
        if self.__cookie_jar:
            os.unlink(self.__cookie_jar)

    # TODO: http://pycurl.io/docs/latest/callbacks.html according the documentation
    # it should receive a byte string object (this could cause an error so should be
    # double checked
    def get_last_curl_resp_headers(self, header):
        """ Set last curl response headers """
        self.__last_resp_headers.append(header.strip())
        return len(header)

    @helpers.static_vars(page_num=0)
    def fetch_raw_data_from_url(self, url, post=None, headers=[], save_data=False):
        """Fetch raw data form a URL with no delays or output

        :param url: string URL to go to
        :param post: mixed POST data or None
        :param headers: list HTTP headers to send
        :param save_data: bool True to save data to file system
        :return: string Raw response
        """
        # Set referrer
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
        self.__ch.setopt(pycurl.HTTPHEADER, headers)

        # Get page
        self.__ch.setopt(pycurl.URL, url)
        self.__last_resp_headers = []  # Clear last response headers

        # Setting up a buffer to write out response
        content = StringIO()
        self.__ch.setopt(pycurl.WRITEDATA, content)
        self.__ch.perform()  # throws Error upon failure

        # Save data
        if save_data:
            self.fetch_raw_data_from_url.page_num += 1
            with open(self.FILE_OUT_FORMAT % (self.__output_dir, os.pathsep,
                                              self.__test_num, 'rawData', self.fetch_raw_data_from_url.page_num,
                                              "info"), "w") as f:
                f.write(pprint.pprint(self.curl_getinfo(self.__ch)) + pprint.pprint(self.__last_resp_headers))
            with open(self.FILE_OUT_FORMAT % (self.__output_dir, os.pathsep,
                                              self.__test_num, 'rawData', self.fetch_raw_data_from_url.page_num,
                                              "content"), "w") as f:
                f.write(content)

        return content

    @staticmethod
    def remove_query_string_and_fragment_from_url(url):
        """Remove query string and fragment from URL

        :param url: string URL
        :return:string URL without query string and fragment
        """
        pos = url.find('?')
        if not pos == -1:
            return url[0:pos]
        pos = url.find('#')
        if not pos == -1:
            return url[0:pos]
        return url

    @helpers.static_vars(page_num=0)
    def go_to_url(self, url, post=None, headers=[], save_data=False, is_user=True):
        """Go to a url

        :param url: string URL to go to
        :param post: mixed POST data or None
        :param headers: list HTTP headers to send
        :param save_data: bool True to write data to file
        :param is_user: bool Is user?
        :return: LoadTestingPageResponse object
        """
        # Add slight delay to simulate user delay
        if self.__min_delay or self.__max_delay:
            delay = random.randrange(self.__min_delay * 1000, self.__max_delay * 1000)
            self.__delay = (delay / 1000000)
            if self.__flags & self.VERBOSE:
                print('Delay: %is' % (delay / 1000000))
            time.sleep(delay / 1000000)

        # Set referrer
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
        self.__ch.setopt(pycurl.HTTPHEADER, headers)

        # Get page
        if self.__flags & self.VERBOSE:
            print(datetime.date.today().strftime("%m/%d/%Y %-H:%M:%S"))
        self.__ch.setopt(pycurl.URL, url)
        self.__last_resp_headers = []  # Clear last response headers
        start_time = time.time()
        try:
            content = self.__ch.perform()
        except pycurl.error as e:
            end_time = time.time()
            total_time = end_time - start_time
            if is_user:
                record_page_time(end_time, total_time, True, 0)  # NOTE: located in run_load_test.py
            record_url_page_load(self.remove_query_string_and_fragment_from_url(url),
                                 end_time, total_time, True, 0)
            raise Exception(e)
        curl_info = self.curl_getinfo(self.__ch)
        rtn.set_content(content, curl_info['content_type'])

        # Get info
        rtn.set_info(curl_info)
        if self.__flags & self.VERBOSE:
            print(datetime.date.today().strftime("%m/%d/%Y %-H:%M:%S"))

        # Record bandwidth
        info = rtn.get_info()
        kb = 0
        if info['download_content_length'] > 0:
            kb = int(info['download_content_length']) / 1024
        elif info['size_download'] > 0:
            kb = int(info['size_download']) / 1024

        # Check response code
        resp_code = rtn.get_http_status()
        resp_error = False
        if not (200 <= resp_code <= 399):
            resp_error = True

        # Record info
        end_time = time.time()
        total_time = rtn.get_total_time()
        if is_user:
            record_page_time(end_time, total_time, resp_error, 0)
        record_url_page_load(self.remove_query_string_and_fragment_from_url(url),
                             end_time, total_time, resp_error, kb)

        # Save files
        if save_data:
            self.go_to_url.page_num += 1
            with open(self.FILE_OUT_FORMAT % (self.__output_dir, os.pathsep,
                                              self.__test_num, 'page', self.go_to_url.page_num, "info"), "w") as f:
                f.write(pprint.pprint(rtn.get_info()) + pprint.pprint(self.__last_resp_headers))
            with open(self.FILE_OUT_FORMAT % (self.__output_dir, os.pathsep,
                                              self.__test_num, 'page', self.go_to_url.page_num, "content"), "w") as f:
                f.write(rtn.get_content())

    def load_resources(self, page):
        """Parse page and request other resources

        :param page: LoadTestingPageResponse page object
        """
        if self.loadable_resource_base_url:
            resources = []

            # Get CSS hrefs
            for href in page.get_css_hrefs():
                if href.find(self.loadable_resource_base_url) == 0:
                    resources.append(href)

            # Get image hrefs
            for href in page.get_image_hrefs():
                if href.find(self.loadable_resource_base_url) == 0:
                    resources.append(href)

            # Get javascript srcs
            for src in page.get_javascript_srcs():
                if src.find(self.loadable_resource_base_url) == 0:
                    resources.append(src)

            # Set up new curl object
            ch = pycurl.Curl()
            if resources and ch:

                # Set options
                ch.setopt(pycurl.HEADER, 1)
                ch.setopt(pycurl.FOLLOWLOCATION, 1)

                # Use persistent connection
                ch.setopt(pycurl.FORBID_REUSE, 1)
                ch.setopt(pycurl.FRESH_CONNECT, 0)

                # Enable compression
                ch.setopt(pycurl.ENCODING, '')

                # Timeouts
                ch.setopt(pycurl.CONNECTTIMEOUT, 30)
                ch.setopt(pycurl.TIMEOUT, 120)

                # Set cookie jar
                ch.setopt(pycurl.COOKIEJAR, self.__cookie_jar)

                # Don't check SSL
                ch.setopt(pycurl.SSL_VERIFYPEER, 0)

                # Get each resource
                num_in_cache = num304s = 0
                for resource in resources:
                    # Check if this is in the cache
                    if helpers.isset(self.__resource_cache, resource) and \
                                    self.__resource_cache[resource] > time.time():
                        num_in_cache += 1
                    else:
                        # Set up headers
                        headers = [
                            'Cache-Control:max-age=0',
                            'Connection: keep-alive',
                            'Keep-Alive: 300'
                        ]

                    # Check if we have a last modified
                    if helpers.isset(self.__resource_data, resource, 'Last-Modified'):
                        headers.append('If-Modified-Since: %s' %
                                       self.__resource_data[resource]['Last-Modified'])
                    # Check if we have an ETag
                    if helpers.isset(self.__resource_data, resource, 'ETag'):
                        headers.append('If-None-Match: %s' %
                                       self.__resource_data[resource]['ETag'])

                    # Set headers
                    ch.setopt(pycurl.HTTPHEADER, headers)

                    # Make request
                    ch.setopt(pycurl.URL, resource)
                    start_time = time.time()
                    try:
                        content = ch.perform()
                    except pycurl.error as e:
                        end_time = time.time()
                        total_time = end_time - start_time
                        record_page_time(end_time, total_time, True, 0)
                        record_url_page_load(self.remove_query_string_and_fragment_from_url(resource),
                                             end_time, total_time, True, 0)
                        raise Exception(e)

                    # Check status code
                    info = self.curl_getinfo(ch)
                    if int(info['http_code']) == 304:
                        num304s += 1

                    # Record bandwidth
                    kb = 0
                    if info['download_content_length'] > 0:
                        kb = int(info['download_content_length']) / 1024
                    elif info['size_download'] > 0:
                        kb = int(info['size_download']) / 1024

                    # Check response code
                    resp_code = int(info['http_code']) if not helpers.empty(info, 'http_code') else None
                    resp_error = False
                    if not (200 <= resp_code <= 399):
                        resp_error = True
                        err = {
                            'uri': self.remove_query_string_and_fragment_from_url(resource),
                            'code': resp_code
                        }
                        record_error(json.dumps(err))

                    # Record time
                    end_time = time.time()
                    record_url_page_load(self.remove_query_string_and_fragment_from_url(resource),
                                         end_time,
                                         float(info['total_time']) if not helpers.empty(info, 'total_time') else 0.0,
                                         resp_error, kb)

                    # Add resource data
                    if not helpers.isset(self.__resource_data, resource):
                        self.__resource_data[resource] = {
                            'Last-Modified': None,
                            'ETag': None
                        }

                    # Read headers
                    lines = re.split('(\r?\n)|\r', content)
                    lines.pop(0)
                    for line in lines:
                        if not line:
                            break

                        # Parse header
                        match = re.match('^([^:]+):(.*)$', line)
                        if not match:
                            raise Exception("%s: Bad header \"%s\"" % (resource, line))
                        header = match.group(1).strip().lower()
                        value = match.group(2).strip().lower()

                        # Check for cache headers
                        expires = None
                        match = re.match('max-age=([0-9]+)', value)
                        if header == 'cache-control' and match:
                            expires = time.time() + match.group(1)
                        elif header == 'expires':
                            expires = datetime.datetime.strptime(value, "%a, %d %b %Y %H:%M:%S GMT")
                        if expires:
                            self.__resource_cache[resource] = expires

                        # Other headers
                        if header == 'last-modified':
                            self.__resource_data[resource]['Last-Modified'] = value
                        if header == 'etag':
                            self.__resource_data[resource]['ETag'] = value

                if self.__flags & self.VERBOSE:
                    print("Page requires %i resources for base domain. %i found in cache. %i Not Modified responses."
                          % (len(resources), num_in_cache, num304s))

    def get_form_auto_value(self, name):
        """Get automatic value for form field

        :param name: string Field name
        :return:string Value or None
        """
        lower_alpha = 'abcdefghijklmnopqrstuvwxyz'

        # Names
        if re.match('.*first.*name', name, re.IGNORECASE):
            return 'Load'
        elif re.match('.*last.*name', name, re.IGNORECASE):
            return 'Test%s' % self.__test_num
        # E-mails
        elif re.match('.*email', name, re.IGNORECASE):
            return lower_alpha[random.randrange(25)] + lower_alpha[random.randrange(25)] + \
                   '-LoadTest' + self.__test_num + '-' + time.time() + '@example.com'
        # Passwords
        elif re.match('.*password', name, re.IGNORECASE):
            return 'password'
        # Address
        elif re.match('.*address', name, re.IGNORECASE):
            return self.__test_num + ' Load Test Ave.'
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
            return "%i/%i/%i" % (random.randrange(1, 12), random.randrange(2, 28), random.randrange(1950, 2005))
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
            return random.randrange(1, 12)
        elif re.match('.*cardExpiresYear', name, re.IGNORECASE):
            return 2050

        return None

    def curl_getinfo(self, c, opt=None):
        """Function that imitates PHP's curl_getinfo()

        :param c: pycurl object to get info from
        :param opt: certain pycurl opt info to return
        :return: dictionary of pycurl request information
        """
        if opt:
            try:
                return c.getinfo(opt)
            except AttributeError:
                return False
        else:
            info_dict = {
                'url': c.getinfo(pycurl.EFFECTIVE_URL), 'content_type': c.getinfo(pycurl.CONTENT_TYPE),
                'http_code': c.getinfo(pycurl.HTTP_CODE), 'header_size': c.getinfo(pycurl.HEADER_SIZE),
                'request_size': c.getinfo(pycurl.REQUEST_SIZE), 'filetime': c.getinfo(pycurl.INFO_FILETIME),
                'ssl_verify_result': c.getinfo(pycurl.SSL_VERIFYRESULT),
                'redirect_count': c.getinfo(pycurl.REDIRECT_COUNT), 'total_time': c.getinfo(pycurl.TOTAL_TIME),
                'namelookup_time': c.getinfo(pycurl.NAMELOOKUP_TIME),
                'connect_time': c.getinfo(pycurl.CONNECT_TIME),
                'pretransfer_time': c.getinfo(pycurl.PRETRANSFER_TIME),
                'size_upload': c.getinfo(pycurl.SIZE_UPLOAD), 'size_download': c.getinfo(pycurl.SIZE_DOWNLOAD),
                'speed_download': c.getinfo(pycurl.SPEED_DOWNLOAD),
                'speed_upload': c.getinfo(pycurl.SPEED_UPLOAD),
                'download_content_length': c.getinfo(pycurl.CONTENT_LENGTH_DOWNLOAD),
                'upload_content_length': c.getinfo(pycurl.CONTENT_LENGTH_UPLOAD),
                'starttransfer_time': c.getinfo(pycurl.STARTTRANSFER_TIME),
                'redirect_time': c.getinfo(pycurl.REDIRECT_TIME), 'certinfo': c.getinfo(pycurl.INFO_CERTINFO),
                'primary_ip': c.getinfo(pycurl.PRIMARY_IP), 'primary_port': c.getinfo(pycurl.PRIMARY_PORT),
                'local_ip': c.getinfo(pycurl.LOCAL_IP), 'local_port': c.getinfo(pycurl.LOCAL_PORT),
                'redirect_url': c.getinfo(pycurl.REDIRECT_URL), 'request_header': self.__sent_headers
            }

            return info_dict
