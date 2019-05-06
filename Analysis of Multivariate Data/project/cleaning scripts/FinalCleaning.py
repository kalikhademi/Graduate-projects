import numpy as np
import csv
import os
import pandas as pd
from MappingScript import EmployerRangeMapping,StateMapping,MajorMapping, RowMapping, JobMajorMapping, EmployerStateListMapping, JobStateListMapping, ListOfState


""" reading the data after Diandra script was ran"""


path = os.path.join(os.path.dirname(__file__), 'clean_data.csv')

visa_data = pd.read_csv(path)

""" use Kiana Code to do the tasks """
print(visa_data.size)
print(visa_data.ndim)
print(visa_data.shape)
visa_data['employer_size'] = EmployerRangeMapping(visa_data)
visa_data['Center'] = StateMapping(visa_data)
visa_data['Applicant Major'] = MajorMapping(visa_data)
visa_data['Career Major'] = JobMajorMapping(visa_data)
visa_data['Job State'] = JobStateListMapping(visa_data)
visa_data['Employer State'] = EmployerStateListMapping(visa_data)

print("I am here!")

print(visa_data.size)
print(visa_data.ndim)
print(visa_data.shape)


visa_data['job_info_work_state'] = visa_data['job_info_work_state'].apply(ListOfState)
""" select the target variables and form the final data"""

finalData = visa_data[['case_received_date','case_status','country_of_citizenship','decision_date','employer_name','Employer State','employer_yr_estab'
						,'foreign_worker_info_education','job_info_alt_combo_ed',
						'Job State', 'us_economic_sector','wage_offer_from_9089','wage_offer_unit_of_pay_9089','employer_size','Center','Applicant Major','Career Major']]

finalData.to_csv('Final_data.csv')



