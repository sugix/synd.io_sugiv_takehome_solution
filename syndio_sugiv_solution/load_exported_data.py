from importlib import resources
import csv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model.models import *

def parse_raw_data(filepath):
    
    with open(filepath) as f:
        csv_reader = csv.DictReader(f)
        data = [row for row in csv_reader]
        return data

def populate_tables(session, company_csv_data):

    for row in company_csv_data:
        geo = (session.query(Geo).filter(Geo.employee_city == row["employee_city"]).one_or_none())

        if geo is None:
            geo = Geo(geo_zone_id=row["geo_zone_id"],
            employee_geo_zone=row["employee_geo_zone"],
            employee_city=row["employee_city"],
            employee_state=row["employee_state"],
            geo_zone_cost_of_living_factor=row["geo_zone_cost_of_living_factor"]
            )

            session.add(geo)

        company = (session.query(Company).filter(Company.company_name == row["company_name"]).one_or_none())

        if company is None:
            company = Company(company_name=row["company_name"],
            company_headquarters_city=row["company_headquarters_city"],
            company_headquarters_state=row["company_headquarters_state"],
            company_sector=row["company_sector"]
            )

            session.add(company)
        

        employee = (session.query(Employee).filter(Employee.employee_id == row["employee_id"]).one_or_none())

        if employee is None:
            employee = Employee(employee_id=row["employee_id"],
            employee_job_group=row["employee_job_group"],
            employee_job_level=row["employee_job_level"],
            employee_job_title=row["employee_job_title"],
            employee_gender=row["employee_gender"],
            employee_race=row["employee_race"],
            employee_compensation=row["employee_compensation"],
            employee_years_of_experience=row["employee_years_of_experience"],
            employee_time_in_role=row["employee_time_in_role"],
            employee_city=row["employee_city"],
            employee_company=row["company_name"]
            )

            session.add(employee)

        geo.employees.append(employee)
        company.employees.append(employee)
        session.commit()

    session.close()

# Parse raw data belonging to different companies

with resources.path("data", "company_a_employee_uploads.csv") as company_1_data_path:
    company_1_flat_data = parse_raw_data(company_1_data_path)

""" Bad data in gender column, leaving it as it is and few columns names had typos and those are fixed

with resources.path("data", "company_b_employee_uploads.csv") as company_2_data_path:
    company_2_flat_data = parse_raw_data(company_2_data_path)

"""
with resources.path("data", "company_c_employee_uploads.csv") as company_3_data_path:
    company_3_flat_data = parse_raw_data(company_3_data_path)

# Re-create the db file at every run

with resources.path("data","input_data.db") as sqlite_db_path:
    if os.path.exists(sqlite_db_path):
        os.remove(sqlite_db_path)

engine = create_engine(f"sqlite:///{sqlite_db_path}", pool_pre_ping=True)
Base.metadata.create_all(engine)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

populate_tables(session, company_1_flat_data)

### Commenting out because of bad data ###

#populate_tables(session,company_2_flat_data)


populate_tables(session,company_3_flat_data)

def main():
    pass

if __name__ == "__main__":
    main()