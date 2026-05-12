# JobPortal – Full-Stack Recruitment Platform

JobPortal is a robust, production-ready web application built with **Python** and **Django**. It serves as a bridge between employers and job seekers, offering a seamless experience for posting, managing, and discovering career opportunities. The project emphasizes clean code architecture, data security, and a high-performance, responsive user interface.

## 🌟 Key Features

### 👤 User & Profile Management
- **Advanced Authentication:** Secure User Registration, Login, and Password Management.
- **Dynamic User Dashboard:** A centralized hub for users to manage their active job postings and personal profile settings.
- **Custom Sidebar Navigation:** Intuitive sidebar for quick access to "Active Notifications," "Profile Settings," and "Account Management."

### 💼 Job Management System
- **CRUD Functionality:** Users can Create, Read, Update, and Delete job listings with ease.
- **Automated Categorization:** Efficient organization of jobs by industry, location, and type (Full-time, Part-time, Remote).
- **Responsive Data Handling:** Custom-built logic that transforms complex data tables into interactive **Cards** on mobile devices for optimized readability.

### 🛠 Administrative Control
- **Custom Admin Interface:** Enhanced Django Admin panel for site moderators to oversee listings, verify users, and manage site categories.
- **Security & Validation:** Server-side form validation and CSRF protection to ensure data integrity.

## 🚀 Tech Stack

- **Backend:** Python , Django 
- **Frontend:** HTML5, CSS3, JavaScript 
- **UI Framework:** Bootstrap 5 (Mobile-First approach)
- **Database:** SQLite (Development) / PostgreSQL (Production ready)
- **Environment:** VS Code, Git/GitHub, Virtualenv

## 📂 Project Structure & Logic

- `models.py`: Architected with relational database logic involving `ForeignKey` relationships between Users, Jobs, and Categories.
- `views.py`: Implements Class-Based Views (CBVs) and Function-Based Views (FBVs) for efficient request handling.
- `context_processors.py`: Used for global data availability (like categories in the navbar).
- `static/css/`: Custom styles that override Bootstrap defaults to ensure a unique "Modern-UI" aesthetic.

