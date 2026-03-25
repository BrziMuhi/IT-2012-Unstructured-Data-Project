from io_utils import (
    setup_logging,
    read_json,
    read_text,
    read_csv,
)


if __name__ == "__main__":
    setup_logging("pipeline.log")

    destination_data = read_json("data/raw/destinations/destination_1.json")
    review_text = read_text("data/raw/reviews/review_1.txt")
    booking_rows = read_csv("data/raw/bookings/bookings.csv")
    
    if destination_data:
        print("Destination name:", destination_data["name"])
        print("Country:", destination_data["country"])
        print("Category:", destination_data["category"])

    if review_text:
        print("\nFirst 100 characters of review:")
        print(review_text[:100])

    if booking_rows:
        print("\nFirst booking row:")
        print(booking_rows[0])

  