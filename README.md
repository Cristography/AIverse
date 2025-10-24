# AI Prompt Library - Django Prototype

A simple full-stack Django web app prototype for discovering, sharing, and organizing AI prompts.

---

You can see the unique feature in this website that will be implmented is one of my past static projects: [live demo](https://cristography.github.io/PromptForge/)

and its github repo: [here](https://github.com/Cristography/PromptForge)

---


---

## Features

- Browse and search prompts with filters (category, difficulty, AI model)  
- User registration, login, and profile management  
- Submit prompts to share with the community  
- Bookmark favorite prompts  
- Dark/light theme toggle  
- English/Arabic language support  
- Copy prompt text to clipboard easily  
- Responsive design for all devices  

---

## Setup Instructions (Prototype)

1. Create and activate a Python virtual environment  
2. Install Django and Pillow (`pip install django pillow`)  
3. Create Django project and apps (`prompts`, `users`, `core`) inside an `apps` folder  
4. Set up templates and static folders as shown in the project structure  
5. Copy code files into appropriate locations  
6. Update `manage.py` to use `config.settings.dev`  
7. Run migrations and create a superuser  
8. Run the development server (`python manage.py runserver`)  
9. Add sample categories and prompts via Django admin at `/admin`  

---

## Notes

- This is a **prototype** project for demonstration and learning purposes  
- Uses SQLite database for easy development  
- Passwords are securely hashed by Django  
- CSRF protection and user sessions handled by default  
- Entirely server-side rendered—no API backend  

---

## Running the Project

python -m venv venv
source venv/bin/activate # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

Then open: `http://127.0.0.1:8000/`

---

## License

This project is for educational and prototype purposes only.

---

If you need help or want to contribute, feel free to contact me.

Enjoy exploring AI prompts! 🎉
