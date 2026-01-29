# Wiki Quiz Generator 📚🤖

An intelligent quiz generator that scrapes Wikipedia articles and automatically generates quizzes using AI (Gemini). Built with **FastAPI** backend, **PostgreSQL** database, and a clean **HTML/JS** frontend.

## ✨ Features

- 📖 **Scrape Wikipedia**: Extract article content, sections, and key information
- 🤖 **AI Quiz Generation**: Generate 5-7 questions using Google Gemini
- 💾 **Database Storage**: Store quizzes with PostgreSQL for history tracking
- 🎨 **Modern UI**: Clean, responsive interface with two main tabs
- 📋 **History & Details**: View previously generated quizzes in a modal
- ⚡ **Caching**: Prevent duplicate scraping of the same URL
- 🎯 **Difficulty Levels**: Easy, Medium, Hard questions
- 🔗 **Related Topics**: AI suggests related Wikipedia articles

## 🏗️ Project Structure

```
wiki-quiz/
├── backend/
│   ├── main.py              # FastAPI app & endpoints
│   ├── database.py          # SQLAlchemy setup
│   ├── models.py            # Database models
│   ├── schemas.py           # Pydantic schemas
│   ├── scraper.py           # Wikipedia scraping logic
│   ├── llm.py               # Gemini API integration
│   ├── crud.py              # Database operations
│   └── .env.example         # Environment template
├── frontend/
│   └── index.html           # Full HTML/CSS/JS UI
├── sample_data/
│   ├── urls.txt             # Example URLs tested
│   └── output.json          # Sample API response
├── README.md                # This file
└── requirements.txt         # Python dependencies
```

## 🚀 Quick Start

### Step 1: Clone & Setup

```bash
cd wiki-quiz
python -m venv venv
venv\Scripts\activate   # Windows
# or
source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
```

### Step 2: Setup PostgreSQL Database

1. **Install PostgreSQL** (if not already installed)
   - Windows: https://www.postgresql.org/download/windows/
   - Mac: `brew install postgresql`
   - Linux: `sudo apt-get install postgresql`

2. **Create database**:
   ```bash
   psql -U postgres
   CREATE DATABASE wikiquiz;
   \q
   ```

### Step 3: Environment Configuration

1. Create `.env` file in `backend/` folder:
   ```bash
   cp backend\.env.example backend\.env
   ```

2. Edit `backend/.env`:
   ```
   DATABASE_URL=postgresql://postgres:your_password@localhost:5432/wikiquiz
   GEMINI_API_KEY=your_gemini_api_key_here
   ENVIRONMENT=development
   ```

### Step 4: Get Gemini API Key

1. Go to https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy and paste into `.env` file

### Step 5: Run Backend

```bash
cd backend
python main.py
```

You should see:
```
✓ Uvicorn running on http://0.0.0.0:8000
```

### Step 6: Open Frontend

Open `frontend/index.html` in your browser (or use Live Server)

---

## 📡 API Endpoints

### 1️⃣ Generate Quiz
**POST** `/api/generate-quiz`

**Request:**
```json
{
  "url": "https://en.wikipedia.org/wiki/Alan_Turing"
}
```

**Response:**
```json
{
  "id": 1,
  "url": "https://en.wikipedia.org/wiki/Alan_Turing",
  "title": "Alan Turing",
  "summary": "Alan Turing was a British mathematician...",
  "sections": ["Early life", "World War II", "Legacy"],
  "quiz": [
    {
      "question": "Where did Alan Turing study?",
      "options": ["Harvard", "Cambridge", "Oxford", "Princeton"],
      "answer": "Cambridge",
      "difficulty": "easy",
      "explanation": "Mentioned in Early life section."
    }
  ],
  "related_topics": ["Cryptography", "Enigma machine"],
  "created_at": "2024-01-29T10:30:00"
}
```

### 2️⃣ Get History
**GET** `/api/history`

**Response:**
```json
[
  {
    "id": 1,
    "url": "https://en.wikipedia.org/wiki/Alan_Turing",
    "title": "Alan Turing",
    "created_at": "2024-01-29T10:30:00"
  }
]
```

### 3️⃣ Get Quiz Details
**GET** `/api/quiz/{id}`

Returns full quiz data for modal display (same as generate response)

---

## 🧪 Testing

### Test with Sample URLs

```
https://en.wikipedia.org/wiki/Alan_Turing
https://en.wikipedia.org/wiki/Marie_Curie
https://en.wikipedia.org/wiki/Isaac_Newton
https://en.wikipedia.org/wiki/Albert_Einstein
https://en.wikipedia.org/wiki/Stephen_Hawking
```

### Using cURL

