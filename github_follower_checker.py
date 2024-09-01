# import tkinter as tk
# from tkinter import messagebox, scrolledtext, filedialog
# import requests
# import threading
# import sqlite3
# import json
# from datetime import datetime
# from analytics import plot_follower_growth, segment_followers
# from utils import get_all_followers, format_list

# # Database setup
# def setup_database(db_name="followers.db"):
#     conn = sqlite3.connect(db_name)
#     cursor = conn.cursor()
#     cursor.execute('''CREATE TABLE IF NOT EXISTS followers (
#                         id INTEGER PRIMARY KEY AUTOINCREMENT,
#                         username TEXT,
#                         timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
#                     )''')
#     conn.commit()
#     return conn

# # Function to insert follower data into the database
# def insert_follower(conn, username):
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO followers (username) VALUES (?)", (username,))
#     conn.commit()

# # Function to track followers
# def track_followers(username, token, followers_file):
#     try:
#         conn = setup_database()
        
#         # Retrieve previous follower data
#         if followers_file and followers_file.endswith('.json') and os.path.exists(followers_file):
#             with open(followers_file, 'r') as f:
#                 follower_data = json.load(f)
#                 previous_followers = follower_data['followers']
#                 follower_history = follower_data['history']
#         else:
#             previous_followers = []
#             follower_history = {}

#         # Retrieve the current list of followers from the GitHub API
#         followers_url = f'https://api.github.com/users/{username}/followers'
#         current_followers = get_all_followers(username, token, followers_url)

#         # Compare the current and previous lists of followers to identify changes
#         new_followers = list(set(current_followers) - set(previous_followers))
#         unfollowers = list(set(previous_followers) - set(current_followers))
#         followers_back = list(set(previous_followers) & set(current_followers))

#         # Update follower history with today's data
#         today = datetime.today().strftime('%Y-%m-%d')
#         follower_history[today] = len(current_followers)

#         # Clear the text widget
#         result_text.config(state=tk.NORMAL)
#         result_text.delete(1.0, tk.END)

#         # Display new followers
#         formatted_new, color_new = format_list("New followers", new_followers, "green")
#         result_text.insert(tk.END, formatted_new, "new_followers")

#         # Display unfollowers
#         formatted_unf, color_unf = format_list("Unfollowers", unfollowers, "red")
#         result_text.insert(tk.END, formatted_unf, "unfollowers")

#         # Display followers who followed back
#         formatted_back, color_back = format_list("Followers who followed back", followers_back, "blue")
#         result_text.insert(tk.END, formatted_back, "followers_back")

#         # Apply the colors
#         result_text.tag_config("new_followers", foreground=color_new)
#         result_text.tag_config("unfollowers", foreground=color_unf)
#         result_text.tag_config("followers_back", foreground=color_back)

#         # Disable editing the text widget
#         result_text.config(state=tk.DISABLED)

#         # Write the current list of followers to file for the next comparison
#         if followers_file and followers_file.endswith('.json'):
#             with open(followers_file, 'w') as f:
#                 json.dump({'followers': current_followers, 'history': follower_history}, f, indent=4)

#         # Insert new followers into the database
#         for follower in current_followers:
#             insert_follower(conn, follower)

#         # Show analytics options
#         show_analytics_button.config(state=tk.NORMAL)
#         segment_followers_button.config(state=tk.NORMAL)

#     except Exception as e:
#         messagebox.showerror("Error", str(e))

# # Function to start tracking in a separate thread
# def start_tracking():
#     username = username_entry.get().strip()
#     token = token_entry.get().strip()
#     followers_file = file_entry.get().strip()

#     if not username or not token or not followers_file:
#         messagebox.showwarning("Input Error", "Please fill in all fields.")
#         return

#     track_button.config(state=tk.DISABLED)  # Disable button while tracking
#     threading.Thread(target=track_followers, args=(username, token, followers_file)).start()

# # Function to show analytics
# def show_analytics():
#     followers_file = file_entry.get().strip()
#     if not os.path.exists(followers_file):
#         messagebox.showwarning("File Not Found", "Followers file not found.")
#         return

