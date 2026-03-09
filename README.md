# Coppertail Website
**Team Members:** `Melanie Fruciano`, `Matthew Greenblatt`, `Alex Blake`, and `Erynn Prado`  

## Overview
A web application project using the Django Framework as part of our Software Engineering course. 

This project aims to provide an 'all-in-one' online presence for Coppertail Grooming, a dog grooming business. Allowing users to navigate services, interact with the site, and securely authenticate through a login system.

Follows Agile development practices with two week sprints focused on planning, development, testing, and improvement.

## Current Goals
**Features:**
- [x] Account Creation
- [ ] Service Creation
- [x] Appointment Tracking 
- [x] Appointment Booking

**Webpages:**
- [x] Home
- [x] Log-in
- [x] Sign-up
- [ ] Services
- [ ] About Us 

## Technologies Used
- `Python` 
- `Django`  
- `HTML/CSS`
- `GitHub`

## Project Architecture
The application follows Django’s `Model-View-Template` (MVT) architecture.

## Initial Setup

### 1. Clone this Repository and Navigate to the Root Directory 
```sh
git clone "https://github.com/alexb544/team2-coppertail-website.git"

cd coppertail-website
```

### 2. Create and Activate Virtual Enviroment
```sh
python -m venv .venv

source .venv\Scripts\activate
```
### 3. Install Missing Dependencies
```sh
pip install -r requirements.txt
```

### 4. Apply Migrations
```sh
python manage.py migrate
```

### 5. Run the Development Server
```sh
python manage.py runserver
```

### 6. Follow the Link provided to open in your Browser:
```sh
http://127.0.0.1:8000/
```

### Branching Strategy
The project uses a feature-branch workflow:
- `development` – The current, most up-to-date, branch — ready for production.  
- `feature/feature-name` – branches for new features being worked on — merged into `development` upon pull request approval. 




