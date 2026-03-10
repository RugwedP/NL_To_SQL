# 🤖 NL2SQL — Natural Language to SQL Query System

> Convert plain English questions into validated SQL queries, execute them on PostgreSQL, and visualize results.

---

## 📌 What is this?

NL2SQL lets anyone query a database using plain English — no SQL knowledge required.

You type: **"show me top 5 customers by total spending"**

The system:
1. Understands what you mean
2. Generates the correct SQL
3. Validates the SQL (without AI)
4. Runs it on your PostgreSQL database
5. Shows you the results as a table or chart

---

## 🏗️ Project Structure

```
NL_To_SQL/
├── app/
│   ├── __init__.py
│      ├── configuration/
│          ├── config.py          # API keys + DB credentials
│      ├── endpoint/
│          ├── api.py                 # FastAPI REST API
│      ├── execution/
│          ├── database.py        # PostgreSQL connection + query runner
│      ├── llm/
│          ├── gemini_client.py   # Groq AI API wrapper
│          ├── prompts.py         # LLM prompt templates
│      ├── schemas/
│          ├── schema.py          ⭐ Define your tables here
│      ├── services/
│          ├── nl2sql.py          # Core pipeline logic
│      ├── validation/
│          ├── validator.py       # SQL validation (pure Python, no AI)

├── frontend/
│   ├── src/
│   │   ├── App.jsx        # React UI with charts
│   │   └── main.jsx       # Entry point
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── main.py                # CLI version (optional)
├── seed.sql                # sql tables and dummay data 
├── .env                   # Your secrets (never commit this)
├── .gitignore
└── requirements.txt
```

---

## 🔄 How It Works — End to End Flow

```
User types a question in plain English
             │
             ▼
┌─────────────────────────────────┐
│  Stage 1: Intent Extraction     │  ← Groq AI (LLM)
│                                 │
│  English → Structured JSON      │
│  {                              │
│    is_relevant: true,           │
│    target_tables: [...],        │
│    selected_columns: {...},     │
│    joins: [...],                │
│    conditions: [...],           │
│    aggregations: [...],         │
│    group_by: [...],             │
│    order_by: [...],             │
│    limit: null                  │
│  }                              │
└─────────────────────────────────┘
             │
             ▼
      Is question relevant?
        /           \
      NO             YES
       │               │
       ▼               ▼
  Tell user      ┌─────────────────────────────────┐
  which tables   │  Stage 2: SQL Generation        │  ← Groq AI (LLM)
  exist          │                                 │
                 │  Intent JSON + Schema → SQL     │
                 │                                 │
                 │  SELECT c.name, SUM(o.total)    │
                 │  FROM customers c               │
                 │  JOIN orders o ON ...           │
                 │  GROUP BY c.name                │
                 └─────────────────────────────────┘
                              │
                              ▼
                 ┌─────────────────────────────────┐
                 │  Stage 3: SQL Validation        │  ← Pure Python (NO AI)
                 │                                 │
                 │  ✓ Table names exist?           │
                 │  ✓ Column names exist?          │
                 │  ✓ GROUP BY complete?           │
                 │  ✓ SELECT + FROM present?       │
                 │  ✓ No invalid references?       │
                 └─────────────────────────────────┘
                         /           \
                    INVALID           VALID
                       │               │
                       ▼               ▼
                 Retry with      ┌─────────────────┐
                 error hints     │ Execute on      │
                 (up to 3x)      │ PostgreSQL      │
                                 └─────────────────┘
                                        │
                                        ▼
                                 Return results
                                 + Show in React UI
                                 as Table / Bar / Line / Pie chart
```

---

## 🗄️ Database Schema

6 tables with real relationships:

```
customers ──────────────── orders
    │                         │
    │                         │
    └──── reviews         order_items
              │                │
              │                │
           products ───────────┘
```

### Table Details

