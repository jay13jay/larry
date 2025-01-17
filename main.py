#!/usr/bin/env python3
import time
import requests
from rich import print

def main():
    url = "http://127.0.0.1:5000/send_message"
    headers = {"Content-Type": "application/json"}

    test_messages = [
        "What are the specials today?",
        "Can you tell me more about the Margherita pizza?",
        "Do you have any vegan options?",
        "I want to order a large Margherita pizza and a side of garlic bread.",
    ]

    total_time = 0

    for msg in test_messages:
        start_time = time.time()
        response = requests.post(url, json={"message": msg}, headers=headers)
        end_time = time.time()
        elapsed_time = end_time - start_time
        total_time += elapsed_time

        if response.status_code == 200:
            print(f"Query: {msg}")
            print(f"Response: {response.json()['response']}")
            print(f"Time taken: {elapsed_time:.4f} seconds\n")
        else:
            print(f"Failed to send message: {msg}")
        # time.sleep(3)  # Wait for 3 seconds between each message

    print(f"Average time taken: {total_time / len(test_messages):.4f} seconds")
    print(f"Total time taken: {total_time:.4f} seconds")

if __name__ == "__main__":
    print("Sending test messages...")
    main()
