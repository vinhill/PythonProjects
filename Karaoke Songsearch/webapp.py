import pandas as pd
from flask import Flask, request, render_template,jsonify
from sqlalchemy import create_engine

app = Flask(__name__)

def query(str, limit=20):
    engine = create_engine("sqlite:///songs.db", echo=False)
    result = engine.execute(
                f"SELECT Source, Artist, Song \
                FROM Songlist \
                WHERE Source LIKE ? OR Artist LIKE ? OR Song LIKE ? \
                LIMIT ?", 
                f"%{str}%", f"%{str}%", f"%{str}%", limit).fetchall()
    df = pd.DataFrame(result, columns=["Source", "Artist", "Song"])
    return df

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/join', methods=['GET','POST'])
def my_form_post():
    webin = request.form['query']
    word = request.args.get('query')
    limit = request.form['limit']
    output = query(webin, limit).to_string()
    result = {
        "output": output
    }
    result = {str(key): value for key, value in result.items()}
    return jsonify(result=result)

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0")