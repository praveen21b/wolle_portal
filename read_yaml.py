import yaml
from collections import defaultdict

from PortalException import PortalException
import os, sys
from portal_logs import logging


def read_yaml_file(file_path:str)->list:#list of dictionary
    """
    Reads a YAML file and returns the contents as a dictionary.
    
    """
    input_dict = defaultdict(list)
    try:
        with open(file_path, 'rb') as yaml_file:
            logging.info(f"Reading of YAML.")
            list_schema_values = yaml.safe_load(yaml_file)
            for value in list_schema_values:
                input_dict[value['brand']]=(value['name'])
            return input_dict
        
    except Exception as e:
        raise PortalException(e,sys) from e