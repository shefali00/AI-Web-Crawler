# AI Web Crawler

**AI Web Crawler** is an intelligent, agent-based web crawler that recursively explores websites to extract, summarize, classify, and embed content using Google’s Gemini AI models. It constructs a structured site map and enables powerful semantic search using FAISS, letting users retrieve information based on meaning—not just keywords.

---

## 🚀 Features

- 🌐 **Dynamic Web Crawling** with customizable depth control  
- 🧠 **Content Summarization** using Gemini Pro models  
- 🏷️ **Page Classification** (e.g., blog, product, login pages)  
- 🔍 **Semantic Search** via FAISS and Gemini embeddings  
- 🌳 **Tree Visualization** of the site structure using Graphviz  
- 📸 **Screenshot Analysis** for image-based content using Gemini Vision  
- 🖥️ **Streamlit UI** for an interactive user experience  

---

## 📦 Prerequisites

- Python 3.8 or higher  
- A valid Google Gemini API key (text + vision access)  
- Chrome browser and [ChromeDriver](https://sites.google.com/chromium.org/driver/) (for Selenium)  

---

## 🛠️ Setup

1. **Clone the repository**  
   ```bash
   git clone https://github.com/yourusername/ai-web-crawler.git
   cd ai-web-crawler
   ```

2. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**  
   Create a `.env` file in the root directory with:
   ```env
   GEMINI_API_KEY=your_google_gemini_api_key
   ```

4. **Install Graphviz**  
   Download and install [Graphviz](https://graphviz.org/download/), then add it to your system path for tree visualization support.

---

## 💻 Usage

Launch the Streamlit app:
```bash
streamlit run app.py
```

Then:
- Enter a base URL to start crawling  
- Set the crawl depth  
- Explore page summaries and classifications  
- Perform semantic search queries  
- Visualize the website structure in tree format  

---

## 🔍 How It Works

1. **Crawling**: Starts at a given URL and recursively discovers internal links based on a user-defined depth.  
2. **Summarization & Classification**: Uses Gemini to summarize page content and classify page types.  
3. **Embedding**: Text data is embedded using Gemini and stored in a FAISS index for fast similarity search.  
4. **Semantic Search**: Users can enter natural language queries to retrieve relevant pages based on meaning.  
5. **Tree Visualization**: The site map is displayed as a tree graph for easy navigation.  
6. **Visual Analysis**: For visual pages, screenshots are analyzed with Gemini Vision to enhance understanding.

