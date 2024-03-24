import sys
import argparse
import urllib.parse
import requests
import socket
from bs4 import BeautifulSoup




# Function to make HTTP GET request
def make_http_request(url):
    try:
        # Make HTTP GET request
        response = requests.get(url)

        # Check for redirection
        if response.history:
            print(f"Request redirected to: {response.url}")

        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

        # Parse HTML response and extract text
        soup = BeautifulSoup(response.content, 'html.parser')
        text = ' '.join([tag.get_text() for tag in soup.find_all(['p', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])])

        return text
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"


def main():
    parser = argparse.ArgumentParser(description="Web Client CLI")
    parser.add_argument("-u", dest="url", help="Make an HTTP request to the specified URL and print the response")
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    if args.url:
        print(make_http_request(args.url))

if __name__ == "__main__":
    main()
