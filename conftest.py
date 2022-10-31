import shutil

import pytest


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="test", help="Target test environment (Default: test)")


def pytest_configure(config):
    # Environment Configurations Setting
    env = config.getoption("--env").lower()
    try:
        shutil.copyfile(f"./configurations/{env}.py", "./configurations/env.py")
    except Exception as e:
        print(f"Invalid Environment: {env}\nError Message: {e}")


@pytest.fixture(scope="function")
def data(request):
    test_data = request.param
    if not bool(test_data['is_run']):
        pytest.skip(f"Skip caused by test data setting.")
    return test_data
