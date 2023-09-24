# URL and IP Address Monitoring Application

This Python-based application is used to monitor and check the security status of provided URLs and IP addresses. It also includes an asynchronous function to identify malicious URLs using the Google Safe Browsing API.

## Getting Started

We use Poetry to run this application in a local environment and manage its dependencies.

### Requirements

- Python 3.x
- Poetry (for managing project dependencies)
- Google Safe Browsing API Key (required for malicious URL scanning)

### Installation

1. Clone this repository to your local machine.

   ```markdown
   git clone https://github.com/Parestezi/URL_IP_BlackList_Checker

2. Navigate to the project directory.
   ```markdown
   cd URL_IP_BlackList_Checker

3. Install and set up the project using Poetry.
   ```markdown
   poetry install

4. Create a .env file and add your Google Safe Browsing API Key.
      ```markdown
      GOOGLE_SAFE_BROWSING_API_KEY=your_api_key_here

### Usage
After launching the application, you will be prompted to enter the name of a file. This file should contain the URLs or IP addresses you want to monitor.

The application reads the file's content and adds the URLs or IP addresses to the database.

The application periodically checks the URLs or IP addresses and verifies their security status.

When a malicious URL is detected, the corresponding entry is updated as "Yes."

If URLs are found to be "Down" or have redirection issues, they are saved to the "down_redirection_urls.txt" file.
