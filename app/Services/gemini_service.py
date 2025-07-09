import os
import cv2
import base64
import json
import time
import google.generativeai as genai
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in .env file.")
    
genai.configure(api_key=GEMINI_API_KEY)

def image_to_base64(img_np):
    """Convert NumPy image to base64 for inline data"""
    # Ensure image is in RGB format (Gemini prefers consistent format)
    if len(img_np.shape) == 2:  # If grayscale
        img_np = cv2.cvtColor(img_np, cv2.COLOR_GRAY2RGB)
    elif img_np.shape[2] == 4:  # If RGBA
        img_np = cv2.cvtColor(img_np, cv2.COLOR_RGBA2RGB)
    
    # Use higher quality for better recognition
    quality_param = [cv2.IMWRITE_JPEG_QUALITY, 95]
    _, buffer = cv2.imencode('.jpg', img_np, quality_param)
    return base64.b64encode(buffer).decode()

def parse_gemini_response(response_text: str) -> Dict[str, str]:
    """Parse and validate Gemini's response"""
    try:
        # First try to extract JSON if it's wrapped in text
        if "```json" in response_text:
            json_str = response_text.split("```json")[1].split("```")[0].strip()
            parsed = json.loads(json_str)
        else:
            # Try to parse the whole response as JSON
            parsed = json.loads(response_text)
            
        # Validate required fields
        if "title" not in parsed or "author" not in parsed:
            return {
                "title": "Unknown title",
                "author": "Unknown author",
                "error": "Incomplete response from AI"
            }
            
        return parsed
        
    except json.JSONDecodeError:
        # If JSON parsing fails, try to extract title and author with basic regex
        import re
        title_match = re.search(r'"title":\s*"([^"]+)"', response_text)
        author_match = re.search(r'"author":\s*"([^"]+)"', response_text)
        
        title = title_match.group(1) if title_match else "Unknown title"
        author = author_match.group(1) if author_match else "Unknown author"
        
        return {
            "title": title,
            "author": author,
            "error": "Response parsing error"
        }

async def extract_book_details(image_np) -> Dict[str, Any]:
    """
    Extract book details using Gemini SDK directly from image
    
    Args:
        image_np: Enhanced image as NumPy array
        
    Returns:
        Dictionary containing title, author and other metadata
    """
    start_time = time.time()
    
    # Create a prompt optimized for direct image analysis
    prompt = """
You are analyzing a book cover image.

TASK: 
1. Identify the BOOK TITLE and AUTHOR NAME based on the visual elements and text in the image.
2. If the book is in Urdu written the data in urdu.
3. If you cannot confidently identify either title or author, mark it as "Unknown".

YOU MUST RETURN ONLY A VALID JSON in exactly this format:
{
  "title": "Book Title Here",
  "author": "Author Name Here"
}

DO NOT include explanations, markdown formatting, or any text outside the JSON object , If you are unable to understand the text just write unable to understand in both title and author if any data is not understood by you , don't make your suggestion or any data by yourslef
If the book name contains more than one word always wrote the first letter captital it means always use title case
"""

    # Convert image to base64
    image_b64 = image_to_base64(image_np)

    try:
        # Use Gemini 2.5 Flash model for fast processing
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        # Send request with image only - no OCR text
        response = model.generate_content([
            prompt,
            {
                "inline_data": {
                    "mime_type": "image/jpeg",
                    "data": image_b64
                }
            }
        ])
        
        # Parse and validate the response
        result = parse_gemini_response(response.text)
        
        # Add AI processing time
        ai_time = time.time() - start_time
        result["ai_processing_time_ms"] = round(ai_time * 1000)
        
        return result
        
    except Exception as e:
        return {
            "title": "Unknown",
            "author": "Unknown",
            "error": f"AI processing error: {str(e)}"
        }  