#     with open(followers_file, 'r') as f:
#         follower_data = json.load(f)
#         follower_history = follower_data['history']

#     plot_follower_growth(follower_history)

# # Function to segment followers
# def segment_followers_ui():
#     segmentation_type = segmentation_type_var.get()
#     followers_file = file_entry.get().strip()

#     if not os.path.exists(followers_file):
#         messagebox.showwarning("File Not Found", "Followers file not found.")
#         return

#     with open(followers_file, 'r') as f:
#         follower_data = json.load(f)
#         followers = follower_data['followers']

#     segments = segment_followers(followers, segmentation_type)
#     result_text.config(state=tk.NORMAL)
#     result_text.delete(1.0, tk.END)

#     for segment, users in segments.items():
#         formatted_segment, color_segment = format_list(f"{segment} followers", users, "purple")
#         result_text.insert(tk.END, formatted_segment, f"{segment}_followers")
#         result_text.tag_config(f"{segment}_followers", foreground="purple")

#     result_text.config(state=tk.DISABLED)

# # Set up the main application window
# root = tk.Tk()
# root.title("GitHub Follower Tracker")

# # Window configuration
# root.geometry('800x600')
# root.resizable(True, True)

# # Header
# header = tk.Label(root, text="GitHub Follower Tracker", font=('Helvetica', 18, 'bold'), pady=10)
# header.pack()

# # Frame for input fields
# input_frame = tk.Frame(root, padx=10, pady=10)
# input_frame.pack()

# # Username input
# username_label = tk.Label(input_frame, text="GitHub Username:", font=('Arial', 12))
# username_label.grid(row=0, column=0, sticky='w', pady=5)
# username_entry = tk.Entry(input_frame, font=('Arial', 12), width=30)
# username_entry.grid(row=0, column=1, pady=5)

# # Token input
# token_label = tk.Label(input_frame, text="Personal Access Token:", font=('Arial', 12))
# token_label.grid(row=1, column=0, sticky='w', pady=5)
# token_entry = tk.Entry(input_frame, font=('Arial', 12), width=30, show="*")
# token_entry.grid(row=1, column=1, pady=5)

# # File name input
# file_label = tk.Label(input_frame, text="Followers File Name:", font=('Arial', 12))
# file_label.grid(row=2, column=0, sticky='w', pady=5)
# file_entry = tk.Entry(input_frame, font=('Arial', 12), width=30)
# file_entry.grid(row=2, column=1, pady=5)

# # ScrolledText widget to display results
# result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=('Arial', 12), height=15, padx=10, pady=10)
# result_text.pack(fill=tk.BOTH, expand=True)

# # Track Button
# track_button = tk.Button(root, text="Start Tracking", command=start_tracking, font=('Arial', 12), bg='#0078D7', fg='white', padx=10, pady=5)
# track_button.pack(pady=10)

# # Show Analytics Button
# show_analytics_button = tk.Button(root, text="Show Analytics", command=show_analytics, font=('Arial', 12), bg='#4CAF50', fg='white', padx=10, pady=5, state=tk.DISABLED)
# show_analytics_button.pack(side=tk.LEFT, padx=(10, 5), pady=10)

# # Segment Followers Button
# segment_followers_button = tk.Button(root, text="Segment Followers", command=segment_followers_ui, font=('Arial', 12), bg='#FF9800', fg='white', padx=10, pady=5, state=tk.DISABLED)
# segment_followers_button.pack(side=tk.LEFT, padx=(5, 10), pady=10)

# # Option Menu for segmentation type
# segmentation_type_var = tk.StringVar()
# segmentation_type_var.set("activity")
# segmentation_option_menu = tk.OptionMenu(root, segmentation_type_var, "activity", "date_followed")
# segmentation_option_menu.pack(side=tk.RIGHT, padx=(5, 10), pady=10)

# root.mainloop()

# -----------------------------------------

