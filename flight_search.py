import requests
from dotenv import load_dotenv
import os
load_dotenv()
iata_url = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
token_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
flight_url = "https://test.api.amadeus.com/v2/shopping/flight-offers"


class FlightSearch:
    def __init__(self):
        self.apikey = os.environ["AMADEUSKEY"]
        self.apiSecret = os.environ["AMADEUSSECRET"]
        self.token = f"Bearer {self.get_token()}"
        self.header = {
            'Authorization': self.token
        }
        self.stops = 0

    def get_token(self):
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = {
            'grant_type': 'client_credentials',
            'client_id': self.apikey,
            'client_secret': self.apiSecret
        }
        try:
            response = requests.post(url=token_url, headers=header, data=body)
            return response.json()['access_token']
        except:
            print("Something went wrong")

    def get_iata_data(self, city):
        params={
            'keyword':city.upper(),
            'max' : 2,
        }
        response = requests.get(url=iata_url, headers=self.header,params=params)
        try:
            code = response.json()["data"][0]['iataCode']
            return code
        except IndexError:
            print(f"IndexError: No airport code found for {city}.")
            return "N/A"
        except KeyError:
            print(f"KeyError: No airport code found for {city}.")
            return "Not Found"

    def check_flight(self,destination_city_code,fromtime,totime,origin_city_code="LON",is_direct=True):
            parameter={
                "originLocationCode":origin_city_code,
                "destinationLocationCode":destination_city_code,
                "departureDate":fromtime.strftime("%Y-%m-%d"),
                "returnDate":totime.strftime("%Y-%m-%d"),
                "nonStop":'true' if is_direct else 'false',
                "max":10,
                "adults":1,
                "currencyCode":"GBP"
            }
            response=requests.get(url=flight_url,headers=self.header,params=parameter)
            if response.status_code != 200 or response.json()['data']==[]:
                return None
            return response.json()