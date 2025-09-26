Jac Projects – Guess Game and Calculator

This repository contains two beginner-friendly projects written in the Jac Language:

Guess Game – A number guessing game that provides hints using AI language models.

Calculator – A simple calculator that performs basic arithmetic operations.

Both projects demonstrate how to use Jac walkers, nodes, and integrate LLMs through byllm and litellm.

Features
Guess Game

Generates a random number between 1 and 10.

Allows the player to make a guess.

Provides AI-generated hints when the guess is incorrect.

Prints a success message when the guess is correct.

Calculator

Performs basic arithmetic operations:

Addition

Subtraction

Multiplication

Division

Demonstrates walker logic for handling simple operations.

Requirements

Jac Language installed

Python 3.12 or higher

Virtual environment recommended

Dependencies: byllm and litellm

Install dependencies:

pip install byllm litellm

API Key Setup

For Gemini or GPT integration, export your API key in the terminal:

export GEMINI_API_KEY="your_api_key_here"


To make it permanent, add the line above to your ~/.bashrc or ~/.zshrc file.

Running the Projects

To run the Guess Game:

jac run guess_game6.jac


To run the Calculator:

jac run calculator.jac

Project Structure
.
├── guess_game6.jac        # Guess Game walker and setup
├── guess_game6.impl.jac   # Guess Game logic implementation
├── calculator.jac         # Calculator project
├── .gitignore             # Ignored files and directories
└── README.md              # Project documentation

Future Improvements

Extend calculator functionality with advanced operations such as modulus and exponents.

Add multiplayer capability to the Guess Game.

Store game scores or history in a database.

Author

This project was created by Neville Shem Amwayi.
For inquiries, you can reach me at shemneville0@gmail.com
.