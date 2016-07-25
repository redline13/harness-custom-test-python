#NOTE: untested as for now

# python helpers to implement PHP-like features
import helpers

# substitute for PHP's DOMDocument
from bs4 import BeautifulSoup

# regex module to match strings
import re

# to choose random elems
import random

# Load Testing Page Response
class LoadTestingPageResponse(object):

    # Request information
    __info = {}

    # Content
    __content = None

    # BS html page object
    __doc = None

    # TODO: docstringify
    # /**
	#  * Set the curl info for the page
	#  * @param string Curl info
	#  */
    def setInfo(self, info):
        self.__info = info

        # Output timing info
        print( "%s: %fs" % (self.getCurrentUrl(), self.getTotalTime()) )


    # TODO: docstringify
    # /**
	#  * Get the curl info for the page
	#  * @return string Curl info
	#  */
    def getInfo(self):
        return self.__info


    # TODO: docstringify
    # NOTE: if content type is not HTML the __doc will remain None | Is it acceptable?
    # /**
	#  * Set the page content.
	#  * @param string Page content
	#  * @param string $contentType Optional content type.  If not detected as HTML,
	#  * 	it wil not be loaded.
	#  */
    def setContent(self, content, content_type = None):
        self.__content = content
        accpt_cont_types = ['text/html', 'application/xhtml+xml', 'text/xml', 'application/xml']
        if not content_type or content_type in accpt_cont_types:
            self.__doc = BeautifulSoup(self.__content, 'html.parser')


    # TODO: docstringify
	# /**
	#  * Get the page content.
	#  * @return string Page content
	#  */
    def getContent(self):
        return self.content


    # TODO: docstringify
    # /**
	#  * Get HTTP status code
	#  * @return int HTTP status code
	#  */
    def getHttpStatus(self):
        return int(self.__info['http_code']) if not helpers.empty(self.__info, 'http_code') else None


    # TODO: docstringify
    # /**
	#  * Check if there was an error
	#  * @return bool True if this looks like there was an error
	#  */
    def hasError(self):
        if not (self.getHttpStatus() == 200):
            return True


    # TODO: docstringify
	# /**
	#  * Get error message returned to user
	#  * @return string Error message returned to the user
	#  */
    def getUserErrorMessage(self):

        # Add application specific code here to get an application specific error message

        return None


    # TODO: docstringify
    # /**
	#  * Check if the page appears as though a POST form submission succeeded
	#  * @return bool True if this looks like a POST form successful submission
	#  */
    def isPlausibleSuccessfulPost(self):

        # Application specific code here

        try:
            is_redirect_count_positive = bool(int(self.__info['redirect_count']) > 0)
        except ValueError, KeyError:
            is_redirect_count_positive = False

        return not self.hasError() and is_redirect_count_positive


    # TODO: docstringify
    # /**
	#  * Get current URL
	#  * @return string Current URL
	#  */
    def getCurrentUrl():
        return int(self.__info['url']) if not helpers.empty(self.__info, 'url') else None


    # TODO: docstringify
    # /**
	#  * Get total time to load page
	#  * @return float Total time to load page
	#  */
    def getTotalTime(self):
        return float(self.__info['total_time']) if not helpers.empty(self.__info, 'total_time') else None


    # TODO: docstringify
	# /**
	#  * Parse the HTML content.
	#  * @return DOMDocument
    def getHtmlDoc(self):
        return self.__doc # NOTE: can return None (see line 44)


    # TODO: docstringify
    # /**
	#  * Get base URL
	#  * @return string Base URL
	#  */
    def getRelativeBase(self):
        base = ''
        base_elem = self.__doc.base
        if(self.__doc.base):
            base = base_elem.get('href')
        else:
            #Check for URLs in the form http://www.domain.com with no trailing slashes
            if helpers.isRelativeBase(self.__info['url']):
                base = self.__info['url']
            else:
                pos = self.__info['url'].find('/')
                if pos >= 0:
                    base = self.__info['url'][0:pos]
        return base


    # TODO: docstringify
	# /**
	#  * Get page protocol (e.g. http or https)
	#  * @return string Protocol
	#  */
    def getPageProtocol(self):
        return helpers.detectUrlScheme(self.__info['url'])


    # TODO: docstringify
	#  /**
	#  * Get base host
	#  * @return string Base URL
	#  */
    def getAbsoluteBase(self):
        base = ''
        base_elem = self.__doc.base
        if(self.__doc.base):
            base = base_elem.get('href')
        else:
            if helpers.isAbsoluteBase(self.__info['url']):
                base = self.__info['url']
        if base and base[-1] == '/':
            base = base[0:-1]
        return base


    # TODO: docstringify
	# /**
	#  * Get list of links on the page.
	#  * @return array List of unique links
	#  */
    def getLinks(self):
        abs_base = self.getAbsoluteBase()
        rel_base = self.getRelativeBase()
        protocol = self.getPageProtocol()

        links = []
        link_elems = self.__doc.findAll('a')
        for link_elem in link_elems:
            link = self.formatLink(link_elem, 'href')
            if not link in links:
                links.append(link)
        return links


    # TODO: docstringify
    # /**
	#  * Get form elements.
	#  * @return array Array of form elements
	#  */
    def getFormElems(self):
        # Find the first non-login form
        forms = self.__doc.findAll('form')
        form = None
        for tmp in forms:
            if not # TODO: match the behavior of source or not?
            # NOTE: UNFINISHED


    # TODO: docstringify
	# /**
	#  * Get form elements names.
	#  * @return array Array of form element names.
	#  */
    def getFormElemNames(self):
        names = []
        for elem in self.getFormElems():
            name = elem.get('name')
            if name:
                names.append(name)
        return names


    # TODO: docstringify
    # /**
	#  * Get submit button texts
	#  * @return array Array of submit button texts
	#  */
    def getSubmitButtonTexts():
        rtn = []
        tmpl = self.__doc.findAll('input')
        for tmp2 in tmpl:
            if tmp2.get('type').lower() == 'submit':
                rtn.append(tmp2.get('value'))
        return rtn


    # TODO: docstringify
    # /**
	#  * Randomly select an option from a select box
	#  * @param DomElement $elem Select box
	#  * @return string Value
	#  */
    def selectDropdownValue(elem):
        return elem.findChildren()[random.randrange(len(elem.findChildren()))].get('value')


    # TODO: docstringify
    # /**
	#  * Get list of css hrefs on the page.
	#  * @return array List of unique css hrefs
	#  */
    def getCssHrefs(self):
        abs_base = self.getAbsoluteBase()
        rel_base = self.getRelativeBase()
        protocol = self.getPageProtocol()

        hrefs = []
        linkElems = self.__doc.findAll('link')
        for link_elem in link_elems:
            # Check if this is a stylesheet
            if link_elem.get('rel') == 'stylesheet':
                href = self.formatLink(link_elem, 'href')
                if not href in hrefs:
                    hrefs.append(href)
        return hrefs


    # TODO: docstringify
    # /**
	#  * Get list of image href on the page.
	#  * @return array List of unique image hrefs
	#  */
    def getImageHrefs(self):
        abs_base = self.getAbsoluteBase()
        rel_base = self.getRelativeBase()
        protocol = self.getPageProtocol()

        srcs = []
        img_elems = self.__doc.findAll('img')
        for img_elem in img_elems:
            src = self.formatLink(img_elem, 'src')
            if not src in srcs:
                srcs.append(src)
        return srcs


    # TODO: docstringify
    # /**
	#  * Get list of javascript srcs on the page.
	#  * @return array List of unique javascript srcs
	#  */
    def getJavascriptSrcs(self):
        abs_base = self.getAbsoluteBase()
        rel_base = self.getRelativeBase()
        protocol = self.getPageProtocol()

        srcs = []
        script_elems = self.__doc.findAll('script')
        for script_elem in script_elems:
            src = self.formatLink(script_elem, 'src')
            if not src in srcs:
                srcs.append(src)
        return srcs


    # TODO: docstringify
    # additional function to
    # incapsulate link formation
    # that is present in several
    # get__ functions
    def formatLink(self, link, attr):
        link = link_elem.get(attr).strip()
        if link and link.find('data:') != 0:
            if helpers.detectUrlScheme(link):
                return link
            elif helpers.detectUrlNetloc(link):
                return "%s:%s" % (protocol, link)
            elif link[0] == '?' or link[0] == '#':
                tmp = self.getCurrentUrl()
                pos = tmp.find(link[0])
                if pos != -1:
                    tmp = tmp[0:pos]
                return tmp + link
            elif link[0] == '/':
                return abs_base + link
            else:
                return "%s/%s" % (rel_base, link)
