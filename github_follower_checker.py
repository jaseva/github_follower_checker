# ## github_follower_checker.py
# ## MIT License
# ## Created Date: 2024-09-01
# ## Version 1.1

# import tkinter as tk
# from tkinter import messagebox, scrolledtext
# import threading
# import os
# import json
# import sqlite3
# from datetime import datetime
# import requests  
# from analytics import create_table, insert_follower, plot_follower_growth, segment_followers
# from dev.prototype.utils import get_all_followers, format_list
# from openai import OpenAI
# from dotenv import load_dotenv

# # Load API key from .env file
# load_dotenv()

# def track_followers(username, token, followers_file):
#     try:
#         conn = sqlite3.connect('follower_data.db')
#         create_table(conn)

#         if os.path.exists(followers_file):
#             with open(followers_file, 'r') as f:
#                 follower_data = json.load(f)
#                 previous_followers = follower_data.get('followers', [])
#                 follower_history = follower_data.get('history', {})
#         else:
#             previous_followers = []
#             follower_history = {}

#         followers_url = f'https://api.github.com/users/{username}/followers'
#         current_followers = get_all_followers(username, token, followers_url)

#         new_followers = list(set(current_followers) - set(previous_followers))
#         unfollowers = list(set(previous_followers) - set(current_followers))
#         followers_back = list(set(previous_followers) & set(current_followers))

#         today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         follower_history[today] = len(current_followers)

#         for follower in current_followers:
#             insert_follower(conn, follower, today)

#         result_text.config(state=tk.NORMAL)
#         result_text.delete(1.0, tk.END)

#         formatted_new, color_new = format_list("New followers", new_followers, "green")
#         result_text.insert(tk.END, formatted_new, "new_followers")

#         formatted_unf, color_unf = format_list("Unfollowers", unfollowers, "red")
#         result_text.insert(tk.END, formatted_unf, "unfollowers")

#         formatted_back, color_back = format_list("Followers who followed back", followers_back, "blue")
#         result_text.insert(tk.END, formatted_back, "followers_back")

#         result_text.tag_config("new_followers", foreground=color_new)
#         result_text.tag_config("unfollowers", foreground=color_unf)
#         result_text.tag_config("followers_back", foreground=color_back)

#         result_text.config(state=tk.DISABLED)

#         with open(followers_file, 'w') as f:
#             json.dump({'followers': current_followers, 'history': follower_history}, f, indent=4)

#         show_analytics_button.config(state=tk.NORMAL)
#         segment_followers_button.config(state=tk.NORMAL)
#         summary_button.config(state=tk.NORMAL)

#         conn.close()

#     except Exception as e:
#         messagebox.showerror("Error", str(e))

# def start_tracking():
#     username = username_entry.get().strip()
#     token = token_entry.get().strip()
#     followers_file = file_entry.get().strip()

#     if not username or not token or not followers_file:
#         messagebox.showwarning("Input Error", "Please fill in all fields.")
#         return

#     threading.Thread(target=track_followers, args=(username, token, followers_file)).start()
#     summary_button.config(state=tk.NORMAL)  # Enable button after tracking

# def show_analytics():
#     try:
#         conn = sqlite3.connect('follower_data.db')
#         plot_follower_growth(conn)
#         conn.close()
#     except Exception as e:
#         messagebox.showerror("Error", str(e))

# def segment_followers_ui():
#     username = username_entry.get().strip()
#     token = token_entry.get().strip()
#     followers_file = file_entry.get().strip()
#     segmentation_type = segmentation_type_var.get()

#     if not username or not token or not followers_file:
#         messagebox.showwarning("Input Error", "Please fill in all fields.")
#         return

#     try:
#         with open(followers_file, 'r') as f:
#             follower_data = json.load(f)
#             followers = follower_data['followers']

#         segments = segment_followers(followers, segmentation_type)

#         result_text.config(state=tk.NORMAL)
#         result_text.delete(1.0, tk.END)