# import tkinter as tk
# from tkinter import messagebox, scrolledtext
# import requests
# import threading
# import os
# import json
# import sqlite3
# from datetime import datetime
# from analytics import create_table, insert_follower, plot_follower_growth, segment_followers
# from utils import get_all_followers, format_list

# # Function to track followers and store in a database
# def track_followers(username, token, followers_file):
#     try:
#         conn = sqlite3.connect('follower_data.db')
#         create_table(conn)

#         # Retrieve previous follower data
#         if os.path.exists(followers_file):
#             with open(followers_file, 'r') as f:
#                 follower_data = json.load(f)
#                 previous_followers = follower_data['followers']
#                 follower_history = follower_data['history']
#         else:
#             previous_followers = []
#             follower_history = {}

#         # Retrieve the current list of followers from the GitHub API
#         followers_url = f'https://api.github.com/users/{username}/followers'
#         current_followers = get_all_followers(username, token, followers_url)

#         # Compare the current and previous lists of followers to identify changes
#         new_followers = list(set(current_followers) - set(previous_followers))
#         unfollowers = list(set(previous_followers) - set(current_followers))
#         followers_back = list(set(previous_followers) & set(current_followers))

#         # Update follower history with today's data
#         today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         follower_history[today] = len(current_followers)

#         # Insert data into the database
#         for follower in current_followers:
#             insert_follower(conn, follower, today)

#         # Clear the text widget
#         result_text.config(state=tk.NORMAL)
#         result_text.delete(1.0, tk.END)

#         # Display new followers
#         formatted_new, color_new = format_list("New followers", new_followers, "green")
#         result_text.insert(tk.END, formatted_new, "new_followers")

#         # Display unfollowers
#         formatted_unf, color_unf = format_list("Unfollowers", unfollowers, "red")
#         result_text.insert(tk.END, formatted_unf, "unfollowers")

#         # Display followers who followed back
#         formatted_back, color_back = format_list("Followers who followed back", followers_back, "blue")
#         result_text.insert(tk.END, formatted_back, "followers_back")

#         # Apply the colors
#         result_text.tag_config("new_followers", foreground=color_new)
#         result_text.tag_config("unfollowers", foreground=color_unf)
#         result_text.tag_config("followers_back", foreground=color_back)

#         # Disable editing the text widget
#         result_text.config(state=tk.DISABLED)

#         # Write the current list of followers to file for the next comparison
#         with open(followers_file, 'w') as f:
#             json.dump({'followers': current_followers, 'history': follower_history}, f, indent=4)

#         # Show analytics options
#         show_analytics_button.config(state=tk.NORMAL)
#         segment_followers_button.config(state=tk.NORMAL)

#         conn.close()

#     except Exception as e:
#         messagebox.showerror("Error", str(e))

# # Function to start tracking in a separate thread
# def start_tracking():
#     username = username_entry.get().strip()
#     token = token_entry.get().strip()
#     followers_file = file_entry.get().strip()

#     if not username or not token or not followers_file:
#         messagebox.showwarning("Input Error", "Please fill in all fields.")
#         return

#     track_button.config(state=tk.DISABLED)  # Disable button while tracking
#     threading.Thread(target=track_followers, args=(username, token, followers_file)).start()

# # Function to show analytics
# def show_analytics():
#     followers_file = file_entry.get().strip()
#     if not os.path.exists(followers_file):
#         messagebox.showwarning("File Not Found", "Followers file not found.")
#         return

#     with open(followers_file, 'r') as f:
#         follower_data = json.load(f)
#         follower_history = follower_data['history']

#     plot_follower_growth(follower_history)

# # Function to segment followers
# def segment_followers_ui():
#     segmentation_type = segmentation_type_var.get()
#     followers_file = file_entry.get().strip()

#     if not os.path.exists(followers_file):
#         messagebox.showwarning("File Not Found", "Followers file not found.")
#         return

#     with open(followers_file, 'r') as f:
#         follower_data = json.load(f)
#         followers = follower_data['followers']

#     segments = segment_followers(followers, segmentation_type)
#     result_text.config(state=tk.NORMAL)
#     result_text.delete(1.0, tk.END)

