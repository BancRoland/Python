import pickle

def save_data(data, filename):
    with open(filename, 'wb') as file:
        pickle.dump(data, file)

def load_data(filename):
    try:
        with open(filename, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        return {}

def log_data(weather_data, date, temperature, humidity):
    # Check if the date already exists
    if date in weather_data:
        # Date exists, update the values
        weather_data[date]["temperature"] = temperature
        weather_data[date]["humidity"] = humidity
    else:
        # Date doesn't exist, add a new entry
        weather_data[date] = {"temperature": temperature, "humidity": humidity}

# Example usage:
weather_data = {}
# weather_data = {
#     "2023-01-01": {"temperature": 25.5, "humidity": 60},
#     "2023-01-02": {"temperature": 24.8, "humidity": 65},
#     # Add more data as needed
# }

log_data(weather_data, "2023-01-01", 25.5, 60)
log_data(weather_data, "2023-01-02", 24.8, 65)
log_data(weather_data, "2023-01-03", 26.3, 64)

# Print the updated weather_data
print(weather_data)

for date in weather_data.keys():
    print(f"Date: {date}")
    print(f"Temperature: {weather_data[date]['temperature']}")
    print(f"Humidity: {weather_data[date]['humidity']}")
    print()

save_data(weather_data, 'weather_data.pkl')

# Load the dictionary back from the binary file
loaded_data = load_data('weather_data.pkl')

# Print the loaded data
print(loaded_data)