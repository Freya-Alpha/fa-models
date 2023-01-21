from setuptools import find_packages, setup
setup(
    name='fa-models',
    packages=find_packages(include=['famodels'], exclude=['tests*']),
    # packages=['famodels'],
    # package_dir={'famodels':'src'}
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