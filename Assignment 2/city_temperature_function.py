# Implement the functions defined below to form a useful 
# set of library functions.  Sometimes also called 
# an Application Programming Interface or API

import csv

# The two functions below are given as useful examples to start with
def get_city_temperatures(filename, city_name):
    """
    Extract temperature data for a specific city from CSV file.
    
    Parameters:
    filename (str): Path to the CSV file
    city_name (str): Name of the city to extract data for
    
    Returns:
    dict: Dictionary mapping 'YYYY-MM' to temperature (float)
          Returns empty dict if city not found
    """
    temperature_data = {}
    
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            # Check if this row matches our city
            if row['City'] == city_name:
                # Extract year-month from date (format: 1849-01-01 -> 1849-01)
                date_str = row['dt']
                year_month = date_str[:7]  # Take first 7 characters (YYYY-MM)
                
                # Get temperature, handle missing values
                temp_str = row['AverageTemperature']
                if temp_str and temp_str.strip():  # Check if not empty
                    try:
                        temperature = round(float(temp_str),3)
                        temperature_data[year_month] = temperature
                    except ValueError:
                        # Skip rows with invalid temperature data
                        continue
    
    return temperature_data


def get_available_cities(filename, limit=None):
    """
    Get list of unique cities in the dataset.
    
    Parameters:
    filename (str): Path to the CSV file
    limit (int): Maximum number of cities to return (None for all)
    
    Returns:
    list: List of unique city names
    """
    cities = set()
    
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            cities.add(row['City'])
            if limit and len(cities) >= limit:
                break
    
    return sorted(list(cities))

# =============================================================================
# ASSIGNMENT: Build a Temperature Data API
# =============================================================================
# Students should implement these 5 functions to create a complete API

def find_temperature_extremes(filename, city_name):
    """
    Find the hottest and coldest months on record for a city.
    
    Parameters:
    filename (str): Path to the CSV file
    city_name (str): Name of the city
    
    Returns:
    dict: {
        'hottest': {'date': 'YYYY-MM', 'temperature': float},
        'coldest': {'date': 'YYYY-MM', 'temperature': float}
    }
    
    """
    # TODO: implementation here
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        temperature_data ={}
        extremetemps ={'hottest':None,'coldest':None}

        for row in reader:
            # Check if this row matches our city
            if row['City'] == city_name:
                # Extract year-month from date (format: 1849-01-01 -> 1849-01)
                date_str = row['dt']
                year_month = date_str[:7] # Take first 7 characters (YYYY-MM)

                temp_str = row['AverageTemperature']
                # Get temperature, handle missing values
                if temp_str and temp_str.strip():
                    try: # Check if not empty
                        temperature = round(float(temp_str),3)
                        temperature_data[year_month] = temperature
                    except ValueError: #Skip Rows with no data
                        continue

    extremetemps['hottest'] = {
        'date': max(temperature_data, key=temperature_data.get),
        'temperature': temperature_data[max(temperature_data, key=temperature_data.get)]    
    }

    extremetemps['coldest'] = {
        'date': min(temperature_data, key=temperature_data.get),
        'temperature': temperature_data[min(temperature_data, key=temperature_data.get)]
    }


    return extremetemps



