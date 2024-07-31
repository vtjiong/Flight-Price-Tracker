#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import data_manager
import flight_search
from datetime import datetime, timedelta
from flight_data import find_cheapest_flight
import notification_manager
notification_manager=notification_manager.NotificationManager()
origin = "LON"
data_manager=data_manager.DataManager()
flight_search=flight_search.FlightSearch()

# Taking customers data
customer_data=data_manager.get_customers_emails()
customer_emails=[row["whatIsYourEmail ?"] for row in customer_data]

for x in range(len(data_manager.city)):
    iata_data = flight_search.get_iata_data(data_manager.city[x])
    data_manager.put_iata_data(data_manager.city[x],iata_data)
tomorrow=datetime.today()+timedelta(days=1)
six_month=datetime.today()+timedelta(days=180)

for destination in data_manager.price_response["prices"]:
    print(f"Getting direct flights for {destination['city']}...")
    flights=flight_search.check_flight(destination['iataCode'],tomorrow,six_month)
    cheapest_flight = find_cheapest_flight(flights)
    if cheapest_flight.price == 'N/A':
        print(f"Getting Indirect flights for {destination['city']}...")
        flights = flight_search.check_flight(destination['iataCode'],tomorrow,six_month, "LON",False)
        cheapest_flight = find_cheapest_flight(flights)
    if cheapest_flight.price != "N/A" and float(cheapest_flight.price) < float(destination['lowestPrice']) :
        for x in customer_emails:
            notification_manager.send_email(x,cheapest_flight.stops,cheapest_flight.price,"LON",cheapest_flight.destination_airport,cheapest_flight.departure_date,cheapest_flight.return_date)