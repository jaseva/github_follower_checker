import requests

def get_all_followers(username, token, url):
    followers = []
    headers = {'Authorization': f'token {token}'}
    while url:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Failed to retrieve followers: {response.status_code}")
        followers.extend([follower['login'] for follower in response.json()])
        url = response.links.get('next', {}).get('url')  # Get the next page URL, if any
    return followers

def format_list(title, items, color):
    formatted = f'{title}:\n'
    for item in items:
        formatted += f'  - {item}\n'
    return formatted, color
