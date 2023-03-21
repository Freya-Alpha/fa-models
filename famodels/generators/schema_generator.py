
from enum import Enum, EnumMeta
from typing import List, Dict, Union, Tuple, Optional, get_args
import typing
from sqlmodel import SQLModel
from typing import TypeVar, Type
from datetime import datetime

T = TypeVar('T')

class SchemaGenerator:
    """Creates schemas from python class to json class schemas to avro schemas in 
    json and eventually to avro schemas. Caution. """
    def __init__(self):
        pass

    def generate_json_schema_for_avro(self, model: typing.Type, namespace:str=None) -> Dict:
        """Accepts a class based on SQLModel and converts it to an avro schema in json.
        Args:
            model_class (type[SQLModel]): The SQLModel you would like to translate into json definition
            of an avro schema.
            namespace (str, optional): Make sure the passed namespace is what your sink system requires. 
            e.g. targeting a pulsar topic, the namespace must be <tenant>.<namespace> which does imply 
            you are sending data to pulsar://<tenant>/<namespace>/<topic>. Same applies in a similar
            way to Kafka, Hadoop, Flink, etc.

        Returns:
            dict: Return the json schema definition of the avro.
        """

        return self.generate_avro_schema(namespace, model)

    def create_json_avro_head(self, namespace:str, name: str) -> Dict:
        """Returning the head of json schema for avro."""
        return {
            "namespace": namespace,
            "type": "record",
            "name": name,
        }

    # def create_field_array(self, model: typing.Type) -> Dict:
    def generate_avro_schema(self, namespace:str , model_type: typing.Type) -> dict:
        fields = []
        for name, python_type in model_type.__annotations__.items():
            origin = typing.get_origin(python_type)
            # print(f"\n\nPYTHON_TYPE : {python_type}, NAME: {name}, ORIGIN: {origin}")

            if origin is not None and origin is typing.Union:
                print(f"NONE ORIGIN BUT OPTIONAL --> PYTHON_TYPE : {python_type}, NAME: {name}, ORIGIN: {origin}")
                # Field is optional, so add a new field definition for each possible type
                # Not clear why not simply taking the first attribute.
                # For now we limit it to the first one.
                # for arg_type in typing.get_args(python_type):
                #     field = self.create_avro_field(name, arg_type, optional=True)
                #     fields.append(field)
                field = self.create_avro_field(name, typing.get_args(python_type)[0], optional=True)
                fields.append(field)

            elif origin is not None:                
                if issubclass(origin, List):
                    # print(f"IS LIST --> PYTHON_TYPE : {python_type}, NAME: {name}, ORIGIN: {origin}")
                    item_type = typing.get_args(python_type)[0]

                    if issubclass(item_type, Enum):
                        fields.append({
                            "name": name,
                            "type": {
                                "type": "array",
                                "items": {
                                    "type": "enum",
                                    "name": item_type.__name__,
                                    "symbols": [e.value for e in item_type]
                                }
                            }
                        })
                    else:
                        fields.append({
                            "name": name,
                            "type": {
                                "type": "array",
                                "items": {"type": self.get_avro_type(item_type)}
                            }
                        })
                elif issubclass(origin, Dict):
                    print(f"IS DICT --> PYTHON_TYPE : {python_type}, NAME: {name}, ORIGIN: {origin}")
                    value_type = typing.get_args(python_type)[1]
                    if issubclass(value_type, Enum):
                        fields.append({
                            "name": name,
                            "type": {
                                "type": "map",
                                "values": {
                                    "type": "enum",
                                    "name": value_type.__name__,
                                    "symbols": [e.value for e in value_type]
                                }
                            }
                        })
                    else:
                        fields.append({
                            "name": name,
                            "type": {
                                "type": "map",
                                "values": {"type": self.get_avro_type(value_type)}
                            }
                        })
                else:
                    print(f"HAS ORIGIN BUT ELSE --> PYTHON_TYPE : {python_type}, NAME: {name}, ORIGIN: {origin}")
                    if python_type.__class__.__name__ == "EnumMeta":
                        print()
                        fields.append({
                            "name": name,
                            "type": {
                                "type": "array",
                                "items": {
                                    "type": "enum",
                                    "name": python_type.__name__,
                                    "symbols": [e.value for e in python_type]
                                }
                            }
                        })

                    else:
                        fields.append({"name": name, "type": {"type": self.get_avro_type(python_type)}})
            else:
                # no origin
                #print(f"NONE ORIGIN --> PYTHON_TYPE : {python_type}, NAME: {name}, ORIGIN: {origin}")
                
                if python_type.__class__.__name__ == "EnumMeta":
                    # it's an ENUM
                    # TODO build-in the OPTIONAL feature
                    # print(f"NONE ORIGIN --> ENUM --> PYTHON_TYPE : {python_type}, NAME: {name}, ORIGIN: {origin}")
                    field = {
                        "name": name,
                        # "type": "enum",
                        #"symbols": [e.value for e in python_type]
                        "type": {
                            "type": "enum",
                            "name": name,
                            "symbols": [e.value for e in python_type]
                            # "items": {
                            #     "type": "enum",
                            #     "name": python_type.__name__,
                            #     "symbols": [e.value for e in python_type]
                            # }
                        }
                    }     
                    #field["default"] = model_type.__annotations__['order_type'].__args__[0].default_factory()         
                else:
                    # it's a simple type like str, int, float, etc.
                    field = {"name": name, "type": self.get_avro_type(python_type)}
                    # add default values if available                                   
                    field = self.add_default_value(field, model_type, python_type, name)

                fields.append(field)

        return {"namespace": namespace, "type": "record", "name": model_type.__name__, "fields": fields}

    def add_default_value(self, field, model_type:typing.Type, python_type: typing.Type, name: str):
        """Checks if the primitive field requires a default value to be set."""
        # now check if it has a default value.
        default_value = None
        # Check for regular classes                     
        if hasattr(python_type, name):
            def_val = getattr(python_type, name)
            if isinstance(default_value, python_type):
                default_value = default_value
        # Check for SQLModel/Pydantic Classes   
        if default_value == None:
            if hasattr(model_type, "__fields__"):
                default_value = model_type.__fields__[name].default                  
        # If there is a default_value, then append it to the json.
        if default_value is not None:
            field["default"] = default_value     
        return field


    def get_avro_type(self, python_type: typing.Type) -> str:
        # print(f"TYPE: {python_type}, ORIGIN: {typing.get_origin(python_type)}")    
        origin = typing.get_origin(python_type)    

        if python_type == str:
            return "string"
        elif python_type == int:
            # since in python a value could be 64Bit, we never know if it is an int or long in avro. Thus long.
            return "long"
        elif python_type == float:
            return "float"
        elif python_type == bool:
            return "boolean"
        elif python_type == typing.Any :
            return "null"
        elif typing.get_origin(python_type) == list:
            return "array"
        elif python_type == tuple or origin == tuple:
            return "array"
        elif python_type.__name__ == "NoneType":
            return "null"
        elif isinstance(python_type, Enum):
            print("YES, IT'S FINALY RECOGNIZES ENUM!!!")
            raise Exception
            return "enum"
        elif python_type.__class__.__name__ == "EnumMeta":
            return "enum"        
        # elif typing.get_origin(python_type) == tuple:
        #     item_type = self.get_avro_type(typing.get_args(python_type)[0])
        #     return {"type": "array", "items": item_type}        
        elif isinstance(python_type, datetime):
            return ""
        elif isinstance(python_type, object):
            raise "record"
        else:            
            raise ValueError(f"Unsupported data type: {python_type}. \
                             {python_type.__name__} \
                             {python_type.__module__} \
                             {python_type.__qualname__} \
                             {python_type.__bases__} \
                             {python_type.__class__} \
                             {python_type.__class__.__name__} \
                             {python_type.__instancecheck__} \
                             {python_type.__subclasscheck__} \
                             {typing.get_origin(python_type)} \
                             ")
    
    def create_avro_field(self, name: str, python_type: typing.Type, optional: bool) -> Dict:
        if optional:
            # Field is optional, so create a union with null and the actual type
            return {
                "name": name,
                "type": ["null", self.get_avro_type(python_type)],
                "default": "null" 
            }
        else:
            return {
                "name": name,
                "type": self.get_avro_type(python_type)
            }




