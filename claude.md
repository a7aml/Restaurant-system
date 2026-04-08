# 🍽️ Arabic Restaurant Management System

## Project Overview
A full-stack web application for managing an Arabic restaurant.
Covers menu management, orders, tables, and customers.
Built with Flask + PostgreSQL using a clean layered architecture.

---

## Tech Stack
- **Backend:** Python 3.11+ / Flask
- **Database:** PostgreSQL + SQLAlchemy ORM
- **Frontend:** HTML5 + Jinja2 Templates + Tailwind CSS
- **Auth:** Flask-Login
- **Migrations:** Flask-Migrate (Alembic)
- **Environment:** python-dotenv (.env file)

---

## Project Structure
```
restaurant/
├── CLAUDE.md                ← You are here
├── run.py                   ← Entry point
├── config.py                ← App configuration classes
├── requirements.txt
├── .env                     ← Environment variables (DO NOT commit)
├── .env.example             ← Template for .env
├── migrations/              ← Alembic migration files (DO NOT edit manually)
├── tests/                   ← Unit tests
└── app/
    ├── __init__.py          ← App factory (create_app)
    ├── models/              ← Database models (SQLAlchemy)
    │   ├── __init__.py
    │   ├── user.py
    │   ├── menu_item.py
    │   ├── order.py
    │   ├── order_item.py
    │   └── table.py
    ├── routes/              ← Flask Blueprints (HTTP layer only)
    │   ├── __init__.py
    │   ├── auth.py
    │   ├── menu.py
    │   ├── orders.py
    │   └── tables.py
    ├── services/            ← Business logic layer
    │   ├── __init__.py
    │   ├── auth_service.py
    │   ├── menu_service.py
    │   ├── order_service.py
    │   └── table_service.py
    ├── templates/           ← Jinja2 HTML templates
    │   ├── base.html
    │   ├── auth/
    │   ├── menu/
    │   ├── orders/
    │   └── tables/
    └── static/              ← CSS, JS, Images
        ├── css/
        ├── js/
        └── images/
```

---

## Architecture Rules — STRICT

### Layer Responsibilities

| Layer | Responsibility | What it CANNOT do |
|-------|---------------|-------------------|
| **Models** | Define DB schema & relationships only | No business logic |
| **Routes** | Handle HTTP requests/responses, call services | No direct DB queries |
| **Services** | All business logic & DB operations via models | No HTTP/request handling |
| **Templates** | Render HTML using Jinja2 | No logic beyond display |
| **Static** | CSS, JS, images | — |

### Golden Rules
- ✅ Routes → call Services → Services → call Models
- ✅ Routes ONLY handle: request parsing, calling service, returning response
- ✅ Services contain ALL business logic
- ✅ Every route must have a matching service function
- ❌ NEVER write DB queries inside routes
- ❌ NEVER write business logic inside models
- ❌ NEVER import `request` inside services

---

## Database Models

### User
```
id, username, email, password_hash, role (admin/waiter/kitchen), created_at
```

### MenuItem
```
id, name_ar, name_en, description_ar, description_en,
price, category, image_url, is_available, created_at
```

### Table
```
id, table_number, capacity, status (available/occupied/reserved)
```

### Order
```
id, table_id, user_id, status (pending/preparing/ready/delivered/cancelled),
total_price, notes, created_at, updated_at
```

### OrderItem
```
id, order_id, menu_item_id, quantity, unit_price, notes
```

---

## Coding Standards

### Python / Flask
- Use **type hints** on all functions
- Use **f-strings** for string formatting
- All service functions must have **docstrings**
- Use **try/except** in services for all DB operations
- Services always return a tuple `(data, error)` pattern:

```python
def get_all_menu_items() -> tuple[list, str | None]:
    """Get all available menu items from the database."""
    try:
        items = MenuItem.query.filter_by(is_available=True).all()
        return items, None
    except Exception as e:
        return [], str(e)
```

### Routes Pattern
```python
@menu_bp.route('/menu', methods=['GET'])
def get_menu():
    items, error = menu_service.get_all_menu_items()
    if error:
        flash('Error loading menu. Please try again.', 'danger')
        return redirect(url_for('main.index'))
    return render_template('menu/index.html', items=items)
```

### Naming Conventions
- **Models:** PascalCase → `MenuItem`, `OrderItem`
- **Functions:** snake_case → `get_order_by_id()`
- **Routes:** kebab-case URLs → `/menu-items`, `/active-orders`
- **Templates:** snake_case folders → `menu/item_detail.html`
- **Arabic content fields:** suffix `_ar` → `name_ar`, `description_ar`
- **English content fields:** suffix `_en` → `name_en`, `description_en`

---

## Environment Variables (.env)
```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://username:password@localhost:5432/restaurant_db
```

---

## UI / Frontend Rules
- **Language:** Arabic UI — always use `dir="rtl"` on `<html>` tag
- **Font:** Cairo or Tajawal from Google Fonts
- **Styling:** Tailwind CSS via CDN
- **Color theme:** Warm tones — amber, orange, brown (restaurant-appropriate)
- **Flash messages:** Display in Arabic
- All forms must have **CSRF protection** via Flask-WTF

---

## Do NOT Touch
- `migrations/` folder — only interact via `flask db migrate` and `flask db upgrade`
- `.env` file — never commit to git, always add to `.gitignore`
- `app/__init__.py` create_app structure — ask before modifying

---

## Commands Reference
```bash
# Run the app
python run.py

# Database migrations
flask db init
flask db migrate -m "describe your change here"
flask db upgrade

# Install dependencies
pip install -r requirements.txt
```

---

## Adding a New Feature — Always Follow This Order
1. Create or update the **Model**
2. Run database **migration**
3. Write **Service** functions with all business logic
4. Create the **Route** that calls the service
5. Create the **Template** for the view
6. Add any required **Static** files (CSS/JS)