#     for segment, users in segments.items():
#         formatted_segment, color_segment = format_list(f"{segment} followers", users, "purple")
#         result_text.insert(tk.END, formatted_segment, f"{segment}_followers")
#         result_text.tag_config(f"{segment}_followers", foreground="purple")

#     result_text.config(state=tk.DISABLED)

# # Set up the main application window
# root = tk.Tk()
# root.title("GitHub Follower Tracker")

# # Window configuration
# root.geometry('700x800')
# root.resizable(False, False)

# # Header
# header = tk.Label(root, text="GitHub Follower Tracker", font=('Helvetica', 18, 'bold'), pady=10)
# header.pack()

# # Frame for input fields
# input_frame = tk.Frame(root, padx=10, pady=10)
# input_frame.pack()

# # Username input
# username_label = tk.Label(input_frame, text="GitHub Username:", font=('Arial', 12))
# username_label.grid(row=0, column=0, sticky='w', pady=5)
# username_entry = tk.Entry(input_frame, font=('Arial', 12), width=30)
# username_entry.grid(row=0, column=1, pady=5)

# # Token input
# token_label = tk.Label(input_frame, text="Personal Access Token:", font=('Arial', 12))
# token_label.grid(row=1, column=0, sticky='w', pady=5)
# token_entry = tk.Entry(input_frame, font=('Arial', 12), width=30, show="*")
# token_entry.grid(row=1, column=1, pady=5)

# # File name input
# file_label = tk.Label(input_frame, text="Followers File Name:", font=('Arial', 12))
# file_label.grid(row=2, column=0, sticky='w', pady=5)
# file_entry = tk.Entry(input_frame, font=('Arial', 12), width=30)
# file_entry.grid(row=2, column=1, pady=5)

# # ScrolledText widget to display results
# result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=('Arial', 12), height=15, padx=10, pady=10)
# result_text.pack(fill=tk.BOTH, expand=True)

# # Track Button
# track_button = tk.Button(root, text="Start Tracking", command=start_tracking, font=('Arial', 12), bg='#0078D7', fg='white', padx=10, pady=5)
# track_button.pack(pady=10)

# # Show Analytics Button
# show_analytics_button = tk.Button(root, text="Show Analytics", command=show_analytics, font=('Arial', 12), bg='#28A745', fg='white', padx=10, pady=5, state=tk.DISABLED)
# show_analytics_button.pack(pady=10)

# # Segment Followers Button
# segmentation_type_var = tk.StringVar(value="activity")
# segment_followers_button = tk.Button(root, text="Segment Followers", command=segment_followers_ui, font=('Arial', 12), bg='#17A2B8', fg='white', padx=10, pady=5, state=tk.DISABLED)
# segment_followers_button.pack(pady=10)

# segmentation_options = tk.OptionMenu(root, segmentation_type_var, "activity", "date_followed")
# segmentation_options.pack(pady=5)

# # Start the GUI event loop
# root.mainloop()

# ---------------------------------------

# import tkinter as tk
# from tkinter import messagebox, scrolledtext
# import requests
# import threading
# import os
# import json
# import sqlite3
# from datetime import datetime
# from analytics import create_table, insert_follower, plot_follower_growth, segment_followers
# from utils import get_all_followers, format_list

# # Function to track followers and store in a database
# def track_followers(username, token, followers_file):
#     try:
#         conn = sqlite3.connect('follower_data.db')
#         create_table(conn)

#         if os.path.exists(followers_file):
#             with open(followers_file, 'r') as f:
#                 follower_data = json.load(f)
#                 previous_followers = follower_data['followers']
#                 follower_history = follower_data['history']
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

#         conn.close()

#     except Exception as e:
#         messagebox.showerror("Error", str(e))

# # Function to start tracking in a separate thread
# def start_tracking():
#     username = username_entry.get().strip()
#     token = token_entry.get().strip()
#     followers_file = file_entry.get().strip()

#     if not username or not token or not followers_file:
#         messagebox.showwarning("Input Error", "Please fill in all fields.")
#         return

