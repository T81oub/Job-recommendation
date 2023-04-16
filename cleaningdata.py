import os
import pandas as pd
from nltk.stem import PorterStemmer

# Load the data
jobs_data = pd.read_csv("data/dice_com-job_us_sample.csv")

# Drop duplicates
jobs_data.drop_duplicates(inplace=True)

# Remove unnecessary columns
jobs_data.drop(columns=['advertiserurl', 'employmenttype_jobstatus', 'joblocation_address', 'postdate',
                         'shift', 'site_name'], inplace=True)

# Remove rows with missing values
jobs_data.dropna(inplace=True)

# Remove jobs with "no skills" information
no_skills_keywords = ["Please See job description", "(See Job Description)", "SEE BELOW",
                      "Telecommuting not available Travel not required", "Refer to Job Description",
                      "Please see Required Skills"]
jobs_data = jobs_data[~jobs_data.skills.isin(no_skills_keywords)]

# Create a new column "jobdescription" by concatenating the "jobtitle", "skills", and "jobdescription" columns
new_data = jobs_data.copy()
new_data['jobdescription'] = new_data['jobtitle'] + " " + new_data['skills'] + " " + new_data['jobdescription']

# Preprocess the "jobdescription" column
new_data['jobdescription'] = new_data['jobdescription'].str.lower()
ps = PorterStemmer()
new_data['jobdescription'] = new_data['jobdescription'].apply(lambda x: " ".join([ps.stem(word) for word in x.split()]))

# Create a "data" folder if it does not exist
if not os.path.exists('data'):
    os.makedirs('data')

# Save the cleaned data to a CSV file in the "data" folder
new_data.to_csv('data/cleaned_jobs_data.csv', index=False)
