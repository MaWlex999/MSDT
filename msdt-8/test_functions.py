import pytest
from pytest_mock import mocker
from paths import SEQUENCES_PATH
from functions import read_json, frequency_test, runs_test, longest_run_of_ones_in_block, longest_run_test


@pytest.fixture
def mock_read_json(mocker):
    mock = mocker.patch('functions.read_json')
    mock.return_value = {
        "cpp": "01001111011111111111010111100100101011010011100010010110100110001110101110110110110110000110001001111100001110001101011001001110",
        "java": "10111001100001010010100101101000110111100110011011110000011100000111100110110001111010000010111111010001111000010100100010111110"
    }
    return mock


def test_read_json_valid(mock_read_json):
    data = read_json(SEQUENCES_PATH)
    assert isinstance(data, dict)
    assert data == {
        "cpp": "01001111011111111111010111100100101011010011100010010110100110001110101110110110110110000110001001111100001110001101011001001110",
        "java": "10111001100001010010100101101000110111100110011011110000011100000111100110110001111010000010111111010001111000010100100010111110"
    }


@pytest.mark.parametrize("input_frequency_result, expected_frequency_result", [
    ("11100101011", 0.36571229628151325),
    ("111111111111111111110000000000000000000", 0.8727801237939118),
    ("100010001", 0.31731050786291415),
])
def test_frequency(input_frequency_result, expected_frequency_result):
    result = frequency_test(input_frequency_result)
    assert result == expected_frequency_result


def test_frequency_test_invalid_sequence():
    sequence = "102030"
    with pytest.raises(ValueError):
        frequency_test(sequence)


@pytest.mark.parametrize("input_runs_result, expected_runs_result", [
    ("11100101011", 0.9527725448755109),
    ("111111111111111111110000000000000000000", 2.9790573497915644e-09),
    ("100010001", 0.4532547047537365),
])
def test_runs(input_runs_result, expected_runs_result):
    result = runs_test(input_runs_result)
    assert result == expected_runs_result


def test_runs_test_invalid_sequence():
    sequence = "1110001"
    p_value = runs_test(sequence)
    assert p_value != 0


def test_longest_run_of_ones_in_block():
    block = "111000111"
    result = longest_run_of_ones_in_block(block)
    assert result == 3


@pytest.mark.parametrize("sequence, expected_p_value", [
    ("111000111000111", 0.6576655449763105),
    ("111111111000000", 0.7723528869386995),
])
def test_longest_run_test_valid(sequence, expected_p_value):
    p_value = longest_run_test(sequence)
    assert 0 <= p_value <= 1
    assert abs(p_value - expected_p_value) < 0.05


def test_longest_run_test_invalid_sequence():
    sequence = "111000"
    with pytest.raises(ValueError):
        longest_run_test(sequence, block_size=10)


if __name__ == "__main__":
    pytest.main(["-v"])