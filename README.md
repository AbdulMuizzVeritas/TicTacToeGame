# Tic Tac Toe Game

A web-based Tic Tac Toe game built with Flask, featuring a computer opponent with AI strategy.

## Features

- Classic 3x3 Tic Tac Toe gameplay
- Play against a computer opponent
- Score tracking
- Win animations and confetti effects
- Responsive design
- Automatic game reset

## Setup

1. Clone the repository:
```bash
git clone <your-repository-url>
cd tic-tac-toe
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file and set your environment variables:
```
FLASK_APP=app
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
```

## Running Locally

1. Start the development server:
```bash
flask run
```

2. Open your browser and navigate to `http://localhost:5000`

## Deployment

### Using Gunicorn

1. Install Gunicorn:
```bash
pip install gunicorn
```

2. Run the application:
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Using a Production Server

1. Set up a reverse proxy (e.g., Nginx) to forward requests to your Gunicorn server
2. Configure your domain and SSL certificates
3. Set up a process manager (e.g., systemd) to keep the application running

## Project Structure

```
tic-tac-toe/
├── app.py              # Main application file
├── requirements.txt    # Project dependencies
├── .env               # Environment variables
├── .gitignore         # Git ignore file
└── README.md          # Project documentation
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 