#     track_button.config(state=tk.DISABLED)
#     threading.Thread(target=track_followers, args=(username, token, followers_file)).start()

# # Function to show analytics
# def show_analytics():
#     followers_file = file_entry.get().strip()
#     if not os.path.exists(followers_file):
#         messagebox.showwarning("File Not Found", "Followers file not found.")
#         return

#     with open(followers_file, 'r') as f:
#         follower_data = json.load(f)
#         follower_history = follower_data['history']

#     plot_follower_growth(follower_history)

# # Function to segment followers
# def segment_followers_ui():
#     segmentation_type = segmentation_type_var.get()
#     followers_file = file_entry.get().strip()

#     if not os.path.exists(followers_file):
#         messagebox.showwarning("File Not Found", "Followers file not found.")
#         return

#     with open(followers_file, 'r') as f:
#         follower_data = json.load(f)
#         followers = follower_data['followers']

#     segments = segment_followers(followers, segmentation_type)
#     result_text.config(state=tk.NORMAL)
#     result_text.delete(1.0, tk.END)

#     for segment, users in segments.items():
#         formatted_segment, color_segment = format_list(f"{segment} followers", users, "purple")
#         result_text.insert(tk.END, formatted_segment, f"{segment}_followers")
#         result_text.tag_config(f"{segment}_followers", foreground="purple")

#     result_text.config(state=tk.DISABLED)

# # Main application window
# root = tk.Tk()
# root.title("GitHub Follower Tracker")

# root.geometry('700x800')
# root.resizable(False, False)

# header = tk.Label(root, text="GitHub Follower Tracker", font=('Helvetica', 18, 'bold'), pady=10)
# header.pack()

# input_frame = tk.Frame(root, padx=10, pady=10)
# input_frame.pack()

# username_label = tk.Label(input_frame, text="GitHub Username:", font=('Arial', 12))
# username_label.grid(row=0, column=0, sticky='w', pady=5)
# username_entry = tk.Entry(input_frame, font=('Arial', 12), width=30)
# username_entry.grid(row=0, column=1, pady=5)

# token_label = tk.Label(input_frame, text="Personal Access Token:", font=('Arial', 12))
# token_label.grid(row=1, column=0, sticky='w', pady=5)
# token_entry = tk.Entry(input_frame, font=('Arial', 12), width=30, show="*")
# token_entry.grid(row=1, column=1, pady=5)

# file_label = tk.Label(input_frame, text="Followers File Name:", font=('Arial', 12))
# file_label.grid(row=2, column=0, sticky='w', pady=5)
# file_entry = tk.Entry(input_frame, font=('Arial', 12), width=30)
# file_entry.grid(row=2, column=1, pady=5)

# result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=('Arial', 12), height=15, padx=10, pady=10)
# result_text.pack(fill=tk.BOTH, expand=True)

# track_button = tk.Button(root, text="Start Tracking", command=start_tracking, font=('Arial', 12), bg='#0078D7', fg='white', padx=10, pady=5)
# track_button.pack(pady=10)

# show_analytics_button = tk.Button(root, text="Show Analytics", command=show_analytics, font=('Arial', 12), bg='#28A745', fg='white', padx=10, pady=5, state=tk.DISABLED)
# show_analytics_button.pack(pady=10)

# segmentation_type_var = tk.StringVar(value="activity")
# segment_followers_button = tk.Button(root, text="Segment Followers", command=segment_followers_ui, font=('Arial', 12), bg='#17A2B8', fg='white', padx=10, pady=5, state=tk.DISABLED)
# segment_followers_button.pack(pady=10)

# segmentation_options = tk.OptionMenu(root, segmentation_type_var, "activity", "date_followed")
# segmentation_options.pack(pady=5)

# root.mainloop()

# ----------------------------------------------------------------------

# import tkinter as tk
# from tkinter import messagebox, scrolledtext
# import requests
# import threading
# import os
# import json
# import sqlite3
# from datetime import datetime
# from analytics import create_table, insert_follower, plot_follower_growth, segment_followers
# from utils import get_all_followers, format_list
# import openai

