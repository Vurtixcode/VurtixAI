🚀 How to use
Using Vurtix AI is very simple:

Run the program:

Wait for the AI model to load. It may take a few seconds.

Write your prompt in the window that appears or in the console.

For example: "Write a function in Python that checks if a string is a palindrome"

Press Generate (or Enter) to start the generation.

Ready! Vurtix AI will write the code and display it on the screen.

Example of work:

> Enter your request: write a Python CSV file parser using pandas
[Vurtix AI generates...]

import pandas as pd

def parse_csv(file_path):
 """
 Reads a CSV file and returns a DataFrame.
 
 Args:
 file_path (str): Path to the CSV file.
 
 Returns:
 pd.DataFrame: DataFrame with data from the file.
 """
 try:
 data = pd.read_csv(file_path)
 return data
 except FileNotFoundError:
 print(f"Error: File {file_path} not found.")
 return None

# Example of use
# df = parse_csv('data.csv')
# print(df.head())
How it will look in the full README (using the short version as an example):
Vurtix AI 🤖✨
Your AI partner for writing code. Just describe what you need, and Vurtix AI will generate the code for you in the programming language of your choice.

🚀 How to use
Run the program: python app.py

Wait for the model to load

Write your request (for example, "write a Python function to check for a palindrome")
