import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
import requests
import threading
import os
import json
from datetime import datetime

from analytics import plot_follower_growth, segment_followers
from utils import get_all_followers, format_list

# Function to track followers
def track_followers(username, token, followers_file):
    try:
        # Retrieve previous follower data
        if os.path.exists(followers_file):
            with open(followers_file, 'r') as f:
                follower_data = json.load(f)
                previous_followers = follower_data['followers']
                follower_history = follower_data['history']
        else:
            previous_followers = []
            follower_history = {}

        # Retrieve the current list of followers from the GitHub API
        followers_url = f'https://api.github.com/users/{username}/followers'
        current_followers = get_all_followers(username, token, followers_url)

        # Compare the current and previous lists of followers to identify changes
        new_followers = list(set(current_followers) - set(previous_followers))
        unfollowers = list(set(previous_followers) - set(current_followers))
        followers_back = list(set(previous_followers) & set(current_followers))

        # Update follower history with today's data
        today = datetime.today().strftime('%Y-%m-%d')
        follower_history[today] = len(current_followers)

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
            json.dump({'followers': current_followers, 'history': follower_history}, f, indent=4)

        # Show analytics options
        show_analytics_button.config(state=tk.NORMAL)
        segment_followers_button.config(state=tk.NORMAL)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to start tracking in a separate thread
def start_tracking():
    username = username_entry.get().strip()
    token = token_entry.get().strip()
    followers_file = file_entry.get().strip()

    if not username or not token or not followers_file:
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    track_button.config(state=tk.DISABLED)  # Disable button while tracking
    threading.Thread(target=track_followers, args=(username, token, followers_file)).start()

# Function to show analytics
def show_analytics():
    followers_file = file_entry.get().strip()
    if not os.path.exists(followers_file):
        messagebox.showwarning("File Not Found", "Followers file not found.")
        return

    with open(followers_file, 'r') as f:
        follower_data = json.load(f)
        follower_history = follower_data['history']

    plot_follower_growth(follower_history)

# Function to segment followers
def segment_followers_ui():
    segmentation_type = segmentation_type_var.get()
    followers_file = file_entry.get().strip()

    if not os.path.exists(followers_file):
        messagebox.showwarning("File Not Found", "Followers file not found.")
        return

    with open(followers_file, 'r') as f:
        follower_data = json.load(f)
        followers = follower_data['followers']

    segments = segment_followers(followers, segmentation_type)
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)

    for segment, users in segments.items():
        formatted_segment, color_segment = format_list(f"{segment} followers", users, "purple")
        result_text.insert(tk.END, formatted_segment, f"{segment}_followers")
        result_text.tag_config(f"{segment}_followers", foreground="purple")

    result_text.config(state=tk.DISABLED)

# Set up the main application window
root = tk.Tk()
root.title("GitHub Follower Tracker")

# Window configuration
root.geometry('600x600')
root.resizable(False, False)

# Header
header = tk.Label(root, text="GitHub Follower Tracker", font=('Helvetica', 18, 'bold'), pady=10)
header.pack()

# Frame for input fields
input_frame = tk.Frame(root, padx=10, pady=10)
input_frame.pack()

# Username input
username_label = tk.Label(input_frame, text="GitHub Username:", font=('Arial', 12))
username_label.grid(row=0, column=0, sticky='w', pady=5)
username_entry = tk.Entry(input_frame, font=('Arial', 12), width=30)
username_entry.grid(row=0, column=1, pady=5)

# Token input
token_label = tk.Label(input_frame, text="Personal Access Token:", font=('Arial', 12))
token_label.grid(row=1, column=0, sticky='w', pady=5)
token_entry = tk.Entry(input_frame, font=('Arial', 12), width=30, show="*")
token_entry.grid(row=1, column=1, pady=5)

# File name input
file_label = tk.Label(input_frame, text="Followers File Name:", font=('Arial', 12))
file_label.grid(row=2, column=0, sticky='w', pady=5)
file_entry = tk.Entry(input_frame, font=('Arial', 12), width=30)
file_entry.grid(row=2, column=1, pady=5)

# ScrolledText widget to display results
result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=('Arial', 12), height=15, padx=10, pady=10)
result_text.pack(fill=tk.BOTH, expand=True)

# Track Button
track_button = tk.Button(root, text="Start Tracking", command=start_tracking, font=('Arial', 12), bg='#0078D7', fg='white', padx=10, pady=5)
track_button.pack(pady=10)

# Show Analytics Button
show_analytics_button = tk.Button(root, text="Show Analytics", command=show_analytics, font=('Arial', 12), bg='#28A745', fg='white', padx=10, pady=5, state=tk.DISABLED)
show_analytics_button.pack(pady=10)

# Segment Followers Button
segmentation_type_var = tk.StringVar(value="activity")
segment_followers_button = tk.Button(root, text="Segment Followers", command=segment_followers_ui, font=('Arial', 12), bg='#17A2B8', fg='white', padx=10, pady=5, state=tk.DISABLED)
segment_followers_button.pack(pady=10)

segmentation_options = tk.OptionMenu(root, segmentation_type_var, "activity", "date_followed")
segmentation_options.pack(pady=5)

# Start the GUI event loop
root.mainloop()
