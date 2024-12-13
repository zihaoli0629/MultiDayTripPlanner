## Multi-Day Trip Planner: A Lightweight TSP-Based Tool ✈️✈️✈️

Hi there👋! This is a lightweight package that helps you plan and visualize **a multi-day trip** using standard [TSP](https://en.wikipedia.org/wiki/Travelling_salesman_problem) techniques. 
### Getting started
1. **Obtain an API key**
   
- To get started, you'll need an API key of OpenRouteService. This key will allow you to access the spherical coordinates of your destinations.
Check out [their website](https://openrouteservice.org/dev/#/api-docs/v2/directions/%7Bprofile%7D/get) and click ''API Key'' at the top right corner of **User Security**. The process should be fast and easy!

2. **Edit places.txt**

  - Update the places.txt file to include your planned destinations.
  - The first line should be the name of your hotel.
  - Every line afterward should be your place of interest. The order can be random.
  - We recommend all inputs to be formatted as `Name, city, country`. Here is an example: 

```
Andaz Tokyo Toranomon Hill, Minato City, Tokyo, Japan
Akihabara, Taito City, Tokyo, Japan
Ginza, Tokyo, Japan
....
```
3. **Install dependencies**
- Run the following command to install the required packages: 
```
$ pip install -r requirements.txt
```
4. **Run the tool**
After editing the `places.txt` file, use the following command to plan your trip: 
```
$ python main.py --api_key {YOUR_API_KEY} --place_names places.txt --max_distance_per_day {MAXIMUM_DISTANCE_PER_DAY} ----max_place_number {MAXIMUM_PLACE_NUM} --num_days {TRAVEL_DAYS} --save_map {SAVE} --save_path {YOUR_PATH}
```
Parameter Details:

- `YOUR_API_KEY` is the OpenRouteService API key you obtained
- `MAXIMUM_DISTANCE_PER_DAY` is the maximum distance you want to travel per day
- `TRAVEL_DAYS` is the number of days for traveling
- `MAXIMUM_PLACE_NUM` is the maximum number of places you want to visit per day
- `SAVE` means whether to save the route map or not. Default True
- `YOUR_PATH` is your path for saving the map. Default "./plan"
### Example workflow

```
$ python main.py --api_key abc123 --place_names places.txt --max_distance_per_day 24 --max_place_number 2 --num_days 4  --save_path "./plan"
```

```
Day 1: Andaz Tokyo Toranomon Hill -> Andaz Tokyo Toranomon Hill
Total distance for day 1 is 0.00 km 

Day 2: Andaz Tokyo Toranomon Hill -> Tokyo national museum -> Sensoji Temple -> Andaz Tokyo Toranomon Hill
Total distance for day 2 is 23.88 km 

Day 3: Andaz Tokyo Toranomon Hill -> Imperial place -> Akihabara -> Andaz Tokyo Toranomon Hill
Total distance for day 3 is 20.29 km 

Day 4: Andaz Tokyo Toranomon Hill -> Meiji Jingu -> Ginza -> Andaz Tokyo Toranomon Hill
Total distance for day 4 is 17.14 km 

Day 1 has been saved to ./plan/day_1_route.html
Day 2 has been saved to ./plan/day_2_route.html
Day 3 has been saved to ./plan/day_3_route.html
Day 4 has been saved to ./plan/day_4_route.html
```

### Note

- Make sure to double-check your `places.txt` format for errors!
- If the program can not find a solution, you can either:
1. Be more energetic by tuning up the `max_distance_per_day` and `max_place_number` 🏃‍♀️🏃, or;
2. Shorten your list of places 🥱🥱
---

## Bon Voyage🛫🛫🛫! 

