🎵 iTunes Search App - Hackathon Edition 🎬

A simple Flask web app to search for music, movies, and podcasts using the iTunes API.

--------------------------
🚀 Features:
--------------------------
- Search iTunes for music, movies, podcasts, audiobooks, and apps.
- Modern dark-themed UI with Bootstrap.
- Fast and smooth AJAX-powered search.
- API rate-limited to 18 requests per minute (prevents abuse).
- Responsive design for mobile and desktop.

--------------------------
📜 Installation:
--------------------------
1. Clone this repository:
   $ git clone https://github.com/DataDiggerJay/itunes-search-app
   $ cd itunes-search-app

2. Install dependencies:
   $ pip install -r requirements.txt

3. Run the Flask app:
   $ python app.py

4. Open in your browser:
   http://127.0.0.1:5000/

--------------------------
📡 API Usage:
--------------------------
The `/search` endpoint fetches results from iTunes.

GET request format:
   /search?term=QUERY&media=TYPE

Example:
   /search?term=Eminem&media=music

Supported media types:
   - music
   - movie
   - software (apps)
   - audiobook
   - podcast

--------------------------
⚖️ License:
--------------------------
MIT License - Free to use, modify, and distribute.

--------------------------
👨‍💻 Contributors:
--------------------------
- Jayesh Berde (@https://github.com/DataDiggerJay)

--------------------------
⭐️ Support:
--------------------------
Like this project? ⭐ Star it on GitHub!
