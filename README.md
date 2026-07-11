# IntelliHCP — AI-First CRM for Pharmaceutical HCP Interaction Logging

An AI-first Customer Relationship Management (CRM) system focused on Healthcare Professional (HCP) interaction logging. The AI assistant is the primary interface — users describe interactions in natural language, and the AI automatically extracts structured data to populate a CRM form.

## 🏗️ Architecture

```
User → Chat → FastAPI → LangGraph Agent → Groq LLM → Tool → PostgreSQL → Redux → Form
```

**Split-Screen Layout:**
- **Left Panel (60%)** — Read-only interaction form (controlled by AI)
- **Right Panel (40%)** — AI chat assistant

**Key Design Decisions:**
- **LangGraph with native ToolNode** — Prebuilt tool execution with `tools_condition` routing
- **MemorySaver** — Multi-turn conversation memory per session
- **Single extraction pattern** — LLM extracts once via tool_call args; tools do deterministic DB work
- **Validation/normalization layer** — Sits between LLM output and database writes

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React + Vite + Redux Toolkit + TailwindCSS v4 |
| Backend | Python 3.12+ + FastAPI |
| AI Agent | LangGraph + LangChain |
| LLM | Groq API → llama-3.3-70b-versatile |
| Database | SQLite (Default for zero-install setup) / PostgreSQL 16 |
| Font | Google Inter |

## 🤖 LangGraph Tools (5)

| # | Tool | Purpose |
|---|------|---------|
| 1 | `log_interaction` | Extract CRM data from natural language and save |
| 2 | `edit_interaction` | Surgically update only changed fields |
| 3 | `search_doctor` | Fuzzy search HCP database |
| 4 | `recommend_products` | Suggest products by specialization |
| 5 | `plan_followup` | Generate follow-up action items |

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Node.js 18+
- Groq API key ([Get one here](https://console.groq.com))
- *Note: PostgreSQL and Docker are fully supported but optional. The app runs out-of-the-box using a local serverless SQLite database.*

### 1. Clone & Setup

```bash
git clone <repository-url>
cd IntelliHCP
```

### 2. Backend Setup (SQLite - Zero Install)

```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# Start the backend
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### 4. Open the app

Navigate to `http://localhost:5173`

## 📁 Project Structure

```
IntelliHCP/
├── backend/
│   ├── app/
│   │   ├── api/v1/          # FastAPI endpoints
│   │   ├── core/            # Config, logging, exceptions
│   │   ├── database/        # Engine, base, seed data
│   │   ├── graph/           # LangGraph agent, state
│   │   ├── models/          # SQLAlchemy ORM models
│   │   ├── prompts/         # LLM system prompt
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── services/        # Business logic (CRUD)
│   │   ├── tools/           # 5 LangGraph tools
│   │   ├── validators/      # Normalization layer
│   │   └── main.py          # FastAPI app factory
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/             # Axios client
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── redux/           # Store, slices, thunks
│   │   └── utils/           # Constants, formatters
│   └── package.json
├── docker-compose.yml       # PostgreSQL
└── README.md
```

## 💬 Usage Examples

**Log an interaction:**
```
Met Dr. Sharma today at Apollo Hospital. Discussed CardioX efficacy 
and shared the Phase III brochure. Sentiment was positive. 
Follow up next week.
```

**Edit an interaction:**
```
Actually the doctor was Dr. Priya Sharma and the sentiment was neutral.
```

**Search doctors:**
```
Search for cardiologists in Mumbai
```

**Get product recommendations:**
```
What products should I discuss with an oncologist?
```

**Plan follow-up:**
```
Suggest follow-up actions for my meeting with Dr. Kumar
```

## 📄 License

MIT
