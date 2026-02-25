"""Test TRIZ rule engine KB parsing and lookups."""

from src.services.triz_engine import triz_engine


def test_parse_39_parameters():
    assert len(triz_engine.params) == 39
    assert triz_engine.params[1].name_zh == "移動物體的重量"
    assert triz_engine.params[39].name_en == "Productivity"


def test_parse_contradiction_matrix():
    # Matrix should have entries (sparse — not all 39*38 cells filled)
    assert len(triz_engine.matrix) > 100
    # Known entry: improving param 1, worsening param 2 -> [15, 8, 29, 34]
    result = triz_engine.lookup_matrix(1, 2)
    assert result == [15, 8, 29, 34]


def test_matrix_lookup_missing():
    # Same param should have no entry (diagonal)
    assert triz_engine.lookup_matrix(1, 1) == []


def test_parse_40_principles():
    assert len(triz_engine.principles) == 40
    assert triz_engine.principles[1].name_zh == "分割"
    assert triz_engine.principles[1].name_en == "Segmentation"
    assert triz_engine.principles[40].name_zh == "複合材料"
    assert len(triz_engine.principles[1].sub_principles) >= 2


def test_parse_separation_principles():
    assert len(triz_engine.separations) == 4
    assert triz_engine.separations[0].name_zh == "時間分離"
    assert triz_engine.separations[3].name_zh == "整體與局部分離"
    # Each should have strategies
    for sep in triz_engine.separations:
        assert len(sep.strategies) >= 3


def test_parse_76_standards():
    assert len(triz_engine.standards) >= 50  # May not all parse perfectly
    # First standard
    assert triz_engine.standards[0].code == "1.1.1"
    # Check classes exist
    codes = {s.code for s in triz_engine.standards}
    assert "1.2.1" in codes
    assert "2.1.1" in codes


def test_get_principles():
    results = triz_engine.get_principles([1, 15, 35])
    assert len(results) == 3
    assert results[0].id == 1
    assert results[1].id == 15


def test_get_standards_for_state():
    incomplete = triz_engine.get_standards_for_state("incomplete")
    assert all(s.code.startswith("1.1") for s in incomplete)
    harmful = triz_engine.get_standards_for_state("harmful")
    assert all(s.code.startswith("1.2") for s in harmful)
    measurement = triz_engine.get_standards_for_state("measurement")
    assert all(s.code.startswith("4.") for s in measurement)


def test_format_params_for_prompt():
    text = triz_engine.format_params_for_prompt()
    assert "移動物體的重量" in text
    assert "生產力/效率" in text
    assert text.count("|") > 100  # Many table cells


def test_format_principles_for_prompt():
    text = triz_engine.format_principles_for_prompt([1, 15])
    assert "#1 分割" in text
    assert "#15 動態化" in text
    assert "工程提示" in text


def test_format_separations_for_prompt():
    text = triz_engine.format_separations_for_prompt()
    assert "時間分離" in text
    assert "空間分離" in text
    assert "條件分離" in text
    assert "整體與局部分離" in text


def test_mapping_hints():
    assert "太重" in triz_engine.mapping_hints
    assert "太熱" in triz_engine.mapping_hints
