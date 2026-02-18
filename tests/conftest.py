import pytest
from backupchan import Connection

TEST_TOKEN = f"bakch-{'a'*64}"

@pytest.fixture
def conn():
    return Connection("http://localhost", 5000, TEST_TOKEN)
