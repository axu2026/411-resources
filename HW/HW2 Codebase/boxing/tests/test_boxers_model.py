from contextlib import contextmanager
import re
import sqlite3
import pytest

from boxing.models.boxers_model import (
    Boxer,
    create_boxer,
    delete_boxer,
    get_leaderboard,
    get_boxer_by_id,
    get_boxer_by_name,
    get_weight_class,
    update_boxer_stats
)

@pytest.fixture
def normalize_whitespace(sql_query: str) -> str:
    return re.sub(r'\s+', ' ', sql_query).strip()

# need to make a mocker

def test_create_boxer():

def test_create_dupe_boxer():

def test_create_boxer_invalid_age():

def test_create_boxer_invalid_height():

def test_create_boxer_invalid_weight():

def test_create_boxer_invalid_reach():

def test_delete_boxer():

def test_delete_boxer_nothing():

def test_get_leaderboard():

def test_get_leaderboard_invalid():

def test_get_boxer_by_id():

def test_get_boxer_by_id_bad():

def test_get_boxer_by_name():

def test_get_boxer_by_name_bad():

def test_get_weight_class():

def test_get_weight_class_bad():

def test_update_boxer_stats():

def test_update_boxer_stats_bad():