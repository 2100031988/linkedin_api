import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

# Function to extract user data from HTML result
def parse_user_data(result):
    profile = {}
    profile["name"] = result.find("h2", class_="search-result__title").text.strip()
    profile["title"] = result.find("h3", class_="search-result__headline").text.strip()
    profile["company"] = result.find("span", class_="search-result__company-name").text.strip()
    profile["location"] = result.find("span", class_="search-result__location").text.strip()
    profile["url"] = result.find("a", class_="search-result__result-link")["href"]
    return profile

# User input
first_name = input("Enter First Name: ")
last_name = input("Enter Last Name: ")

# Build search URL
search_url = f"https://www.linkedin.com/search/results/people/?keywords={first_name}%20{last_name}"

# Initialize headless Chrome driver
driver = webdriver.Chrome()

try:
    # Open LinkedIn search page
    driver.get(search_url)

    # Wait for dynamic content to load
    time.sleep(150)  # Adjust as needed

    # Scroll down to load more profiles
    for _ in range(3):  # Adjust the number of times to scroll based on your needs
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Adjust as needed

    # Parse HTML content with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Extract user data from each search result
    user_data = [parse_user_data(result) for result in soup.find_all("li", class_="search-result__occluded-item ember-view")]

    # Filter to top 5 relevant results
    relevant_data = user_data[:5]

    # Print or save the relevant data as needed
    for user in relevant_data:
        print(f"Name: {user['name']}, Title: {user['title']}, Company: {user['company']}, Location: {user['location']}, URL: {user['url']}")

finally:
    # Close browser driver
    driver.quit()












# import requests
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import csv
# import time
#
# def get_linkedin_data(client_id, client_secret, first_name, last_name):
#     # OAuth2 Authentication to get access token
#     token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
#     api_url = f'https://api.linkedin.com/v2/people-search?first_name={first_name}&last_name={last_name}&count=10'
#
#     auth_params = {
#         'grant_type': 'client_credentials',
#         'client_id': client_id,
#         'client_secret': client_secret
#     }
#
#     token_response = requests.post(token_url, data=auth_params)
#     access_token = token_response.json().get('access_token', '')
#
#     # Make request to LinkedIn API
#     headers = {'Authorization': f'Bearer {access_token}'}
#     response = requests.get(api_url, headers=headers)
#     data = response.json()
#
#     # Extract relevant information from the response
#     results = data.get('elements', [])[:5]
#
#     # Save the data to a CSV file
#     with open('linkedin_api_output.csv', 'w', newline='') as csvfile:
#         fieldnames = ['Name', 'Title', 'Location', 'Profile URL']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()
#
#         for result in results:
#             name = result.get('name', '')
#             title = result.get('title', '')
#             location = result.get('location', {}).get('country', '')
#             profile_url = result.get('publicIdentifier', '')
#
#             writer.writerow({'Name': name, 'Title': title, 'Location': location, 'Profile URL': profile_url})
#
#
# def get_linkedin_data_browser(client_id, client_secret, first_name, last_name):
#     # OAuth2 Authentication to get authorization code
#     redirect_uri = 'http://localhost:8000'
#     auth_url = 'https://www.linkedin.com/oauth/v2/authorization'
#     auth_url += f'?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope=r_liteprofile%20r_emailaddress'
#
#     # Open the browser for user authentication
#     driver = webdriver.Chrome()
#     driver.get(auth_url)
#
#     # Wait for the user to manually log in and grant access
#     input("Press Enter after granting access on the LinkedIn page...")
#
#     # After user interaction, grab the current URL
#     current_url = driver.current_url
#
#     # Close the browser
#     driver.quit()
#
#     # Extract authorization code from the URL
#     authorization_code = current_url.split('code=')[1].split('&')[0]
#
#     # Exchange authorization code for access token
#     access_token = exchange_code_for_token(client_id, client_secret, redirect_uri, authorization_code)
#
#     # Use access token to make requests to LinkedIn API
#     get_linkedin_api_data(access_token, first_name, last_name)
#
#
# def exchange_code_for_token(client_id, client_secret, redirect_uri, authorization_code):
#     # OAuth2 Token Request Parameters
#     token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
#     token_params = {
#         'grant_type': 'authorization_code',
#         'code': authorization_code,
#         'redirect_uri': redirect_uri,
#         'client_id': client_id,
#         'client_secret': client_secret
#     }
#
#     # Request access token
#     token_response = requests.post(token_url, data=token_params)
#     token_data = token_response.json()
#
#     # Extract access token from response
#     access_token = token_data.get('access_token', '')
#
#     return access_token
#
#
# def get_linkedin_api_data(access_token, first_name, last_name):
#     # LinkedIn API Request URL
#     api_url = f'https://api.linkedin.com/v2/people-search?first_name={first_name}&last_name={last_name}&count=10'
#
#     # Make request to LinkedIn API
#     headers = {'Authorization': f'Bearer {access_token}'}
#     response = requests.get(api_url, headers=headers)
#     data = response.json()
#
#     # Extract relevant information from the response
#     results = data.get('elements', [])[:5]
#
#     # Save the data to a CSV file
#     with open('linkedin_browser_output.csv', 'w', newline='') as csvfile:
#         fieldnames = ['Name', 'Title', 'Location', 'Profile URL']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()
#
#         for result in results:
#             name = result.get('name', '')
#             title = result.get('title', '')
#             location = result.get('location', {}).get('country', '')
#             profile_url = result.get('publicIdentifier', '')
#
#             writer.writerow({'Name': name, 'Title': title, 'Location': location, 'Profile URL': profile_url})
#
#
# # Example usage
# client_id = '78ans2hzt2cwfv'
# client_secret = 'sRtmd5DCUsykp9qJ'
# get_linkedin_data(client_id, client_secret, 'John', 'Doe')
# get_linkedin_data_browser(client_id, client_secret, 'John', 'Doe')

