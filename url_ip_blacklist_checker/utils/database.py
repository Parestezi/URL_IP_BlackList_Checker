import sqlite3
from datetime import datetime
import validators
from utils.check import check_ip_status, check_url_status, check_url
from utils.extract import extract_domain_from_url, extract_scheme, is_url

# Function to create the database schema
def create_database(database_path):
    # Create a cursor using the database connection
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    # Create the database table using SQL query
    cursor.execute(
        # 1-> PRIMARY KEY = unique id value, AUTOINCREMENT = id automatically increments on a new record.
        # 2-3-4 -> NOT NULL = specifies that they cannot contain empty values, meaning domain_ip, first_scanned, and last_scanned must be filled.
        """CREATE TABLE IF NOT EXISTS url_ip_list (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              domain_ip TEXT NOT NULL,
              first_scanned DATE NOT NULL,
              last_scanned DATE NOT NULL,
              blacklist TEXT
            )"""
    )

    # Save the changes to the database (commit)
    connection.commit()
    # Close the connection
    connection.close()

# Function to insert or update data in the database
def insert_or_update_into_database(database_path, domain_ip, blacklist):
    # Create a database connection
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    try:
        # Get the current date and time
        now = datetime.now()
        current_date = now.strftime("%d.%m.%Y")

        # Check if the specified domain or IP address already exists in the database
        cursor.execute("""SELECT * FROM url_ip_list WHERE domain_ip=?""", (domain_ip,))
        # Fetch the data returned by the SQL query into existing_data
        existing_data = cursor.fetchone()

        # If the data already exists, update it
        if existing_data:
            cursor.execute(
                """UPDATE url_ip_list SET last_scanned=?, blacklist=? WHERE domain_ip=?""",
                (current_date, blacklist, domain_ip),
            )
        # If the data doesn't exist, insert a new record
        else:
            cursor.execute(
                """INSERT INTO url_ip_list (domain_ip, first_scanned, last_scanned, blacklist)
                  VALUES (?, ?, ?, ?)""",
                (domain_ip, current_date, current_date, blacklist),
            )

        # Save the changes to the database (commit)
        connection.commit()
    finally:
        # Close the connection
        connection.close()

# Asynchronous function to check and update the database
async def check_and_update_database(database_path):
    # Create a database connection
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    # Select all records where the "blacklist" column is set to "No"
    cursor.execute("""SELECT * FROM url_ip_list WHERE blacklist='No' """)
    # Fetch all rows returned by the query and store them in the rows list
    rows = cursor.fetchall()
    # List to store URLs with "Down" or "Redirection" status
    down_redirection_urls = []

    # Process each selected record
    for row in rows:
        # Get the URL or IP address from the second column of each record
        url_or_ip = row[1]

        # Remove the URL scheme (http:// or https://) from the URL
        scheme = extract_scheme(url_or_ip)
        if scheme:
            # Check the status of URLs with a scheme (by sending an HTTP request)
            status = check_url_status(url_or_ip)
        else:
            # Check the status of URLs without a scheme (by sending an HTTP request)
            status = check_ip_status(url_or_ip)

        # Add URLs with "Down" or "Redirection" status to the list
        if status == "Down" or status == "Redirection":
            down_redirection_urls.append(f"{url_or_ip}: {status}")
        # If the URL is an IP address, add it to the list
        elif validators.ipv4(url_or_ip) or validators.ipv6(url_or_ip):
            down_redirection_urls.append(f"{url_or_ip}: {status}")

        # If the URL is valid or a domain can be extracted, extract the domain
        if is_url(url_or_ip):
            domain = extract_domain_from_url(url_or_ip)
        else:
            domain = url_or_ip

        # Check the URL using the Google Safe Browsing API (asynchronous process)
        response = await check_url(url_or_ip)

        # If the URL is malicious (has "matches" data), update the database
        if response.status_code == 200 and response.json().get("matches"):
            print(f"{domain} marked as malicious!")
            cursor.execute(
                """UPDATE url_ip_list SET blacklist='Yes' WHERE domain_ip=?""",
                (url_or_ip,),
            )
        else:
            # If the URL is safe
            print(f"{domain} is safe. \n")

    # Save database changes
    connection.commit()

    if down_redirection_urls:
        # If the down_redirection_urls list is not empty
        with open("down_redirection_urls.txt", "w") as output_file:
            # Open a text file named "down_redirection_urls.txt" in write mode
            for url_info in down_redirection_urls:
                # Write each URL information from the down_redirection_urls list to the file
                output_file.write(url_info + "\n")
            # Display a message when the writing process is completed
            print("Down or redirection URLs saved in a new file.")

    # Close the connection
    connection.close()
