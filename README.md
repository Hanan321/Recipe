🍽️ Arabic AI Chef

Arabic AI Chef is an interactive AI-powered Python application that generates traditional recipes from Arabic cities using real-time AI.

The user selects a city, and the system produces a complete dish description including ingredients, cooking steps, cost estimation, plating, and an image prompt.

🚀 Features
🌍 Choose from multiple Arabic cities
🤖 AI-generated recipes using OpenAI API
🧾 Structured output:
Ingredients
Recipe steps
Estimated cost
Plating description
Image prompt
🔁 Interactive loop (run multiple queries in one session)
🧼 Clean and simple user experience
🧠 How It Works
The user selects a city from a menu
The program maps the city to a traditional dish
A structured prompt is sent to the AI model
The AI generates a complete recipe dynamically
The result is displayed in a clean format

This simulates a simplified AI agent workflow:

Input → Processing → AI generation → Output
🛠️ Technologies Used
Python 🐍
Google Colab
OpenAI API
Prompt Engineering
⚙️ Setup Instructions
Clone the repository:
git clone https://github.com/your-username/your-repo-name.git
Open the notebook in Google Colab
Install dependencies:
!pip install openai
Run the notebook and enter your API key when prompted:
from getpass import getpass
import os

os.environ["OPENAI_API_KEY"] = getpass("Enter your API key: ")
🔐 Security Note
The API key is not stored in this repository
Users must provide their own API key at runtime
This follows best practices for API security
🌍 Supported Cities
Riyadh → Chicken Kabsa
Cairo → Koshari
Amman → Mansaf
Rabat → Chicken Tagine
Tripoli → Bazeen
Khartoum → Mulah
🎯 Project Goal

This project was built to:

Learn how AI-powered applications are designed
Practice integrating APIs into Python projects
Understand prompt engineering and structured outputs
Build a real-world AI prototype
📈 Future Improvements
Allow user to enter any city dynamically
Add multilingual support (Arabic/English)
Convert to a web app (Streamlit or Flask)
Add AI-generated food images
Save/export recipes
👩‍💻 Author

Hanan Elarabi
AI Enthusiast | Python Developer | Future AI Engineer
