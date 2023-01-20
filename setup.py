from setuptools import find_packages, setup
setup(
    name='famodels',
    packages=find_packages(include=['src'], exclude=['tests*']),
    #packages=find_packages(),
    #version='0.1.0',
    # description='The library describes the most common models used in trading systems.',
    # author='Brayan Svan',
    # license='MIT',
    # install_requires=['sqlmodel'], 
    # setup_requires=['pytest-runner'],
    # tests_require=['pytest==4.4.1'],
    # test_suite='tests',
)