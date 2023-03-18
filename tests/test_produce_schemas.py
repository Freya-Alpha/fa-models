import importlib.util
import inspect
import os

def test_produce_schemas():
    """check if the models are in the right place and produce the avro avsc files."""
    for filename in os.listdir('famodels/models'):
        if filename.endswith('.py') and filename != '__init__.py':
            print(filename)
            module_name = os.path.splitext(filename)[0]
            print(os.getcwd())
            module_path = os.path.join('famodels/models/', filename)
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            print(module)
            #spec.loader.exec_module(module)
            # for name, obj in inspect.getmembers(module, inspect.isclass):
            #     if obj.__module__ == module_name:
            #         print(name)