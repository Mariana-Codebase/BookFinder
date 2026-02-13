# 📚 BookFinder

**BookFinder** is a Flask-based web application that integrates a MySQL relational database with the Spanish Wikipedia API to enrich book search results with real-time summaries.

Built as an academic project with a strong focus on backend integration, API consumption, and environment-based configuration.

---

## 🔎 Overview

This project demonstrates:

* Server-side search functionality using Flask
* Relational database querying with MySQL
* External API integration (Spanish Wikipedia)
* Environment variable configuration using `.env`
* Clean separation between backend logic and templates

The application allows users to search for books stored in a database and dynamically enhances results with contextual summaries from Wikipedia.

---

## 🧠 Technical Highlights

* REST-style routing with Flask
* Secure configuration via environment variables
* MySQL integration using `mysql-connector-python`
* External API consumption with `wikipedia-api` and `requests`
* Jinja2 templating engine
* Structured dependency management via `requirements.txt`
* Prepared for future GraphQL expansion (`graphene`, `flask-graphql`)

---

## 🏗 Architecture

```
User → Flask Route → MySQL Query
                    ↓
             Wikipedia API Request
                    ↓
          Jinja2 Template Rendering
```

Flow:

1. User submits a book title.
2. Backend queries the `libro` table.
3. For each result, a Spanish Wikipedia summary is retrieved.
4. Results are rendered dynamically in the frontend.

---

## 🛠 Tech Stack

**Backend**

* Python 3
* Flask

**Database**

* MySQL
* mysql-connector-python

**API Integration**

* wikipedia-api
* requests

**Frontend**

* HTML
* CSS
* Font Awesome
* Google Fonts

**Utilities**

* python-dotenv
* httpx
* beautifulsoup4

---

## ⚙️ Installation & Setup

### 1️⃣ Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 2️⃣ Configure environment variables

Create a `.env` file based on the example:

**Windows**

```bash
copy config\env.example .env
```

**macOS/Linux**

```bash
cp config/env.example .env
```

Add your database credentials:

```
DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASS=
```

---

### 3️⃣ Run the application

```bash
python app.py
```

Open your browser:

```
http://127.0.0.1:5000/
```

---

## 🗄 Database Requirements

* MySQL installed and running
* A database containing a table named `libro`
* The `libro` table must include at least:

  * `nombre` (book title)

---

## 📌 Design Decisions

* Credentials are stored in environment variables (not hardcoded).
* Wikipedia language defaults to Spanish (`es`) to match dataset context.
* Debug mode is enabled for development.
* GraphQL dependencies included for future scalability.

---

## 🚀 Future Improvements

* Docker containerization
* Pagination support
* Caching Wikipedia responses
* REST API endpoint exposure
* Deployment configuration (Render, Railway, AWS)
* Unit and integration testing
* Full GraphQL implementation

---

## 👩‍💻 Author

Mariana Sinisterra
Informatics Engineering Student
Backend Development • Automation • Scalable Systems
