
# coding: utf-8

# # WeatherPy
# ----
# 
# ### Analysis
# * As expected, the weather becomes significantly warmer as one approaches the equator (0 Deg. Latitude). More interestingly, however, is the fact that the southern hemisphere tends to be warmer this time of year than the northern hemisphere. This may be due to the tilt of the earth.
# * There is no strong relationship between latitude and cloudiness. However, it is interesting to see that a strong band of cities sits at 0, 80, and 100% cloudiness.
# * There is no strong relationship between latitude and wind speed. However, in northern hemispheres there is a flurry of cities with over 20 mph of wind.
# 
# ---
# 
# #### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[1]:


# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import time
from datetime import datetime
import random
import seaborn as sns
import csv


# Import API key
import api_keys

# Incorporated citipy to determine city based on latitude and longitude
from citipy import citipy

# Output File (CSV)
output_data_file = "output_data/cities.csv"


# ## Generate Cities List

# In[2]:


#Create dataframe for cities
cities_df = pd.DataFrame()

# Create a set of random lat and lng combinations
cities_df['Lat'] = [np.random.uniform(-90,90) for x in range(1500)]
cities_df['Lngs'] = [np.random.uniform(-180, 180) for x in range(1500)]


cities_df['City'] = ""
cities_df['Country'] = ""

# Identify nearest city for each latitude & longitude 
count = 0
for index, row in cities_df.iterrows():
    near_city = citipy.nearest_city(row['Lat'], row['Lngs']).city_name
    near_country = citipy.nearest_city(row['Lat'], row['Lngs']).country_code
    cities_df.set_value(index,"City",near_city)
    cities_df.set_value(index,"Country",near_country)

cities_df['Max Temp'] = ""
cities_df['Humidity'] = ""
cities_df['Clouds'] = ""
cities_df['Wind Speed'] = ""

cities_df.head()


# In[3]:


#Remove duplicates
cities_df = cities_df.drop_duplicates(subset='City').reset_index()

len(cities_df)


# ### Perform API Calls
# * Perform a weather check on each city using a series of successive API calls.
# * Include a print log of each city as it'sbeing processed (with the city number and city name).
# 

# In[4]:


#create empty lists for columns
max_temp = []
humidity =[]
clouds = []
wind = []
country = []

counter = 0
url = "https://api.openweathermap.org/data/2.5/weather?"
units = "imperial"
key = "7dc7e401dba8bb260ffdcae2edd106a4"

#Iterate through rows and pull data from the api 

print("Beginning Data Retrieval")

for index, row in cities_df.iterrows():
    counter +=1
    city = row["City"]
    target_url = url+"units="+units+"&appid="+key+"&q="+city
    weather_json = requests.get(target_url).json()
    if weather_json["cod"] == "404":
        print("City not found, skipping...")
   
    else: 
        latitude = weather_json["coord"]["lat"]
        longitude = weather_json["coord"]["lon"]
        temp = weather_json["main"]["temp_max"]
        humidity = weather_json["main"]["humidity"]
        cloud = weather_json["clouds"]["all"]
        wind = weather_json["wind"]["speed"]
        cities_df.set_value(index,"Max Temp", temp)
        cities_df.set_value(index,"Humidity",humidity)
        cities_df.set_value(index,"Wind Speed", wind)
        cities_df.set_value(index,"Clouds",cloud)
        cities_df.set_value(index,"Lat", latitude)
        cities_df.set_value(index,"Lngs",longitude)
    
        print("-----------------------------")
        print("Processing Record "+str(counter) + ' | ' +row["City"])
        print(target_url)
    
        time.sleep(1)
print("Data Retrieval Complete")
print("-----------------------------")


# ### Convert Raw Data to DataFrame
# * Export the city data into a .csv.
# * Display the DataFrame

# In[ ]:


cities_df.to_csv("output_data/cities.csv")


# In[ ]:


cities_df.count()


# In[ ]:


#Replace " " with NaN
cities_df['Max Temp'] = pd.to_numeric(cities_df['Max Temp'], errors = 'coerce')
cities_df['Humidity'] = pd.to_numeric(cities_df['Humidity'], errors = 'coerce')
cities_df['Wind Speed'] = pd.to_numeric(cities_df['Wind Speed'], errors = 'coerce')
cities_df['Clouds'] = pd.to_numeric(cities_df['Clouds'], errors = 'coerce')


cities_df.head()


# ### Plotting the Data
# * Use proper labeling of the plots using plot titles (including date of analysis) and axes labels.
# * Save the plotted figures as .pngs.

# #### Latitude vs. Temperature Plot

# In[ ]:


plt.scatter(cities_df["Lat"], 
            cities_df["Max Temp"], c=cities_df["Max Temp"],
            edgecolor="black", linewidths=1, marker="o", 
            cmap='Blues', alpha=0.9, label="City", s=30)

# Incorporate the other graph properties
plt.title(f"City Latitude vs. Max Temperature {datetime.now().strftime('%m/%d/%Y')}")
plt.ylabel("Max Temperature (F)")
plt.xlabel("Latitude")
plt.grid(True)
plt.xlim([-60, 85])
plt.ylim([0, 120])

# Save the figure
plt.savefig("output_data/LatitudevsTemperature.png")


# Show plot
plt.show()


# #### Latitude vs. Humidity Plot

# In[ ]:


#Build a scatter plot for Latitude vs. Humidity (%)

plt.scatter(cities_df["Lat"], 
            cities_df["Humidity"], c=cities_df["Humidity"],
            edgecolor="black", linewidths=1, marker="o", 
            cmap='Blues', alpha=0.9, label="City")

plt.style.use('seaborn')
plt.title(f"City Latitude vs. Humidity {datetime.now().strftime('%m/%d/%Y')}")
plt.ylabel("Humidity (%)")
plt.xlabel("Latitude")
plt.grid(True)
plt.xlim([-60, 85])
plt.ylim([0, 120])

# Save the figure
plt.savefig("output_data/LatitudevsHumidity.png")

# Show plot
plt.show()


# #### Latitude vs. Cloudiness Plot

# In[ ]:


#Build a scatter plot for Latitude vs. Cloudiness (%)

plt.scatter(cities_df["Lat"], 
            cities_df["Clouds"], c=cities_df["Clouds"],
            edgecolor="black", linewidths=1, marker="o",
            cmap='Blues', alpha=0.9, label="City")

plt.style.use('seaborn')
plt.title(f"City Latitude vs. Cloudiness {datetime.now().strftime('%m/%d/%Y')}")
plt.ylabel("Cloudiness (%)")
plt.xlabel("Latitude")
plt.grid(True)
plt.xlim([-80, 100])
plt.ylim([-10, 125])

# Save the figure
plt.savefig("output_data/LatitudevsCloudiness.png")

# Show plot
plt.show()


# #### Latitude vs. Wind Speed Plot

# In[ ]:


#Build a scatter plot for Latitude vs. Wind Speed (mph)

plt.scatter(cities_df["Lat"], 
            cities_df["Wind Speed"], c=cities_df["Wind Speed"],
            edgecolor="black", linewidths=1, marker="o", 
            cmap='Blues', alpha=0.9, label="City")

plt.style.use('seaborn')
plt.title(f"City Latitude vs. Wind Speed {datetime.now().strftime('%m/%d/%Y')}")
plt.ylabel("Wind Speed (mph)")
plt.xlabel("Latitude")
plt.grid(True)
plt.xlim([-80, 100])
plt.ylim([-5, 40])

# Save the figure
plt.savefig("output_data/LatitudevsWindSpeed.png")

# Show plot
plt.show()