| Table | Description | Key Columns |
|-------|-------------|-------------|
| `customers` | Registered users | customer_id (PK), name, email, country, city, age, gender |
| `products` | Product catalog | product_id (PK), product_name, category, brand, price, stock, rating |
| `orders` | Purchase orders | order_id (PK), customer_id (FK), order_date, status, total_amount |
| `order_items` | Items in each order | item_id (PK), order_id (FK), product_id (FK), quantity, unit_price |
| `employees` | Staff members | employee_id (PK), name, department, role, salary, is_active |
| `reviews` | Product reviews | review_id (PK), customer_id (FK), product_id (FK), rating, review_text |

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-----------|
| AI / LLM | Groq API (llama-3.3-70b-versatile) |
| Backend | FastAPI (Python) |
| Database | PostgreSQL |
| DB Driver | psycopg2 |
| Frontend | React.js + Vite |
| Charts | Recharts |
| Validation | Pure Python + Regex (no AI) |

---

## 🚀 Setup Guide

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL installed and running
- Groq API key (free at [console.groq.com](https://console.groq.com))

---

### Step 1 — Clone the repository

```bash
git clone https://github.com/yourusername/NL_To_SQL.git
cd NL_To_SQL
```

### Step 2 — Create and activate virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate        # Linux/Mac
# .venv\Scripts\activate         # Windows
```

### Step 3 — Install Python dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Set up PostgreSQL database

```bash
# Create database
sudo -u postgres psql -c "CREATE DATABASE nl2sql_db;"

# Run seed file (creates all 6 tables + sample data)
sudo -u postgres psql -d nl2sql_db -f seed.sql
```

Or using pgAdmin:
1. Right click **Databases** → **Create** → **Database** → name it `nl2sql_db`
2. Open **Query Tool** → open `seed.sql` → press **F5**

### Step 5 — Configure environment variables

Create a `.env` file in the root folder:

```env
# Groq AI
GROQ_API_KEY=your_groq_api_key_here

# PostgreSQL
DB_HOST=localhost
DB_PORT=5432
DB_NAME=nl2sql_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password_here
```

### Step 6 — Start the FastAPI backend

```bash
uvicorn api:app --reload
```

API running at: **http://localhost:8000**
API docs at: **http://localhost:8000/docs**

## Docker & Kubernetes

Quick guide to build images locally and run with Docker Compose or deploy to Kubernetes.

- Build backend image:

```bash
docker build -f backend.Dockerfile -t nl2sql-backend:local .
```

- Build frontend image (from `frontend/`):

```bash
cd frontend
docker build -t nl2sql-frontend:local .
```

- Run locally with Docker Compose:

```bash
docker compose up --build
```

- Kubernetes manifests are in the `k8s/` folder. Example to apply locally (minikube/kind/GKE):

```bash
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/backend-service.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/frontend-service.yaml
```

Notes:
- Images in the manifests reference `nl2sql-backend:latest` and `nl2sql-frontend:latest` — push them to a registry or load them into your k8s cluster (e.g., `kind load docker-image` or `minikube image load`).
- If you want an Ingress or LoadBalancer, add an `ingress.yaml` or change service `type` to `LoadBalancer`.
### Step 7 — Start the React frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend running at: **http://localhost:3000**

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Check if API is running |
| GET | `/health` | Check API + database status |
| POST | `/ask` | Ask a natural language question |

### Example — Ask a question

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "show me all customers from India"}'
```

### Example Response

```json
{
  "question": "show me all customers from India",
  "intent": {
    "is_relevant": true,
    "target_tables": ["customers"],
    "selected_columns": { "customers": ["*"] },
    "conditions": [{ "column": "country", "operator": "=", "value": "India" }]
  },
  "sql": "SELECT * FROM customers WHERE country = 'India'",
  "validation": { "is_valid": true, "errors": [] },
  "db_result": {
    "success": true,
    "columns": ["customer_id", "name", "email", "country", ...],
    "rows": [...],
    "row_count": 5
  },
  "success": true,
  "message": "SQL generated and validated successfully.",
  "attempts": 1
}
```

---

## 💬 Example Questions to Try

```
show me all customers from India
which products have rating above 4.5?
how many orders are in delivered status?
top 5 customers by total order amount
list all employees in Sales department
show products with stock less than 50
which products were ordered in 2024?
show all reviews with rating 5
what is the average salary per department?
list all pending orders with customer names
which products have discount more than 15%?
show me customers who have placed more than 1 order
```

