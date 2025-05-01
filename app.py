import streamlit as st
from crawler import crawl
from tree_visualizer import render_tree
from semantic_search import extract_nodes_with_embeddings, build_faiss_index, search

st.set_page_config(layout="wide")
st.title("🤖 Agentic AI Crawler")

# Input section
url = st.text_input("Enter the website URL (e.g., https://quotes.toscrape.com)", "https://quotes.toscrape.com")
depth = st.number_input("Enter the depth for crawling:", min_value=1, max_value=5, value=2)
use_selenium = st.checkbox("Use Selenium for dynamic content?", value=False)

# Session state for persistence
if "tree" not in st.session_state:
    st.session_state.tree = None

if "semantic_index" not in st.session_state:
    st.session_state.semantic_index = None

if "semantic_nodes" not in st.session_state:
    st.session_state.semantic_nodes = None

# Crawl website
if st.button("🚀 Start Crawling"):
    if url:
        st.info("Starting the crawl... This may take a few seconds...")
        tree = crawl(url, depth=0, max_depth=depth, use_selenium=use_selenium)

        if tree:
            st.session_state.tree = tree  # Save in session state

            st.subheader("📚 Navigation Tree (JSON Format)")
            st.json(tree)

            st.subheader("🌳 Visual Tree Structure")
            try:
                st.graphviz_chart(render_tree(tree))
            except Exception as e:
                st.error(f"Graphviz rendering failed: {e}")

            # Build FAISS index after crawl
            nodes = extract_nodes_with_embeddings(tree)
            if nodes:
                st.session_state.semantic_nodes = nodes
                try:
                    st.session_state.semantic_index, st.session_state.semantic_nodes = build_faiss_index(nodes)
                    st.success(f"✅ Indexed {len(nodes)} pages with valid embeddings.")
                except ValueError as ve:
                    st.error(f"Indexing failed: {ve}")
            else:
                st.warning("No valid pages with embeddings found to index.")

        else:
            st.error("Crawling failed or returned no content.")
    else:
        st.warning("Please enter a valid URL.")

# Semantic search UI
st.subheader("🔍 Search by Meaning")
query = st.text_input("Enter your query (e.g., motivation, quotes on love)")

if st.button("Search") and query:
    if st.session_state.semantic_index and st.session_state.semantic_nodes:
        results = search(query, st.session_state.semantic_index, st.session_state.semantic_nodes, top_k=5)

        for res in results:
            st.markdown(f"**[{res['url']}]({res['url']})**")
            st.write(res["summary"])
            st.write(f"🔗 Score: {res['score']:.3f}")
            st.markdown("---")
    else:
        st.warning("Please crawl the website first before searching.")
# Search for a specific page from the tree
st.subheader("🔎 Page Navigator")
target_input = st.text_input("Which page do you want to access? (Keyword or URL)")

from difflib import SequenceMatcher

def find_best_match(tree, keyword):
    best = {"score": 0.0, "path": [], "node": None}

    def dfs(node, path):
        title = node.get("title", "")
        url = node.get("url", "")
        score = max(
            SequenceMatcher(None, keyword.lower(), title.lower()).ratio(),
            SequenceMatcher(None, keyword.lower(), url.lower()).ratio()
        )
        if score > best["score"]:
            best["score"] = score
            best["path"] = path + [node]
            best["node"] = node

        for child in node.get("children", []):
            dfs(child, path + [node])

    dfs(tree, [])
    return best

if target_input and st.session_state.tree:
    result = find_best_match(st.session_state.tree, target_input)

    if result:
        st.success(f"✅ Best match found: {result['node']['title']}")

        st.markdown("### 📍 Navigation Path (Titles)")
        path_titles = " → ".join([step.get("title", "[No title]") for step in result["path"]])
        st.markdown(f"`{path_titles}`")

        st.markdown("### 🔗 Navigation Path (Clickable URLs)")
        for i, step in enumerate(result["path"]):
            title = step.get("title", "Untitled")
            url = step.get("url", "#")
            st.markdown(f"{'👉' if i == len(result['path']) - 1 else '↪️'} [{title}]({url})")

        selected_node = result["node"]
        from utils import capture_screenshot
        from gemini_vision import analyze_image

        with st.spinner("Capturing screenshot and analyzing..."):
            screenshot_path = capture_screenshot(selected_node["url"])
            st.image(screenshot_path, caption="📸 Screenshot of selected page", use_container_width=True)

            vision_summary = analyze_image(screenshot_path)
            st.subheader("🧠 Gemini Vision Summary")
            st.markdown(vision_summary)