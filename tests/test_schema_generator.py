
import pytest
from famodels.schema_generator import SchemaGenerator
from famodels.trading_signal import TradingSignal
import json

@pytest.mark.parametrize("name, namespace", [
    ("MyRecord", "fa.signal-processing.MyRecord"),
    ("TradingSignal", "tks.signal-processing.TradingSignal")
])
def test_create_json_avro_head(name, namespace):
    header = SchemaGenerator().create_json_avro_head(name=name, namespace=namespace)
    expected_header = {
            "namespace": namespace,
            "type": "record",
            "name": name
        }
    assert header == expected_header

def test_create_json_schema_for_avro():
    generated_avro_schema = SchemaGenerator().generate_json_schema_for_avro(model_class=TradingSignal)

    with open('./tests/avro_schema_expected.json', 'r') as f:
        # Load the JSON data from the file
        __expected_avro_schema__ = json.load(f)

    assert generated_avro_schema == __expected_avro_schema__