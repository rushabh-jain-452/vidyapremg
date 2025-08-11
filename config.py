import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'vidhyaprem017@gmail.com')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'yourpassword')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your-openai-api-key')