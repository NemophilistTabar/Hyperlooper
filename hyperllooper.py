import os
import json


# Dictionary data
FILE_NAMES = {
    "1": "trip1_seats.json",
    "2": "trip2_seats.json",
    "3": "trip3_seats.json"
}

# Allows for dynamic saving of data to relevant trip json
def save_seat_data(trip, trip_num):
    file_name = FILE_NAMES[trip_num]
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(trip, file, indent=4)
    print(f"Changes saved to {file_name}")

# Creates the required json files
def load_seat_data(trip_num):
    file_name = FILE_NAMES[trip_num]
    if os.path.exists(file_name):
        if os.stat(file_name).st_size == 0:
            print("Warning: JSON file is empty. Creating default seats.")
            return {"seats": ["available"] * 16, "num_seats": 16}
        try:
            with open(file_name, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Error: JSON file is corrupted. Resetting to default.")
    return {"seats": ["available"] * 16, "num_seats": 16}  # Default

# Count available seats
def available_seats(trip):
    return sum(1 for seat in trip["seats"] if seat.lower() == "available")

# Assess user intent
user_goal = input("Would you like to book a trip? Y/N: ").strip().lower()

if user_goal == "y":
    user_trip = input("What trip would you like to book? 1, 2, 3? ").strip()

    if user_trip in FILE_NAMES:
        trip_info = load_seat_data(user_trip)

        while True:
            print("We have:", available_seats(trip_info), "seats available")

            try:
                user_booking = int(input("What seat would you like? "))

                # makes sure user input is a valid seat
                if 1 <= user_booking <= 16:
                    seat_index = user_booking - 1

                    # if the seat is available assign that seat to the user
                    if trip_info["seats"][seat_index] == "available":
                        user_name = input("What is your name? ")
                        trip_info["seats"][seat_index] = user_name
                        print(f"Seat {user_booking} booked successfully!")
                        save_seat_data(trip_info, user_trip)
                        break

                    else:
                        print(f"Seat {user_booking} is unavailable. Please try again.")

                else:
                    # revert if seat does not exist
                    print("Invalid seat! Choose a number between 1 and 16.")

            except ValueError:
                # revert if user does not name a seat
                print("Invalid input! Please enter a number.")

# root out dull users
elif user_goal == "n":
    print("Then what the hell are you doing here?")

# Allows the administrator to reset and print the data
elif user_goal == "admin":
    admin_intent = input("Do you want to reset or print seats? ").strip().lower()
    admin_trip = input("Which trip? 1, 2, or 3? ").strip()

    if admin_trip in FILE_NAMES:
        trip_info = load_seat_data(admin_trip)

        # Reset data
        if admin_intent == "reset":
            trip_info["seats"] = ["available"] * trip_info["num_seats"]
            save_seat_data(trip_info, admin_trip)
            print("Seats Reset")

        # Print data
        elif admin_intent == "print":
            print(trip_info)
