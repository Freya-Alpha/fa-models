from typing import List, Tuple
import pytest
from famodels.generators.schema_generator import SchemaGenerator
from famodels.models.trading_signal import TradingSignal
import json

from famodels.models.side import Side

# @pytest.mark.skip(reason="temporary for focus")
@pytest.mark.parametrize("name, namespace", [
    ("TradingSignal", "fa.signalprocessing"),
    #("TradingSignal", "tks.signal-processing.TradingSignal")
])
def test_create_json_avro_head(name, namespace):
    header = SchemaGenerator().create_json_avro_head(name=name, namespace=namespace)
    expected_header = {
            "namespace": namespace,
            "type": "record",
            "name": name
        }
    assert header == expected_header

# @pytest.mark.skip(reason="temporary disable because SQL Models are too complex.")
def test_create_json_schema_for_avro():
    generated_avro_schema = SchemaGenerator().generate_json_schema_for_avro(
        model=TradingSignal, 
        namespace="fa.signalprocessing")
    # print(generated_avro_schema)

    with open('./tests/avro_schema_expected.json', 'r') as f:
        # Load the JSON data from the file
        __expected_avro_schema__ = json.load(f)
    # print(__expected_avro_schema__)

    assert generated_avro_schema == __expected_avro_schema__

class SimpleClass:
    nothing: str
    something: int
    a_lot: List[str]
    more: Tuple[float]
    less: tuple
    side: Side

# @pytest.mark.skip(reason="temporary disabld")
def test_create_json_schema_for_avro_simple():
    """genereate the schema with a simple non-SQLMethod class."""

    generated_avro_schema = SchemaGenerator().generate_json_schema_for_avro(
        model=SimpleClass, 
        namespace="fa.signalprocessing")
    print(generated_avro_schema)

    with open('./tests/data/avro_simple_schema.json', 'r') as f:
        # Load the JSON data from the file
        __expected_avro_schema__ = json.load(f)
    # print(__expected_avro_schema__)

    assert generated_avro_schema == __expected_avro_schema__
