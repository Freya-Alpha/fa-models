from typing import List
import pytest
from fastavro import schemaless_writer, parse_schema

class SimpleClass:
    nothing: str
    something: int
    a_lot: List[str]
    more: List[float]

    def __init__(self):
        self.nothing = ""
        self.something = 0
        self.a_lot = []
        self.more = []

simple = SimpleClass()
simple.nothing = "sfafa"
simple.something = 32
simple.a_lot = ['one', 'two', 'three']
simple.more = [10.0, 20.0, 30.0]

schema = {
  "type": "record",
  "name": "SimpleClass",
  "fields": [
    {"name": "nothing", "type": "string"},
    {"name": "something", "type": "int"},
    {"name": "a_lot", "type": {"type": "array", "items": "string"}},
    {"name": "more", "type": {"type": "array", "items": "float"}}
  ]
}

@pytest.mark.skip(reason="need to adapt the schema")
def test_simple_class_avro_schema():
    # Serialize the SimpleClass object using the schema
    writer = schemaless_writer(schema)
    writer(simple.__dict__)
    bytes_data = writer.getvalue()

    # Deserialize the bytes data back to a Python object using the schema
    parsed_schema = parse_schema(schema)
    record = parsed_schema.to_record(bytes_data)
    obj = SimpleClass()
    obj.__dict__.update(record)

    # Validate the deserialized object against the schema
    assert obj.nothing == "sfafa"
    assert obj.something == 32
    assert obj.a_lot == ['one', 'two', 'three']
    assert obj.more == [10.0, 20.0, 30.0]