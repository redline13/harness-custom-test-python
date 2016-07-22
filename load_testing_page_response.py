#NOTE: untested as for now

# Load Testing Page Response
class LoadTestingPageResponse(object):

    # Request information
    __info = {} # NOTE: assumed it's a python dictionary (see line 67 of a php source)

    # Content
    __content = None

    # DOMDocument of content
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
    # /**
	#  * Set the page content.
	#  * @param string Page content
	#  * @param string $contentType Optional content type.  If not detected as HTML,
	#  * 	it wil not be loaded.
	#  */
    def setContent(self, content, content_type = None):
        self.__content = content
        self.__doc = # TODO: new lxml or bs object (will decide later) new DOMDocument();
        #TODO: finish the function


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
        try:
            is_not_empty = bool(self.__info['http_code'])
        except KeyError:
            is_not_empty = False
        return int(self.__info['http_code']) if is_not_empty else None


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
        #return not self.hasError() and TODO: finish this one
        # NOTE: @ symbol is for error messages suppression
