import os
import json
import google.generativeai as genai
from google.generativeai import embed_content
from dotenv import load_dotenv

load_dotenv()


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
embedding_model = genai.get_model("models/embedding-001")
text_model = genai.GenerativeModel("gemini-1.5-pro")


EXPECTED_EMBEDDING_DIM = 768

def get_embedding(text):
    try:
        
        response = genai.embed_content(
            model="models/embedding-001",
            content=text,
            task_type="retrieval_document"
        )

        print(f"🔎 Response received: {response}")  

        # Extract the embedding
        embedding = response.get("embedding", [])
        print(f"🔍 Extracted embedding: {embedding[:10]}...") 

        
        if embedding and isinstance(embedding, list) and len(embedding) == 768:
            return embedding
        else:
            print(f"⚠️ Invalid embedding shape: got {len(embedding)} elements")
            return []
    except Exception as e:
        print(f"❌ Embedding error: {e}")
        return []




def summarize_and_classify(content):
    prompt = f"""
You are an intelligent assistant. Summarize the following content and classify the type of webpage. 
Return **only** valid JSON in the format: {{"summary": "...", "type": "..."}} — no commentary, no explanation.

Content:
\"\"\"
{content[:2000]}
\"\"\"
"""
    try:
        response = text_model.generate_content(prompt)
        text = response.text.strip()

        print(f"🔎 Model response:\n{text}\n")  # Optional debug

        # Strip triple backticks if they exist
        if text.startswith("```") and "```" in text[3:]:
            text = text.split("```")[1].strip()

        # Find the first { to ensure clean parsing
        first_brace = text.find('{')
        if first_brace != -1:
            text = text[first_brace:]

        json_output = json.loads(text)
        return json_output.get("summary", ""), json_output.get("type", "")
    except Exception as e:
        print(f"❌ Summarization error: {e}")
        return "Summary failed", "Unknown"
