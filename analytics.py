# import matplotlib.pyplot as plt
# from datetime import datetime

# # Function to plot follower growth over time
# def plot_follower_growth(follower_history):
#     # Convert dates to datetime objects for proper plotting
#     dates = [datetime.strptime(date, '%Y-%m-%d') for date in follower_history.keys()]
#     follower_counts = list(follower_history.values())

#     plt.figure(figsize=(10, 5))
#     plt.plot(dates, follower_counts, marker='o', linestyle='-', color='b')
#     plt.title('Follower Growth Over Time')
#     plt.xlabel('Date')
#     plt.ylabel('Number of Followers')
#     plt.grid(True)
#     plt.xticks(rotation=45)
#     plt.tight_layout()
#     plt.show()

# def segment_followers(followers, segmentation_type):
#     segments = {}

#     if segmentation_type == "activity":
#         # Example segmentation by username length as a proxy for activity
#         segments['short_usernames'] = [user for user in followers if len(user) < 7]
#         segments['long_usernames'] = [user for user in followers if len(user) >= 7]

#     elif segmentation_type == "date_followed":
#         # Placeholder as date followed is not available from GitHub API
#         segments['date_followed_segment'] = followers  # Dummy segment for demonstration

#     return segments

# ------------------------------

import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

# Function to create a table if it doesn't exist
def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS followers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()

# Function to insert a follower into the database
def insert_follower(conn, username, timestamp):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO followers (username, timestamp)
        VALUES (?, ?)
    ''', (username, timestamp))
    conn.commit()

# Function to plot follower growth over time
def plot_follower_growth(follower_history):
    dates = [datetime.strptime(date, '%Y-%m-%d %H:%M:%S') for date in follower_history.keys()]
    follower_counts = list(follower_history.values())

    plt.figure(figsize=(10, 5))
    plt.plot(dates, follower_counts, marker='o', linestyle='-', color='b')
    plt.title('Follower Growth Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Followers')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Function to segment followers
def segment_followers(followers, segmentation_type):
    segments = {}

    if segmentation_type == "activity":
        segments['short_usernames'] = [user for user in followers if len(user) < 7]
        segments['long_usernames'] = [user for user in followers if len(user) >= 7]

    elif segmentation_type == "date_followed":
        segments['date_followed_segment'] = followers  # Dummy segment for demonstration

    return segments
