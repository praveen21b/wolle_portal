import pandas as pd
from portal_logs import logging
import PortalException
import os, sys

def save_as_csv(data:pd.DataFrame) -> None:
    try:
        # overwrites the file
        logging.info(f'A CSV file created')
        data.to_csv('wolle_portal.csv', index=False)
        logging.info(f'A CSV file created successfully')
    except Exception as e:
        raise PortalException(e,sys) from e