# # Initialize OpenAI GPT
# def initialize_gpt(api_key):
#     openai.api_key = api_key

# # Function to fetch GitHub profile data
# def fetch_github_profile_data(username, token):
#     headers = {'Authorization': f'token {token}'}
#     profile_url = f'https://api.github.com/users/{username}'
#     repos_url = f'https://api.github.com/users/{username}/repos'
#     starred_url = f'https://api.github.com/users/{username}/starred'
    
#     profile_response = requests.get(profile_url, headers=headers)
#     repos_response = requests.get(repos_url, headers=headers)
#     starred_response = requests.get(starred_url, headers=headers)

#     profile_response.raise_for_status()
#     repos_response.raise_for_status()
#     starred_response.raise_for_status()

#     profile_data = profile_response.json()
#     repos_data = repos_response.json()
#     starred_data = starred_response.json()

#     return {
#         "bio": profile_data.get("bio", ""),
#         "repos": [repo["name"] for repo in repos_data],
#         "stars": [repo["name"] for repo in starred_data]
#     }

# # Function to generate a GitHub profile summary using GPT
# def generate_github_summary(profile_data):
#     query = (
#         f"Summarize the following GitHub profile:\n\n"
#         f"Bio: {profile_data['bio']}\n"
#         f"Repositories: {', '.join(profile_data['repos'])}\n"
#         f"Starred Repositories: {', '.join(profile_data['stars'])}\n"
#     )

#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=query,
#         max_tokens=150
#     )

#     summary = response.choices[0].text.strip()
#     return summary

# # Function to display the GitHub profile summary
# def display_profile_summary(username, token):
#     try:
#         profile_data = fetch_github_profile_data(username, token)
#         summary = generate_github_summary(profile_data)

#         result_text.config(state=tk.NORMAL)
#         result_text.delete(1.0, tk.END)
#         result_text.insert(tk.END, f"Summary for {username}:\n\n{summary}")
#         result_text.config(state=tk.DISABLED)

#     except Exception as e:
#         messagebox.showerror("Error", str(e))

# # Function to track followers and store in a database
# def track_followers(username, token, followers_file):
#     try:
#         conn = sqlite3.connect('follower_data.db')
#         create_table(conn)

#         if os.path.exists(followers_file):
#             with open(followers_file, 'r') as f:
#                 follower_data = json.load(f)
#                 previous_followers = follower_data['followers']
#                 follower_history = follower_data['history']
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

# # Function to start tracking in a separate thread
# def start_tracking():
#     username = username_entry.get().strip()
#     token = token_entry.get().strip()
#     followers_file = file_entry.get().strip()

#     if not username or not token or not followers_file:
#         messagebox.showwarning("Input Error", "Please fill in all fields.")
#         return

#     track_button.config(state=tk.DISABLED)
#     threading.Thread(target=track_followers, args=(username, token, followers_file)).start()

# # Function to show analytics
# def show_analytics():
#     followers_file = file_entry.get().strip()
#     if not os.path.exists(followers_file):
#         messagebox.showwarning("File Not Found", "Followers file not found.")
#         return

#     with open(followers_file, 'r') as f:
#         follower_data = json.load(f)
#         follower_history = follower_data['history']

#     plot_follower_growth(follower_history)

# # Function to segment followers
# def segment_followers_ui():
#     segmentation_type = segmentation_type_var.get()
#     followers_file = file_entry.get().strip()

#     if not os.path.exists(followers_file):
#         messagebox.showwarning("File Not Found", "Followers file not found.")
#         return

#     with open(followers_file, 'r') as f:
#         follower_data = json.load(f)
#         followers = follower_data['followers']

#     segments = segment_followers(followers, segmentation_type)
#     result_text.config(state=tk.NORMAL)
#     result_text.delete(1.0, tk.END)

#     for segment, users in segments.items():
#         formatted_segment, color_segment = format_list(f"{segment} followers", users, "purple")
#         result_text.insert(tk.END, formatted_segment, f"{segment}_followers")
#         result_text.tag_config(f"{segment}_followers", foreground="purple")

