from flask import Flask, render_template, request, redirect, url_for, flash
import os
from dotenv import load_dotenv
from supabase import create_client
import postgrest
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()  # Load environment variables

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generates a random secret key

supaURL = os.getenv("SUPA_URL")
supaKey = os.getenv("SUPA_KEY")
supabase = create_client(supaURL,supaKey)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

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

        welcome  = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to VOLT</title>
</head>
<body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; margin: 0;">
    <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);">
        <div style="text-align: center; padding-bottom: 20px;">
            <img src="https://drive.google.com/uc?export=view&id=1ravESqgux1BWw73aRDQjrLDZmpJxE2_k" alt="VOLT Logo" style="max-width: 200px; height: auto;">
        </div>
        <h2 style="color: #333333;">Welcome to VOLT – Your Go-To Source for Market Volatility Insights</h2>
        <br>
        <p style="font-size: 16px; color: #333333;">
            Welcome to <strong>VOLT</strong>! We're excited to have you join our community of active market participants. You'll now receive weekly updates, designed to keep you ahead of the curve on market volatility.
        </p>
        <h3 style="color: #333333;">Here’s what you can expect:</h3>
        <ul style="font-size: 16px; color: #333333;">
            <li><strong>Market-moving insights:</strong> Stay informed with in-depth analysis on volatility trends and the earnings impact on the market.</li>
            <li><strong>Actionable data:</strong> Access critical data to guide your trading decisions, whether you're monitoring major indices or specific sectors.</li>
        </ul>
        <p style="font-size: 16px; color: #333333;">
            Our next issue will hit your inbox this Sunday, so keep an eye out!
        </p>
        <p style="font-size: 16px; color: #333333;">
            If you have any questions, feedback, or topics you'd like us to cover, feel free to reach out at 
            <a href="mailto:help@voltvolatility.com" style="color: #0073e6;">help@voltvolatility.com</a>. We're always happy to hear from you.
        </p>
        <p style="font-size: 16px; color: #333333;">
            Thank you for subscribing to VOLT, where volatility meets opportunity.
        </p>
        <br>
        <p style="font-size: 16px; color: #333333;">Best regards,</p>
        <p style="font-size: 16px; color: #333333;">The VOLT Team</p>
        <p style="font-size: 16px; color: #333333;">
            <a href="https://voltvolatility.com" style="color: #0073e6;">voltvolatility.com</a>
        </p>
    </div>
</body>
</html>
        '''
        message = Mail(
        from_email='Volt@voltvolatility.com',
        to_emails=email,
        subject='Welcome to VOLT – Your Go-To Source for Market Volatility Insights',
        html_content=welcome)

        try:
            sg = SendGridAPIClient(os.getenv('EMAIL_KEY'))
            response = sg.send(message)
            print(response.status_code)
        except Exception as e:
            print(e)
    except postgrest.exceptions.APIError:
        flash('This email is already registered.')
    except Exception as e:
        flash('An error occurred. Please try again later.')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)