# Recruitment & Labor Market Engine

A backend-heavy platform designed to bridge the gap between job seekers and employers. Built with a focus on domain-driven logic and regulatory compliance, automating the full recruitment lifecycle from resume parsing to final placement.

## Tech Focus

*   **Django-powered Core**: Utilizing ORM for complex relational data (KVED industries, education specialties, and geographic locations).
*   **State-Driven Logic**: Robust status management for vacancies and applications, ensuring data integrity across the entire workflow.
*   **Modular Architecture**: Separated apps for dictionaries, location services, and core business logic for better maintainability.
*   **Modern Tooling**: Managed by **uv** for ultra-fast, reproducible dependency management.

## Key Engineering Challenges

*   **Compliance Integration**: Mapping regional labor laws into hardcoded business rules and state machine transitions.
*   **Data Normalization**: Handling extensive industry classifications and educational standards through a unified dictionary system.
*   **Access Control**: Role-based logic for candidates, recruiters, and platform admins.

## Status: Active MVP
The project is currently in the active development phase, focusing on expanding the reporting engine and matching algorithms.

---

## Installation

### Prerequisites
- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

### Setup

```bash
# Clone the repository
git clone https://github.com/dmitrysdevfs/job-app.git
cd job-app

# Sync dependencies
uv sync

# Configure environment
# Create .env with DJANGO_SECRET_KEY and ENV=dev

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```
