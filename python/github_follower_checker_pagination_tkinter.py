## github-follower-checker-pagination-tkinter
## MIT License
## Created Date: 2024-08-31
## Version 1.0

import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests
import threading
import time

# Your GitHub username and personal access token
USERNAME = 'your-username'
TOKEN = 'your-personal-access-token'

# The URL endpoint to retrieve your followers
followers_url = f'https://api.github.com/users/{USERNAME}/followers'

# The file name to store the previous list of followers
followers_file = 'followers.txt'

def get_all_followers(url):
    """Retrieve all followers, handling pagination."""
    followers = []
    headers = {'Authorization': f'token {TOKEN}'}
    while url:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Failed to retrieve followers: {response.status_code}")
        followers.extend([follower['login'] for follower in response.json()])
        url = response.links.get('next', {}).get('url')  # Get the next page URL, if any
    return followers

def format_list(title, items, color):
    """Format the list with a title and color for display."""
    formatted = f'{title}:\n'
    for item in items:
        formatted += f'  - {item}\n'
    return formatted, color

def track_followers():
    try:
        # Retrieve the previous list of followers from file, or initialize an empty list
        try:
            with open(followers_file, 'r') as f:
                previous_followers = f.read().splitlines()
        except FileNotFoundError:
            previous_followers = []

        # Retrieve the current list of followers from the GitHub API
        current_followers = get_all_followers(followers_url)

        # Compare the current and previous lists of followers to identify changes
        new_followers = list(set(current_followers) - set(previous_followers))
        unfollowers = list(set(previous_followers) - set(current_followers))
        followers_back = list(set(previous_followers) & set(current_followers))

        # Clear the text widget
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)

        # Display new followers
        formatted_new, color_new = format_list("New followers", new_followers, "green")
        result_text.insert(tk.END, formatted_new, "new_followers")

        # Display unfollowers
        formatted_unf, color_unf = format_list("Unfollowers", unfollowers, "red")
        result_text.insert(tk.END, formatted_unf, "unfollowers")

        # Display followers who followed back
        formatted_back, color_back = format_list("Followers who followed back", followers_back, "blue")
        result_text.insert(tk.END, formatted_back, "followers_back")

        # Apply the colors
        result_text.tag_config("new_followers", foreground=color_new)
        result_text.tag_config("unfollowers", foreground=color_unf)
        result_text.tag_config("followers_back", foreground=color_back)

        # Disable editing the text widget
        result_text.config(state=tk.DISABLED)

        # Write the current list of followers to file for the next comparison
        with open(followers_file, 'w') as f:
            f.write('\n'.join(current_followers))

    except Exception as e:
        messagebox.showerror("Error", str(e))

def start_tracking():
    # Run the tracking in a separate thread to keep the UI responsive
    threading.Thread(target=track_followers).start()

# Set up the main application window
root = tk.Tk()
root.title("GitHub Follower Tracker")

# Window configuration
root.geometry('600x450')
root.resizable(False, False)

# Header
header = tk.Label(root, text="GitHub Follower Tracker", font=('Helvetica', 18, 'bold'), pady=10)
header.pack()

# ScrolledText widget to display results
result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=('Arial', 12), height=15, padx=10, pady=10)
result_text.pack(fill=tk.BOTH, expand=True)

# Track Button
track_button = tk.Button(root, text="Start Tracking", command=start_tracking, font=('Arial', 12), bg='#0078D7', fg='white', padx=10, pady=5)
track_button.pack(pady=10)

# Start the GUI event loop
root.mainloop()
