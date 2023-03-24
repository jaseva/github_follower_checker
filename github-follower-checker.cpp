## Github-Follower-Checker
## MIT License
## Created Date: 2023-03-23
## Version 1.0

#include <iostream>
#include <fstream>
#include <vector>
#include <set>
#include <algorithm>
#include <chrono>
#include <thread>
#include <string>
#include <sstream>

#include "curl/curl.h"
#include "nlohmann/json.hpp"

using json = nlohmann::json;

// Your Github username and personal access token
const std::string USERNAME = "your-username";
const std::string TOKEN = "your-personal-access-token";

// The URL endpoint to retrieve your followers
const std::string FOLLOWERS_URL = "https://api.github.com/users/" + USERNAME + "/followers";

// The file name to store the previous list of followers
const std::string FOLLOWERS_FILE = "followers.txt";

std::vector<std::string> get_followers() {
  // Retrieve the current list of followers from the Github API
  struct curl_slist *headers = NULL;
  headers = curl_slist_append(headers, ("Authorization: token " + TOKEN).c_str());
  
  CURL *curl;
  CURLcode res;
  std::string readBuffer;
  curl = curl_easy_init();
  if(curl) {
    curl_easy_setopt(curl, CURLOPT_URL, FOLLOWERS_URL.c_str());
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, [](void *buffer, size_t size, size_t nmemb, void *userp) -> size_t {
      static_cast<std::string*>(userp)->append(static_cast<char*>(buffer), size * nmemb);
      return size * nmemb;
    });
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
    res = curl_easy_perform(curl);
    curl_easy_cleanup(curl);
  }
  
  std::vector<std::string> current_followers;
  if (res == CURLE_OK) {
    auto json_data = json::parse(readBuffer);
    for (auto& follower : json_data) {
      current_followers.push_back(follower["login"]);
    }
  }

  return current_followers;
}

int main() {
  // Retrieve the previous list of followers from file, or initialize an empty list
  std::vector<std::string> previous_followers;
  std::ifstream followers_file(FOLLOWERS_FILE);
  if (followers_file.is_open()) {
    std::string follower;
    while (getline(followers_file, follower)) {
      previous_followers.push_back(follower);
    }
    followers_file.close();
  }

  // Retrieve the current list of followers from the Github API
  std::vector<std::string> current_followers = get_followers();

  // Compare the current and previous lists of followers to identify changes
  std::set<std::string> new_followers;
  std::set<std::string> unfollowers;
  std::set<std::string> followers_back;
  std::sort(previous_followers.begin(), previous_followers.end());
  std::sort(current_followers.begin(), current_followers.end());
  std::set_difference(previous_followers.begin(), previous_followers.end(), current_followers.begin(), current_followers.end(), std::inserter(unfollowers, unfollowers.begin()));
  std::set_difference(current_followers.begin(), current_followers.end(), previous_followers.begin(), previous_followers.end(), std::inserter(new_followers, new_followers.begin()));
  std::set_intersection(previous_followers.begin(), previous_followers.end(), current_followers.begin(), current_followers.end(), std::inserter(followers_back, followers_back.begin()));

  // Print out the changes in the followers list
  std::cout << "
