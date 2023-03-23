from famodels.models.trading_signal import TradingSignal
from famodels.models.direction import Direction
from famodels.models.side import Side
from famodels.generators.schema_generator import SchemaGenerator
from pulsar.schema import AvroSchema, Record, JsonSchema, String
from pulsar import Producer, Client
import fastavro
import json

def test_generate_avro_with_object():
    """This test will generate a Trading object and populate it with test data 
    in order to run it against the validation."""
    signal = TradingSignal(id=None, algo_id="sjlaf", provider_id="dfkadf", 
                           market="BTC/USDT", exchange="BINANCE", trade_correlation_id="423424", 
                           direction=Direction.LONG, side=Side.BUY, price=21431.14, tp=2444.8, 
                           sl=20950, timestamp_of_creation=1679428344467, 
                           timestamp_of_registration=None)
    # generate the json-definition for the avro schema
    schema_definition = SchemaGenerator().generate_json_schema_for_avro(TradingSignal, "fa.signalprocessing")
    print(f"SCHEMA: {schema_definition}")
    parsed_avro = fastavro.parse_schema(schema_definition)
    #print(schema_definition)
    # make sure the schema is correct and matches with the data
    data = signal.__dict__
    print(data)
    assert fastavro.validate(data, schema=schema_definition)    
    # check if the pulsar Avro Schema accepts it too.    
    avro_schema = AvroSchema(None, schema_definition=parsed_avro)


def test_generate_avro_for_pulsar():
    """This test will take a fixed avro schema written in json and compare it 
    against the generated avro schema (also in json) - and validate it
    Pulsar localhost is not yet mocked. Keep Pulsar up for these tests and deactivate 
    if checking into GitHub. Otherwise it will fail in GitHub Actions.
    """

    # load test data
    with open('./tests/data/trading_signal_sample.json', 'r') as f:
        # Load the JSON data from the file
        signal = json.load(f) 

    # generate the json-definition for the avro schema
    schema_definition = SchemaGenerator().generate_json_schema_for_avro(TradingSignal, "fa.signalprocessing")
    print(schema_definition)
    parsed_avro = fastavro.parse_schema(schema_definition)
    #print(schema_definition)
    # make sure the schema is correct and matches with the data
    assert fastavro.validate(signal, schema=schema_definition)    
    # check if the pulsar Avro Schema accepts it too.    
    avro_schema = AvroSchema(None, schema_definition=parsed_avro)
    # client = Client("pulsar://localhost:6650")
    # producer = client.create_producer(
    #     topic='persistent://fa/signal-processing/raw-signals',
    #     schema=avro_schema
    # )    
    # producer.send(signal)
    # client.close()
