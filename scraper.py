import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_text_from_url(url):
    """
    Fetches the text content from a given URL.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # This will raise an HTTPError if the request was unsuccessful
        soup = BeautifulSoup(response.text, 'html.parser')

        # We'll extract only the main text content, ignoring things like scripts and styles.
        for script in soup(["script", "style"]):
            script.extract()
        
        text = soup.get_text(separator=' ', strip=True)
        return text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return ""

def get_links_from_url(url):
    """
    Extracts internal links from a given URL to a depth of 1.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        internal_links = set()
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(url, href)
            # Check if the link is on the same domain and is not a file or anchor link
            if full_url.startswith(url) and not full_url.endswith(('.png', '.jpg', '.jpeg', '.gif', '.pdf', '.zip')) and '#' not in full_url:
                internal_links.add(full_url)
        return list(internal_links)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching links from {url}: {e}")
        return []

# The following code block is correctly de-indented and its contents are indented.
if __name__ == "__main__":
    # You can test with any URL you want
    test_url = "https://www.coca-cola.com/ca/en"
    print(f"Fetching text from: {test_url}")
    text_content = get_text_from_url(test_url)
    print("--- Text Content ---")
    print(text_content[:500])  # Print the first 500 characters

    print("\n--- Internal Links ---")
    links = get_links_from_url(test_url)
    for i, link in enumerate(links[:5]):
        print(f"{i+1}. {link}")