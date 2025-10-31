# canchat-role-change-app

This app is a FastAPI application that allows testers to change their role in CANchat.

## Getting Started

To get started with running the app, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/canchat-role-change-app.git
   ```

2. **Navigate to the project directory**:
   ```bash
   cd canchat-role-change-app
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```

4. **Create a virtual environment with Conda**:
   ```bash
   conda create --name canchat-role-change python=3.12
   conda activate canchat-role-change
   ```

5. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

6. **Run the application**:
   ```bash
   fastapi dev app/main.py
   ```

Make sure you have Python, pip, and Conda installed on your machine.
