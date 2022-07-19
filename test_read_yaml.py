import pytest

from read_yaml import read_yaml_file
from PortalException import PortalException

#file not exist
def test_yaml_file_exist():
    # the exception raised due to non existance of file handled using pytest.raises()
    with pytest.raises(PortalException):
        read_yaml_file('file_not_exist.yaml')