#     result_text.config(state=tk.DISABLED)

# # Main application window
# root = tk.Tk()
# root.title("GitHub Follower Tracker")

# root.geometry('700x900')
# root.resizable(False, False)

# header = tk.Label(root, text="GitHub Follower Tracker", font=('Helvetica', 18, 'bold'), pady=10)
# header.pack()

# input_frame = tk.Frame(root, padx=10, pady=10)
# input_frame.pack()

# username_label = tk.Label(input_frame, text="GitHub Username:", font=('Arial', 12))
# username_label.grid(row=0, column=0, sticky='w', pady=5)
# username_entry = tk.Entry(input_frame, font=('Arial', 12), width=30)
# username_entry.grid(row=0, column=1, pady=5)

# token_label = tk.Label(input_frame, text="Personal Access Token:", font=('Arial', 12))
# token_label.grid(row=1, column=0, sticky='w', pady=5)
# token_entry = tk.Entry(input_frame, font=('Arial', 12), width=30, show="*")
# token_entry.grid(row=1, column=1, pady=5)

# file_label = tk.Label(input_frame, text="Followers File Name:", font=('Arial', 12))
# file_label.grid(row=2, column=0, sticky='w', pady=5)
# file_entry = tk.Entry(input_frame, font=('Arial', 12), width=30)
# file_entry.grid(row=2, column=1, pady=5)

# result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=('Arial', 12), height=15, padx=10, pady=10)
# result_text.pack(fill=tk.BOTH, expand=True)

# track_button = tk.Button(root, text="Start Tracking", command=start_tracking, font=('Arial', 12), bg='#0078D7', fg='white', padx=10, pady=5)
# track_button.pack(pady=10)

# show_analytics_button = tk.Button(root, text="Show Analytics", command=show_analytics, font=('Arial', 12), bg='#28A745', fg='white', padx=10, pady=5, state=tk.DISABLED)
# show_analytics_button.pack(pady=10)

# segmentation_type_var = tk.StringVar(value="repo")
# segmentation_options = ["repo", "star"]
# segmentation_frame = tk.Frame(root)
# segmentation_frame.pack()

# segmentation_label = tk.Label(segmentation_frame, text="Segment Followers by:", font=('Arial', 12))
# segmentation_label.grid(row=0, column=0, padx=5)

# segmentation_menu = tk.OptionMenu(segmentation_frame, segmentation_type_var, *segmentation_options)
# segmentation_menu.config(font=('Arial', 12))
# segmentation_menu.grid(row=0, column=1, padx=5)

# segment_followers_button = tk.Button(root, text="Segment Followers", command=segment_followers_ui, font=('Arial', 12), bg='#FFC107', fg='black', padx=10, pady=5, state=tk.DISABLED)
# segment_followers_button.pack(pady=10)

# summary_button = tk.Button(root, text="Generate Summary", command=lambda: display_profile_summary(username_entry.get().strip(), token_entry.get().strip()), font=('Arial', 12), bg='#DC3545', fg='white', padx=10, pady=5, state=tk.DISABLED)
# summary_button.pack(pady=10)

# root.mainloop()

# --------------------------------------------------------

import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests
import threading
import os
import json
import sqlite3
from datetime import datetime
from analytics import create_table, insert_follower, plot_follower_growth, segment_followers
from utils import get_all_followers, format_list
import openai
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to track followers and store them in a database
def track_followers(username, token, followers_file):
    try:
        conn = sqlite3.connect('follower_data.db')
        create_table(conn)

        if os.path.exists(followers_file):
            with open(followers_file, 'r') as f:
                follower_data = json.load(f)
                previous_followers = follower_data['followers']
                follower_history = follower_data['history']
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

        conn.close()

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to generate a summary using GPT
def generate_summary(username, token):
    try:
        headers = {'Authorization': f'token {token}'}
        profile_url = f'https://api.github.com/users/{username}'
        repos_url = f'https://api.github.com/users/{username}/repos'

        profile_response = requests.get(profile_url, headers=headers)
        repos_response = requests.get(repos_url, headers=headers)

        profile_data = profile_response.json()
        repos_data = repos_response.json()

        # Extract relevant information
        profile_description = profile_data.get('bio', 'No bio available')
        repos_contributed_to = [repo['name'] for repo in repos_data]

        # Construct prompt for GPT
        prompt = (f"User {username} has the following bio: {profile_description}. "
                  f"They have contributed to the following repositories: {', '.join(repos_contributed_to)}. "
                  "Summarize the user's profile and contributions.")

        # Call OpenAI GPT API
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )

        summary = response.choices[0].text.strip()
        return summary

    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None

