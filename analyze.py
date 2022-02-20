import json
import re
import requests

models_path = "models_data_back.json"
Google_API_key = "Your API key here"

def fe(v):
  if v < 0:
    return 0
  elif v < 20:
    return v+5
  elif v < 25:
    return 0.6*v+13
  elif v < 50:
    return 0.08*v+26
  elif v < 60:
    return -0.2*v+40
  return max(0, -v/3 + 48)

def fuel_econ(f_city, f_hwy, v):
  if f_city > f_hwy:
    if v < 0:
      return 0
    elif v < 25:
      return 0.25*(v-25)+f_city
    elif v < 50:
      return v*(f_hwy-f_city)/25+f_hwy
    return -0.14*(v-50)+f_hwy
  else:
    return (f_hwy/55)*(fe(v) - 5) + 5

def remove_html(s):
  s = re.sub("[\<].*?[\>]", "", s)
  # s = s.replace("</br>", "\n").replace("<div>", "\n").replace("</wbr>", "\n")
  # out = ""
  # skipping = False
  # for c in s:
  #   if ((not skipping) and (c == '<')) or ((c == '>') and skipping):
  #     skipping = not skipping
  #   elif not skipping:
  #     out += c
  return s.replace("Destination", ". Destination")

def analyze(start, dest, car_id):
  payload = {}
  headers = {}
  url = f"https://maps.googleapis.com/maps/api/directions/json?origin={start}&destination={dest}&departure_time=now&alternatives=true&key=" + Google_API_key
  response = requests.request("GET", url, headers=headers, data=payload)
  
  with open(models_path, 'r') as f:
    car_info = json.load(f)

  city_econ = float(car_info[car_id]["mpg_city"])
  hwy_econ = float(car_info[car_id]["mpg_highway"])
  co2_rate = float(car_info[car_id]["co2"])

  routes = response.json()["routes"]
  route_gas = [0 for x in range(len(routes))]
  instructions = [[] for x in range(len(routes))]

  for x, route in enumerate(routes):
    steps = route["legs"][0]["steps"]

    for i in steps:
      instructions.append(remove_html(i["html_instructions"]))
      start_lat = i["start_location"]["lat"]
      start_lng = i["start_location"]["lng"]
      end_lat = i["end_location"]["lat"]
      end_lng = i["end_location"]["lng"]
      url = f"https://maps.googleapis.com/maps/api/directions/json?origin={start_lat},{start_lng}&destination={end_lat},{end_lng}&departure_time=now&key=" + Google_API_key
      
      payload = {}
      headers = {}

      if (len(routes))*10 < 30:
        step_data = requests.request("GET", url, headers=headers, data=payload).json()["routes"][0]["legs"][0]
        distance = step_data["distance"]["value"] / 1609.344 # m -> mi
        time = step_data["duration_in_traffic"]["value"] / 3600 # s -> h
      else:
        distance = i["distance"]["value"] / 1609.344 # m -> mi
        time = i["duration"]["value"] / 3600
      speed = distance / time # mph
      route_gas[x] += distance / fuel_econ(city_econ, hwy_econ, speed) * 3.785411784 # gal -> L

  route_co2 = [0.264172 * (city_econ + hwy_econ)/2 * co2_rate * x / 1000 for x in route_gas]

  out_dict = {}
  
  for i, V in enumerate(route_gas):
    out_dict[str(i+1)] = {}
    out_dict[str(i+1)]["fuel_type"] = car_info[car_id]["fuel_type"]
    out_dict[str(i+1)]["fuel"] = round(V, 3)
    out_dict[str(i+1)]["instructions"] = instructions

  for i, m in enumerate(route_co2):
    out_dict[str(i+1)]["CO2"] = round(m,3)
  
  # print(out_dict)
  return format_analyze(out_dict)


def format_analyze(out_dict):

  fuel_legend = {"gasoline": "calculated via MPG",
                 "diesel": "calculated via MPG",
                 "electric": "calculated gasoline equivalent MPG",
                 "cng": "calculated gasoline equivalent MPG",
                 "hybrid": "calculated as average MPGe",
                 "pi-hybrid": "calculated as average MPGe"}      

  while True:

    for cnt in range(1, len(out_dict)+1):
      print("   Route", str(cnt))
      print("   - Predicted Fuel Consumption:", out_dict[str(cnt)]['fuel'], "L")
      print("                                 " + fuel_legend[out_dict[str(cnt)]['fuel_type']])
      print("   - Predicted Tailpipe CO2 Emission:", out_dict[str(cnt)]['CO2'], "kg")
      print("")

    opt = input("   CHOOSE ONE ROUTE NUMBER TO SEE THE DETAILS\n   > ")

    if int(opt) < 1 or int(opt) > len(out_dict):
      print("   Invalid input. Please try again.")
      continue
    
    for i in out_dict[opt]['instructions']:
      if i:
        print("  ", i)
    if input("\n   Return? (y/n)\n   ") == "y".casefold():
      continue
    else:
      break
