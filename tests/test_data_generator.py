import pytest
from famodels.data_generator import DataGenerator

def test_generate_batch_of_signals():
    gen = DataGenerator()
    try:
        gen.generate_batch_of_signals()
    except Exception as e:
        pytest.fail(f"Exception occured: {e}")
