class FlightData:
    def __init__(self,price,origin_airport,destination_airport,departure_date,return_date,stops):
        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.departure_date = departure_date
        self.return_date = return_date
        self.stops=stops

def find_cheapest_flight(data):
    if data == None:
        print("No flight data")
        return FlightData("N/A", "N/A", "N/A", "N/A", "N/A","N/A")
    first_flight = data['data'][0]
    origin = first_flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
    stops = len(first_flight['itineraries'][0]['segments']) - 1
    destination = first_flight["itineraries"][0]["segments"][stops]["arrival"]["iataCode"]
    departure_date = first_flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
    return_date = first_flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]
    cheapest_price=float(first_flight["price"]["grandTotal"])
    for x in data["data"]:
        if float(x["price"]["grandTotal"]) < cheapest_price:
            cheapest_price=float(x["price"]["grandTotal"])
            stops = len(x["itineraries"]["segments"]) - 1
            origin = x["itineraries"][0]["segments"][0]["departure"]["iataCode"]
            destination = x["itineraries"][0]["segments"][stops]["arrival"]["iataCode"]
            departure_date = x["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
            return_date = x["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]
    print(f"Lowest price to {destination} is £{cheapest_price}")
    return FlightData(cheapest_price,origin,destination,departure_date,return_date,stops)