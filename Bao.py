import random

import time

import os

# Import required modules for HTTP requests and JSON parsing

import requests

import json

# Define server ID to send messages to

server_id = input("Masukkan server ID: ")
print(f"Server ID yang dimasukkan adalah {server_id}")

# Read messages from txt file and store them in a list

with open('pesan.txt', 'r') as f:

    messages = f.readlines()

# Remove newline characters from messages

messages = [m.strip() for m in messages]

# Define time interval in seconds to send messages

interval = 150

# Define time interval in seconds to delete messages

delete_interval = 30

# Define list of error messages

error_messages = [

    "Gagal mengirim pesan. Silakan coba lagi nanti.",

    "Terjadi kesalahan saat mengirim pesan. Mohon tunggu beberapa saat dan coba lagi.",

    "Pesan gagal dikirim. Mohon coba beberapa saat lagi."

]

# Function to send message to a channel

def send_message(channel_id, message):

    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"

    headers = {

        "Authorization": f"Bot {token}",

        "Content-Type": "application/json"

    }

    data = {

        "content": message

    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code != 200:

        print(f"Failed to send message to channel {channel_id}")

        notify_error()

# Function to notify errors

def notify_error():

    error_message = random.choice(error_messages)

    print(error_message)

# Function to send messages to the server

def send_messages():

    url = f"https://discord.com/api/v9/guilds/{server_id}/channels"

    headers = {

        "Authorization": f"Bot {token}",

        "Content-Type": "application/json"

    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:

        print(f"Failed to get channels from server {server_id}")

        notify_error()

    else:

        channels = json.loads(response.text)

        for channel in channels:

            if channel['type'] == 0: # text channel

                channel_id = channel['id']

                message = random.choice(messages)

                send_message(channel_id, message)

                time.sleep(5)

# Function to delete messages in a channel

def delete_messages(channel_id):

    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"

    headers = {

        "Authorization": f"Bot {token}",

        "Content-Type": "application/json"

    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:

        print(f"Failed to get messages from channel {channel_id}")

        notify_error()

    else:

        messages = json.loads(response.text)

        for message in messages:

            message_id = message['id']

            url = f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}"

            response = requests.delete(url, headers=headers)

            if response.status_code != 204:

                print(f"Failed to delete message {message_id} in channel {channel_id}")

                notify_error()

# Event handler for timer event

def on_timer():

    while True:

        send_messages()

        time.sleep(interval)

# Event handler for message received event

def on_message():

    message = input("Masukkan perintah: ")

    if message.startswith('!delete'):

        channel_id = message.split()[1]

        delete_messages

