import requests
import random
import string
import time
from colorama import init, Fore

init(autoreset=True)

WORD_URL = "https://raw.githubusercontent.com/first20hours/google-10000-english/refs/heads/master/google-10000-english-usa-no-swears-long.txt"


def load_words():
    r = requests.get(WORD_URL)
    r.raise_for_status()
    return r.text.splitlines()


def generate_username(words):
    return random.choice(words).lower() + random.choice(words).lower()


def get_domain():
    r = requests.get("https://api.mail.tm/domains")
    r.raise_for_status()
    return r.json()["hydra:member"][0]["domain"]


def create_account(email, password):
    r = requests.post("https://api.mail.tm/accounts", json={
        "address": email,
        "password": password
    })
    return r.status_code, r.text


def get_token(email, password):
    r = requests.post("https://api.mail.tm/token", json={
        "address": email,
        "password": password
    })
    return r.json().get("token")


def save_account(email, password):
    with open("Accounts.txt", "a") as f:
        f.write(f"{email}:{password}\n")


def main():
    print(Fore.CYAN + "Mail.tm Bulk Account Generator")

    words = load_words()
    domain = get_domain()

    amount = int(input("How many accounts do you want? "))
    base_password = input("What should the password be? ")

    created = 0
    failed = 0

    for i in range(amount):
        password = base_password + str(random.randint(100, 9999))

        username = generate_username(words)
        email = f"{username}@{domain}"

        print(Fore.YELLOW + f"[{i+1}/{amount}] Creating: {email}")

        status, _ = create_account(email, password)

        if status in (200, 201):
            token = get_token(email, password)

            if token:
                save_account(email, password)
                created += 1
                print(Fore.GREEN + f"✓ Created {email}")
            else:
                failed += 1
                print(Fore.RED + "Login failed")
        else:
            failed += 1
            print(Fore.RED + f"Failed ({status})")

        time.sleep(random.uniform(0.5, 1.5))

    print(Fore.CYAN + "\n========== Summary ==========")
    print(Fore.GREEN + f"Accounts Created: {created}")
    print(Fore.RED + f"Failed: {failed}")
    print(Fore.YELLOW + "Saved To: Accounts.txt")

    input("\nPress Enter to exit...")
if __name__ == "__main__":
    main()
