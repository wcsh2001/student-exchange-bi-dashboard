import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker()
Faker.seed(42)
random.seed(42)

academic_years = ["2022/2023", "2023/2024", "2024/2025"]
num_records_per_year = [450, 520, 600] 

# Expanded to 45 global institutions
host_institutions = {
    "National University of Singapore": "Singapore",
    "Nanyang Technological University": "Singapore",
    "University College London": "United Kingdom",
    "Imperial College London": "United Kingdom",
    "King's College London": "United Kingdom",
    "University of Edinburgh": "United Kingdom",
    "University of Manchester": "United Kingdom",
    "University of Oxford": "United Kingdom",
    "University of Cambridge": "United Kingdom",
    "University of Glasgow": "United Kingdom",
    "University of Sydney": "Australia",
    "University of Melbourne": "Australia",
    "UNSW Sydney": "Australia",
    "University of Queensland": "Australia",
    "Monash University": "Australia",
    "Australian National University": "Australia",
    "ETH Zurich": "Switzerland",
    "EPFL": "Switzerland",
    "University of Tokyo": "Japan",
    "Kyoto University": "Japan",
    "Osaka University": "Japan",
    "Sciences Po": "France",
    "Sorbonne University": "France",
    "Lund University": "Sweden",
    "Uppsala University": "Sweden",
    "University of Amsterdam": "Netherlands",
    "Delft University of Technology": "Netherlands",
    "LMU Munich": "Germany",
    "Heidelberg University": "Germany",
    "Technical University of Munich": "Germany",
    "University of Hong Kong": "Hong Kong",
    "Chinese University of Hong Kong": "Hong Kong",
    "Tsinghua University": "China",
    "Peking University": "China",
    "Seoul National University": "South Korea",
    "Yonsei University": "South Korea",
    "University of Copenhagen": "Denmark",
    "KU Leuven": "Belgium",
    "Trinity College Dublin": "Ireland",
    "UC Berkeley": "United States",
    "UCLA": "United States",
    "University of Washington": "United States",
    "University of Michigan": "United States",
    "Cornell University": "United States",
    "New York University": "United States"
}

faculties = ["Faculty of Arts & Science", "Faculty of Engineering", "School of Business", "Faculty of Information", "Faculty of Music"]
colleges = ["University College", "Trinity College", "Victoria College", "New College", "Woodsworth College", "None"]
programs = ["Computer Science", "Economics", "History", "Physics", "Data Science", "Psychology", "International Relations", "Sociology", "Information Systems"]
pathways = ["University-Wide", "Faculty-Specific", "Summer Research"]
statuses = ["Admitted", "Nominated", "Not Admitted", "Withdrawn"]

def simulate_blanks(value, blank_probability=0.05):
    """Randomly returns None to simulate missing data."""
    if random.random() < blank_probability:
        return None
    return value

def generate_exchange_data(year, num_records):
    data = []
    student_pool_size = int(num_records * 0.7) 
    student_ids = [fake.unique.random_int(min=100000000, max=999999999) for _ in range(student_pool_size)]
    
    student_profiles = {}
    for sid in student_ids:
        student_profiles[sid] = {
            "Citizenship": simulate_blanks(fake.country(), 0.02),
            "Disability": simulate_blanks(random.choices(["Yes", "No", "Prefer not to say"], weights=[0.05, 0.90, 0.05])[0], 0.10),
            "Gender": simulate_blanks(random.choices(["Female", "Male", "Non-binary", "Prefer not to say"], weights=[0.55, 0.40, 0.03, 0.02])[0], 0.05),
            "Indigenous Status": simulate_blanks(random.choices(["Yes", "No", "Prefer not to say"], weights=[0.02, 0.95, 0.03])[0], 0.15),
            "Legal Status in Canada": simulate_blanks(random.choices(["Citizen", "Permanent Resident", "International Student"], weights=[0.60, 0.15, 0.25])[0], 0.05),
            "Faculty": simulate_blanks(random.choice(faculties), 0.01),
            "College": simulate_blanks(random.choice(colleges), 0.08),
            "Program 1": random.choice(programs), # Assuming primary program is always required
            "Program 2": simulate_blanks(random.choice(programs), 0.60), # High chance of blank (no second program)
            "Program 3": simulate_blanks(random.choice(programs), 0.90), # Very high chance of blank
            "Master Program Name": simulate_blanks(random.choice(["Honours Bachelor of Arts", "Honours Bachelor of Science", "Bachelor of Engineering", "Master of Information"]), 0.10)
        }

    for _ in range(num_records):
        sid = random.choice(student_ids)
        profile = student_profiles[sid]
        
        host_inst = random.choice(list(host_institutions.keys()))
        host_country = host_institutions[host_inst]
        
        prog_combined = profile["Program 1"]
        if profile["Program 2"]:
            prog_combined += f", {profile['Program 2']}"
        if profile["Program 3"]:
            prog_combined += f", {profile['Program 3']}"

        record = {
            "Academic Year": year,
            "Student ID": sid,
            "Host Institution": simulate_blanks(host_inst, 0.02),
            "Host Institution Choice": simulate_blanks(random.choice([1, 2, 3]), 0.05),
            "Pathway": simulate_blanks(random.choice(pathways), 0.03),
            "Status": random.choices(statuses, weights=[0.4, 0.2, 0.3, 0.1])[0], # Status usually required in BI
            "Country of Institution": host_country,
            "Citizenship": profile["Citizenship"],
            "Disability": profile["Disability"],
            "Gender": profile["Gender"],
            "Indigenous Status": profile["Indigenous Status"],
            "Legal Status in Canada": profile["Legal Status in Canada"],
            "Faculty": profile["Faculty"],
            "College": profile["College"],
            "Program 1": profile["Program 1"],
            "Program 2": profile["Program 2"],
            "Program 3": profile["Program 3"],
            "Program of Study (Combined)": prog_combined,
            "Master Program Name": profile["Master Program Name"],
            "Choice Level": simulate_blanks(random.choice(["Primary", "Secondary", "Tertiary"]), 0.05)
        }
        data.append(record)
        
    return pd.DataFrame(data)

for year, num in zip(academic_years, num_records_per_year):
    df = generate_exchange_data(year, num)
    file_year = year.replace("/", "-")
    filename = f"exchange_applications_raw_{file_year}.csv"
    df.to_csv(filename, index=False)
    print(f"Generated {filename} with {num} records.")