```bash
curl -X POST http://localhost:8000/api/generate-quiz \
  -H "Content-Type: application/json" \
  -d "{\"url\": \"https://en.wikipedia.org/wiki/Alan_Turing\"}"
```

---

## 🤖 LLM Prompt Templates

### Quiz Generation Prompt

```python
prompt = f"""
You are an expert quiz generator. Based on the following Wikipedia article text, 
generate a structured JSON response with quiz questions and related topics.

IMPORTANT RULES:
1. Generate EXACTLY 5-7 multiple choice questions
2. All questions MUST be answerable from the provided text
3. Each question must have 4 options (A, B, C, D)
4. Difficulty levels: "easy" (1-2 questions), "medium" (2-3), "hard" (1-2)
5. Explanations must cite the specific section or fact
6. Related topics should be 3-5 Wikipedia topics mentioned in the text

ARTICLE TITLE: {title}

ARTICLE TEXT:
{text[:3000]}

Return ONLY valid JSON (no markdown, no explanation) in this exact format:
{{
  "quiz": [
    {{
      "question": "Question text here?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": "Correct Option",
      "difficulty": "easy|medium|hard",
      "explanation": "Why this is correct based on the text"
    }}
  ],
  "related_topics": ["Topic1", "Topic2", "Topic3"]
}}
"""
```

---

## 📋 Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | FastAPI 0.104.1 |
| Database | PostgreSQL 15+ |
| ORM | SQLAlchemy 2.0 |
| Scraping | BeautifulSoup 4 |
| LLM | Google Gemini API |
| Frontend | HTML5 + CSS3 + Vanilla JS |
| Environment | Python 3.9+ |

---

## 🎯 Features Implemented

### Core
- ✅ Wikipedia scraping with BeautifulSoup
- ✅ Quiz generation with Gemini AI
- ✅ PostgreSQL database storage
- ✅ RESTful API with FastAPI
- ✅ Clean, responsive UI
- ✅ Tab-based navigation
- ✅ History/Details modal

### Bonus
- ✅ URL caching (no duplicate scraping)
- ✅ Error handling & validation
- ✅ Difficulty level assignment
- ✅ Related topics extraction
- ✅ Beautiful card-based layout
- ✅ Mobile responsive design

### In Progress
- ⏳ "Take Quiz" mode with scoring
- ⏳ Section-wise question grouping
- ⏳ Raw HTML storage in DB

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'fastapi'"
```bash
pip install -r requirements.txt
```

### "FATAL: Ident authentication failed for user 'postgres'"
Change PostgreSQL password in `.env`:
```
DATABASE_URL=postgresql://postgres:your_actual_password@localhost:5432/wikiquiz
```

### "GEMINI_API_KEY not found"
Make sure `.env` file exists in `backend/` folder with your API key

### "Connection refused" error
Make sure PostgreSQL is running:
```bash
# Windows
pg_ctl -D "C:\Program Files\PostgreSQL\15\data" start

# Mac
brew services start postgresql

# Linux
sudo systemctl start postgresql
```

---

## 📸 Screenshots

### Tab 1: Generate Quiz
- Input Wikipedia URL
- Click "Generate Quiz"
- View formatted quiz with questions, options, and explanations
- See related topics

### Tab 2: History
- View all previously generated quizzes
- Click "View Details" to open modal
- Modal shows same format as Tab 1

### Modal Display
- Full quiz details in a beautiful card layout
- Difficulty badges
- Explanations for each answer
- Related topics tags

---

## 🚀 Deployment

### Option 1: Render (Backend)

```bash
git push # Push to GitHub
# On Render.com:
# - Connect GitHub repo
# - Set environment variables
# - Deploy
```

### Option 2: Vercel (Frontend)

```bash
# Deploy frontend to Vercel
# Update API_URL in index.html to point to live backend
```

---

## 📚 Learning Outcomes

You'll understand:
1. ✅ How to build REST APIs with FastAPI
2. ✅ Web scraping with BeautifulSoup
3. ✅ Database modeling with SQLAlchemy
4. ✅ LLM integration with LangChain
5. ✅ Frontend-Backend communication
6. ✅ Error handling & validation
7. ✅ CORS & async operations
8. ✅ Environment management

---

## 🤝 Contributing

Found a bug? Want to improve? 
1. Fork the repo
2. Create feature branch
3. Submit PR

---

## 📄 License

MIT License - Feel free to use for learning!

---

## 💡 Next Steps

1. ✅ Run Phase 0-1 setup
2. ✅ Get Gemini API key
3. ✅ Start backend
4. ✅ Test with sample URLs
5. ✅ Deploy to production

**Happy Coding! 🚀**
