from setuptools import setup

setup(name='RedLine13 Test Harness',
      version='0.1',
      description='Python Harness for RedLine13',
      url='https://github.com/redline13/harness-custom-test-python',
      author='Artem Fliunt',
      author_email='ddnomad@protonmail.com',
      license='MIT',
      install_requires=[
          'bs4',
          'pycurl'
      ],
      zip_safe=False)
