## Multi-Day Trip Planner: A Lightweight TSP-Based Tool ✈️✈️✈️

Hi there👋! This is a lightweight package helps you plan **a multi-day trip** using standard [TSP](https://en.wikipedia.org/wiki/Travelling_salesman_problem) techniques. 
### Getting started
1. **Obtain an API key**
   
- To get started, you'll need an API key of OpenRouteService. This key will allow you to access the spherical coordinates of your destinations.
Check out [their website](https://openrouteservice.org/dev/#/api-docs/v2/directions/%7Bprofile%7D/get) and click ''API Key'' at the top right Zone of **User Security**. The process should be fast and easy!

2. **Edit places.tx**

  - Update the places.txt file file to include your planned destinations.
  - The first line should be the name of your hotel.
  - Every line afterward should be your place of interest. The order can be random.
  - We recomment all inputs to be formatted as `Name, city, country`. Here is an example: 

```
Andaz Tokyo Toranomon Hill, Minato City, Tokyo, Japan
Akihabara, Taito City, Tokyo
Ginza, Tokyo
....
```
3. **Install dependencies**
- Run the following command to install the required packages: 
```
pip install -r requirements.txt
```
4. **Run the tool**
After editing the `places.txt` file, use the following command to plan your trip: 
```
python main.py --api_key {YOUR_API_KEY} --place_names places.txt --max_distance_per_day {MAXIMUM_DISTANCE_PER_DAY} --penalty {PLACE_PENALTY} --num_days {TRAVEL_DAYS}
```
Parameter Details:

- `YOUR_API_KEY` is the OpenRouteService API key you obtained
- `MAXIMUM_DISTANCE_PER_DAY` is the maximum distance you want to travel per day
-  `TRAVEL_DAYS` is the number of days for traveling.
- A larger `PLACE_PENALTY` decreases the number of places you visit every day -- feel free to adjust this value for your preferences!

### Example workflow

```
python main.py --api_key abc123 --place_names places.txt --max_distance_per_day 50 --penalty 10 --num_days 3
```

### Note

- Make sure to double-check your `places.txt` format for errors!
- Experiment with the `PLACE_PENALTY` value to balance your daily plans.

---

## Bon Voyage🛫🛫🛫! 

