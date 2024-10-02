from app import app
from dotenv import load_dotenv
import os

load_dotenv()
port = os.getenv('PORT') or 4000

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=port)