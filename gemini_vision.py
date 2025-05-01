# gemini_vision.py
import os
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_image(path):
    model = genai.GenerativeModel("gemini-1.5-flash")
    img = Image.open(path)

    prompt = """Give a detailed summary of this webpage based on the image. 
What type of page is this (e.g., blog, product, news, quote site, login page, etc.)?"""

    response = model.generate_content([prompt, img])
    return response.text
