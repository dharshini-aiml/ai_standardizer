"""Pytest configuration and fixtures.

Ensure the repository root is on `sys.path` so tests can import the
application package (`app`) regardless of how `pytest` is invoked.
"""
import sys
import os

# Compute repository root (parent of the `tests` directory)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if ROOT_DIR not in sys.path:
	sys.path.insert(0, ROOT_DIR)
