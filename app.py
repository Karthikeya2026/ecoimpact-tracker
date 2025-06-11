import os
from app import create_app

if __name__ == '__main__':
    app = create_app()
    
    # Use PORT from environment variable, fallback to 5000 for local dev
    port = int(os.environ.get("PORT", 5000))

    # Bind to 0.0.0.0 to allow external access (Render needs this)
    app.run(host='0.0.0.0', port=port)
