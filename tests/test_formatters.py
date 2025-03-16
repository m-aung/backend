import datetime
import pytest
from utilities.formatters import format_date_to_utc

def test_format_date_to_utc():
    data = (4, 'Jon', 'Doe', 'user@example.com', '123456789', 'owner', '123#abc', datetime.datetime(2025, 3, 16, 15, 9, 25, 382070))
    keys = ['id', 'first_name', 'last_name', 'email', 'phone', 'role', 'password_hash', 'created_at']
    dateKey = 'created_at'
    
    expected_output = {
        'id': 4,
        'first_name': 'Jon',
        'last_name': 'Doe',
        'email': 'user@example.com',
        'phone': '123456789',
        'role': 'owner',
        'password_hash': '123#abc',
        'created_at': datetime.datetime(2025, 3, 16, 15, 9, 25, 382070).astimezone(datetime.timezone.utc).isoformat()
    }
    
    assert format_date_to_utc(data, keys, dateKey) == expected_output

def test_format_date_to_utc_no_date():
    data = (4, 'Jon', 'Doe', 'user@example.com', '123456789', 'owner', '123#abc', None)
    keys = ['id', 'first_name', 'last_name', 'email', 'phone', 'role', 'password_hash', 'created_at']
    dateKey = 'created_at'
    
    expected_output = {
        'id': 4,
        'first_name': 'Jon',
        'last_name': 'Doe',
        'email': 'user@example.com',
        'phone': '123456789',
        'role': 'owner',
        'password_hash': '123#abc',
        'created_at': None
    }
    
    assert format_date_to_utc(data, keys, dateKey) == expected_output

def test_format_date_to_utc_no_date_key():
    data = (4, 'Jon', 'Doe', 'user@example.com', '123456789', 'owner', '123#abc', datetime.datetime(2025, 3, 16, 15, 9, 25, 382070))
    keys = ['id', 'first_name', 'last_name', 'email', 'phone', 'role', 'password_hash', 'created_at']
    dateKey = 'non_existent_key'
    
    expected_output = {
        'id': 4,
        'first_name': 'Jon',
        'last_name': 'Doe',
        'email': 'user@example.com',
        'phone': '123456789',
        'role': 'owner',
        'password_hash': '123#abc',
        'created_at': datetime.datetime(2025, 3, 16, 15, 9, 25, 382070)
    }
    
    assert format_date_to_utc(data, keys, dateKey) == expected_output