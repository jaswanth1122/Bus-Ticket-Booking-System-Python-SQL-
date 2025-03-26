import sqlite3

# Function to create the database and tables
def initialize_db():
    conn = sqlite3.connect("bus_ticket.db")
    cursor = conn.cursor()

    # Create bus table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bus (
            seat_number INTEGER PRIMARY KEY,
            booked INTEGER DEFAULT 0,
            passenger_name TEXT DEFAULT NULL
        )
    ''')

    # Insert 10 seats if the table is empty
    cursor.execute("SELECT COUNT(*) FROM bus")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO bus (seat_number) VALUES (?)", [(i,) for i in range(1, 11)])

    conn.commit()
    conn.close()

# Function to display available seats
def view_available_seats():
    conn = sqlite3.connect("bus_ticket.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bus WHERE booked=0")
    seats = cursor.fetchall()

    if seats:
        print("\nAvailable Seats:")
        for seat in seats:
            print(f"Seat {seat[0]} - Available")
    else:
        print("\nNo seats available.")
    
    conn.close()

# Function to book a seat
def book_seat():
    seat_number = int(input("\nEnter seat number to book (1-10): "))

    conn = sqlite3.connect("bus_ticket.db")
    cursor = conn.cursor()

    cursor.execute("SELECT booked FROM bus WHERE seat_number=?", (seat_number,))
    result = cursor.fetchone()

    if result and result[0] == 0:
        passenger_name = input("Enter your name: ")
        cursor.execute("UPDATE bus SET booked=1, passenger_name=? WHERE seat_number=?", (passenger_name, seat_number))
        conn.commit()
        print(f"\n✅ Seat {seat_number} booked successfully for {passenger_name}!")
    else:
        print("\n❌ Seat is already booked or does not exist.")

    conn.close()

# Function to view booked seats
def view_booked_seats():
    conn = sqlite3.connect("bus_ticket.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bus WHERE booked=1")
    seats = cursor.fetchall()

    if seats:
        print("\nYour Booked Seats:")
        for seat in seats:
            print(f"Seat {seat[0]} - Booked by {seat[2]}")
    else:
        print("\nNo seats booked yet.")

    conn.close()

# Function to cancel a booking
def cancel_seat():
    seat_number = int(input("\nEnter seat number to cancel: "))

    conn = sqlite3.connect("bus_ticket.db")
    cursor = conn.cursor()

    cursor.execute("SELECT booked FROM bus WHERE seat_number=?", (seat_number,))
    result = cursor.fetchone()

    if result and result[0] == 1:
        cursor.execute("UPDATE bus SET booked=0, passenger_name=NULL WHERE seat_number=?", (seat_number,))
        conn.commit()
        print(f"\n✅ Seat {seat_number} booking cancelled successfully!")
    else:
        print("\n❌ Seat is not booked or does not exist.")

    conn.close()

# Main menu function
def main():
    initialize_db()

    while True:
        print("\n🎟️ Bus Ticket Booking System 🎟️")
        print("1️⃣ View Available Seats")
        print("2️⃣ Book a Seat")
        print("3️⃣ View Your Booked Seats")
        print("4️⃣ Cancel a Booking")
        print("5️⃣ Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            view_available_seats()
        elif choice == "2":
            book_seat()
        elif choice == "3":
            view_booked_seats()
        elif choice == "4":
            cancel_seat()
        elif choice == "5":
            print("\nThank you for using the Bus Ticket Booking System! 🚍")
            break
        else:
            print("\n❌ Invalid choice. Please try again.")

# Run the program
if __name__ == "__main__":
    main()
