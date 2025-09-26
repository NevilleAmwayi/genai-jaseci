Jac Projects – Guess Game & Calculator

This repository contains two beginner-friendly projects written in Jac Language:

🎲 Guess Game – A number guessing game that gives fun AI-generated hints using LLMs (Gemini or GPT).

➗ Calculator – A simple calculator that performs basic arithmetic operations.

Both projects demonstrate how to combine Jac walkers, nodes, and LLM integration using byllm and litellm.

🚀 Features
Guess Game

Random number generated between 1 and 10.

Player guesses the number.

If the guess is wrong, the AI provides a fun hint.

If correct → 🎉 Congratulations message.

Calculator

Supports basic operations:

Addition

Subtraction

Multiplication

Division

Demonstrates Jac walker logic for handling input.

🛠️ Requirements

Jac Language
 installed

Python 3.12+

Virtual environment (.env) recommended

byllm and litellm for LLM integration

Install dependencies:

pip install byllm litellm

🔑 API Key Setup (for Gemini / GPT)

Export your Gemini key (or other provider key) in terminal:

export GEMINI_API_KEY="your_api_key_here"


Make it permanent by adding it to ~/.bashrc or ~/.zshrc.

▶️ Running the Projects
Guess Game
jac run guess_game6.jac

Calculator
jac run calculator.jac

📂 Project Structure
.
├── guess_game6.jac        # Main Guess Game walker + setup
├── guess_game6.impl.jac   # Game logic implementation
├── calculator.jac         # Simple calculator project
├── .gitignore             # Git ignored files (env, cache, etc.)
└── README.md              # Project documentation

✨ Future Improvements

Add more operations to the calculator (exponents, modulus).

Make the Guess Game multiplayer.

Store game scores in a database.

👤 Author

Neville Shem Amwayi

💼 GitHub

📧 shemneville0@gmail.com