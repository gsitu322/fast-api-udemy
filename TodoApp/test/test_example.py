import pytest
from sqlalchemy.testing.pickleable import User


def test_equal_or_not_equal():
    assert 3 == 3
    assert 3 != 1


def test_is_instance():
    assert isinstance("This is a string", str)
    assert not isinstance("10", int)


def test_boolean():
    assert True == True
    assert False == False
    assert True == True


class Student():
    def __init__(self, first_name: str, last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years


@pytest.fixture
def default_employee():
    return Student("John", "Doe", "Computer Science", 1)


def test_person_initialization(default_employee):
    assert default_employee.first_name == "John"
    assert default_employee.last_name == "Doe"
    assert default_employee.major == "Computer Science"
    assert default_employee.years == 1