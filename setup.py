from setuptools import find_packages, setup

setup(
    name='fa-models',
    packages=find_packages(include=['famodels',
                                    'famodels.*'
                                    ], exclude=['tests*']),
    install_requires=['fa-signal-provider']
)
