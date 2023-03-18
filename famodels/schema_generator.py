
from enum import EnumMeta
from typing import List, Dict, Union, Tuple, Optional, get_args
from sqlmodel import SQLModel
from typing import TypeVar, Type

T = TypeVar('T')

class SchemaGenerator:
    """Creates schemas from python class to json class schemas to avro schemas in 
    json and eventually to avro schemas. Caution. """
    def __init__(self):
        pass

    def generate_json_schema_for_avro(self, model_class: Type[T], namespace:str=None) -> Dict:
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
        # create the avro schema head (in json).    
        if namespace == None:
            mod_namespace = "public"  
        else:
            mod_namespace = namespace

        schema = self.create_json_avro_head(mod_namespace, model_class.__name__)
        # now attach the fields.
        schema["fields"] = self.create_field_array(model_class=model_class)
        # append fields to the head.

        return schema

    def create_json_avro_head(self, namespace:str, name: str) -> Dict:
        """Returning the head of json schema for avro."""
        return {
            "namespace": namespace,
            "type": "record",
            "name": name,
        }

    def create_field_array(self, model_class: Type[T]) -> Dict:
        fields = []
        for field in model_class.__fields__.values():
            if issubclass(field.type_, SQLModel):
                # Recursively generate schema for nested models
                fields.append({"name": field.name, "type": self.create_field_array(self, field.type_)})
            elif field.type_ == str:
                fields.append({"name": field.name, "type": "string"})
            elif field.type_ == int:
                fields.append({"name": field.name, "type": "int"})
            elif field.type_ == float:
                fields.append({"name": field.name, "type": "float"})
            elif field.type_ == bool:
                fields.append({"name": field.name, "type": "boolean"})
            elif isinstance(field.type_, EnumMeta):
                # Generate Avro schema for enums
                symbols = [e.value for e in field.type_]
                enum_schema = {"type": "enum", "name": field.type_.__name__, "symbols": symbols}
                fields.append({"name": field.name, "type": enum_schema})
            elif issubclass(field.type_, list):
                # Generate Avro schema for arrays
                item_schema = self.create_field_array(get_args(field.type_)[0])
                array_schema = {"type": "array", "items": item_schema}
                fields.append({"name": field.name, "type": array_schema})
            elif issubclass(field.type_, dict):
                # Generate Avro schema for maps
                value_schema = self.create_field_array(get_args(field.type_)[1])
                map_schema = {"type": "map", "values": value_schema}
                fields.append({"name": field.name, "type": map_schema})
            elif issubclass(field.type_, tuple):
                # Generate Avro schema for unions
                union_types = []
                for t in get_args(field.type_):
                    if t == type(None):
                        union_types.append("null")
                    else:
                        union_types.append(self.create_field_array(t))
                union_schema = union_types if len(union_types) > 1 else union_types[0]
                fields.append({"name": field.name, "type": union_schema})
            # elif isinstance(field.type_, schema.Fixed):
            #     # Generate Avro schema for fixed types
            #     fixed_schema = {"type": "fixed", "name": field.type_.__name__, "size": field.type_.__args__[0]}
            #     fields.append({"name": field.name, "type": fixed_schema})
            else:
                raise ValueError(f"Unsupported data type: {field.type_}")

        return fields
