import pytest
from Chapter09.introduction_fixtures import Address, Gender, Person


@pytest.fixture
def address():
    return Address(
        street_address="12 Squirell Street",
        postal_code="424242",
        city="Woodtown",
        country="US",
    )


@pytest.fixture()
def person(address):
    return Person(
        first_name="John",
        last_name="Doe",
        gender=Gender.MALE,
        birthdate="1991-01-01",
        interests=["travel", "sports"],
        address=address,
    )


def test_address_country(address):
    assert address.country == "US"


def test_person_first_name(person):
    assert person.first_name == "John"


def test_person_address_city(person):
    assert person.address.city == "Woodtown"

# Once again, pytest makes it very straightforward: fixtures are simple functions decorated with the fixture decorator. 
# Inside, you can write any logic and return the data you'll need in your tests. 
# Here, in address, we instantiate an Address object with fake data and return it.

# Now, how can we use this fixture? 
# If you look at the test_address_country test, you'll see some magic happening: by setting an address argument on the test function, 
    # pytest automatically detects that it corresponds to the address fixture, executes it, and passes its return value. 
# Inside the test, we have our Address object ready to use. 
# pytest calls this requesting a fixture.

# You may have noticed that we also defined another fixture, person. 
# Once again, we instantiate a Person model with dummy data. 
# The interesting thing to note, however, is that we actually requested the address fixture to use it inside! 
# That's what makes this system so powerful: fixtures can depend on other fixtures, which can also depend on others, and so on. 
# In some way, it's quite similar to dependency injection, as we discussed in Chapter 5, Dependency Injections in FastAPI.

# With that, our quick introduction to pytest has come to an end. 
# Of course, there are so many more things to say, but this will be enough for you to get started. 
# If you want to explore this topic further, you can read the official pytest documentation, which includes tons of examples showing you how you can benefit from all its features: https://docs.pytest.org/en/latest/.