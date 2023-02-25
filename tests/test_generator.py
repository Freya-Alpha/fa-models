import pytest
from famodels.generator import Generator

def test_generate_batch_of_signals():
    gen = Generator()
    try:
        gen.generate_batch_of_signals()
    except Exception as e:
        pytest.fail(f"Exception occured: {e}")