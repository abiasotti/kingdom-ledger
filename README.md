# Kingdom Ledger

Kingdom Ledger is a Django-based real estate bookkeeping application designed for landlords and property managers who want powerful, clear, and lightweight tools without unnecessary bloat.

---

## Planned Features

### Dashboard (Home Page)

* Overview of all properties.
* Displays income, expenses, and net totals in a **Schedule E style category breakdown**.
* Aggregated totals for quick performance insights.

### Property Management

* Add, edit, and remove properties.
* Store essential details for each property (address, acquisition date, purchase price, etc.).
* View individual property performance metrics.

### Transactions Management

* Unified page to track **all income and expense entries**.
* Categorization of transactions according to Schedule E categories.
* Ability to filter by date, property, type, or vendor.
* Support for recurring transactions.

### Data Import & Export \*(Future)

* Import CSV/XLSX for bulk transaction entry.
* Export tax-ready reports.

### Multi-User Support *(Future)*

* Role-based permissions for property managers, accountants, and owners.

---

## Technology Stack

* **Backend:** Django (Python)
* **Frontend:** Django templates (with optional modern JS enhancements)
* **Database:** SQLite for development, PostgreSQL for production
* **Styling:** Tailwind CSS (planned)

---

## Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/kingdom-ledger.git
cd kingdom-ledger

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

---

## Development Roadmap

* [ ] Create base Django project & app structure
* [ ] Implement property model & management views
* [ ] Implement transaction model & unified transaction page
* [ ] Build dashboard page with Schedule E category aggregation
* [ ] Add basic authentication & user accounts
* [ ] Add data import/export functionality
* [ ] Deploy initial MVP
