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

# Custom country weights to emphasize Canada (55%) and heavily populated nations
populous_countries = [
    "Canada", "China", "India", "United States", "Indonesia", "Pakistan", "Brazil", 
    "Nigeria", "Bangladesh", "Russia", "Mexico", "Japan", "Ethiopia", "Philippines", 
    "Egypt", "Vietnam", "DR Congo", "Turkey", "Iran", "Germany", "France", "United Kingdom"
]
country_weights = [
    0.55, 0.08, 0.08, 0.05, 0.02, 0.02, 0.02, 
    0.02, 0.02, 0.02, 0.02, 0.02, 0.01, 0.01, 
    0.01, 0.01, 0.01, 0.01, 0.005, 0.005, 0.005, 0.005
]

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
        # Guarantee 3 unique citizenships before applying sequential blanks
        c1 = random.choices(populous_countries, weights=country_weights)[0]
        c2 = c1
        while c2 == c1:
            c2 = random.choices(populous_countries, weights=country_weights)[0]
        c3 = c1
        while c3 in (c1, c2):
            c3 = random.choices(populous_countries, weights=country_weights)[0]
            
        c1_final = simulate_blanks(c1, 0.02)
        c2_final = simulate_blanks(c2, 0.75) if c1_final else None
        c3_final = simulate_blanks(c3, 0.95) if c2_final else None

        # Guarantee 3 unique programs before applying sequential blanks
        p1, p2, p3 = random.sample(programs, 3)
        p1_final = p1  # Original had no blank probability for Program 1
        p2_final = simulate_blanks(p2, 0.60) if p1_final else None
        p3_final = simulate_blanks(p3, 0.90) if p2_final else None

        student_profiles[sid] = {
            "Citizenship 1": c1_final,
            "Citizenship 2": c2_final,
            "Citizenship 3": c3_final,
            "Disability": simulate_blanks(random.choices(["Yes", "No", "Prefer not to say"], weights=[0.05, 0.90, 0.05])[0], 0.10),
            "Gender": simulate_blanks(random.choices(["Female", "Male", "Non-binary", "Prefer not to say"], weights=[0.55, 0.40, 0.03, 0.02])[0], 0.05),
            "Indigenous Status": simulate_blanks(random.choices(["Yes", "No", "Prefer not to say"], weights=[0.02, 0.95, 0.03])[0], 0.15),
            "Legal Status in Canada": simulate_blanks(random.choices(["Citizen", "Permanent Resident", "International Student"], weights=[0.60, 0.15, 0.25])[0], 0.05),
            "Faculty": simulate_blanks(random.choice(faculties), 0.01),
            "College": simulate_blanks(random.choice(colleges), 0.08),
            "Program 1": p1_final, 
            "Program 2": p2_final, 
            "Program 3": p3_final
        }

    for _ in range(num_records):
        sid = random.choice(student_ids)
        profile = student_profiles[sid]
        
        # Guarantee 3 unique host institutions before applying sequential blanks
        h1, h2, h3 = random.sample(list(host_institutions.keys()), 3)
        h1_final = simulate_blanks(h1, 0.02)
        h2_final = simulate_blanks(h2, 0.50) if h1_final else None
        h3_final = simulate_blanks(h3, 0.90) if h2_final else None

        record = {
            "Academic Year": year,
            "Student ID": sid,
            "Host Institution 1": h1_final,
            "Country of Institution 1": host_institutions[h1_final] if h1_final else None,
            "Host Institution 2": h2_final,
            "Country of Institution 2": host_institutions[h2_final] if h2_final else None,
            "Host Institution 3": h3_final,
            "Country of Institution 3": host_institutions[h3_final] if h3_final else None,
            "Pathway": simulate_blanks(random.choice(pathways), 0.03),
            "Status": random.choices(statuses, weights=[0.4, 0.2, 0.3, 0.1])[0],
            "Citizenship 1": profile["Citizenship 1"],
            "Citizenship 2": profile["Citizenship 2"],
            "Citizenship 3": profile["Citizenship 3"],
            "Disability": profile["Disability"],
            "Gender": profile["Gender"],
            "Indigenous Status": profile["Indigenous Status"],
            "Legal Status in Canada": profile["Legal Status in Canada"],
            "Faculty": profile["Faculty"],
            "College": profile["College"],
            "Program 1": profile["Program 1"],
            "Program 2": profile["Program 2"],
            "Program 3": profile["Program 3"]
        }
        data.append(record)
        
    return pd.DataFrame(data)

for year, num in zip(academic_years, num_records_per_year):
    df = generate_exchange_data(year, num)
    file_year = year.replace("/", "-")
    filename = f"exchange_applications_raw_{file_year}.csv"
    df.to_csv(filename, index=False)
    print(f"Generated {filename} with {num} records.")