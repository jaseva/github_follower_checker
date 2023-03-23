# github_follower_unchecker
This app tracks your Github profile for who follows you, who follows you back, and who unfollows you.

This is a Python script that allows you to check your Github followers, track who has unfollowed you, and who has followed you back. The script uses the Github API and the requests library to fetch the list of followers for a given user and compare it to the list of followers from the previous check. It then outputs the changes in the follower count and status.

# Getting Started
To get started, you'll need to have Python 3 installed on your machine, along with the requests library. You'll also need a personal access token from Github to authenticate your requests to the API. Follow the instructions in the script to obtain a personal access token.

# Usage
To use the Github follower checker, clone this repository to your local machine and run the github_follower_checker.py script in the terminal. The script takes the following arguments:

username (required): The Github username to check for followers.
token (required): Your personal access token from Github.
output (optional): The name of the output file. By default, the output is written to a file named follower_changes.txt.

Here's an example of how to run the script:

python github_follower_checker.py --username USERNAME --token YOUR_TOKEN --output FILENAME

# Contributing
Contributions are always welcome! If you find a bug or want to add a new feature, feel free to submit a pull request. To get started, fork this repository and create a new branch for your changes. Make your changes and submit a pull request with a brief description of your changes.

# License
This project is licensed under the MIT License - see the LICENSE.md file for details.

# Acknowledgments
Thanks to the Github API team for providing an easy-to-use API for fetching user data.
Thanks to the requests library team for creating a great Python library for making HTTP requests.
