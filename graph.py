import requests
from bs4 import BeautifulSoup
from graphviz import Digraph
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import re

session = requests.Session()
retry_strategy = Retry(
    total=3,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)
session.mount("http://", adapter)

BASE_URL = "https://en.wikipedia.org"

def fetch_url(url):
    try:
        response = session.get(url)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_links(soup, base_url):
    links = set()
    for link in soup.find_all('a', href=True):
        href = link['href']
        if is_valid_link(href):
            full_url = href if href.startswith('http') else base_url + href
            links.add(full_url)
    return links

def is_valid_link(href):
    return href and len(href) > 1 and not href.startswith('#') and not href.startswith('mailto:') and href.startswith('/')

def sanitize_name(name):
    # Replace problematic characters with underscores
    return re.sub(r'[^\w\s]', '_', name)

def create_graph(g, start, max_pages):
    visited = set()
    queue = [start]
    num_edges = 0

    while queue and len(visited) < max_pages:
        current_vertex = queue.pop(0)
        if current_vertex not in visited:
            visited.add(current_vertex)
            sanitized_current_vertex = sanitize_name(current_vertex)
            g.node(sanitized_current_vertex)
            url = BASE_URL + current_vertex
            print(f"Fetching URL: {url}")
            response = fetch_url(url)
            if not response:
                continue
            soup = BeautifulSoup(response.content, 'html.parser')
            links = extract_links(soup, BASE_URL)
            for link in links:
                relative_link = link.replace(BASE_URL, '')
                if relative_link not in visited:
                    sanitized_relative_link = sanitize_name(relative_link)
                    g.edge(sanitized_current_vertex, sanitized_relative_link)
                    queue.append(relative_link)
            num_edges += 1
            print(f"Processed: {current_vertex} | Pages Visited: {len(visited)} | Edges: {num_edges}")

    print("Final No. of pages:", len(visited))
    print("Final No. of edges:", num_edges)
    g.render(filename='graph_vis', format='pdf', cleanup=True)
    g.view()

# Visualize the graph
g = Digraph(strict=True)
create_graph(g, '/wiki/%22I_AM%22_Activity', max_pages=20)
