from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
import os


app = Flask(__name__)

# Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'chandrakantgadiluhar@gmail.com')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'b2296602')
mail = Mail(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/achievements')
def achievements():
    return render_template('achievements.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        
        # Send email
        msg = Message(
            subject=f"New Contact Form Submission from {name}",
            sender=email,
            recipients=['vidhyaprem017@gmail.com']
        )
        msg.body = f"""
        Name: {name}
        Email: {email}
        Phone: {phone}
        
        Message:
        {message}
        """
        mail.send(msg)
        
        return redirect(url_for('contact_success'))
    return render_template('contact.html')

@app.route('/contact/success')
def contact_success():
    return render_template('contact.html', success=True)

@app.route('/about-ai-chat', methods=['POST'])
def about_ai_chat():
    data = request.get_json()
    user_message = data['message']
    
    try:
        # Create a streaming response
        def generate():
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": """You are VidhyaPrem's career counseling assistant. 
                    Explain our services, team, and GROW methodology in under 50 words. 
                    Be professional yet friendly. Never say "As an AI model"."""},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                stream=True  # Enable streaming
            )
            
            full_response = ""
            for chunk in completion:
                if chunk.choices[0].delta.get('content'):
                    text_chunk = chunk.choices[0].delta['content']
                    full_response += text_chunk
                    yield f"data: {json.dumps({'chunk': text_chunk})}\n\n"
            
        return Response(generate(), mimetype='text/event-stream')
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)