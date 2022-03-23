from pytest_factoryboy import register

from tests.factory import AdFactory, UserFactory, SelectionFactory

# fixtures
pytest_plugins = "tests.fixtures"


# factories
register(AdFactory)
register(UserFactory)
register(SelectionFactory)
