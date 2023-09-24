import os
import httpx

# Get the Google Safe Browsing API key from the environmental variable named GOOGLE_SAFE_BROWSING_API_KEY
GOOGLE_SAFE_BROWSING_API_KEY = os.getenv("GOOGLE_SAFE_BROWSING_API_KEY")

# Function to check the status of a given URL
def check_url_status(url):
    try:
        # Send an HTTP GET request and receive a response
        response = httpx.get(url)
        # If the response status code is 200, mark the URL as "OK"
        if response.status_code == 200:
            return "OK"
        # If the response status code is 404, mark the URL as "Down"
        elif response.status_code == 404:
            return "Down"
        # If the response status code is between 300 and 399, mark the URL as "Redirection"
        elif 300 <= response.status_code < 400:
            return "Redirection"
        # If there's another status code, return it with "HTTP Error"
        else:
            return f"HTTP Error: {response.status_code}"
    except httpx.RequestError as e:
        # If an error occurs while sending the HTTP request, return the error message with "Request Error"
        return f"Request Error: {str(e)}"

# Function to check the status of a URL without a schema - httpx is used for asynchronous operation; requests is synchronous
def check_ip_status(url):
    try:
        # Check the URL with "http://" added to it
        response = httpx.get("http://" + url)
        # If the response status code is 200, mark the URL as "OK"
        if response.status_code == 200:
            return "OK"
        # If the response status code is 404, mark the URL as "Down"
        elif response.status_code == 404:
            return "Down"
        # If the response status code is between 300 and 399, mark the URL as "Redirection"
        elif 300 <= response.status_code < 400:
            return "Redirection"
        # If there's another status code, return it with "HTTP Error"
        else:
            return f"HTTP Error: {response.status_code}"
    except httpx.RequestError as e:
        # If an error occurs while sending the HTTP request, return the error message with "Request Error"
        return f"Request Error: {str(e)}"

# Asynchronous function to check a URL using the Google Safe Browsing API
async def check_url(url):
    # Print a message to the console indicating that an API request is being made
    print(f"Making API request: {url}")

    # Start an asynchronous HTTP client with httpx.AsyncClient()
    async with httpx.AsyncClient() as client:
        # Send a request to the Google Safe Browsing API and wait for the response
        response = await client.get(
            f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={GOOGLE_SAFE_BROWSING_API_KEY}",
            params={
                "client": {
                    "clientId": "my-app",
                    "clientVersion": "1.0",
                },
                "threatInfo": {
                    "threatTypes": [
                        "MALWARE",
                        "SOCIAL_ENGINEERING",
                        "THREAT_TYPE_UNSPECIFIED",
                    ],
                    "platformTypes": ["ANY_PLATFORM"],
                    "threatEntryTypes": ["URL"],
                    "threatEntries": [{"url": url}],
                },
            },
        )
        # Print the API response to the console
        print(f"API response: {response.text}")
        # Return the response
        return response
