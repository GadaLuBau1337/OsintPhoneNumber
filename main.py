import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import pyfiglet
import folium
import googlemaps

# Replace 'YOUR_API_KEY' with your actual Google Maps API key
gmaps = googlemaps.Client(key='YOUR_API_KEY')

def get_number_info(phone_number):
    parsed_number = phonenumbers.parse(phone_number, "ID")
    country = geocoder.description_for_number(parsed_number, "en")
    provider = carrier.name_for_number(parsed_number, "en")
    time_zone = timezone.time_zones_for_number(parsed_number)

    # Get location information using Google Maps API
    geocode_result = gmaps.geocode(country)
    location = geocode_result[0]['geometry']['location'] if geocode_result else None

    return {
        "Country": country,
        "Provider": provider,
        "Time Zone": time_zone,
        "Location": location
    }

def create_map(location):
    if location:
        latitude = location['lat']
        longitude = location['lng']
        map_location = folium.Map(location=[latitude, longitude], zoom_start=12)
        folium.Marker([latitude, longitude]).add_to(map_location)
        return map_location._repr_html_()
    else:
        return "Location not found"

def main():
    print(pyfiglet.figlet_format("OSINT Phone"))
    phone_number = input("Enter phone number (e.g. +628123456789): ")
    number_info = get_number_info(phone_number)

    print("\nPhone Number Information:")
    for key, value in number_info.items():
        if key == "Location":
            map_html = create_map(value)
            print(f"{key}: {map_html}")
        else:
            print(f"{key}: {value}")

if __name__ == "__main__":
    main()
