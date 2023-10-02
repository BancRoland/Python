import folium
# import random
from selenium import webdriver


lat = 47.4707
lon = 19.0855

# Create a Folium map
m = folium.Map(location=[lat, lon], zoom_start=5)  # Centered at (0, 0) with a zoom level of 5
folium.Marker([lat, lon]).add_to(m)

# Save the map to an HTML file
m.save("map.html")

# # Initialize the WebDriver (assuming the Chrome WebDriver is in your PATH)
# driver = webdriver.Chrome()

# # Open the saved HTML file
# driver.get("file://home/bancr/Desktop/Python/geography/mapmaker/random_map.html")  # Replace with the correct path

# # Capture a screenshot and save it as a PNG image
# driver.save_screenshot("random_map.png")

# # Close the WebDriver
# driver.quit()
