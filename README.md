An offline tester to validate your custom Python RedLine13 Load Test.

## Quick Start
```
git clone https://github.com/redline13/harness-custom-test-python.git
cd harness-custom-test-python
python setup.py install
```
The project has a couple dependencies which should be installed with the command above. Alternatively they can be installed with pip
* bs4
* pycurl


### Specify test on Command Line
* python run_load_test.py example_test.py
* python run_load_test.py example_test
  * This opens module example_test.py and looks for a subclass of LoadTestingTest

### Specify configuration in loadtest.ini
  You can also specify configuration data in loadtest.ini which is read in and provided to your class as a dict from self.get_ini_settings()
```
# used in sample load test to define iterations
iterations=4
# can define test to run example_test or example_test.py
classfilename=example_test
```
  * python run_load_test.py

### Examples Provided
- CustomLoadTest, custom_load_test.py
  - Simple URL which does echo
- ExampleTest, example_test.py
  - Loops 100 times with random wait, each loop is a recorded as URL and overall a PAGE
- FormLoadTest, form_load_test.py
  - Gets data from a webpage, finds a form, and submits that form with data
- LoginLoadTest, login_load_test.py
  - Submits a login form (to use see code, need to add in data)
- SimpleLoadTest, simple_load_test.py 
  - Hits a URL, parses for other endpoints (JS, CSS) and times those as well

# Simulating inputs for test
Modify loadtest.ini with parameters, in your custom test you can access settings via get_ini_settings.  The object is a dict

```python
from load_testing_test import LoadTestingTest
import record_helpers
import time
import random


class ExampleTest(LoadTestingTest):

    def start_test(self):
        """ Start test """

        # Example getting information from Config Dict
        config = self.get_ini_settings()
        iterations = 1
        if config.has_key( 'iterations' ):
            iterations = int(config.get( 'iterations', 1 ))

        start_user_time = time.time()

        for x in range(1, iterations):
            start_time = time.time()
            time.sleep(random.randint(2, 5))
            diff = time.time() - start_time
            record_helpers.record_url_page_load(x, start_time, diff)

        end_user_elapsed = time.time() - start_user_time
        record_helpers.record_page_time(start_user_time, end_user_elapsed)

        return True
```

# Output
The load test will generate local information on performance results and errors.

# More on Custom Performance Tests
https://www.redline13.com/blog/writing-a-custom-load-test/
