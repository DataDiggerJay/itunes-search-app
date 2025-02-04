from flask import Flask, render_template_string, request, jsonify
import requests
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(get_remote_address, app=app, default_limits=["18 per minute"])

ITUNES_API_URL = "https://itunes.apple.com/search"

# Function to fetch results with a limit of 10
def search_itunes(term, media_type, limit=10):
    params = {
        "term": term,
        "media": media_type,
        "limit": limit,
        "country": "US"
    }
    response = requests.get(ITUNES_API_URL, params=params)
    results = response.json().get("results", [])
    return results

@app.route("/")
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>iTunes Search - Hackathon Edition</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css">
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <style>
            body { background-color: #121212; color: #fff; font-family: 'Arial', sans-serif; }
            .container { max-width: 800px; margin: auto; padding: 40px; }
            .search-box { background: #1e1e1e; padding: 15px; border-radius: 10px; }
            .search-box input, .search-box select { background: #252525; color: #fff; border: none; }
            .search-box input::placeholder { color: #bbb; }
            .card { background: #222; color: #fff; border-radius: 10px; transition: transform 0.2s; }
            .card:hover { transform: scale(1.05); box-shadow: 0px 0px 15px rgba(255, 255, 255, 0.2); }
            .btn-custom { background: #007bff; color: #fff; border: none; }
            .btn-custom:hover { background: #0056b3; }
            .no-results { color: #bbb; font-size: 18px; margin-top: 15px; }
        </style>
    </head>
    <body>
        <div class="container text-center">
            <h2 class="mb-4">🎵 iTunes Search App - Hackathon Edition 🎬</h2>

            <div class="search-box">
                <form id="searchForm" class="d-flex">
                    <input type="text" id="searchTerm" class="form-control me-2" placeholder="Search for music, movies, podcasts...">
                    <select id="mediaType" class="form-select me-2">
                        <option value="music">Music</option>
                        <option value="movie">Movies</option>
                        <option value="software">Apps</option>
                        <option value="audiobook">Audiobooks</option>
                        <option value="podcast">Podcasts</option>
                    </select>
                    <button type="submit" class="btn btn-custom">Search</button>
                </form>
            </div>

            <div id="results" class="mt-4"></div>
        </div>

        <script>
            $(document).ready(function () {
                $("#searchForm").submit(function (event) {
                    event.preventDefault();
                    
                    let term = $("#searchTerm").val();
                    let media = $("#mediaType").val();

                    if (term === "") {
                        alert("Please enter a search term!");
                        return;
                    }

                    $("#results").html("<p>Loading...</p>");

                    $.getJSON("/search?term=" + term + "&media=" + media, function (data) {
                        $("#results").html("");

                        if (data.length === 0) {
                            $("#results").html("<p class='no-results'>No results available</p>");
                            return;
                        }

                        data.forEach(item => {
                            let card = `
                                <div class="card p-3 mb-3 d-flex flex-row align-items-center">
                                    <img src="${item.artworkUrl100 || 'https://via.placeholder.com/100'}" class="me-3 rounded">
                                    <div>
                                        <h5>${item.trackName || item.collectionName || item.trackCensoredName}</h5>
                                        <p>By ${item.artistName}</p>
                                        <a href="${item.trackViewUrl}" target="_blank" class="btn btn-sm btn-info">View on iTunes</a>
                                    </div>
                                </div>
                            `;
                            $("#results").append(card);
                        });

                        if (data.length < 10) {
                            $("#results").append("<p class='no-results'>No more results available</p>");
                        }
                    });
                });
            });
        </script>
    </body>
    </html>
    """)

@app.route("/search", methods=["GET"])
@limiter.limit("18 per minute")  
def search():
    term = request.args.get("term", "")
    media_type = request.args.get("media", "music")
    results = search_itunes(term, media_type)
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
