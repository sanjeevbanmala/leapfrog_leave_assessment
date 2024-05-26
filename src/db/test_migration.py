import os
import sys
import pytest
from unittest.mock import patch
from io import StringIO

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from db.db_migrate import migration_up, migration_down


def test_migration_up(capfd):
    migration_up()
    captured = capfd.readouterr()
    expected_output = "[+] Executed extract_employees.sql\n\n"
    assert expected_output in captured.out


def test_migration_down(capfd):
    migration_down()
    captured = capfd.readouterr()
    expected_output = "[+] VyagutaInfo Database cleaned!\n\n"
    assert captured.out == expected_output