#         for segment, members in segments.items():
#             formatted_segment, color_segment = format_list(segment, members, "blue")
#             result_text.insert(tk.END, formatted_segment, "segment")

#         result_text.tag_config("segment", foreground="blue")
#         result_text.config(state=tk.DISABLED)

#     except Exception as e:
#         messagebox.showerror("Error", str(e))

# def generate_summary(username, token):
#     try:
#         # Initialize OpenAI API key
#         client = OpenAI(
#             api_key=os.environ['OPENAI_API_KEY'],  # this is also the default, it can be omitted
#         )

#         # Define GitHub API URLs
#         headers = {'Authorization': f'token {token}'}
#         profile_url = f'https://api.github.com/users/{username}'
#         repos_url = f'https://api.github.com/users/{username}/repos'

#         # Fetch GitHub profile and repos data
#         profile_response = requests.get(profile_url, headers=headers)
#         repos_response = requests.get(repos_url, headers=headers)

#         # Check for successful API response
#         profile_response.raise_for_status()
#         repos_response.raise_for_status()

#         profile_data = profile_response.json()
#         repos_data = repos_response.json()

#         # Extract profile information and repos
#         profile_description = profile_data.get('bio', 'No bio available')
#         repos_contributed_to = [repo['name'] for repo in repos_data if isinstance(repo, dict)]

#         # Create prompt for OpenAI API
#         prompt = (f"User {username} has the following bio: {profile_description}. "
#                   f"They have contributed to the following repositories: {', '.join(repos_contributed_to)}. "
#                   "Summarize the user's profile and contributions.")

#         # Make request to OpenAI chat completions
#         completion = client.chat.completions.create(
#             model='gpt-4o-mini',
#             messages=[
#                 {"role": "system", "content": prompt},
#                 {
#                     "role": "user",
#                     "content": "Write a summary from this user's GitHub profile."
#                 }
#             ],
#             # max_tokens=150
#         )

#                 # Extract and return summary using object attributes
#         summary = completion.choices[0].message.content.strip()
#         print(summary)
#         return summary
        

#     except Exception as e:
#         messagebox.showerror("Error", str(e))
#         return None

# def generate_summary_wrapper(summary_button):
#   username = username_entry.get().strip()
#   token = token_entry.get().strip()
#   if not username or not token:
#     messagebox.showwarning("Input Error", "Please enter username and token.")
#     return
#   summary = generate_summary(username, token)
#   if summary:
#     summary_button.config(state=tk.NORMAL)
#     result_text.config(state=tk.NORMAL)
#     result_text.delete(1.0, tk.END)
#     result_text.insert(tk.END, f"Summary: {summary}", "summary")
#     result_text.tag_config("summary", foreground="black")
#     result_text.config(state=tk.DISABLED)

#     # summary_button.config(command=generate_summary_wrapper)  # Bind button to wrapper function
#     # summary_button.config(command=lambda: generate_summary_wrapper(summary_button))
#     # summary_button = tk.Button(root, text="Generate Summary", command=lambda: generate_summary(username_entry.get().strip(), token_entry.get().strip()), state=tk.DISABLED)
#     summary_button = tk.Button(root, text="Generate Summary", command=generate_summary_wrapper, state=tk.DISABLED)

# # GUI setup
# root = tk.Tk()
# root.title("GitHub Follower Tracker")

# username_label = tk.Label(root, text="GitHub Username:")
# username_label.pack()
# username_entry = tk.Entry(root)
# username_entry.pack()

# token_label = tk.Label(root, text="GitHub Token:")
# token_label.pack()
# token_entry = tk.Entry(root, show="*")
# token_entry.pack()

# file_label = tk.Label(root, text="Followers File:")
# file_label.pack()
# file_entry = tk.Entry(root)
# file_entry.pack()

# track_button = tk.Button(root, text="Track Followers", command=start_tracking)
# track_button.pack()

# show_analytics_button = tk.Button(root, text="Show Analytics", command=show_analytics, state=tk.DISABLED)
# show_analytics_button.pack()

