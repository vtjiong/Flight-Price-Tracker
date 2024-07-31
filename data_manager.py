import requests
from dotenv import load_dotenv
import os
load_dotenv()
price_end_point = os.environ["price_ep"]
users_end_point = os.environ["user_ep"]
class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.header={
            "Authorization": f"Bearer {os.environ["TOKEN"]} "
        }
        self.price_response = requests.get(price_end_point, headers=self.header).json()
        self.city = self.get_city()
        self.customer_data={}

    def get_customers_emails(self):
        response=requests.get(users_end_point,headers=self.header).json()
        self.customer_data=response['users']
        return self.customer_data
    def get_city(self):
        city=[]
        for x in self.price_response['prices']:
            city.append(x['city'])
        return city

    def put_iata_data(self,city,iatacode):
        response = self.price_response["prices"]
        for x in response:
            if x['city'] == city and x['iataCode'] == "":
                data = {
                    "price": {
                        "iataCode": f"{iatacode}"
                    }
                }
                endpoint=f"{price_end_point}/{str(x['id'])}"
                response=requests.put(endpoint, json=data, headers=self.header)
            else:
                pass

    def post_city(self,iataCode="",lowestPrice=""):
        user_input = input("Enter city name: ")
        if user_input in self.city:
            print("City already exists")
            while True:
                user_input = input("Enter city name: ")
                if user_input not in self.city:
                    break
        data = {
            'price':{
                'city': user_input.title(),
                'iataCode': iataCode,
                'lowestPrice': lowestPrice
            }
        }
        self.city.append(user_input.title())
        requests.post(price_end_point, json=data, headers=self.header)