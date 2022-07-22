import connectorx as cx
import polars as pl
from importlib import resources
import logging
import sys

def main():

    log_format = logging.Formatter('[%(asctime)s] [%(levelname)s] - %(message)s')
    log = logging.getLogger(__name__)                                  
    log.setLevel(logging.INFO)                                       

                                                       
    handler = logging.StreamHandler(sys.stdout)                             
    handler.setLevel(logging.INFO)                                        
    handler.setFormatter(log_format)                                        
    log.addHandler(handler)                                            
                                                                
    
    with resources.path("data","input_data.db") as sqlite_db_path:
        sqlite_conn = f"sqlite://{sqlite_db_path}"

    query = "SELECT employee_job_group,employee_gender,AVG(employee_compensation) from employee GROUP BY employee_job_group,employee_gender"
    log.info(pl.read_sql(query,sqlite_conn))
    

if __name__ == "__main__":
    main()