# segment_followers_button = tk.Button(root, text="Segment Followers", command=segment_followers_ui, state=tk.DISABLED)
# segment_followers_button.pack()

# summary_button = tk.Button(root, text="Generate Summary", command=lambda: generate_summary(username_entry.get().strip(), token_entry.get().strip()), state=tk.DISABLED)
# summary_button.pack()

# segmentation_type_var = tk.StringVar(value="repo")
# segmentation_label = tk.Label(root, text="Segment By:")
# segmentation_label.pack()
# segmentation_menu = tk.OptionMenu(root, segmentation_type_var, "repo", "activity")
# segmentation_menu.pack()

# result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED)
# result_text.pack(expand=True, fill='both')

# root.geometry("800x600")
# root.mainloop()


import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
import os
import json
import sqlite3
from datetime import datetime
import requests
from analytics import create_table, insert_follower, plot_follower_growth, segment_followers
from dev.prototype.utils import get_all_followers, format_list
from openai import OpenAI
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

# Function to track followers
def track_followers(username, token, followers_file):
    try:
        conn = sqlite3.connect('follower_data.db')
        create_table(conn)

        if os.path.exists(followers_file):
            with open(followers_file, 'r') as f:
                follower_data = json.load(f)
                previous_followers = follower_data.get('followers', [])
                follower_history = follower_data.get('history', {})
        else:
            previous_followers = []
            follower_history = {}

        followers_url = f'https://api.github.com/users/{username}/followers'
        current_followers = get_all_followers(username, token, followers_url)

        new_followers = list(set(current_followers) - set(previous_followers))
        unfollowers = list(set(previous_followers) - set(current_followers))
        followers_back = list(set(previous_followers) & set(current_followers))  

        today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        follower_history[today] = len(current_followers)

        for follower in current_followers:
            insert_follower(conn, follower, today)

        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)

        formatted_new, color_new = format_list("New followers", new_followers, "green")
        result_text.insert(tk.END, formatted_new, "new_followers")

        formatted_unf, color_unf = format_list("Unfollowers", unfollowers, "red")
        result_text.insert(tk.END, formatted_unf, "unfollowers")

        formatted_back, color_back = format_list("Followers who followed back", followers_back, "blue")
        result_text.insert(tk.END, formatted_back, "followers_back")

        result_text.tag_config("new_followers", foreground=color_new)
        result_text.tag_config("unfollowers", foreground=color_unf)
        result_text.tag_config("followers_back", foreground=color_back)

        result_text.config(state=tk.DISABLED)

        with open(followers_file, 'w') as f:
            json.dump({'followers': current_followers, 'history': follower_history}, f, indent=4)

        show_analytics_button.config(state=tk.NORMAL)
        segment_followers_button.config(state=tk.NORMAL)
        summary_button.config(state=tk.NORMAL)

        conn.close()

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to start tracking in a separate thread
def start_tracking():
    username = username_entry.get().strip()
    token = token_entry.get().strip()
    followers_file = followers_file_entry.get().strip()

    if not username or not token or not followers_file:
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    threading.Thread(target=track_followers, args=(username, token, followers_file)).start()
    summary_button.config(state=tk.NORMAL)  # Enable button after tracking

# Function to show analytics
def show_analytics():
    try:
        conn = sqlite3.connect('follower_data.db')
        plot_follower_growth(conn)
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to segment followers
def segment_followers_ui():
    username = username_entry.get().strip()
    token = token_entry.get().strip()
    followers_file = followers_file_entry.get().strip()
    segmentation_type = segmentation_type_var.get()

    if not username or not token or not followers_file:
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    try:
        with open(followers_file, 'r') as f:
            follower_data = json.load(f)
            followers = follower_data['followers']

        segments = segment_followers(followers, segmentation_type)

        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)

        for segment, members in segments.items():
            formatted_segment, color_segment = format_list(segment, members, "blue")
            result_text.insert(tk.END, formatted_segment, "segment")

        result_text.tag_config("segment", foreground="blue")
        result_text.config(state=tk.DISABLED)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to generate AI summary 
