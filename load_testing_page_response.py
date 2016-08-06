# python helpers to implement PHP-like features
import helpers

# substitute for PHP's DOMDocument
from bs4 import BeautifulSoup

# regex module to match strings
import re

# to choose random elems
import random


class LoadTestingPageResponse(object):
    """ Load Testing Page Response """

    def __init__(self):

        # Request information
        self.__info = {}

        # Content
        self.__content = None

        # BS html page object
        self.__doc = None

    def set_info(self, info):
        """Set the curl info for the page

        :param info: string Curl info
        """
        self.__info = info

        # Output timing info
        print("%s: %fs" % (self.get_current_url(), self.get_total_time()))

    def get_info(self):
        """Get the curl info for the page

        :returns: string Curl info
        """
        return self.__info

    def set_content(self, content, content_type=None):
        """Set the page content

        :param content: string Page content
        :param content_type: string optional content type. If not detected as HTML,
                it won't be loaded
        """
        #print('------------------')
        #print('SETTING CONTENT ...')
        #print(content)
        #print('------------------')
        self.__content = content

        if not content_type or re.match(r"^(text/html|application/xhtml\+xml|text/xml|application/xml)",
                                        content_type, re.IGNORECASE):
            self.__doc = BeautifulSoup(self.__content, 'html.parser')

        #print('------')
        #print('THE __DOC IS: ')
        #print(self.__doc)
        #print('------')

    def get_content(self):
        """Get the page content

        :return: string Page content
        """
        return self.__content

    def get_http_status(self):
        """Get HTTP status code

        :return: int HTTP status code
        """
        return int(self.__info['http_code']) if not helpers.empty(self.__info, 'http_code') else None

    def has_error(self):
        """Check if there was an error

        :return: bool True if this looks like there was an error
        """
        if not (self.get_http_status() == 200):
            return True

        # Application specific code here
        # Check for 'err' URL parameter
        params = helpers.parse_qs_wrap(helpers.detect_url_query(self.__info['url']))
        return helpers.isset(params, 'err')

    def get_user_error_message(self):
        """Get error message returned to user

        :return: string Error message returned to the user
        """
        # Add application specific code here to get an application specific error message

        return None

    def is_plausible_successful_post(self):
        """Check if the page appears as though a POST form submission succeeded

        :return: bool True if this looks like a POST form successful submission
        """
        # Application specific code here

        try:
            is_redirect_count_positive = bool(int(self.__info['redirect_count']) > 0)
        except (ValueError, KeyError):
            is_redirect_count_positive = False

        return not self.has_error() and is_redirect_count_positive

    def get_current_url(self):
        """Get current URL

        :return: string Current URL
        """
        return self.__info['url'] if not helpers.empty(self.__info, 'url') else None

    def get_total_time(self):
        """Get total time to load page

        :return: float Total time to load page
        """
        return float(self.__info['total_time']) if not helpers.empty(self.__info, 'total_time') else None

    def get_html_doc(self):
        """Parse the HTML content

        :return: BeautifulSoup object
        """
        return self.__doc

    def get_relative_base(self):
        """Get base URL

        :return: string Base URL
        """
        base = ''
        base_elem = self.__doc.base
        if self.__doc.base:
            base = base_elem.get('href')
        else:
            # Check for URLs in the form http://www.domain.com with no trailing slashes
            if helpers.is_relative_base(self.__info['url']):
                base = self.__info['url']
            else:
                pos = self.__info['url'].find('/')
                if pos >= 0:
                    base = self.__info['url'][0:pos]
        return base

    def get_page_protocol(self):
        """Get page protocol (e.g. http or https)

        :return: string Protocol
        """
        return helpers.detect_url_scheme(self.__info['url'])

    def get_absolute_base(self):
        """Get base host

        :return: string Base URL
        """
        base = ''
        base_elem = self.__doc.base
        if self.__doc.base:
            base = base_elem.get('href')
        else:
            if helpers.is_absolute_base(self.__info['url']):
                base = self.__info['url']
        if base and base[-1] == '/':
            base = base[0:-1]
        return base

    def get_links(self):
        """Get list of links on the page

        :return: array List of unique links
        """
        links = []
        link_elems = self.__doc.findAll('a')
        for link_elem in link_elems:
            link = self.format_link(link_elem, 'href')
            if link not in links:
                links.append(link)
        return links

    def get_form_elems(self):
        """Get form elements

        :return: array Array of form elements
        """
        elems = []
        tmp1 = self.__doc.findAll('input')
        for tmp2 in tmp1:
            elems.append(tmp2)
        tmp1 = self.__doc.findAll('textarea')
        for tmp2 in tmp1:
            elems.append(tmp2)
        tmp1 = self.__doc.findAll('select')
        for tmp2 in tmp1:
            elems.append(tmp2)
        tmp1 = self.__doc.findAll('button')
        for tmp2 in tmp1:
            elems.append(tmp2)
        return elems

    def get_form_elem_names(self):
        """Get form elements names

        :return: array Array of form element names
        """
        names = []
        for elem in self.get_form_elems():
            name = elem.get('name')
            if name:
                names.append(name)
        return names

    def get_submit_button_texts(self):
        """Get submit button texts

        :return: array Array of submit button texts
        """
        rtn = []
        tmpl = self.__doc.findAll('input')
        for tmp2 in tmpl:
            if tmp2.get('type').lower() == 'submit':
                rtn.append(tmp2.get('value'))
        return rtn

    def select_dropdown_value(self, elem):
        """Randomly select an option from a select box

        :param elem: DOM element holding a select box (BeautifulSoup)
        :return: string Value
        """
        return elem.findChildren()[random.randrange(len(elem.findChildren()))].get('value')

    def get_css_hrefs(self):
        """Get list of css hrefs on the page

        :return: array List of unique css hrefs
        """
        hrefs = []
        link_elems = self.__doc.findAll('link')
        for link_elem in link_elems:
            # Check if this is a stylesheet
            if link_elem.get('rel')[0] == 'stylesheet':
                href = self.format_link(link_elem, 'href')
                if href and href not in hrefs:
                    hrefs.append(href)
        return hrefs

    def get_image_hrefs(self):
        """Get list of image href on the page

        :return: array List of unique image hrefs
        """
        srcs = []
        img_elems = self.__doc.findAll('img')
        for img_elem in img_elems:
            src = self.format_link(img_elem, 'src')
            if src and src not in srcs:
                srcs.append(src)
        return srcs

    def get_javascript_srcs(self):
        """Get list of javascript srcs on the page

        :return: array List of unique javascript srcs
        """
        srcs = []
        script_elems = self.__doc.findAll('script')
        for script_elem in script_elems:
            src = self.format_link(script_elem, 'src')
            if src and src not in srcs:
                srcs.append(src)
        return srcs

    def format_link(self, link_elem, attr):
        """Format link to get the absolute path to the resource

        :param link_elem: BS object that holds the link
        :param attr: type of the link to get from the link_elem
        :return: string Absolute link to the resource
        """

        abs_base = self.get_absolute_base()
        rel_base = self.get_relative_base()
        protocol = self.get_page_protocol()

        link = link_elem.get(attr)
        if not link:
            return None
        link.strip()
        if link and link.find('data:') != 0:
            if helpers.detect_url_scheme(link):
                return link
            elif helpers.detect_url_netloc(link):
                return "%s:%s" % (protocol, link)
            elif link[0] == '?' or link[0] == '#':
                tmp = self.get_current_url()
                pos = tmp.find(link[0])
                if pos != -1:
                    tmp = tmp[0:pos]
                return tmp + link
            elif link[0] == '/':
                return abs_base + link
            else:
                return "%s/%s" % (rel_base, link)
