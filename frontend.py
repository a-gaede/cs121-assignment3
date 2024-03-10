from flask import Flask, request
from search import Search

# Default name for flask
app = Flask(__name__)
 

# Search and results page
@app.route('/',methods=['POST', 'GET'])
def run_search():
    # Fill html for landing page
    src = '<html><body><style>form{background-color: lightblue;padding:5px;}</style><form action = "http://localhost:5000/" method = "post"><p>Search The ICS Webserver:</p><p><input type="text" name = "query" placeholder="Search..." /></p><p><input type = "submit" value = "Submit" /></p></form></body></html>'
    query = request.form['query'] # Get query from form
    raw_results = Search(query) # Search for results
    results = src +"<pre>" + raw_results + "</pre>"
    return results

 
# main driver function
if __name__ == '__main__':
    app.run(debug=False)