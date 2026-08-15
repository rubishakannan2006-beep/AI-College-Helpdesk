# AI-Based College Helpdesk and Student Support Chatbot

This is a full-stack Flask application (TYBSc final-year project) that provides an AI FAQ-based chatbot for college students and an admin panel to manage FAQs and content.

See project structure and run instructions below.

## Run (Linux / macOS)

1. Create virtualenv

```bash
python3 -m venv venv
```

2. Activate

```bash
source venv/bin/activate
```

3. Install

```bash
pip install -r requirements.txt
```

4. Initialize DB and seed

```bash
python seed/seed_data.py
```

5. Run

```bash
python app.py
```

Default admin credentials: ADMIN_EMAIL and ADMIN_PASSWORD environment variables (defaults: admin@college.edu / admin123)
