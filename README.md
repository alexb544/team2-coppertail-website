# Coppertail Grooming Website

A full-stack Django web application for **Coppertail Grooming**, created as a Software Engineering course project. The website gives the business a centralized online presence that allows customers to explore services, manage their account, and book grooming appointments through all in one place.

## Contributors

- Melanie Fruciano
- Matthew Greenblatt
- Alex Blake
- Erynn Prado

## Overview

Coppertail Grooming is designed as an all-in-one website for a dog grooming business. The project combines customer-facing pages with account management and appointment scheduling, making it easier for users to move from browsing services to booking an appointment in one place.

From a development perspective, the application follows Django's **Model-View-Template (MVT)** pattern and splits into focused apps so the codebase stays understandable and maintainable.

## Feature Highlights

- Customer registration, login, logout, and password reset
- Account profile management
- Dog profile creation and editing
- Service browsing for available grooming options
- Appointment booking with confirmation flow
- Appointment cancellation for confirmed bookings
- Staff dashboard for managing services, time slots, and bookings
- Contact and FAQ pages for customer support content
- Image upload support for user and dog profiles

## User Flow

The primary customer experience on the site:

1. A user creates an account or signs in.
2. The user adds profile details and dog information.
3. The user goes to book an appointment and selects a date, time, dog, and service. 
4. The user reviews the booking and confirms it.

Staff users also have access to dashboard tools for maintaining services, appointment slots, and booking records.

## Tech Stack

- **Backend:** Python, Django
- **Database:** SQLite
- **Frontend:** Django templates, HTML, Tailwind CSS
- **Media handling:** Pillow

## Project Structure

This project is organized into several Django apps:

- `accounts`  
  Handles authentication, registration, account pages, dog management, contact, FAQ, and the main public-facing pages.

- `booking`  
  Handles appointment creation, confirmation, success pages, cancellation, and available time slot data.

- `services`  
  Stores and displays grooming service information.

- `dashboard`  
  Provides staff-only management tools for services, bookings, and time slots.

- `coppertail_website`  
  Contains project-level settings, root URL configuration, and deployment entry points.

## Key Pages and Routes

| Route | Purpose |
| ---   | ---     |
| 🏠 `/` | Home page |
| 🔐 `/login/` | User login |
| 📝 `/register/` | Account registration |
| ✂️ `/services/` | Grooming services |
| 📅 `/booking/new/` | Create a new appointment |
| 👤 `/account/` | Customer account page |
| 🛠️ `/dashboard/` | Staff dashboard |
| ℹ️ `/about/`, `/contact/`, `/faq/` | Supporting informational pages |

## Built With

- Django `6.0.2`
- Pillow `12.2.0`
- SQLite

See [requirements.txt](d:/Projects/coppertail-website/requirements.txt) for the current dependency list.

## Local Development Setup

### Prerequisites

- Python `3.12+`
- `pip`
- A virtual environment tool, such as `venv`

### 1. Create a virtual environment

```sh
python -m venv .venv
```

### 2. Activate the virtual environment

On Windows PowerShell:

```sh
.venv\Scripts\Activate.ps1
```

On Windows Git Bash:
```
source .venv/bin/activate
```

On macOS or Linux:

```sh
source .venv/bin/activate
```

### 3. Install project dependencies

```sh
pip install -r requirements.txt
```

### 4. Make & apply migrations

```sh
python manage.py makemigrations
```
```sh
python manage.py migrate
```

### 5. Start the development server

```sh
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/  <- also provided in your terminal
```

## Useful Commands

Run the full test suite:

```sh
python manage.py test
```

Create new migrations after model changes:

```sh
python manage.py makemigrations
```

Apply migrations:

```sh
python manage.py migrate
```

Create an admin user:

```sh
python manage.py createsuperuser
```

## Testing

The project includes Django test modules across multiple apps, including `accounts`, `services`, `booking`, and `dashboard`.

To run tests:

```sh
python manage.py test
```

## Development Notes

- The project uses SQLite for local development.
- Uploaded files are stored in the `media/` directory.
- Templates and static files are primarily organized within each app.
- The dashboard is intended for staff or admin users.

## Academic Context

This repository was developed as a college Software Engineering team project. The goal was to build a practical Django application using clear project structure, team collaboration, and iterative development practices that follow Agile SDLC practices that resemble a real-world workflow.
