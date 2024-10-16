from flask import Flask, render_template, request, redirect, url_for, flash
import os
from dotenv import load_dotenv
from supabase import create_client
import postgrest

load_dotenv()  # Load environment variables

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generates a random secret key

supaURL = os.getenv("SUPA_URL")
supaKey = os.getenv("SUPA_KEY")
supabase = create_client(supaURL,supaKey)

# Routes
@app.route('/')
def index():
    return render_template('test.html')

@app.route('/submit', methods=['POST'])
def submit():
    email = request.form['email']
    
    if not email:
        flash('Email is required!')
        return redirect(url_for('index'))
    
    try:
        # Insert email into the database
        supabase.table('emails').insert({'email':email}).execute()
        flash('Email successfully submitted!')
    except postgrest.exceptions.APIError:
        flash('This email is already registered.')
    except Exception as e:
        flash('An error occurred. Please try again later.')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)