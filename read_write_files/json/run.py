import json

# Sample variables
name = "John"
age = 25
city = "New York"

# Create a dictionary with the variables
data = {
    "name": name,
    "age": age,
    "city": city
}

# Specify the file path where you want to save the JSON data
file_path = "example.json"

# write into JSON file
with open(f'data.json', 'w') as json_file:
    json_file.write("{\n")
    comma_flag=1
    for key, value in data.items():
        if comma_flag==0:   # if not first line, then start with come+newline
            json_file.write(f',\n')
        else:
            comma_flag=0
        json_file.write(f'\"{key}\": {json.dumps(value)}')
        print(f'\"{key}\": {json.dumps(value)}')
    json_file.write("\n}")

print(f"Data has been saved to {file_path}")

# Read the data back from the JSON file
with open(f'data.json', 'r') as json_file:
    loaded_data = json.load(json_file)

# Display the loaded data
print("Loaded data:")
print(loaded_data)

# Access individual variables from the loaded data
loaded_name = loaded_data["name"]
loaded_age = loaded_data["age"]
loaded_city = loaded_data["city"]

# Display individual loaded variables
print("\nIndividual loaded variables:")
print(f"Name: {loaded_name}")
print(f"Age: {loaded_age}")
print(f"City: {loaded_city}")
