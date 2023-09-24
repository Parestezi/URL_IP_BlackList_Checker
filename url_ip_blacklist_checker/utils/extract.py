from urllib.parse import urlparse
import validators

# Function to extract the scheme (http:// or https://) from a URL
def extract_scheme(url):
    # Parse the given URL and assign it to a variable (e.g., https://youtube.com -> youtube.com)
    parsed_url = urlparse(url)

    # If there is a scheme (scheme) in the URL, return it in lowercase (e.g., HTTPS://youtube.com -> https://)
    scheme = parsed_url.scheme
    if scheme:
        return scheme.lower()
    else:
        return None

# Function to check if the given text is a URL
def is_url(input_str):
    try:
        # Parse the given text as a URL
        parsed_url = urlparse(input_str)

        # If the URL has a 'netloc' (domain) or 'path' (path), it is considered a URL
        if parsed_url.netloc or parsed_url.path:
            return True
        # If the given text is an IPv4 or IPv6 address, it is not a URL and returns False
        elif validators.ipv4(input_str) or validators.ipv6(input_str):
            return False
        else:
            return False
    except ValueError:
        # If there is an error during URL parsing, it is not a URL and returns False
        return False

# Function to extract the domain from a given URL
def extract_domain_from_url(url):
    try:
        # Parse the given URL
        parsed_url = urlparse(url)

        # If there is a domain (netloc) in the URL, return it
        if parsed_url.netloc:
            return parsed_url.netloc
        # If there is a path (path) in the URL, split it and return the first section
        elif parsed_url.path:
            return parsed_url.path.split("/")[0]
        # If there is a fragment (fragment) in the URL, split it and return the first section
        elif parsed_url.fragment:
            return parsed_url.fragment.split("/")[0]
        # If the given text is a domain, return it
        elif validators.domain(url):
            return url
        else:
            return None
    except ValueError:
        # If there is an error during URL parsing, return None
        return None
