# GitHub Follower Checker

This app tracks your GitHub profile for who follows you, who follows you back, and who unfollows you. It now includes advanced analytics to visualize follower growth trends, track engagement metrics, and segment followers.

## Features
- Tracks followers and unfollowers.
- Stores follower data in a database.
- Provides analytics, including follower growth plots and segmentation.

## Getting Started

### Prerequisites

To get started, you'll need:

- **Python 3** installed on your machine.
- The following Python libraries:
  - `requests`
  - `matplotlib`
  - `tkinter`
  - `openai`
  - `python-dotenv`
  
- A **personal access token** from GitHub to authenticate your requests to the API.
- An **API Key** from OpenAI to access GTP LLM models to summarize GitHub API requests.

### Installation

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/yourusername/github_follower_checker.git
    cd github_follower_checker
    ```

2. **Install Dependencies**:
    Install the required libraries using pip:
    ```sh
    pip install -r requirements.txt
    ```

3. **Set Up Your GitHub Token**:
   - Generate a personal access token from GitHub by following [these instructions](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token).

### Usage

To use the GitHub Follower Checker, run the `github_follower_checker.py` script in the terminal or a Python IDE.
- Input your GitHub username, personal access token, and the desired file name to store followers.
- Click **Start Tracking** to begin monitoring your followers.
- Use **Show Analytics** to visualize follower growth.
- Use **Segment Followers** to categorize followers by activity or other metrics.

```sh
python github_follower_checker.py
```
<div align="center">
<img width="526" alt="image" src="https://github.com/user-attachments/assets/60f5c3c4-fa76-4237-81be-656f630799f6">

<img width="745" alt="image" src="https://github.com/user-attachments/assets/b58d8488-995b-441c-9a11-3d8127d1078c">
</div>

## User Interface

- **GitHub Username**: Enter the GitHub username you want to track.
- **Personal Access Token**: Enter your GitHub personal access token.
- **Followers File Name**: Specify the name of the file where follower data will be stored (e.g., `followers.json`).
- **Start Tracking**: Click this button to begin tracking your followers.
- **Show Analytics**: After tracking, use this button to visualize follower growth trends.
- **Segment Followers**: This feature allows you to group your followers based on various criteria like activity or date followed.

### Advanced Analytics

The GitHub Follower Tracker now includes advanced analytics features:

- **Follower Growth Trends**: Visualize your follower growth over time with charts and graphs.
- **Engagement Metrics**: Although this feature is currently a placeholder, it will eventually track your interaction history with followers (e.g., comments, likes).
- **Follower Segmentation**: Group followers based on criteria like activity level, date followed, or contribution to repositories.

## Notes
- Follower history is stored in a SQLite database (`followers.db`).
- Date of following is approximated by when the tracking script is run.

### Example

1. **Start Tracking**:
    ```sh
    python github_follower_checker.py
    ```

2. **View Follower Growth**:
    - After running the script and tracking followers, click on the "Show Analytics" button to visualize your follower growth over time.

3. **Segment Followers**:
    - Choose a segmentation type from the dropdown and click "Segment Followers" to group followers accordingly.

### Project Structure

- `github_follower_checker.py`: The main script to run the application.
- `analytics.py`: Handles the advanced analytics, such as plotting follower growth and segmenting followers.
- `utils.py`: Contains utility functions for fetching and formatting follower data.
- `requirements.txt`: Lists the dependencies required to run the application.
- `README.md`: Documentation for the project.

### Contributing

Contributions are always welcome! If you find a bug or want to add a new feature, feel free to submit a pull request. To get started:

1. Fork this repository.
2. Create a new branch for your changes.
3. Make your changes and submit a pull request with a brief description.

### License

This project is licensed under the MIT License - see the `LICENSE.md` file for details.

### Acknowledgments

- Thanks to the GitHub API team for providing an easy-to-use API for fetching user data.
- Thanks to the developers of the `requests`, `matplotlib`, `tkinter`, `openai`, and `python-dotenv` libraries for making HTTP requests and data visualization in Python straightforward.
