# Website Link Network Visualizer

**This Project** is a web scraper and visualizer designed to traverse and graphically represent the structure of linked web pages starting from a given URL on any website(a Wikipedia page is used here as an example). The project uses Python, BeautifulSoup for web scraping, and Graphviz for visualization.

## Features


- **Web Scraping with Retry Logic**: Utilizes `requests` with a retry strategy to handle network issues and ensure reliable data fetching.
- **Link Extraction**: Extracts valid links from the web pages to traverse and build a graph structure.
- **Graph Visualization**: Uses Graphviz to create a visual representation of the web page network.

** The Whole code is in the `web-graph-visualizer.py`, but to test it run `web-graph-visualizer-limit.py`. See the Example below:

##Example
1. Starting URL: https://en.wikipedia.org/wiki/%22I_AM%22_Activity
2. Maximum Pages: `200`
3. Total Edges: `193`

The script will fetch and process up to 200 pages (you can customize this) starting from the given URL , then generate a graph and save it as a PDF. Thhe full graph for 20 pages is [here(pdf)](https://github.com/shrad059/web-visualizer/blob/main/graph_vis.pdf) *you might have to zoom in to see the graph*

