
import logging
from app.utils.logger import setup_logger


def clear_logger(name):
    logger = logging.getLogger(name)
    logger.handlers.clear()
    logger.propagate = False
    return logger


def test_setup_logger_full_handlers(monkeypatch):
    clear_logger("full_logger")

    monkeypatch.setattr(logging.Logger, "hasHandlers", lambda self: False)

    logger = setup_logger("full_logger")

    assert isinstance(logger, logging.Logger)
    assert len(logger.handlers) == 2

    handler_types = [type(handler).__name__ for handler in logger.handlers]

    assert "RotatingFileHandler" in handler_types
    assert "StreamHandler" in handler_types


def test_setup_logger_prevents_duplicate_handlers(monkeypatch):
    clear_logger("duplicate_logger")

    monkeypatch.setattr(logging.Logger, "hasHandlers", lambda self: False)

    logger1 = setup_logger("duplicate_logger")
    handler_count_1 = len(logger1.handlers)

    monkeypatch.setattr(logging.Logger, "hasHandlers", lambda self: True)

    logger2 = setup_logger("duplicate_logger")
    handler_count_2 = len(logger2.handlers)

    assert handler_count_1 == handler_count_2


def test_setup_logger_level(monkeypatch):
    clear_logger("level_logger")

    monkeypatch.setattr(logging.Logger, "hasHandlers", lambda self: False)

    logger = setup_logger("level_logger")

    assert logger.level in [
        logging.DEBUG,
        logging.INFO,
        logging.WARNING,
        logging.ERROR,
        logging.CRITICAL,
    ]