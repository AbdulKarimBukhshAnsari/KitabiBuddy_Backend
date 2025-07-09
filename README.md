# 📚 KitabiBuddy Backend API

A robust FastAPI backend for **KitabiBuddy**, an intelligent application that helps users manage their personal book library. This backend processes book cover images with advanced OCR and connects with **Google Gemini 2.5 Flash** to accurately extract book **title** and **author** information, with special optimization for Urdu text.

## 🚀 Features

- 🧠 AI-powered image analysis using Google Gemini 2.5 Flash
- � Advanced OCR processing for both English and Urdu text
- 🖼️ Smart image preprocessing for better recognition
- 📊 Detailed response with confidence scores and metadata
- ⚡ Fast, scalable REST API built with FastAPI
- 🛡️ Robust error handling with helpful error messages
- 📱 Cross-platform compatibility (for web and mobile clients)
- 🔐 Secure API key management

## 🛠️ Tech Stack

- **Python 3.10+**
- **FastAPI** (REST API framework)
- **EasyOCR** (Optical Character Recognition)
- **OpenCV** (Image preprocessing)
- **Google Generative AI SDK** (Gemini integration)
- **Uvicorn** (ASGI server)

## 📁 Project Structure

```
kitabibuddy-backend/
├── app/
│   ├── main.py              # FastAPI application setup
│   ├── routes/
│   │   └── book.py          # Book scanning endpoint
│   └── Services/
│       ├── gemini_service.py # Gemini AI integration
│       └── ocr_service.py    # Image processing & OCR
├── requirements.txt         # Project dependencies
└── README.md                # Documentation
```

## 🔧 Setup and Installation

### Prerequisites
- Python 3.10 or higher
- A Google Generative AI API key (Gemini)

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/kitabibuddy-backend.git
   cd kitabibuddy-backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your Gemini API key:
   ```
   GEMINI_API_KEY=your-api-key-here
   ```

5. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

## 📡 API Endpoints

### `POST /api/book/scan`

Upload a book cover image and receive extracted title and author information.

#### Request
- **Content-Type**: `multipart/form-data`
- **Body**: Form data with `file` field containing the image

#### Successful Response (200 OK)
```json
{
  "success": true,
  "data": {
    "title": "Book Title",
    "author": "Author Name",
    "ocr_blocks_count": 8,
    "detection_confidence": 0.85,
    "processing_time_ms": 1250
  }
}
```

#### Error Response (400, 422, 500)
```json
{
  "success": false,
  "error": "Error message",
  "details": "Detailed explanation"
}
```

### `GET /health`

Health check endpoint to verify API status.

#### Response
```json
{
  "status": "healthy"
}
```

## � Error Codes

| Status Code | Description                                           |
|-------------|-------------------------------------------------------|
| 400         | Bad request (invalid image format)                    |
| 413         | Image file too large (>10MB)                          |
| 422         | Image processing error (not a book or unclear image)  |
| 500         | Internal server error                                 |

## 🧪 Testing the API

Using cURL:
```bash
curl -X POST -F "file=@/path/to/book-cover.jpg" http://localhost:8000/api/book/scan
```

Using Python:
```python
import requests

url = "http://localhost:8000/api/book/scan"
files = {"file": open("book-cover.jpg", "rb")}

response = requests.post(url, files=files)
print(response.json())
```

## 📖 Documentation

Once the server is running, you can access:
- Interactive API docs: http://localhost:8000/api/docs
- Alternative docs: http://localhost:8000/api/redoc

#### 📤 Sample Response
```json
{
  "data": {
    "title": "Atomic Habits",
    "author": "James Clear"
  }
}
````

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/kitabi-ai-backend.git
cd kitabi-ai-backend
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Gemini API Key

Set your environment variable:

```bash
export GOOGLE_API_KEY="your-gemini-api-key"
```

Or use `.env` file + `python-dotenv`.

### 4. Run the Server

```bash
uvicorn main:app --reload
```

Now open: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📱 React Native Integration Example

```js
const formData = new FormData();
formData.append("image", {
  uri: imageUri,
  name: "cover.jpg",
  type: "image/jpeg",
});

const response = await fetch("https://your-api.onrender.com/extract-book-details/", {
  method: "POST",
  headers: {
    "Content-Type": "multipart/form-data",
  },
  body: formData,
});

const result = await response.json();
console.log(result.data); // → { title: "xyz", author: "abc" }
```

---

## 🌍 Deployment Options

You can deploy this backend easily to:

| Platform                                             | Free Tier | Suitable                 |
| ---------------------------------------------------- | --------- | ------------------------ |
| [Render](https://render.com/)                        | ✅         | ✅ Production-ready       |
| [Railway](https://railway.app/)                      | ✅         | ✅ Simple CI/CD           |
| [Fly.io](https://fly.io/)                            | ✅         | ✅ Container-based        |
| [Hugging Face Spaces](https://huggingface.co/spaces) | ✅         | ⚠️ Only for testing/demo |

---

## 🔐 Security Notes

* Never expose your Gemini API key in the frontend.
* Limit image size to prevent abuse.
* Optionally restrict by API token or IP if public.

---

## 👤 Author

**Abdul Karim Bukhsh Ansari**
📱 Creator of **KitabiBuddy**
