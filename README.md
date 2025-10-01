# 🛒 Grocery List App #

## Project Overview ##

This Grocery List App is a minimal software application built with FastAPI and SQLite.
It allows users to manage their grocery list through a RESTful API, supporting operations such as:
- Add new grocery items
- View all items
- Update item details
- Mark items as purchased
- Delete items

This project was developed as part of the DevOps Pipeline Design assignment, following the Software Development Life Cycle (SDLC) approach.

## Tech Stack ##

- **Backend:** Python (FastAPI)
- **Database:** SQLite
- **Frontend:** HTML + JavaScript 

## Setup Instructions ##
1. Clone the repository

`git clone https://github.com/SofiaBc004/grocery_list.git`

2. Create and activate a virtual environment

``` 
python3 -m venv venv
source venv/bin/activate    # Mac/Linux
venv\Scripts\activate       # Windows 
```

3. Install dependencies

`pip install -r requirements.txt`

4. Run the application

`uvicorn app.main:app --reload`

5. Access the API
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Frontend Instructions ##
The project also includes a simple frontend (HTML + JavaScript) that allows users to interact with the grocery list visually.
1. Start the backend (see setup instructions above).
2. Serve the frontend:
   - Option A: In VS Code, right-click `frontend/index.html` → **Open with Live Server** (extension needed).
   - Option B: Run a simple Python server:
     ```
     cd frontend
     python3 -m http.server 5500
     ```
     Then open [http://127.0.0.1:5500/index.html](http://127.0.0.1:5500/index.html) in your browser.

3. Features in the frontend:
   - Add grocery items
   - Delete grocery items
   - Mark/unmark items as purchased
   - Items grouped by category (e.g., fruit, dairy, vegetables)
   - Search by name or ID


## Project Structure ##
```
grocery_list/
│── app/
│   ├── __init__.py
│   ├── main.py        # FastAPI entry point
│   ├── models.py      # Data schema (models)
│   ├── crud.py        # Database operations (CRUD)
│   ├── db.py          # SQLite connection and table setup
│
│── frontend/          # HTML + JS frontend interface
│── docs/              # SDLC documentation (planning, requirements, design)
│── grocery.db         # SQLite database (auto-created, ignored in .gitignore)
│── requirements.txt   # Python dependencies
│── README.md
```
## API Endpoints ##

| Method | Endpoint             | Description              |
|--------|----------------------|--------------------------|
| POST   | `/items`             | Create a new grocery item |
| GET    | `/items`             | Get all grocery items     |
| GET    | `/items/{id}`        | Get item by ID           |
| PATCH  | `/items/{id}`        | Update an item           |
| PATCH  | `/items/{id}/toggle` | Toggle purchased status  |
| DELETE | `/items/{id}`        | Delete an item           |

## Future Improvements ##
- Add user authentication
- Containerize with Docker for DevOps pipeline integration
- Deploy to cloud (Azure, AWS)

## Author ##
Sofia Boicenco

BCSAI, 3rd Year student at IE University