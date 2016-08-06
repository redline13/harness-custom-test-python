from load_testing_test import LoadTestingTest
import record_helpers
import time
import sys

class LoginLoadTest(LoadTestingTest):

    SITE_USERNAME = 'buburebuh@ex.ua'
    SITE_PASSWORD = 'buburebuhbuburebuh'

    def __init__(self, test_num, rand):
        super(LoginLoadTest, self).__init__(test_num, rand)

    def start_test(self):

        start_time = time.time()
        delay = 0
        bytes = 0

        # Set delay that will be used with each call to go_to_url
        print("Starting test for user %i" % self.test_num)
        self.set_delay(1000, 2000)

        # Load page
        page = self.load_login_page()
        bytes += sys.getsizeof(page) * 1024
        delay += self.get_delay()/1000

        # Do login
        page = self.do_login(page)
        bytes += sys.getsizeof(page) * 1024
        delay += self.get_delay()/1000

        # Do search
        page = self.do_search()
        bytes += sys.getsizeof(page) * 1024
        delay += self.get_delay() / 1000

        # Analyze search results
        self.analyze_search_page(page)

        # Gen fake error
        self.generate_fake_error()

        end_time = time.time()

        self.session.cleanup()

        total_time = end_time - start_time - delay
        record_helpers.record_page_time(end_time, total_time, False, bytes / 1024.0)
        print("BYTES RECORDED %i" % bytes)

    def load_login_page(self):
        page = self.session.go_to_url('http://app.dictionary.com/login', None, [], True, False)

        if 'username' not in page.get_form_elem_names():
            raise RuntimeError('Missing expected for login form.')
        return page

    def do_login(self, page):
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
        page = self.session.go_to_url('http://www.dictionary.com/browse/testing?s=t', None, [], True, False)
        return page

    def analyze_search_page(self, page):

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

        record_helpers.record_url_page_load("AnalyzeSearchPage", end_time, total_time, False, 0)

    @staticmethod
    def generate_fake_error():
        end_time = time.time()
        record_helpers.record_url_page_load("FakeError", end_time, 0, True, 0)

        record_helpers.record_error("We generated an a fake error")



