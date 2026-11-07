
<div align="center">

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:071B18,50:064E3B,100:10B981&height=190&section=header&text=STOCK%20MANAGEMENT&fontSize=42&fontColor=FFFFFF&fontAlignY=42&desc=Inventory%20Control%20%7C%20Business%20Operations%20%7C%20Stock%20Intelligence&descAlignY=65&descSize=14" width="100%"/>

<br/>

# 📦 Stock Management System

### Inventory Control • Product Tracking • Business Operations

<p>
  <img src="https://img.shields.io/badge/Python-3.0%2B-3776AB?style=flat-square&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Flask-3.0.3-000000?style=flat-square&logo=flask&logoColor=white"/>
  <img src="https://img.shields.io/badge/Database-SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white"/>
  <img src="https://img.shields.io/badge/ORM-SQLAlchemy-D71F00?style=flat-square"/>
  <img src="https://img.shields.io/badge/Interface-Web%20Application-10B981?style=flat-square"/>
</p>

**A web-based inventory management application designed to organize products, manage suppliers, track transactions, and maintain stock records.**

<br/>

[Explore Repository](https://github.com/rohanthanuj06-rgb/STOCK_MANAGEMENT_SYSTEM) • [Report an Issue](https://github.com/rohanthanuj06-rgb/STOCK_MANAGEMENT_SYSTEM/issues)

</div>

---

## 🟢 01 — Project Overview

Managing inventory requires accurate product records, organized supplier information, transaction tracking, and visibility into stock availability.

The **Stock Management System** is a Flask-based web application developed to bring these operations together through a centralized inventory management platform.

The application organizes essential business operations, including product management, supplier records, sales, purchase orders, invoice handling, and stock auditing.

Rather than maintaining disconnected records, the system uses a structured database-backed approach to manage inventory information and transaction history.

### Project Objectives

- Centralize product and inventory information.
- Organize supplier and purchase records.
- Manage sales-related transactions.
- Monitor available, reserved, and damaged stock.
- Maintain records of inventory changes.
- Provide authenticated access to application functionality.

---

## 🧩 02 — Core Modules

<table>
<tr>
<td width="50%">

### 📊 Dashboard
Centralized entry point for accessing inventory and business operations.

### 📦 Product Management
Organize product details, SKU identifiers, categories, prices, and stock information.

### 🏷️ Category Management
Group products into structured categories.

### 🚚 Supplier Management
Maintain supplier contact details and supplier-related purchase information.

</td>
<td width="50%">

### 💰 Sales Management
Maintain sales transactions and associated product quantities.

### 🛒 Purchase Management
Organize supplier purchase orders and their statuses.

### 🧾 Invoice Management
Dedicated application module for invoice-related operations.

### 📋 Stock Audit
Record inventory changes, quantities, reasons, and associated users.

</td>
</tr>
</table>

---

## 📦 03 — Inventory Tracking

The application maintains different stock states for products.

| Stock Attribute | Description |
|---|---|
| Available Stock | Quantity currently available |
| Reserved Stock | Quantity reserved for other operations |
| Damaged Stock | Quantity marked as damaged |
| Minimum Threshold | Configured minimum stock level |

### Stock Status Logic

The application determines product availability using its stock status logic:

| Condition | Status |
|---|---|
| Available stock ≤ 0 | 🔴 Out of Stock |
| Available stock ≤ Minimum Threshold | 🟡 Low Stock |
| Available stock > Minimum Threshold | 🟢 In Stock |

This helps identify products that require attention.

---

## 🔄 04 — Application Workflow

```mermaid
flowchart TD
    A([Start Application]) --> B[User Authentication]
    B --> C[Dashboard]
    C --> D[Product Management]
    C --> E[Supplier Management]
    C --> F[Sales Management]
    C --> G[Purchase Management]
    C --> H[Invoice Management]
    D --> I[Inventory Records]
    E --> J[Supplier Records]
    F --> K[Sales Transactions]
    G --> L[Purchase Orders]
    I --> M[Stock Audit Log]
    K --> M
    L --> M
    M --> N[(SQLite Database)]
    J --> N
    H --> N
```

The application uses Flask routes and database models to organize the different modules.

---

## 🏗️ 05 — Technical Architecture

The application follows a modular Flask architecture.

```text
                 USER
                   |
                   v
          Flask Web Application
                   |
          ---------------------
          |         |         |
       Routes    Templates   Static
          |         |        CSS
          |
          v
       SQLAlchemy
          |
          v
       SQLite DB
          |
     Business Records
```

### Repository Structure

```text
STOCK_MANAGEMENT_SYSTEM/
│
├── routes/
│   ├── auth.py
│   ├── dashboard.py
│   ├── products.py
│   ├── suppliers.py
│   ├── sales.py
│   ├── purchases.py
│   ├── audit.py
│   └── invoices.py
│
├── static/
│   └── css/
│
├── templates/
│
├── utils/
│
├── app.py
├── config.py
├── extensions.py
├── models.py
├── init_db.py
├── seed_users.py
├── requirements.txt
└── stock_management.db
```

---

## ⚙️ 06 — Technology Stack

| Technology | Application |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| Flask-SQLAlchemy | Database integration |
| SQLite | Data storage |
| Flask-Login | User authentication |
| Flask-Migrate | Database migrations |
| Flask-WTF | Form handling |
| Werkzeug | Password hashing and security utilities |
| HTML / CSS | Web interface |
| Git & GitHub | Version control |

---

## 🚀 07 — Installation & Setup

### Prerequisites

- Python installed
- Git installed
- A code editor such as VS Code

### Step 1 — Clone the Repository

```bash
git clone https://github.com/rohanthanuj06-rgb/STOCK_MANAGEMENT_SYSTEM.git
```

### Step 2 — Navigate to the Project

```bash
cd STOCK_MANAGEMENT_SYSTEM
```

### Step 3 — Create a Virtual Environment

```bash
python -m venv venv
```

Activate it:

**Windows**
```bash
venv\Scripts\activate
```

**Linux / macOS**
```bash
source venv/bin/activate
```

### Step 4 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5 — Initialize the Database

Review `config.py` and `init_db.py` for the project's database initialization requirements before running the application.

### Step 6 — Run the Application

```bash
python app.py
```

Open the local address displayed by Flask in your browser.

---

## 🔐 08 — Data & Authentication

The project includes an authentication model with:

- Username and email fields.
- Password hashing using Werkzeug.
- Flask-Login integration.
- User roles: Admin, Manager, and Staff.

The application also maintains structured records for products, suppliers, sales, purchase orders, and stock audit activity.

**Security note:** Configure a secure Flask secret key before deployment. Do not expose production credentials or sensitive configuration in the repository.

---

## 🖥️ 09 — Screenshots & Demonstration

Screenshots can be added here to demonstrate the actual application interface.

Suggested repository organization:

```text
assets/
└── screenshots/
    ├── login.png
    ├── dashboard.png
    ├── products.png
    ├── suppliers.png
    ├── sales.png
    ├── purchases.png
    └── stock-audit.png
```

Once screenshots are added, display them using:

```markdown
![Dashboard](assets/screenshots/dashboard.png)
```

---

## 🧠 10 — Engineering Concepts Demonstrated

- Modular application development using Flask Blueprints.
- Relational database modeling.
- Object-relational mapping with SQLAlchemy.
- Authentication and password hashing.
- Inventory state management.
- Transaction and purchase-order modeling.
- Database relationships.
- Audit logging.
- Separation of application routes, templates, and static resources.

---

## 🔮 11 — Future Development Roadmap

- [ ] Advanced inventory analytics and visual reports.
- [ ] Low-stock notifications.
- [ ] Exportable inventory and sales reports.
- [ ] Improved search and filtering.
- [ ] Barcode-based product identification.
- [ ] Enhanced role and permission management.
- [ ] Automated backup and deployment support.
- [ ] Responsive dashboard improvements.

---

## 👨‍💻 12 — Developer

<div align="center">

### Rohan Thanuj P.

**B.Tech Information Technology | K. Ramakrishnan College of Engineering**

Interested in building practical software applications through programming, structured engineering, and continuous learning.

<br/>

<a href="https://github.com/rohanthanuj06-rgb">
  <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white"/>
</a>
<a href="https://www.linkedin.com/in/rohan-thanuj-9b451b352">
  <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white"/>
</a>

<br/><br/>

**Designed to bring inventory operations into one organized system.**

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:10B981,50:064E3B,100:071B18&height=70&section=footer" width="100%"/>

</div>
