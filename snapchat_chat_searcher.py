import json
from datetime import datetime
import re

file_path = "REPLACE THIS WITH THE PATH TO YOUR SNAPCHAT JSON CHAT FILE"

with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)


def search_emails_and_passwords(data):
    search_results = []
    current_email = None
    current_password = None

    for chat in data["Received Saved Chat History"]:
        text = chat["Text"]
        email_matches = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', text)

        if email_matches:
            current_email = email_matches[0]
        elif current_email and not current_password:
            current_password = text.strip()
            search_results.append({"Email": current_email, "Password": current_password})
            current_email = None
            current_password = None

    return search_results


def search_chats_and_emails(data, search_type, search_person, search_term, start_date, end_date):
    if search_type == "chat":
        return chats(data, search_type, search_person, search_term, start_date, end_date)
    elif search_type == "email":
        return search_emails_and_passwords(data)
    elif search_type == "count":
        person_counts = {}
        for chat in data["Received Saved Chat History"]:
            person = chat["From"]
            if person not in person_counts:
                person_counts[person] = 0
            if search_term in chat["Text"] and (search_person is None or person == search_person):
                person_counts[person] += 1
        return [(person, count) for person, count in person_counts.items()]
    elif search_type == "person":
        search_results = []
        for chat in data["Received Saved Chat History"]:
            if chat["From"] == search_person and (search_term is None or search_term in chat["Text"]):
                search_results.append(chat)
        return search_results
    elif search_type == "date":
        search_results = []
        for chat in data["Received Saved Chat History"]:
            time_string = chat["Created"].replace(" UTC", "")
            chat_date = datetime.strptime(time_string, "%Y-%m-%d %H:%M:%S")
            if (search_person is None or chat["From"] == search_person) and (search_term is None or search_term in chat["Text"]) and (start_date is None or chat_date >= start_date) and (end_date is None or chat_date <= end_date):
                search_results.append(chat)
        return search_results
    else:
        return []




def chats(data, search_type, search_person, search_term, start_date, end_date):
    search_results = []
    if search_type == "count":
        person_counts = {}
        for chat in data["Received Saved Chat History"]:
            person = chat["From"]
            if person not in person_counts:
                person_counts[person] = 0
            if search_term in chat["Text"] and (search_person is None or person == search_person):
                person_counts[person] += 1
        search_results = [(person, count) for person, count in person_counts.items()]
    else:
        for chat in data["Received Saved Chat History"]:
            time_string = chat["Created"].replace(" UTC", "")
            chat_date = datetime.strptime(time_string, "%Y-%m-%d %H:%M:%S")
            if search_type == "person":
                if chat["From"] == search_person and (search_term is None or search_term in chat["Text"]):
                    search_results.append(chat)

            elif search_type == "chat":
                if (search_person is None or chat["From"] == search_person) and (search_term is None or search_term in chat["Text"]):
                    search_results.append(chat)

            elif search_type == "date":
                if (search_person is None or chat["From"] == search_person) and (start_date is None or chat_date >= start_date) and (end_date is None or chat_date <= end_date):
                    search_results.append(chat)
    return search_results


search_type = input("Enter search type (person/chat/date/count/email): ")
search_person = None
search_term = None
start_date_input = ""
end_date_input = ""

if search_type == "person":
    search_person = input("Enter search person: ")
    search_term = input("Enter search term from that person (or leave blank): ")

elif search_type == "chat":
    search_term = input("Enter search term: ")
    search_person = input("Enter search person (or leave blank): ")
    if search_person == "":
        search_person = None

elif search_type == "date":
    start_date_input = input("Enter start date (YYYY-MM-DD): ")
    end_date_input = input("Enter end date (YYYY-MM-DD): ")

elif search_type == "count":
    search_person = input("Enter person to count (or leave blank): ")
    search_term = input("Enter search term to count: ")
    if search_person == "":
        search_person = None


start_date = datetime.strptime(start_date_input, "%Y-%m-%d") if start_date_input else None
end_date = datetime.strptime(end_date_input, "%Y-%m-%d") if end_date_input else None

results = search_chats_and_emails(data, search_type, search_person, search_term, start_date, end_date)

if search_type == "count":
    if results:
        print(f"{search_person or 'All persons'} said '{search_term}' {results[0][1]} times.")
    else:
        print(f"No instances found of '{search_term}' said by {search_person or 'any person'}.")
elif search_type == "email":
    if results:
        print("Search Results:")
        print("----------------")
        for result in results:
            print(f"Email: {result['Email']}")
            print(f"Password: {result['Password']}")
            print("----------------")
    else:
        print("No results found.")
else:
    if results:
        print("Search Results:")
        print("----------------")
        for result in results:
            print(f"From: {result['From']}")
            print(f"To: {result.get('To', 'N/A')}")
            print(f"Text: {result['Text']}")
            print(f"Created: {result['Created']}")
            print("----------------")
    else:
        print("No results found.")
