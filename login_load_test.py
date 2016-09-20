from load_testing_test import LoadTestingTest
import record_helpers
import time
import sys


class LoginLoadTest(LoadTestingTest):
    """Example testing a login page on dictionary.com. To play
    with this test create an account on dictionary.com and use
    your username+password in the definition above. The parent
    class documentation see:

    https://www.redline13.com/customTestDoc/class-LoadTestingTest.html
    """

    SITE_USERNAME = '<site_username>'
    SITE_PASSWORD = '<site_password>'

    def __init__(self, test_num, rand):
        """Constructor needs to pass up the information

        :param test_num: int Test number, if you if you specify simulate 40 users - this represents that user
        :param rand: string The rand is a token used to keep track of this test, not used, just pass to parent
        """

        super(LoginLoadTest, self).__init__(test_num, rand)

    def start_test(self):
        """Start test is the main entry point. Here we script/control the flow of the test.
        Typically in a custom test we consider the start and stop of this function as the
        'User' time, really the overall time for the set of operations performed by the user.

        Within that page we have URLs, really the components that make up our overall ('page')
        time. This could be actual URLs, Code Blocks, Calls to DB, ....

        User = 520ms
        URL1 = 200ms
        URL2 = 200ms
        SOME CODE (recorded as URL3) = 100ms

        The missing time might be spent in some in-between parsing operations.
        """

        # Track the amount of delay
        delay = 0
        # Track overall bytes captured
        bytes = 0

        try:
            # Echo statements output will be shown in our logs.out for the test.
            # This output is available in a paid subscription
            print("Starting test for user %i" % self.test_num)

            # Set delay that will be used with each call to go_to_url
            # set-Delay() @see https://www.redline13.com/customTestDoc/class-LoadTestingTest.html#_setDelay
            self.set_delay(1000, 2000)

            # Load page
            page = self.load_login_page()
            # How many bytes
            bytes += sys.getsizeof(page) * 1024
            # We need track the delay used since we don't want this in our performance calculation.
            # getDelay() @see https://www.redline13.com/customTestDoc/class-LoadTestingTest.html#_getDelay
            delay += self.get_delay() / 1000

            # Do login
            page = self.do_login(page)
            # How many bytes
            bytes += sys.getsizeof(page) * 1024
            # We need track the delay used since we don't want this in our performance calculation
            delay += self.get_delay() / 1000

            # Do search
            page = self.do_search()
            # How many bytes
            bytes += sys.getsizeof(page) * 1024
            # We need track the delay used since we don't want this in our performance calcuation
            delay += self.get_delay() / 1000

            # Analyze search results
            self.analyze_search_page(page)
            # There is no delay or data retrieved, nothing to do for $bytes and $delay

            # You can see how to generate an error, and see it in the error section.
            #  This will not throw an error, page will be recorded as normal.
            self.generate_fake_error()

            # The test really ended here, let's not capture the cleanup
            end_time = time.time()

            # Clean up session file
            self.session.cleanup()

        except Exception as e:
            # Echo statements output will be shown in our logs.out for the test.
            # This output is available in a paid subscription.
            print('Test failed.')
            raise e

    def load_login_page(self):
        """This will open the login page for dictionary.com and we will let the underlying call
        record the URL load time. We use self.session which is a reference to an object that will
        keep track of cookies and build a user session. partially simulating the behavior of a browser.

        self.session is @see https://www.redline13.com/customTestDoc/class-LoadTestingSession.html

        :return: LoadTestingPageResponse Page @see https://www.redline13.com/customTestDoc/class-LoadTestingPageResponse.html
        """

        # Go to Login Page
        # 'http://app.dictionary.com/login' - URL to load
        # None - this represent a DATA array, if passed in the request will be a POST, otherwise a GET.
        # [] = custom headers, which we have none.
        # True - Save Data - this will write out the contents of the response and make it available in the output after
        # test completion (pro-feature).
        # False - Record as PAGE (true) or URL (false).  Since we are controlling PAGE in our startTest we set to false.
        page = self.session.go_to_url('http://app.dictionary.com/login', None, [], True, False)

        # The response is a custom object see https://www.redline13.com/customTestDoc/class-LoadTestingPageResponse.html
        #  We can test to see if there is a form element named username, validating our request.
        if 'username' not in page.get_form_elem_names():
            # Throw exception.  This will end the test on error and record Exception message
            raise RuntimeError('Missing expected for login form.')

        # Returns @see https://www.redline13.com/customTestDoc/class-LoadTestingPageResponse.html
        return page

    def do_login(self, page):
        """This will login the user by using a POST request to the login form.

        :return: LoadTestingPageResponse Page @see https://www.redline13.com/customTestDoc/class-LoadTestingPageResponse.html
        """

        # Execute a login
        # 'http://app.dictionary.com/login' - URL to load
        # { source, ... } - this represent a DATA dictionary, and will therefore execute a POST request on the URL.
        # [] = custome headers, which we have none.
        # True - Save Data - this will write out the contents of the response and make it available in the output after
        # test completion (pro-feature).
        # False - Record as PAGE (true) or URL (false).  Since we are controlling PAGE in our startTest we set to false.
        page = self.session.go_to_url('http://app.dictionary.com/login/core/fullpage',
                                      {
                                          'source': 'undefined',
                                          'logindest': 'http://www.dictionary.com',
                                          'username': self.SITE_USERNAME,
                                          'password': self.SITE_PASSWORD,
                                          'keep_me_signed': 1
                                      }, [], True, False)
        return page

    def do_search(self):
        """Do search

        :return: LoadTestingPageResponse Page @see https://www.redline13.com/customTestDoc/class-LoadTestingPageResponse.html
        """

        # Execute a search.
        # 'http://app.dictionary.com/login' - URL to load
        # None - this represent a DATA array, if passed in the request will be a POST, otherwise a GET.
        # [] = custome headers, which we have none.
        # True - Save Data - this will write out the contents of the response and make it available in the output after
        # test completion (pro-feature)
        # False - Record as PAGE (true) or URL (false).  Since we are controlling PAGE in our startTest we set to false.
        page = self.session.go_to_url('http://www.dictionary.com/browse/testing?s=t', None, [], True, False)
        return page

    def analyze_search_page(self, page):
        """Echo some information about the request and analyze the data we know about.

        :param page: LoadTestingPageResponse $page @see https://www.redline13.com/customTestDoc/class-LoadTestingPageResponse.html
        """
        start_time = time.time()

        links = len(page.get_links())
        print('# of Links on page: %i' % links)

        elems = len(page.get_form_elems())
        print("# of Form Elements on page: %i" % elems)

        css = len(page.get_css_hrefs())
        print("# of CSS Resources: %i" % css)

        hrefs = len(page.get_image_hrefs())
        print("# of Images: %i" % hrefs)

        js = len(page.get_javascript_srcs())
        print("# of JS Files: %i" % js)

        end_time = time.time()
        total_time = end_time - start_time
        # Record this block of time as a URL
        # AnalyzeSearchPage - name to show in reports
        # end_time - timestamp
        # total_time - total time of this block
        # False - boolean true there was an error, false this was a success
        # 0 - Kilobytes of response data, not relevant for this one.
        # recordURLPageLoad - @see https://www.redline13.com/customTestDoc/function-recordURLPageLoad.html
        record_helpers.record_load("AnalyzeSearchPage", end_time, total_time, False, 0)

    @staticmethod
    def generate_fake_error():
        """Generate an error in the URL section and see error show up in the error message log within page.
        @see https://www.redline13.com/customTestDoc/function-recordError.html
        """
        end_time = time.time()
        # Record this block as a URL but with Error set to true.
        # FakeError - name to show in reports
        # end_time - timestamp
        # 0 - total time of this block
        # True - boolean true there was an error, true since we are faking an error.
        # 0 - Kilobytes of response data, not relevant for this one.
        # recordURLPageLoad - @see https://www.redline13.com/customTestDoc/function-recordURLPageLoad.html
        record_helpers.record_load("FakeError", end_time, 0, True, 0)

        # We can also record error messages using https://www.redline13.com/customTestDoc/function-recordError.html
        record_helpers.record_error("We generated an a fake error",time.time())
