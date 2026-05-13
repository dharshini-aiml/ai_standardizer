import pytest
from app.utils.data_cleaner import DataCleaner

def test_clean_email():
    cleaner = DataCleaner()
    assert cleaner.clean_email(" TEST@GMAIL.COM ") == "test@gmail.com"