import requests
from tabulate import tabulate
from colorama import Fore, Style
import json
import os
import random
import mimetypes
import sys
from loguru import logger
from urllib.parse import parse_qs
import time
from datetime import datetime, timedelta, timezone

log_line = "~" * 38
mrh = Fore.LIGHTRED_EX
pth = Fore.LIGHTWHITE_EX
hju = Fore.LIGHTGREEN_EX
kng = Fore.LIGHTYELLOW_EX
bru = Fore.LIGHTBLUE_EX
reset = Style.RESET_ALL
htm = Fore.LIGHTBLACK_EX
putih = Fore.LIGHTWHITE_EX

def load_config():
    with open('config.json') as f:
        return json.load(f)

config = load_config()

logger.remove()
logger.add(sink=sys.stdout, format="<white>{time:YYYY-MM-DD HH:mm:ss}</white>"
                                   " | <level>{level: <8}</level>"
                                   " | <cyan><b>{line}</b></cyan>"
                                   " - <white><b>{message}</b></white>")
logger = logger.opt(colors=True)

hitam = Fore.LIGHTBLACK_EX
def log(message):
    now = datetime.now().isoformat(" ").split(".")[0]
    print(f"{hitam}[{now}]{putih} {message}{reset}")

CATS_PATH = r"cats"
def countdown_timer(seconds):
    while seconds:
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        h = str(h).zfill(2)
        m = str(m).zfill(2)
        s = str(s).zfill(2)
        print(f"{pth}please wait until {h}:{m}:{s} ", flush=True, end="\r")
        seconds -= 1
        time.sleep(1)
    print(f"{pth}please wait until {h}:{m}:{s} ", flush=True, end="\r")
def get_authorization_tokens():
    with open('query.txt', 'r') as file:
        return [line.strip() for line in file if line.strip()]