def generate_summary(username, token):
    try:
        # Initialize OpenAI API key
        client = OpenAI(
            api_key=os.environ['OPENAI_API_KEY']
        )

        # Define GitHub API URLs
        headers = {'Authorization': f'token {token}'}
        profile_url = f'https://api.github.com/users/{username}'
        repos_url = f'https://api.github.com/users/{username}/repos'

        # Fetch GitHub profile and repos data
        profile_response = requests.get(profile_url, headers=headers)
        repos_response = requests.get(repos_url, headers=headers)

        # Check for successful API response
        profile_response.raise_for_status()
        repos_response.raise_for_status()

        profile_data = profile_response.json()
        repos_data = repos_response.json()

        # Extract profile information and repos
        profile_description = profile_data.get('bio', 'No bio available')
        repos_contributed_to = [repo['name'] for repo in repos_data if isinstance(repo, dict)]

        # Create prompt for OpenAI API
        prompt = (f"User {username} has the following bio: {profile_description}. "
                 f"They have contributed to the following repositories: {', '.join(repos_contributed_to)}. "
                 "Summarize the user's profile and contributions.")

        # Make request to OpenAI chat completions
        completion = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {"role": "system", "content": prompt},
                {
                    "role": "user",
                    "content": "Write a summary from this user's GitHub profile."
                }
            ]
        )

        # Extract and return summary using object attributes
        summary = completion.choices[0].message.content.strip()
        print(summary)  # For debugging
        return summary

    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None

# Function to wrap AI generated summary
def generate_summary_wrapper():
    username = profile_entry.get().strip()
    token = token_entry.get().strip()
    if not username or not token:
        messagebox.showwarning("Input Error", "Please enter username and token.")
        return
    summary = generate_summary(username, token)
    if summary:
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Summary: {summary}", "summary")
        result_text.tag_config("summary", foreground="black")
        result_text.config(state=tk.DISABLED)

# GUI setup
root = tk.Tk()
root.title("GitHub Follower Checker")

# Increase window size to accomodate all elements
root.geometry("800x600")
root.resizable(True, True)

# Header
header = tk.Label(root, text="GitHub Follower Checker", font=('Helvetica', 18, 'bold'), pady=10)
header.pack()

# Frame for input fields
input_frame = tk.Frame(root, padx=10, pady=10)
input_frame.pack()

# Username input
username_label = tk.Label(root, text="GitHub Username:")
username_label.pack()
username_entry = tk.Entry(root)
username_entry.pack()

# Token input
token_label = tk.Label(root, text="GitHub Token:")
token_label.pack()
token_entry = tk.Entry(root, show="*")
token_entry.pack()

# Follower file name input
followers_file_label = tk.Label(root, text="Followers File:")
followers_file_label.pack()
followers_file_entry = tk.Entry(root)
followers_file_entry.pack()

# Track Button
track_button = tk.Button(root, text="Track Followers", command=start_tracking)
track_button.pack()

# Show Analytics Button
show_analytics_button = tk.Button(root, text="Show Analytics", command=show_analytics, state=tk.DISABLED)
show_analytics_button.pack()

# Segment Followers Button
segment_followers_button = tk.Button(root, text="Segment Followers", command=segment_followers_ui, state=tk.DISABLED)
segment_followers_button.pack()

# OptionMenu for segmentation
segmentation_type_var = tk.StringVar(value="repo")
segmentation_label = tk.Label(root, text="Segment By:")
segmentation_label.pack()
segmentation_menu = tk.OptionMenu(root, segmentation_type_var, "repo", "activity")
segmentation_menu.pack()

# GitHub Profile to summarize
profile_label = tk.Label(root, text="Profile to Summarize:")
profile_label.pack()
profile_entry = tk.Entry(root)
profile_entry.pack()

# Generate Summary Button
summary_button = tk.Button(root, text="Generate Summary", command=generate_summary_wrapper, state=tk.DISABLED)
summary_button.pack()

result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED)
result_text.pack(expand=True, fill='both')

# Start the GUI event loop
root.mainloop()