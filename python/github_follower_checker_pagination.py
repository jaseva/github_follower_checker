## github-follower-checker-pagination
## MIT License
## Created Date: 2024-08-31
## Version 1.0

import requests
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

# Print out the changes in the followers list
print(f'New followers: {new_followers}')
print(f'Unfollowers: {unfollowers}')
print(f'Followers who followed back: {followers_back}')

# Write the current list of followers to file for the next comparison
with open(followers_file, 'w') as f:
    f.write('\n'.join(current_followers))

# Wait for 1 hour before checking again
time.sleep(3600)
