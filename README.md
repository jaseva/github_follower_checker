# GitHub Follower Checker

This app tracks your GitHub profile for who follows you, who follows you back, and who unfollows you. It now includes advanced analytics to visualize follower growth trends, track engagement metrics, and segment followers.

## Features
- Tracks followers and unfollowers.
- Stores follower data in a database.
- Provides analytics, including follower growth plots and segmentation.
- Generates AI Summaries of user profiles (OpenAI GPT Models).

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

3. **Set Up Your Credentials**:
   - This step involves setting up two credentials:

   a. **GitHub Personal Access Token**:

      - Generate a personal access token from GitHub by following [these instructions](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token).   
      - Make sure to grant the "repo" and "user" scopes to allow the application to access your follower data and profile information.
      - Save your token securely. We recommend using a password manager or a dedicated secrets store.

   b. **OpenAI API Key**:

      - Create an OpenAI API key by following these instructions: https://platform.openai.com/account/api-keys
      - You'll need an OpenAI account for this.
      - Save your API key securely.

4. **Create a .env File**:

   - Create a new file named .env in the root directory of your project (where the README.md file is located).
   - This file is used to store sensitive information like API keys.
   - Important: Do not commit the .env file to version control (e.g., Git). This prevents your API keys from being exposed publicly.
   - Add the following line to your .env file, replacing <your_github_token> and <your_openai_api_key> with your actual credentials:
   - GITHUB_TOKEN=<your_github_token>
   - OPENAI_API_KEY=<your_openai_api_key>

5. **Run the Application**:

   - Once you've completed these steps, you can run the application using the following command:
     
   ```sh
   python github_follower_checker.py
   ```

   - This will start the Github Follower Tracker application with the necessary credentials.
  
### Usage

To use the GitHub Follower Checker, run the `github_follower_checker.py` script in the terminal or a Python IDE.
- Input your GitHub username, personal access token, and the desired file name to store followers.
- Click **Start Tracking** to begin monitoring your followers.
- Use **Show Analytics** to visualize follower growth.
- Use **Segment Followers** to categorize followers by activity or other metrics.

<div align="center">
<img width="526" alt="image" src="https://github.com/user-attachments/assets/d90fc901-8322-4139-bdaf-9748733a0be7">

<img width="748" alt="image" src="https://github.com/user-attachments/assets/320bf3a8-d7fa-4cd9-8b35-3a4ac4db6b36">

<img width="602" alt="image" src="https://github.com/user-attachments/assets/578d5077-fed5-4126-8639-ab2a0db3dc24">

<img width="865" alt="image" src="https://github.com/user-attachments/assets/3692f375-61c6-458d-8969-efaddbb504f3">

<img width="601" alt="image" src="https://github.com/user-attachments/assets/84b44518-b56c-4520-b56a-883309879d4c">

<img width="253" alt="image" src="https://github.com/user-attachments/assets/1d2b1917-e73e-4c73-b513-938e134eaef0">

<img width="309" alt="image" src="https://github.com/user-attachments/assets/2f78c707-f960-41ab-ab51-e675281938c1">
</div>

## User Interface

- **GitHub Username**: Enter the GitHub username you want to track or generate a summary (uses OpenAI GPT models).
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