# Function to display the summary in the GUI
def show_summary():
    username = username_entry.get().strip()
    token = token_entry.get().strip()

    if not username or not token:
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    summary = generate_summary(username, token)

    if summary:
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, summary)
        result_text.config(state=tk.DISABLED)

# Function to start tracking in a separate thread
def start_tracking():
    username = username_entry.get().strip()
    token = token_entry.get().strip()
    followers_file = file_entry.get().strip()

    if not username or not token or not followers_file:
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    track_button.config(state=tk.DISABLED)
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

    # Main application window
root = tk.Tk()
root.title("GitHub Follower Tracker")

root.geometry('700x900')
root.resizable(False, False)

header = tk.Label(root, text="GitHub Follower Tracker", font=('Helvetica', 18, 'bold'), pady=10)
header.pack()

input_frame = tk.Frame(root, padx=10, pady=10)
input_frame.pack()

username_label = tk.Label(input_frame, text="GitHub Username:", font=('Arial', 12))
username_label.grid(row=0, column=0, sticky='w', pady=5)
username_entry = tk.Entry(input_frame, font=('Arial', 12), width=30)
username_entry.grid(row=0, column=1, pady=5)

token_label = tk.Label(input_frame, text="Personal Access Token:", font=('Arial', 12))
token_label.grid(row=1, column=0, sticky='w', pady=5)
token_entry = tk.Entry(input_frame, font=('Arial', 12), width=30, show="*")
token_entry.grid(row=1, column=1, pady=5)

file_label = tk.Label(input_frame, text="Followers File Name:", font=('Arial', 12))
file_label.grid(row=2, column=0, sticky='w', pady=5)
file_entry = tk.Entry(input_frame, font=('Arial', 12), width=30)
file_entry.grid(row=2, column=1, pady=5)

result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=('Arial', 12), height=15, padx=10, pady=10)
result_text.pack(fill=tk.BOTH, expand=True)

track_button = tk.Button(root, text="Start Tracking", command=start_tracking, font=('Arial', 12), bg='#0078D7', fg='white', padx=10, pady=5)
track_button.pack(pady=10)

show_analytics_button = tk.Button(root, text="Show Analytics", command=show_analytics, font=('Arial', 12), bg='#28A745', fg='white', padx=10, pady=5, state=tk.DISABLED)
show_analytics_button.pack(pady=10)

segmentation_type_var = tk.StringVar(value="repo")
segmentation_options = ["repo", "star"]
segmentation_frame = tk.Frame(root)
segmentation_frame.pack()

segmentation_label = tk.Label(segmentation_frame, text="Segment Followers by:", font=('Arial', 12))
segmentation_label.grid(row=0, column=0, padx=5)

segmentation_menu = tk.OptionMenu(segmentation_frame, segmentation_type_var, *segmentation_options)
segmentation_menu.config(font=('Arial', 12))
segmentation_menu.grid(row=0, column=1, padx=5)

segment_followers_button = tk.Button(root, text="Segment Followers", command=segment_followers_ui, font=('Arial', 12), bg='#FFC107', fg='black', padx=10, pady=5, state=tk.DISABLED)
segment_followers_button.pack(pady=10)

summary_button = tk.Button(root, text="Generate Summary", command=lambda: display_profile_summary(username_entry.get().strip(), token_entry.get().strip()), font=('Arial', 12), bg='#DC3545', fg='white', padx=10, pady=5, state=tk.DISABLED)
summary_button.pack(pady=10)

root.mainloop()

