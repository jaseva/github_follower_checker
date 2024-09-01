# import requests

# def get_all_followers(username, token, followers_url):
#     followers = []
#     headers = {'Authorization': f'token {token}'}

#     while followers_url:
#         response = requests.get(followers_url, headers=headers)
#         response.raise_for_status()
#         data = response.json()
#         followers.extend([user['login'] for user in data])
#         followers_url = response.links.get('next', {}).get('url')
    
#     return followers

# def format_list(title, user_list, color):
#     if not user_list:
#         return f"{title}: None\n", color

#     formatted_list = f"{title} ({len(user_list)}):\n" + '\n'.join(user_list) + '\n'
#     return formatted_list, color

# ------------------------

import requests

def get_all_followers(username, token, followers_url):
    followers = []
    headers = {'Authorization': f'token {token}'}
    while followers_url:
        response = requests.get(followers_url, headers=headers)
        response.raise_for_status()
        followers += [follower['login'] for follower in response.json()]
        followers_url = response.links.get('next', {}).get('url')
    return followers

def format_list(title, followers, color):
    if not followers:
        return f"{title}: None\n", color
    formatted_list = f"{title}:\n" + "\n".join(f"- {follower}" for follower in followers) + "\n\n"
    return formatted_list, color
