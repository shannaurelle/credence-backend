
import os
import django
import random
import math
from datetime import date, timedelta, time

# ==========================================
# CONFIGURE DJANGO
# ==========================================

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'credencev2.settings'
)
django.setup()

# ==========================================
# IMPORT MODELS
# ==========================================

from credencev2_1.models import (
    UserAccount,
    DistanceTravelled
)

# ==========================================
# CONFIGURATION
# ==========================================

USER_ACCOUNT_ID = 3
VEHICLE_TYPE = "motorcycle"

DAYS = 30
MIN_TRIPS = 1
MAX_TRIPS = 4

# ==========================================
# EASTERN VISAYAS LOCATIONS
# ==========================================

LOCATIONS = [
    # LEYTE
    (11.2433, 125.0047),  # Tacloban City
    (10.7430, 124.7960),  # Ormoc City
    (10.6780, 124.8000),  # Baybay City
    (11.1860, 124.5630),  # Carigara
    (11.3290, 124.8490),  # Palo
    (11.0560, 124.6070),  # Alangalang
    (11.0400, 124.8850),  # Tanauan
    (10.8750, 124.8810),  # Abuyog

    # SOUTHERN LEYTE
    (10.3940, 125.1700),  # Maasin City
    (10.2820, 124.9980),  # Sogod
    (10.3200, 125.0800),  # Bontoc
    (10.1250, 125.0000),  # Padre Burgos

    # SAMAR
    (11.7750, 125.0060),  # Catbalogan City
    (11.7780, 124.8870),  # Calbayog City
    (11.5600, 125.0000),  # Basey
    (11.6000, 125.2000),  # Jiabong
    (11.8000, 125.0000),  # Gandara

    # NORTHERN SAMAR
    (12.2700, 125.0000),  # Catarman
    (12.3400, 124.6500),  # Laoang
    (12.5000, 124.6000),  # San Roque
    (12.1500, 124.6000),  # Bobon

    # EASTERN SAMAR
    (11.7780, 125.4400),  # Borongan City
    (11.2000, 125.4000),  # Guiuan
    (11.5000, 125.3000),  # Llorente
    (11.8500, 125.5000),  # Maydolong
]

# ==========================================
# HAVERSINE DISTANCE CALCULATION
# ==========================================

def calculate_distance(lat1, lon1, lat2, lon2):

    EARTH_RADIUS = 6371

    lat1, lon1, lat2, lon2 = map(
        math.radians,
        [lat1, lon1, lat2, lon2]
    )

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return round(EARTH_RADIUS * c, 2)


# ==========================================
# GENERATE RANDOM DESTINATION
# ==========================================

def generate_destination(start_lat, start_lon):

    while True:

        end_lat = round(
            start_lat + random.uniform(-0.015, 0.015),
            6
        )

        end_lon = round(
            start_lon + random.uniform(-0.015, 0.015),
            6
        )

        distance = calculate_distance(
            start_lat,
            start_lon,
            end_lat,
            end_lon
        )

        if 0.5 <= distance <= 5.0:
            return end_lat, end_lon, distance


# ==========================================
# SEED DISTANCE TRAVELLED
# ==========================================

def seed_distance_travelled():

    # IMPORTANT:
    # UserAccount uses user_id as its primary key.
    try:
        user_account = UserAccount.objects.get(
            user_id=USER_ACCOUNT_ID
        )

    except UserAccount.DoesNotExist:
        print(
            f"UserAccount with user_id {USER_ACCOUNT_ID} does not exist."
        )
        return

    records = []

    today = date.today()

    print("Generating Eastern Visayas travel records...")

    # Generate records for the last 30 days
    for day_offset in range(DAYS - 1, -1, -1):

        travel_date = today - timedelta(days=day_offset)

        # Random number of trips per day
        trips = random.randint(
            MIN_TRIPS,
            MAX_TRIPS
        )

        for _ in range(trips):

            # Select a starting location
            start_lat, start_lon = random.choice(LOCATIONS)

            start_lat = round(start_lat, 6)
            start_lon = round(start_lon, 6)

            # Generate nearby destination
            end_lat, end_lon, distance = generate_destination(
                start_lat,
                start_lon
            )

            # Generate travel time
            travel_time = time(
                hour=random.randint(6, 21),
                minute=random.randint(0, 59),
                second=random.randint(0, 59)
            )

            # Create travel record
            record = DistanceTravelled(
                user_account=user_account,
                t_date=travel_date,
                t_time=travel_time,
                start_latitude=start_lat,
                start_longitude=start_lon,
                end_latitude=end_lat,
                end_longitude=end_lon,
                km=distance,
                vehicle_type=VEHICLE_TYPE
            )

            records.append(record)

    # Insert records into database
    DistanceTravelled.objects.bulk_create(records)

    # ==========================================
    # DISPLAY SUMMARY
    # ==========================================

    total_km = sum(record.km for record in records)

    print("\n========== SEEDING COMPLETE ==========")
    print(f"User Account ID : {USER_ACCOUNT_ID}")
    print(f"Vehicle Type    : {VEHICLE_TYPE}")
    print(f"Total Records   : {len(records)}")
    print(f"Total Distance  : {total_km:.2f} km")
    print(
        f"Average Trip    : {total_km / len(records):.2f} km"
        if records else "Average Trip    : 0 km"
    )
    print(f"Date From       : {today - timedelta(days=DAYS - 1)}")
    print(f"Date To         : {today}")
    print("======================================")


# ==========================================
# EXECUTE SEEDER
# ==========================================

if __name__ == "__main__":
    seed_distance_travelled()
