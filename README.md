# GitHub Follower Tracker

This app tracks your GitHub profile for followers, who follows you back, and who unfollows you. It also provides a user-friendly graphical interface for easy use.

This Python application allows you to monitor your GitHub followers, track who has unfollowed you, and who has followed you back. The application uses the GitHub API and the `requests` library to fetch the list of followers for a given user and compare it to the list of followers from previous checks. It then outputs the changes in follower count and status through a GUI.

## Getting Started

To get started, you'll need to have Python 3 installed on your machine, along with the `requests` and `tkinter` libraries. You'll also need a personal access token from GitHub to authenticate your requests to the API. The application provides an input form to enter your GitHub username, personal access token, and specify the file name for storing follower data.

## Usage

To use the GitHub Follower Tracker, clone this repository to your local machine and run the `github_follower_tracker_UserInputForm.py` script.

Here's how to use the application:

1. Run the script in the terminal or your preferred Python environment:
   ```bash
   python github_follower_tracker_UserInputFornm.py

2. A graphical user interface (GUI) will appear.

3. Enter your GitHub username, personal access token, and the file name where you want to save the follower data.

4. Click the "Start Tracking" button to begin monitoring your followers. The application will display new followers, unfollowers, and followers who have followed you back in the GUI window.

## Example
Below is an example of the application's GUI in action:

<img width="444" alt="image" src="https://github.com/user-attachments/assets/e9c5f7f0-8d9e-4acf-a673-d6335b8ad3f0">

## Contributing
Contributions are always welcome! If you find a bug or want to add a new feature, feel free to submit a pull request. To get started, fork this repository and create a new branch for your changes. Make your changes and submit a pull request with a brief description of your modifications.

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.

## Acknowledgments
Thanks to the GitHub API team for providing an easy-to-use API for fetching user data.
Thanks to the requests and tkinter teams for creating great Python libraries for making HTTP requests and building GUIs, respectively.
