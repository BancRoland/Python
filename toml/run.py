import tomli

# Open and read the TOML file in binary mode
with open('config.toml', 'rb') as toml_file:
   toml_data = tomli.load(toml_file)

# Access values from the TOML data
title = toml_data.get('title')
author = toml_data.get('author')
port = toml_data.get('port')
enabled = toml_data.get('enabled')

# Print the values
print(f"Title: {title}")
print(f"Author: {author}")
print(f"Port: {port}")
print(f"Enabled: {enabled}")
