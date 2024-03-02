from setuptools import find_packages, setup
# from setuptools.command.build import build
# import importlib.util
# import inspect
# import os

# class ProduceAvroSchemas(build):
#     ## TODO Still working on #1
#     def run(self):
#         for filename in os.listdir('famodels/models'):
#             if filename.endswith('.py') and filename != '__init__.py':
#                 print(filename)
#                 # module_name = os.path.splitext(filename)[0]
#                 # print(os.getcwd())
#                 #module_path = os.path.join('famodels/models/', filename)
#                 # spec = importlib.util.spec_from_file_location(module_name, module_path)
#                 # module = importlib.util.module_from_spec(spec)
#                 # spec.loader.exec_module(module)
#                 # for name, obj in inspect.getmembers(module, inspect.isclass):
#                 #     if obj.__module__ == module_name:
#                 #         print(name)

#         build.run(self)

setup(
    name='fa-models',
    packages=find_packages(include=['famodels',
                                    'famodels.market',
                                    'famodels.exchange',
                                    'famodels.fund'
                                    ], exclude=['tests*']),
    # packages=['famodels'],
    # package_dir={'famodels':'src'}
    #packages=find_packages(),
    #version='0.1.0',
    # description='The library describes the most common models used in trading systems.',
    # author='Brayan Svan',
    # license='MIT',
    install_requires=['fasignalsupplier'],
    # setup_requires=['pytest-runner'],
    # tests_require=['pytest==4.4.1'],
    # test_suite='tests',
    # cmdclass={
    #     'build': ProduceAvroSchemas,
    # },
)

