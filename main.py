import time
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
# from notification_manager import NotificationManager

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
# notification_manager = NotificationManager()

ORIGIN_CITY = "Istanbul"
ORIGIN_CITY_IATA = 'IST'

# ----------------------Update the Airport Codes in Google Sheet----------------------
'''
for row in sheet_data:
    if row["iataCode"] == "":
        row["iataCode"] = flight_search.get_destination_code(row["city"])
        # slowing down requests to avoid rate limit
        time.sleep(2)
print(f"sheet_data:\n {sheet_data}")

data_manager.destination_data = sheet_data
data_manager.update_destination_codes()
'''
# ----------------------Search for Flights----------------------

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

for destination in sheet_data:
    print(f"Getting flights for {ORIGIN_CITY} to {destination['city']}...")
    flights = flight_search.search_flights(
        origin_city=ORIGIN_CITY_IATA,
        destination_city=destination["iataCode"],
        from_date=tomorrow,
        to_date=six_month_from_today
    )
    cheapest_flight = find_cheapest_flight(flights)
    print(f"{destination['city']}: ${cheapest_flight.price}")
    # Slowing down requests to avoid rate limit
    time.sleep(2)

# ----------------------Search for Flights and Send Notifications----------------------
'''
for destination in sheet_data:
    print(f"Getting flights for {ORIGIN_CITY} to {destination['city']}...")
    flights = flight_search.search_flights(
        origin_city=ORIGIN_CITY_IATA,
        destination_city=destination["iataCode"],
        from_date=tomorrow,
        to_date=six_month_from_today
    )
    cheapest_flight = find_cheapest_flight(flights)
    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:
        print(f"Lower price flight found to {destination['city']}!")
        # notification_manager.send_sms(
        #     message_body=f"Low price alert! Only £{cheapest_flight.price} to fly "
        #                  f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
        #                  f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
        # )
        # Try whatsapp unless SMS is not working.
        notification_manager.send_whatsapp(
            message_body=f"Low price alert! Only £{cheapest_flight.price} to fly "
                         f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
                         f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
        )
'''