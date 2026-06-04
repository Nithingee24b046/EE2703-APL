import matplotlib.pyplot as plt
import city_temperature_function


filename = 'GlobalLandTemperaturesByMajorCity.csv'
city_name = 'Madras'
x = city_temperature_function.get_city_temperatures(filename,city_name)

keys = list(x.keys())
values = list(x.values())

x_positions = range(len(x))

# Scatter plot
plt.scatter(x_positions, values, color="blue", s=100)

# Set proper ticks and labels
# plt.xticks(x_positions, keys[:5])
plt.xlabel("Months")
plt.ylabel("Temperatures")
plt.title("Months vs Temperatures for the given city")
plt.xlim(-0.5, len(keys)-0.5)  # adds width to x-axis
plt.show()