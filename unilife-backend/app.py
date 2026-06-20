from flask import Flask, request, jsonify
from flask_cors import CORS
from search import search  

app = Flask(__name__)
CORS(app)  

@app.route("/search", methods=["GET"])
def search_route():
    query = request.args.get("q", "")
    
    if not query.strip():
        return jsonify([])  
    
    results = search(query)
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)