# Function to set headers with the provided token
def get_headers(token):
    return {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": f"tma {token}",
        "content-type": "application/json",
        "priority": "u=1, i",
        "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Microsoft Edge\";v=\"127\", \"Chromium\";v=\"127\", \"Microsoft Edge WebView2\";v=\"127\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "Referer": "https://cats-frontend.tgapps.store/",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }

def fetch_tasks(headers):
    url = "https://api.catshouse.club/tasks/user?group=cats"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def clear_task(task_id, task_title, headers):
    url = f"https://api.catshouse.club/tasks/{task_id}/complete"
    response = requests.post(url, headers=headers, json={})
    if response.status_code == 200:
        log(Fore.GREEN + f"Task {Fore.WHITE}{task_title} {Fore.GREEN}successfully marked as completed.")
        return response.json()
    else:
        log(Fore.RED + f"Failed to mark task {task_title} as completed.")
        response.raise_for_status()

def generate_random_string(length):
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    random_string = ''
    for _ in range(length):
        random_index = int((len(characters) * int.from_bytes(os.urandom(1), 'big')) / 256)
        random_string += characters[random_index]
    return random_string

def generate_random_string_lower(length):
    characters = ('abcdefghijklmnopqrstuvwxyz0123456789')
    random_string = ''
    for _ in range(length):
        random_index = int((len(characters) * int.from_bytes(os.urandom(1), 'big')) / 256)
        random_string += characters[random_index]
    return random_string




def get_random_cat_image():
    images = [f for f in os.listdir(CATS_PATH) if f.lower().endswith(('.png', '.jpeg', '.jpg'))]


    image = random.choice(images)
    image_path = os.path.join(CATS_PATH, image)
    mime_type = mimetypes.guess_type(image_path)

    with open(image_path, 'r+b') as file:
        data = file.read()

    image_data = (f'Content-Disposition: form-data; name="photo"; filename="{image}"\r\n'
                  f'Content-Type: {mime_type}\r\n\r\n').encode('utf-8')
    image_data += data
    return image_data

def check_avatar(token):
    url = f"https://api.catshouse.club/user/avatar"
    headers = get_headers(token)
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    response_json = response.json()
    time_obj = datetime.fromisoformat(response_json['attemptTime'][:-1]) + timedelta(hours=24)
    return time_obj



def update_avatar(token):
    try:
        url = f"https://api.catshouse.club/user/avatar/upgrade"
        headers = get_headers(token)
        cat_image = get_random_cat_image()
        hash_id = generate_random_string(length=16)
        headers['Content-Type'] = f'multipart/form-data; boundary=----WebKitFormBoundary{hash_id}'
        data = (f'------WebKitFormBoundary{hash_id}\r\n'.encode('utf-8') + cat_image +
                    f'\r\n------WebKitFormBoundary{hash_id}--\r\n'.encode('utf-8'))

        response = requests.post(url,headers=headers, data=data)
        response.raise_for_status()
        response_json = response.json()
        logger.info(
            f"| Avatar task completed! | Reward: <e>+{response_json['rewards']}</e> CATS")
        return response_json
    except Exception as e:
        logger.error(f"| Unknown error while processing avatar task | Error: {e}")













def print_welcome_message():
    banner = f"""{Fore.GREEN}
     ██████  ██    ██   ██████  ██    ██  ███    ███  ██████   ███████  ██████  
    ██       ██    ██  ██       ██    ██  ████  ████  ██   ██  ██       ██   ██ 
    ██       ██    ██  ██       ██    ██  ██ ████ ██  ██████   █████    ██████  
    ██       ██    ██  ██       ██    ██  ██  ██  ██  ██   ██  ██       ██   ██ 
     ██████   ██████    ██████   ██████   ██      ██  ██████   ███████  ██   ██     
        Auto Claim Bot For Cats - Cucumber Automation
        Github  : https://github.com/cucumber-pickle
        Telegram: https://t.me/cucumber_script
            {Style.RESET_ALL}"""
    print(banner)
    print(log_line)

def extract_user_data(auth_data: str) -> dict:
    query_params = parse_qs(auth_data)
    user_info = json.loads(query_params['user'][0])
    return user_info

def complete_all_tasks():
    tokens = get_authorization_tokens()

    for i, token in enumerate(tokens):
        account = f"account_{i+1}"
        user_info = extract_user_data(token)


        log(bru + f"Number : {pth}{account}")
        log(bru + f"Account : {pth}{user_info.get("username")}")
        headers = get_headers(token)

        # Attempt to fetch tasks with error handling
        try:
            tasks = fetch_tasks(headers).get('tasks', [])
        except requests.exceptions.HTTPError as e:
            log(Fore.RED + f"HTTPError for token {token}: {e}")
            log(Fore.YELLOW + "Waiting for 30 seconds before retrying...")
            time.sleep(5)  # Wait for 30 seconds
            continue  # Skip to the next token


        time_at = check_avatar(token)
        if time_at.tzinfo is None:
            time_at = time_at.replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)

        if time_at < now:
            update_avatar(token)
            countdown_timer(3)
        else:
            log("Time for updating the avatar has not yet come")

        for task in tasks:
            if not task['completed']:
                if task['type'] == 'YOUTUBE_WATCH' or task['type'] == 'SUBSCRIBE_TO_CHANNEL' or task['type'] == 'ACTIVITY_CHALLENGE' or task['type'] == 'BOOST_CHANNEL':
                    continue
                try:
                    clear_task(task['id'], task['title'], headers)
                    countdown_timer(1)
                except requests.RequestException:
                    log(Fore.WHITE + f"Skipping task {task['title']} due to an error.")
                    countdown_timer(1)

        log("All available tasks have been completed")

        acc_delay = config.get('account_delay')
        print(log_line)
        countdown_timer(acc_delay)

def user():
    tokens = get_authorization_tokens()
    all_user_data = []
    total_rewards_sum = 0

    for i, token in enumerate(tokens):

        headers = get_headers(token)
        url = "https://api.catshouse.club/user"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()


            # Extract required fields
            account = f"account_{i+1}"


            first_name = data.get('firstName')
            last_name = data.get('lastName')
            telegram_age = data.get('telegramAge')
            total_rewards = data.get('totalRewards')


            countdown_timer(1)

            # Collect user data
            all_user_data.append([account, first_name, last_name, telegram_age, total_rewards])
            total_rewards_sum += total_rewards  # Accumulate total rewards
        else:
            print(Fore.RED + f"Failed to fetch user data for token {token}.")
    
    # Prepare data for tabulate
    table_data = [
        ['account_num', "First Name", "Last Name", "Telegram Age", "Total Rewards"]
    ]
    table_data.extend(all_user_data)
    
    # Print table
    print(tabulate(table_data, headers='firstrow', tablefmt='grid'))
    
    # Print total rewards sum with color
    print(Fore.GREEN + f"\nTotal Rewards: " + Fore.WHITE + f"{total_rewards_sum}" + Style.RESET_ALL)



def main():
    while True:
        print_welcome_message()
        complete_all_tasks()
        print(Fore.WHITE + f"\nDisplaying user information...")
        user()
        cycle_delay = config.get('cycle_delay')
        countdown_timer(cycle_delay)

# Example usage
if __name__ == "__main__":
    main()
