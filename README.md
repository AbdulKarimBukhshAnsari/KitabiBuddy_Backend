# 🧠 Kitabi AI Backend

A lightweight FastAPI backend for **KitabiBuddy 📚**, a smart mobile app that helps users manage their personal book library. This backend connects with **Google Gemini Pro Vision API** to extract the book **title** and **author** from uploaded cover images.

---

## 🚀 Features

- 🧠 AI-powered image analysis using Gemini Pro Vision
- 📤 Accepts book cover images and returns structured data
- ⚡ Built with FastAPI — fast, scalable, and minimal
- 📱 Designed for React Native (Expo) frontends
- 🔐 Keeps Gemini API key secure (never exposed to client)

---

## 🛠 Tech Stack

- **Python 3.10+**
- **FastAPI** (REST API framework)
- **Pillow** (Image preprocessing)
- **Google Generative AI SDK** (Gemini integration)
- **Uvicorn** (ASGI server)

---

## 📁 Project Structure

```

kitabi-ai-backend/
├── main.py                 # FastAPI entry point
├── utils/
│   └── image\_processing.py # Optional: image cleanup, rotation etc.
├── requirements.txt        # Python dependencies
└── README.md

````

---

## 🌐 API Endpoint

### `POST /extract-book-details/`

Upload a book cover image and receive extracted title/author from Gemini.

#### 🔧 Request
- `image`: JPEG/PNG file (cover image)

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
