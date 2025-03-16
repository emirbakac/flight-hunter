import os
from dotenv import load_dotenv
import requests

load_dotenv()
FLIGHT_ENDPOINT = os.getenv("ENV_FLIGHT_ENDPOINT")
IATA_ENDPOINT = os.getenv("ENV_IATA_ENDPOINT")
TOKEN_ENDPOINT = os.getenv("ENV_TOKEN_ENDPOINT")

class FlightSearch:
    def __init__(self):
        self._api_key = os.getenv("ENV_AMADEUS_API_KEY")
        self._api_secret = os.getenv("ENV_AMADEUS_SECRET")
        self._token = self._get_new_token()

    def _get_new_token(self):

        header = {
            "Content-Type": 'application/x-www-form-urlencoded'
        }
        body = {
            "grant_type": "client_credentials",
            "client_id": self._api_key,
            "client_secret": self._api_secret,
        }
        response = requests.post(TOKEN_ENDPOINT, headers=header, data=body)
        response.raise_for_status()

        print(f"Your token is {response.json()['access_token']}")
        print(f"Your token expires in {response.json()['expires_in']} seconds.")
        return response.json()['access_token']

    def get_destination_code(self, city_name):
        headers = {"Authorization": f"Bearer {self._token}"}
        query = {
            "keyword": city_name,
            "max": 2,
            "include": "AIRPORTS"
        }
        response = requests.get(url=IATA_ENDPOINT, headers=headers, params=query)
        print(f"Status code: {response.status_code}. Airport IATA: {response.text}")

        try:
            code = response.json()["data"][0]['iataCode']
        except IndexError:
            print(f"IndexError: No airport code found for {city_name}.")
            return "N/A"
        except KeyError:
            print(f"KeyError: No airport code found for {city_name}.")
            return "Not Found"
        else:
            return code

    def search_flights(self, origin_city, destination_city, from_date, to_date):
        headers = {"Authorization": f"Bearer {self._token}"}
        query = {
            "originLocationCode": origin_city,
            "destinationLocationCode": destination_city,
            "departureDate": from_date.strftime("%Y-%m-%d"),
            "returnDate": to_date.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": 'true',
            "currencyCode": "USD",
            "max": 10
        }
        response = requests.get(url=FLIGHT_ENDPOINT, headers=headers, params=query)
        response.raise_for_status()

        return response.json()