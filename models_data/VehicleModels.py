import csv
import requests



for i in range(1978, 2024):
#for i in range(50, 51):

    if i%100 < 10:
        url = "https://www.fueleconomy.gov/feg/epadata/0" + str(i%100) + "data.zip"
    else:
        url = "https://www.fueleconomy.gov/feg/epadata/" + str(i%100) + "data.zip"

    print(url)
    r = requests.get(url)
    #if response.ok:
    open("./VehicleData/"+str(i)+"guide.zip", 'wb').write(r.content)
    #else:
    #print("ERROR" + i)