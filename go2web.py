import sys
import argparse
import urllib.parse
import requests
import requests_cache
from bs4 import BeautifulSoup

# Google Custom Search API credentials
API_KEY = 'AIzaSyDGx6E7DPqSozqRRFEeDn9FQ4akYXEVA7E'
SEARCH_ENGINE_ID = '2028de92bd5ca4bc7'

# Enable cache with a timeout of 3600 seconds (1 hour)
requests_cache.install_cache(cache_name='web_cache', expire_after=3600)

# Function to make HTTP GET request
def make_http_request(url, accept='text/html'):
    try:
        headers = {'Accept': accept}
        # Make HTTP GET request with specified Accept header
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        
        # Disable cache after request
        requests_cache.clear()
        
        # Check for redirection
        if response.history:
            print(f"Request redirected to: {response.url}")

        # Parse HTML response and extract text
        soup = BeautifulSoup(response.content, 'html.parser')
        text = ' '.join([tag.get_text() for tag in soup.find_all(['p', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])])

        return text
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# Function to search using Google Custom Search API
def search(term):
    try:
        # Construct Google Custom Search API URL
        url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={urllib.parse.quote(term)}"

        # Make HTTP GET request to the Google Custom Search API
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

        # Parse JSON response
        results = response.json()

        # Extract first 10 search results
        search_results = []
        for item in results.get('items', [])[:10]:
            search_results.append(item['title'] + ' - ' + item['link'])

        return '\n'.join(search_results)
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def main():
    parser = argparse.ArgumentParser(description="Web Client CLI")
    parser.add_argument("-u", dest="url", help="Make an HTTP request to the specified URL and print the response")
    parser.add_argument("-s", dest="search_term", help="Make an HTTP request to search the term using your favorite search engine and print top 10 results")
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    if args.url:
        print(make_http_request(args.url))
    elif args.search_term:
        print(search(args.search_term))
    else:
        parser.print_help(sys.stderr)

if __name__ == "__main__":
    main()
