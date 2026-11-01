# Intended for CLI use..

import os
import json, urllib.request
from datetime import date, timedelta

endpoint = f"https://www.nytimes.com/svc/wordle/v2/%s.json"

# Utility

def clear_cli():
    os.system('cls' if os.name == 'nt' else 'clear')

# Main Functions

def GetAnswerForDate(year: int, month: int, day: int):
    url = endpoint % f"{year}-{month:02d}-{day:02d}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    data = json.load(urllib.request.urlopen(req))
    return data['solution']

def GenerateHelp():
    print((
        "\nHELP :\n"
        "\tCommands:\n"
        "\t? or help - Show this help message\n"
        "\te - Exit the program\n"
        "\t.gen <integer = 5> - Generates a list of answers for the next following days\n"
    ))

# Initialization

def main():
    print((
        "This script fetches the answer for today's New York Times Wordle puzzle.\n"
        "Type ? or help for help.\n"
    ))

    day_input = input("Enter a date (YYYY-MM-DD)\n\n\tDate: ")

    today = date.today()

    if day_input.lower() in ["?", "help"]:
        GenerateHelp()
        return True
    elif day_input.lower() == "e":
        return False
    elif day_input.lower().startswith(".gen"):
        try:
            num_days = int(day_input.split()[1]) if len(day_input.split()) > 1 else 5

            if num_days > 10:
                print("\n.gen caps out at 10 to prevent excessive requests. Generating 10 days instead.\n")
                num_days = 10
            
            for i in range(num_days):
                future_date = today + timedelta(days=i)
                answer = GetAnswerForDate(future_date.year, future_date.month, future_date.day)
                print(f"\t{future_date}: {answer.upper()}")

        except ValueError:
            print("\nInvalid number of days. Please provide an integer.")
        
        return True
    
    elif day_input == "":
        answer = GetAnswerForDate(today.year, today.month, today.day)
    else:
        try:
            year, month, day = map(int, day_input.split("-"))
            answer = GetAnswerForDate(year, month, day)
        except ValueError:
            print("\nInvalid date format. Please use YYYY-MM-DD.")
            return True

    print(f"\n>> {answer.upper()} << ({day_input if day_input else today})")
    return True

if __name__ == "__main__":
    while True:
        if not main():
            break
        else:
            if input("\nPress Enter to restart or 'e' to exit...") == 'e':
                break
            else:
                clear_cli()
                continue