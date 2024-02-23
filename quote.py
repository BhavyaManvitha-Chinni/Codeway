import tkinter as tk
import random

def get_random_quote():
    quotes = [
        "The only way to do great work is to love what you do. – Steve Jobs",
        "Believe you can and you're halfway there. – Theodore Roosevelt",
        "It does not matter how slowly you go as long as you do not stop. – Confucius",
        "The best time to plant a tree was 20 years ago. The second best time is now. – Chinese Proverb",
        "The future belongs to those who believe in the beauty of their dreams. – Eleanor Roosevelt"
    ]
    return random.choice(quotes)

def show_quote():
    quote_text.set(get_random_quote())

def share_quote():
    # Code to share the current quote via messaging or social media
    pass

def save_favorite():
    # Code to save the current quote as a favorite
    pass

root = tk.Tk()
root.title("Daily Inspiration")

quote_text = tk.StringVar()

quote_label = tk.Label(root, textvariable=quote_text, wraplength=300)
quote_label.pack(pady=20)

show_button = tk.Button(root, text="Show Quote", command=show_quote)
show_button.pack(pady=10)

share_button = tk.Button(root, text="Share Quote", command=share_quote)
share_button.pack(pady=5)

save_button = tk.Button(root, text="Save Favorite", command=save_favorite)
save_button.pack(pady=5)

show_quote()  # Show a quote when the app starts

root.mainloop()
