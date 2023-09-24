from dotenv import load_dotenv
import asyncio
from utils.database import create_database, insert_or_update_into_database, check_and_update_database

# Load environment variables from the .env file using the load_dotenv() function
load_dotenv()

# Function to read URLs or IP addresses from a file
def read_urls_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            # Read all lines from the file and add each line to a list
            lines = file.readlines()
            # Strip any trailing spaces from each line and add it to the URL list
            urls = [line.strip() for line in lines]
            # Return the URL list
            return urls
    except FileNotFoundError:
        # Print an error message if the file is not found and return an empty list
        print(f"{file_path} file not found.")
        return []

async def main():
    # Get the name of a file from the user containing URLs or IP addresses
    file_path = input("Enter the name of the file containing URLs or IP addresses: ")
    # Create a list of URLs by reading the file content
    url_list = read_urls_from_file(file_path)

    if url_list:
        # Specify the name of the SQLite database file
        database_path = "url_ip_database.db"

        # Create the database schema
        create_database(database_path)

        for url_or_ip in url_list:
            # Add each URL or IP address to the database with a "No" flag, which can be updated to "Yes" after analysis with an API
            insert_or_update_into_database(database_path, url_or_ip, "No")

        # Display a message indicating successful data addition to the database
        print("Data successfully added to the database.")

        # Check and update the status of URLs (asynchronously)
        await check_and_update_database(database_path)
    else:
        # Display an appropriate error message if the file content is empty or if there's an error
        print("File read error or empty file.")

if __name__ == "__main__":
    # Start the main process and run the program
    asyncio.run(main())