def get_seasonal_averages(filename, city_name, season):
    """
    Calculate average temperature for a specific season across all years.
    Never mind that Chennai only has Hot, Hotter and Hottest...
    
    Parameters:
    filename (str): Path to the CSV file
    city_name (str): Name of the city
    season (str): 'spring', 'summer', 'fall', or 'winter'
    
    Returns:
    dict: {
        'city': str,
        'season': str,
        'average_temperature': float
    }
        
    Assume: Spring = Mar,Apr,May; Summer = Jun,Jul,Aug; 
          Fall = Sep,Oct,Nov; Winter = Dec,Jan,Feb
    """
    # TODO: Your implementation here

    #Assigning month indexes for the appropriate months
    season_dict ={'spring' : ['03','04','05'], 'summer' : ['06','07','08'], 'fall' : ['09','10','11'], 'winter' : ['12','01','02']}

    count = 0

    Season_temps =[]
    with open(filename, 'r', encoding = 'utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            # Check if this row matches our city
            if row['City'] == city_name:
                date_str = row['dt']
                month = date_str[5:7] #Taking the month index

                if month in season_dict[season]: #Checking if the month belongs to that particular season
                    temp_str = row['AverageTemperature']
                    if temp_str and temp_str.strip():
                        try:
                            temperature = round(float(temp_str),3) #Rounding to 3 decimals
                            Season_temps.append(temperature)
                        except ValueError:
                            continue
    
    #Average Temperature calculation
    average_temperature = sum(Season_temps)/len(Season_temps)
    dict = {
        'city': city_name,
        'season': season,
        'average_temperature': average_temperature
    }

    return dict



def compare_decades(filename, city_name, decade1, decade2):
    """
    Compare average temperatures between two decades for a city.
    
    Parameters:
    filename (str): Path to the CSV file
    city_name (str): Name of the city
    decade1 (int): First decade (e.g., 1980 for 1980s)
    decade2 (int): Second decade (e.g., 2000 for 2000s)
    
    Returns:
    dict: {
        'city': str,
        'decade1': {'period': '1980s', 'avg_temp': float, 'data_points': int},
        'decade2': {'period': '2000s', 'avg_temp': float, 'data_points': int},
        'difference': float,
        'trend': str  # 'warming', 'cooling', or 'stable'
    }
    
    """
    # TODO: Your implementation here
    with open(filename,'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        #Creating lists for storing the temperature values of the particular decades
        decade1_temps = []
        decade2_temps = []

        for row in reader:
            if row['City'] == city_name:
                date_str = row['dt']
                decade = int(date_str[:3]) #Extract the first 3 digits of the year to comapre with

                #First 3 digits of the year of both decade1 and decade2
                decade1_yr = decade1//10 
                decade2_yr = decade2//10

                if decade1_yr == decade:
                    temp_str = row['AverageTemperature']
                    if temp_str and temp_str.strip():
                        try:
                            temperature = round(float(temp_str),3) #Round to 3 decimals
                            decade1_temps.append(temperature)
                        except ValueError:
                            continue
                
                if decade2_yr == decade:
                    temp_str = row['AverageTemperature']
                    if temp_str and temp_str.strip():
                        try:
                            temperature = round(float(temp_str),3) #Round to 3 decimals
                            decade2_temps.append(temperature)
                        except ValueError:
                            continue

        
    #Average Temperature calculation
    average_temperature_1 = sum(decade1_temps)/len(decade1_temps)
    average_temperature_2 = sum(decade2_temps)/len(decade2_temps)

    #period in string
    period_1 = str(decade1) + 's'
    period_2 = str(decade2) + 's'

    #difference
    difference = abs(average_temperature_1-average_temperature_2)

    #trend 
    if average_temperature_1 < average_temperature_2:
        trend = 'warming'
    elif average_temperature_1 > average_temperature_2:
        trend = 'cooling'
    else:
        average_temperature_2 == average_temperature_1
        trend = 'stable'
    dict = {
        'city': city_name,
        'decade1': {'period': period_1, 'avg_temp': average_temperature_1, 'data_points': len(decade1_temps)},
        'decade2': {'period': period_2, 'avg_temp': average_temperature_2, 'data_points': len(decade2_temps)},
        'difference': difference,
        'trend': trend
    }

    return dict




def find_similar_cities(filename, target_city, tolerance=2.0):
    """
    Find cities with similar average temperatures to the target city.
    
    Parameters:
    filename (str): Path to the CSV file
    target_city (str): Reference city name
    tolerance (float): Temperature difference threshold in °C
    
    Returns:
    dict: {
        'target_city': str,
        'target_avg_temp': float,
        'similar_cities': [
            {'city': str, 'country': str, 'avg_temp': float, 'difference': float}
        ],
        'tolerance': float
    }
    
    """
    # TODO: Your implementation here
    
    city_temps ={}

    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        sums, counts = {}, {}
        
        # Finding the average temperature for every city.
        for row in reader:
            city = row['City']
            temp_str = row['AverageTemperature']
            if temp_str and temp_str.strip():
                try:
                    t = round(float(temp_str),3)
                    sums[city] = sums.get(city, 0) + t #Count of no-none type temperature entries.
                    counts[city] = counts.get(city, 0) + 1
                except ValueError:
                    continue
    
    for c in sums:
        city_temps[c] = sums[c] / counts[c] #Average temperature for every city
    
    target_avg = city_temps.get(target_city)
    
    #Test passing if no target_avg
    if target_avg is None:
        return {
            'target_city': target_city,
            'target_avg_temp': None,
            'similar_cities': [],
            'tolerance': tolerance
        }
    
    similar = []
    #Creating a list of similar cities.
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            city = row['City']
            if city != target_city and city in city_temps:
                avg = city_temps[city]
                diff = abs(avg - target_avg)
                if diff <= tolerance:
                    k= ({
                        'city': city,
                        'country': row['Country'],
                        'avg_temp': round(avg, 2),
                        'difference': round(diff, 2)
                    })
                    #Avoiding duplicate similar city entries
                    if k not in similar:
                        similar.append(k)
    
    return {
        'target_city': target_city,
        'target_avg_temp': round(target_avg, 2),
        'similar_cities': similar,
        'tolerance': tolerance
    }



def get_temperature_trends(filename, city_name, window_size=5):
    """
    Calculate temperature trends using moving averages and identify patterns.
    
    Parameters:
    filename (str): Path to the CSV file
    city_name (str): Name of the city
    window_size (int): Number of years for moving average calculation
    
    Returns:
    dict: {
        'city': str,
        'raw_annual_data': {'YYYY': float},  # Annual averages
        'moving_averages': {'YYYY': float},  # Moving averages
        'trend_analysis': {
            'overall_slope': float,  # °C per year
            'warming_periods': [{'start': year, 'end': year, 'rate': float}],
            'cooling_periods': [{'start': year, 'end': year, 'rate': float}]
        }
    }
    
    """
    # TODO: Your implementation here
    with open(filename, 'r', encoding= 'utf-8') as file:
        reader = csv.DictReader(file)
        temp_yearly_average = {}
        temp_moving_average = {}

        for row in reader:
            if row['City'] == city_name:
                yr = int(row['dt'][:4])
                temp_str = row['AverageTemperature']
                if temp_str and temp_str.strip():
                    try:
                        temp = round(float(temp_str),3)
                        temp_yearly_average[yr] = temp_yearly_average.get(yr,0) + temp #Computing sum of all temperatures
                    except ValueError:
                        continue
        
        #Annual Average
        for i in temp_yearly_average:
            temp_yearly_average[i] = round(temp_yearly_average[i]/12,3)

        #Moving Averages
        k = sorted(list(temp_yearly_average.items())) #Creating a list of tuples for the yearly average dictionary
        for i in range(window_size-1,len(k)):
            k_sum = 0
            for j in range(i-(window_size-1),i+1):
                k_sum = k_sum + k[j][1]
            temp_moving_average[k[i][0]] = round((k_sum/window_size),3)

        q = sorted(list(temp_moving_average.items())) #Creating a list of tuples for the moving average dictionary
        overall_slope = round(((q[-1][1] - q[0][1])/(len(q)-1)),3) #Overall slope

        # Finding the trend in the dataset
        f = detect_warming_cooling_slopes(temp_moving_average)
        
    dict = {
        'city': city_name,
        'raw_annual_data': temp_yearly_average,  # Annual averages
        'moving_averages': temp_moving_average,  # Moving averages
        'trend_analysis': {
            'overall_slope': overall_slope,  # °C per year
            'warming_periods': f['warming'],
            'cooling_periods': f['cooling']
        }
    }

    return dict



def detect_warming_cooling_slopes(moving_averages):
    """
    Calculates the warming and cooling periods

    Parameters:
    moving_averages (dictionary): The dictionary to analyze the trend


    Returns:
    {'warming_periods': [{'start': year, 'end': year, 'rate': float}],
    'cooling_periods': [{'start': year, 'end': year, 'rate': float}]}
    """
    years = sorted(moving_averages.keys())
    years_int = [int(y) for y in years]
    temps = [moving_averages[y] for y in years]

    results = {"warming": [], "cooling": []}
    
    start_idx = 0
    direction = None  # 'warming' or 'cooling'
    
    for i in range(1, len(years)):
        if temps[i] > temps[i-1]:
            new_dir = "warming"
        elif temps[i] < temps[i-1]:
            new_dir = "cooling"
        else:
            continue  # flat, skip

        if direction is None:
            direction = new_dir
        
        # If direction flips, close old segment
        if new_dir != direction:
            slope = (temps[i-1] - temps[start_idx]) / (years_int[i-1] - years_int[start_idx])
            results[direction].append({
                "start": years[start_idx],
                "end": years[i-1],
                "rate": round(slope, 4)
            })
            start_idx = i-1
            direction = new_dir

    # close final run
    if direction:
        slope = (temps[-1] - temps[start_idx]) / (years_int[-1] - years_int[start_idx])
        results[direction].append({
            "start": years[start_idx],
            "end": years[-1],
            "rate": round(slope, 4)
        })
    
    return results


# =============================================================================
# TESTING CODE 
# =============================================================================

def test_api_functions():
    """
    Test all API functions with sample data.
    """
    filename = 'GlobalLandTemperaturesByMajorCity.csv'
    test_city = 'Madras'
    
    print("Testing Temperature Data API")
    print("=" * 40)
    
    # Test basic function
    temps = get_city_temperatures(filename, test_city)
    print(f"Basic function: Found {len(temps)} temperature records")
    
    # Test extremes
    extremes = find_temperature_extremes(filename, test_city)
    print(f"Extremes: Hottest = {extremes['hottest']['temperature']}°C")
    
    # Test seasonal averages
    summer_avg = get_seasonal_averages(filename, test_city, 'summer')
    print(f"Seasonal: Summer average = {summer_avg['average_temperature']:.1f}°C")
    
    # Test decade comparison
    comparison = compare_decades(filename, test_city, 1980, 2000)
    print(f"Decades: Temperature change = {comparison['difference']:.2f}°C")
    
    # Test similar cities
    similar = find_similar_cities(filename, test_city, tolerance=3.0)
    print(f"Similar cities: Found {len(similar['similar_cities'])} matches")
    
    # Test trends
    trends = get_temperature_trends(filename, test_city)
    print(f"Trends: Overall slope = {trends['trend_analysis']['overall_slope']:.4f}°C/year")


if __name__ == "__main__":
    test_api_functions()