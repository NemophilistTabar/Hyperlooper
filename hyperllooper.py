import os
import json
from typing import TextIO

# variables
user_booking = 0
double_check = "y"

# dictionary data
FILE_NAME = "seats.json"



# Save seat data to file
def save_seat_data(trip):
    with open(FILE_NAME, "w", encoding="utf-8") as file:  # type: TextIO
        json.dump(trip, file, indent=4)
    print(f"Changes saved to {FILE_NAME}")


# Ensure seats.json exists
def ensure_seat_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump({"seats": ["available"] * 16, "num_seats": 16}, file, indent=4)
        print(f"Created {FILE_NAME}")

# Loads / creates data dictionary
def load_seat_data():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)  # Load data from file
    else:
        return {"seats": ["available"] * 16, "num_seats": 16}  # Default

# Load seat data into trip info

trip_info = load_seat_data()

def available_seats(trip):

    seats = trip["seats"]  # A list of seat statuses ("available" or "occupied")
    num_seats = trip["num_seats"]  # Total number of seats
    assert len(seats) == num_seats, f"Expected {num_seats} seats, but got {len(seats)}"

    # count seats available
    count = sum(1 for seat in seats if seat.lower() == "available")

    return count


user_goal = input("would you like to book a trip? Y/N: ")  # judge the intent of user

if user_goal in ["Y", "y"]:

    while double_check in ["y", "Y"]:  # Outer loop to handle multiple attempts

        print("We have:", available_seats(trip_info), "seats available")  # Inform user

        while True:  # Inner loop to keep asking for a seat until confirmed
            user_booking = input("What seat would you like? ")

            try:
                user_booking = int(user_booking)

                if 1 <= user_booking <= 16:
                    print(f"You would like to book seat {user_booking}?")
                    double_check = input("Confirm (Y/N): ").strip().lower()

                    if double_check == "y":
                        double_check = "n"  # Force exit from outer loop
                        seat_index = user_booking - 1

                        if trip_info["seats"][seat_index] == "available":
                            trip_info["seats"][seat_index] = "occupied"
                            print(f"Seat {user_booking} booked successfully!")
                            save_seat_data(trip_info)
                            break  # Exit inner loop

                        else: print(f"Seat {user_booking} is unavailable. Please try again.")

                        break

                    elif double_check == "n":
                        print("Booking canceled. Choose another seat.")  # Loops back to seat selection

                    else:
                        print("Invalid input. Please enter Y or N.")

                else:
                    print("Invalid seat! Choose a number between 1 and 16.")

            except ValueError:
                print("Invalid input! Please enter a number.")



elif user_goal in ["N", "n"]:

    print("Then what the hell are you doing here?")  # roots out the idiots

# allows administrator reset
elif user_goal in ["admin", "Admin"]:
    trip_info["seats"] = ["available"] * trip_info["num_seats"]
    save_seat_data(trip_info)  # Save the reset data
    print("Seats Reset")
