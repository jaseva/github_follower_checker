## Github-Follower-Checker
## MIT License
## Created Date: 2023-03-23
## Modified Date: 2023-03-28
## Version 1.1

import requests
import time

# Your Github username and personal access token
USERNAME = 'your-username'
TOKEN = 'your-personal-access-token'

# The URL endpoints to retrieve your followers and users you follow
followers_url = f'https://api.github.com/users/{USERNAME}/followers'
following_url = f'https://api.github.com/users/{USERNAME}/following'

# The file names to store the previous list of followers and users you follow
followers_file = 'followers.txt'
following_file = 'following.txt'

# Retrieve the previous lists of followers and users you follow from file, or initialize empty lists
try:
    with open(followers_file, 'r') as f:
        previous_followers = f.read().splitlines()
except FileNotFoundError:
    previous_followers = []

try:
    with open(following_file, 'r') as f:
        previous_following = f.read().splitlines()
except FileNotFoundError:
    previous_following = []

# Retrieve the current lists of followers and users you follow from the Github API
headers = {'Authorization': f'token {TOKEN}'}
response = requests.get(followers_url, headers=headers)
current_followers = [follower['login'] for follower in response.json()]

response = requests.get(following_url, headers=headers)
current_following = [user['login'] for user in response.json()]

# Compare the current and previous lists of followers and users you follow to identify changes
new_followers = list(set(current_followers) - set(previous_followers))
unfollowers = list(set(previous_followers) - set(current_followers))
followers_back = list(set(previous_followers) & set(current_followers))

new_following = list(set(current_following) - set(previous_following))
not_following_back = list(set(current_following) - set(current_followers))

# Print out the changes in the followers and following lists
print(f'New followers: {new_followers}')
print(f'Unfollowers: {unfollowers}')
print(f'Followers who followed back: {followers_back}')
print(f'New following: {new_following}')
print(f'Users you follow but who don\'t follow you back: {not_following_back}')

# Write the current lists of followers and users you follow to file for the next comparison
with open(followers_file, 'w') as f:
    f.write('\n'.join(current_followers))

with open(following_file, 'w') as f:
    f.write('\n'.join(current_following))

# Wait for 1 hour before checking again
time.sleep(3600)
