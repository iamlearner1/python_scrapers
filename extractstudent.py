import json

data = """
REESHMA	5065	8	84	9652301990
SANTHOSHGOUD	5099	8	77	9666200974
SAIDEEKSHITH	5080	8	69	9014465637
SPANDANA	5804	8	66	7286092309
SAHITHI	5063	8	64	9618823673


"""

# Split the data into lines
lines = data.strip().split("\n")

# Initialize a list to hold the formatted output
formatted_data = []

# Process each line
for line in lines:
    parts = line.split()
    admission_no = parts[1]
    number = parts[-1]
    formatted_data.append({"admission_no": admission_no, "number": number})

# Define the filename
filename = 'formatted_data.json'

# Write the formatted data to a JSON file
with open(filename, 'w') as file:
    json.dump(formatted_data, file, indent=2)

print(f"Data has been written to {filename}")
