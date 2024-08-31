import matplotlib.pyplot as plt
import datetime

def plot_follower_growth(follower_history):
    dates = list(follower_history.keys())
    follower_counts = list(follower_history.values())

    plt.figure(figsize=(10, 6))
    plt.plot(dates, follower_counts, marker='o')
    plt.title('Follower Growth Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Followers')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def segment_followers(followers, segmentation_type):
    if segmentation_type == "activity":
        # Example segmentation logic: create groups based on follower activity
        return {"Active": [f for f in followers if is_active(f)],
                "Inactive": [f for f in followers if not is_active(f)]}
    elif segmentation_type == "date_followed":
        # Example segmentation logic: create groups based on date followed
        return {"Recent": [f for f in followers if followed_recently(f)],
                "Old": [f for f in followers if not followed_recently(f)]}
    # Add more segmentation types as needed

def is_active(follower):
    # Placeholder for activity check logic
    return True  # or False based on real criteria

def followed_recently(follower):
    # Placeholder for date followed logic
    return True  # or False based on real criteria
