from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils import summarize_content_from_html, get_page_content

MAX_WORKERS = 10  

def crawl(url, depth, max_depth=3, visited=None, use_selenium=False):
    if visited is None:
        visited = set()

    if depth > max_depth or url in visited:
        return None

    visited.add(url)
    print(f"Crawling: {url} | Depth: {depth}")
    
    # Fetch content
    content = get_page_content(url, use_selenium)
    if not content:
        print(f"❌ No content found at: {url}")
        return None

    soup = BeautifulSoup(content, 'html.parser')

    # Extract internal links
    links = set()
    for link in soup.find_all('a', href=True):
        href = link['href']
        full_url = urljoin(url, href)
        if urlparse(full_url).netloc == urlparse(url).netloc and full_url not in visited:
            links.add(full_url)

    # Summarize and get embedding
    summary, page_type, embedding = summarize_content_from_html(content)

    # 🛡️ Safety check for embedding before returning node
    if not embedding or not isinstance(embedding, list) or len(embedding) != 768:
        print(f"⚠️ Skipping node at {url} due to invalid embedding.")
        return None

    children = []

    def crawl_child(link):
        return crawl(link, depth + 1, max_depth, visited, use_selenium)

    #  Crawl in parallel
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_url = {executor.submit(crawl_child, link): link for link in links}
        for future in as_completed(future_to_url):
            child = future.result()
            if child:
                children.append(child)

    return {
        "title": url,
        "url": url,
        "summary": summary,
        "type": page_type,
        "embedding": embedding,
        "children": children
    }
