import requests
import json
import os

BASE_URL = "http://127.0.0.1:5000"

# --- Helper Functions ---
def print_response(name, response):
    print(f"--- {name} ---")
    print(f"Status Code: {response.status_code}")
    content_type = response.headers.get('content-type', '')
    if 'application/json' in content_type:
        try:
            print(f"Response JSON: {json.dumps(response.json(), indent=2)}")
        except json.JSONDecodeError:
            print(f"Response Text: {response.text}")
    elif 'image' in content_type:
        print("Image received successfully")
    else:
        print(f"Response Text: {response.text}")
    print("-" * (len(name) + 6))
    print()

# --- Test Data ---
user_credentials = {
    "username": "testuser6",
    "password": "testpassword"
}
token = None

# --- Test Functions ---
def test_register():
    print("--- Testing Registration ---")
    response = requests.post(f"{BASE_URL}/auth/register", json=user_credentials)
    print_response("Register", response)
    return response.status_code == 201

def test_login():
    global token
    print("--- Testing Login ---")
    response = requests.post(f"{BASE_URL}/auth/login", auth=(user_credentials['username'], user_credentials['password']))
    print_response("Login", response)
    if response.status_code == 200:
        token = response.json().get('token')
        return True
    return False

def test_notes():
    print("--- Testing Notes ---")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create Note
    note_data = {"title": "Test Note", "content": "This is a test note."}
    response = requests.post(f"{BASE_URL}/notes/", json=note_data, headers=headers)
    print_response("Create Note", response)
    
    # Get All Notes to find the created note's ID
    response = requests.get(f"{BASE_URL}/notes/", headers=headers)
    print_response("Get All Notes", response)
    note_id = response.json()['notes'][0]['id']

    # Get Note by ID
    response = requests.get(f"{BASE_URL}/notes/{note_id}", headers=headers)
    print_response("Get Note by ID", response)

    # Update Note
    update_data = {"title": "Updated Note"}
    response = requests.put(f"{BASE_URL}/notes/{note_id}", json=update_data, headers=headers)
    print_response("Update Note", response)

    # Delete Note
    response = requests.delete(f"{BASE_URL}/notes/{note_id}", headers=headers)
    print_response("Delete Note", response)

def test_trades(image_content):
    print("--- Testing Trades ---")
    headers = {"Authorization": f"Bearer {token}"}

    # Create Trade with Image
    trade_data = {
        "ticker": "AAPL",
        "result": "Win",
        "total_pnl": 250.00,
        "entry_datetime": "2025-09-01T09:30:00Z",
        "exit_datetime": "2025-09-01T15:45:00Z",
        "risk_reward": 2.5,
        "position": "Long",
        "stoploss_pips": 10,
        "range": 50,
        "result_type": "Good Win",
        "entry_model": "Breakout",
        "trade_model": "Scalp",
        "setup_type": "A+",
        "confluences": json.dumps(["Breakout", "EMA Cross"]),
        "trade_note": "Good entry on breakout.",
        "roadmap": "Planned to take profit at 155.00."
    }
    with open("demo.png", "rb") as f:
        files = {"screenshot": f}
        response = requests.post(f"{BASE_URL}/trades/", data=trade_data, files=files, headers=headers)
    print_response("Create Trade", response)

    # Get All Trades to find the created trade's ID and screenshot filename
    response = requests.get(f"{BASE_URL}/trades/", headers=headers)
    print_response("Get All Trades", response)
    trade_id = response.json()['trades'][0]['id']
    screenshot_filename = response.json()['trades'][0]['screenshot_filename']

    # Get Trade by ID
    response = requests.get(f"{BASE_URL}/trades/{trade_id}", headers=headers)
    print_response("Get Trade by ID", response)

    # Get Screenshot
    response = requests.get(f"{BASE_URL}/trades/screenshots/{screenshot_filename}", headers=headers)
    print_response("Get Screenshot", response)
    if response.content == image_content:
        print("Screenshot content matches uploaded content.")
    else:
        print("Screenshot content does not match uploaded content.")

    # Update Trade
    update_data = {"ticker": "MSFT"}
    response = requests.put(f"{BASE_URL}/trades/{trade_id}", data=update_data, headers=headers)
    print_response("Update Trade", response)

    # Delete Trade
    response = requests.delete(f"{BASE_URL}/trades/{trade_id}", headers=headers)
    print_response("Delete Trade", response)

def test_playbooks():
    print("--- Testing Playbooks ---")
    headers = {"Authorization": f"Bearer {token}"}

    # Create Playbook
    playbook_data = {
        "title": "Breakout Strategy",
        "entry_model": "Breakout",
        "trade_model": "Intraday",
        "setup_grade": "A+",
        "confluences": ["Volume Spike", "RSI Divergence"],
        "rules": ["Enter on the first pullback to the broken resistance."],
        "confirmations": ["Price closes above resistance on H1 timeframe."],
        "invalidations": ["False breakout with immediate rejection."],
        "roadmap": ["Identify key level", "Wait for price to break and close above"],
        "tags": ["strategy", "breakout", "intraday"]
    }
    response = requests.post(f"{BASE_URL}/playbooks/", json=playbook_data, headers=headers)
    print_response("Create Playbook", response)
    playbook_id = response.json().get('playbook_id')

    # Get All Playbooks
    response = requests.get(f"{BASE_URL}/playbooks/", headers=headers)
    print_response("Get All Playbooks", response)

    # Get Playbook by ID
    response = requests.get(f"{BASE_URL}/playbooks/{playbook_id}", headers=headers)
    print_response("Get Playbook by ID", response)

    # Update Playbook
    update_data = {"title": "Updated Breakout Strategy"}
    response = requests.put(f"{BASE_URL}/playbooks/{playbook_id}", json=update_data, headers=headers)
    print_response("Update Playbook", response)

    # Delete Playbook
    response = requests.delete(f"{BASE_URL}/playbooks/{playbook_id}", headers=headers)
    print_response("Delete Playbook", response)

def test_events():
    print("--- Testing Events ---")
    response = requests.get(f"{BASE_URL}/events")
    print_response("Get Events", response)

def test_user_and_avatar():
    print("--- Testing User and Avatar ---")
    headers = {"Authorization": f"Bearer {token}"}

    # Get User
    response = requests.get(f"{BASE_URL}/auth/user", headers=headers)
    print_response("Get User", response)

    # Upload Avatar
    avatar_data = {"avatar": "SGVsbG8gV29ybGQ="} # base64 encoded "Hello World"
    response = requests.post(f"{BASE_URL}/auth/avatar", json=avatar_data, headers=headers)
    print_response("Upload Avatar", response)

    # Get User again to see updated avatar
    response = requests.get(f"{BASE_URL}/auth/user", headers=headers)
    print_response("Get User After Avatar Upload", response)

if __name__ == "__main__":
    # It's recommended to run the Flask app in a separate terminal
    # And then run this script.
    # Make sure to add a demo.png file to the same directory as this script.
    if not os.path.exists("demo.png"):
        # create a dummy demo.png file
        with open("demo.png", "w") as f:
            f.write("dummy content")

    with open("demo.png", "rb") as f:
        image_content = f.read()

    if test_register() and test_login():
        test_notes()
        test_trades(image_content)
        test_playbooks()
        test_events()
        test_user_and_avatar()
