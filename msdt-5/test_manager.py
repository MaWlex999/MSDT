import pytest
from unittest.mock import Mock
from manageer import LinkManager

@pytest.fixture
def link_manager():
    return LinkManager()

def test_add_link_success(link_manager):
    link_manager.add_link(1, ["item1", "item2"], 100)
    assert len(link_manager.links) == 1

def test_add_link_duplicate_id(link_manager):
    link_manager.add_link(1, ["item1"], 50)
    with pytest.raises(ValueError, match="Link ID already exists"):
        link_manager.add_link(1, ["item2"], 100)

def test_add_link_negative_total(link_manager):
    with pytest.raises(ValueError, match="Total cannot be negative"):
        link_manager.add_link(1, ["item1"], -50)

def test_get_link_success(link_manager):
    link_manager.add_link(1, ["item1"], 100)
    link = link_manager.get_link(1)
    assert link["total"] == 100
    assert "item1" in link["items"]

def test_get_link_not_found(link_manager):
    with pytest.raises(ValueError, match="Link not found"):
        link_manager.get_link(99)

def test_remove_link_success(link_manager):
    link_manager.add_link(1, ["item1"], 100)
    link_manager.remove_link(1)
    assert len(link_manager.links) == 0

def test_remove_link_not_found(link_manager):
    with pytest.raises(ValueError, match="Link not found"):
        link_manager.remove_link(99)


@pytest.mark.parametrize("links,expected_total", [
    ([{"link_id": 1, "items": ["item1"], "total": 50}], 50),
    ([{"link_id": 1, "items": ["item1"], "total": 50},
      {"link_id": 2, "items": ["item2"], "total": 100}], 150),
    ([], 0),
])
def test_calculate_total_links(link_manager, links, expected_total):
    link_manager.links = links
    assert link_manager.calculate_total_links() == expected_total


def test_mock_add_link():
    mock_manager = Mock(spec=LinkManager)
    mock_manager.add_link.return_value = None
    mock_manager.add_link(1, ["item1"], 100)
    mock_manager.add_link.assert_called_once_with(1, ["item1"], 100)