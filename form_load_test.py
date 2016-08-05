from load_testing_test import LoadTestingTest

try:
    import urllib
except ImportError:
    import urllib.parse as urllib


class FormLoadTest(LoadTestingTest):

    def __init__(self, test_num, rand):
        """Constructor

        :param test_num: int Test number
        :param rand: string Random token for test
        """
        # Call parent constructor
        super(FormLoadTest, self).__init__(test_num, rand)

    def start_test(self):
        """ Start the test """
        #try:
        # Load page
        page = self.load_page()

        # Set delay that will be used with each call to go_to_url
        self.set_delay(5000, 7000)

        # Do search
        page = self.do_query(page)

        # Clean up session file
        self.session.cleanup()

        #except Exception as e:
            #print("Test failed.")
            #raise e

    def load_page(self):
        """Load page

        :return: LoadTestingPageResponse Page
        """
        self.set_delay(1000, 3000)

        # Go to first page
        page = self.session.go_to_url('http://www.google.com')

        # Simple check for error
        if 'q' not in page.get_form_elem_names():
            raise RuntimeError('Missing expected for parameter.')

        return page

    def do_query(self, page):
        """Do search

        :param page: Current page
        :return: LoadTestingPageResponse Next page
        """
        # Build post
        get = {}
        form_url = None
        for elem in page.get_form_elems():
            name = elem.get('name')

            if name:
                if name == 'q':
                    get[name] = 'RedLine13 Load Testing'

                    # Get form URL
                    elem2 = elem.parent
                    while elem2 is not None:
                        if elem2.name and elem2.name.lower() == 'form':
                            form_url = elem2.get('action')
                            if form_url[0] and form_url[0] == '/':
                                form_url = 'http://www.google.com' + form_url
                            break
                        elem2 = elem2.parent

        url = form_url + '?' + urllib.urlencode(get)
        page = self.session.go_to_url(url)

        return page
