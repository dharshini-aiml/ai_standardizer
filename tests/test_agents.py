import pytest
from app.agents.fixer import Fixer  # 'DataFixer'-ku bathila 'Fixer'

def test_fix_common_issues():
    # Fixer.fix_common_issues direct-ah call pannalaam (Static method)
    assert Fixer.fix_common_issues("null") is None
    assert Fixer.fix_common_issues("Hello    World") == "Hello World"
    assert Fixer.fix_common_issues("test\u2019s") == "test's"

def test_standardize_field_value():
    # Email standardization test
    email = "TEST@GMAIL.COM  "
    # Note: Ithu DataCleaner-ai call pannum, so DataCleaner sariya irukanum
    result = Fixer.standardize_field_value("email", "TEST@GMAIL.COM")
    assert result is not None

def test_calculate_quality_score():
    original = {"name": "John"}
    fixed = {"name": "John"}
    score = Fixer.calculate_quality_score(original, fixed)
    assert score == 1.0

    # Test with missing data
    fixed_missing = {"name": None}
    score_missing = Fixer.calculate_quality_score(original, fixed_missing)
    assert score_missing < 1.0