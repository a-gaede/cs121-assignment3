from flask import Flask, request, render_template
from search import Search

# Default name for flask
app = Flask(__name__)
 

# Search and results page
@app.route('/',methods=['POST', 'GET'])
def run_search():
    # Fill html for landing page
    if request.method == 'POST':
        query = request.form['query'] # Get query from form
        raw_results = Search(query) # Search for results
        results = render_template("search.html") +"<pre>" + raw_results + "</pre>"
        return results
    elif request.method == 'GET':
        return render_template("search.html")

 
# main driver function
if __name__ == '__main__':
    app.run(debug=False)