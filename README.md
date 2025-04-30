# MessageTranslator 📝🌍
A translator in the chat app

## 🛠️ Setup Instructions

Follow these steps to set up and run the Django project:

1️⃣ Clone the Repository
If you haven't cloned the project yet, run:

`git clone https://github.com/MeghashyamRavuru/MessageTranslator.git`<br>
`cd MessageTranslator`

2️⃣ Create a Virtual Environment

`python3 -m venv venv`<br>
`source venv/bin/activate`  # On Windows, use: `venv\Scripts\activate`

3️⃣ Installations

`pip3 install -r requirements.txt`<br>
`sudo apt install redis-server`<br>


4️⃣ Apply Migrations

Before migrations you have to update your mysql password.

MessageTranslator -> settings.py

`python3 manage.py makemigrations`<br>
`python3 manage.py migrate`

5️⃣ Run the Server
Start the Django development server:

`python3 manage.py runserver 0.0.0.0:8000`<br><br>
Now open http://127.0.0.1:8000/ in your browser. 🎉
