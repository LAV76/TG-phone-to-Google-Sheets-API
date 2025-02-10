# Telegram Bot for Saving Phone Numbers to Google Sheets

This Telegram bot allows users to submit their phone numbers, which are then saved in a Google Sheets document. The bot supports various phone number formats, including international codes, and ensures that only unique numbers are added to the table.

## Table of Contents
1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Running the Bot](#running-the-bot)
6. [Docker Support](#docker-support)
7. [How It Works](#how-it-works)
8. [Contacts](#contacts)

---
## Features
- Accepts phone numbers in various formats (e.g., `+79265958382`, `89265958382`, `(926) 595-83-82`, `0012345678900`).
- Converts all numbers to a standardized international format (e.g., `+7XXXXXXXXXX`).
- Checks for duplicates in Google Sheets before saving.
- Logs errors for debugging purposes.
- Supports Docker for easy deployment.

---
## Prerequisites
Before running the bot, ensure you have the following:
1. **Python 3.8+** installed on your system.
2. A project in **Google Cloud** with the Google Sheets API enabled.
3. A **JSON service account key** for accessing Google Sheets.
4. A **Telegram bot token** from [@BotFather](https://t.me/BotFather).
5. **Docker** (optional, for containerized deployment).

---
## Installation
### Step 1: Clone the Repository
Clone this repository to your local machine:
```bash
git clone https://github.com/LAV76/TG-phone-to-Google-Sheets-API.git
cd TG-phone-to-Google-Sheets-API
```
### Step 2: Install Dependencies
Install the required Python packages using pip:
```bash
pip install -r requirements.txt
```
If you're using Docker, skip this step and proceed to the [Docker Support](#поддержка-docker) section.


---


## Configuration
### Step 1: Create a .env File
Create a .env file in the root directory of the project and add the following variables:
```bash
BOT_TOKEN="your_bot_token"
GOOGLE_SPREADSHEET_ID='your_spreadsheet_id'
```
**How to Get These Values:**
- **BOT_TOKEN**: Create a bot via  [**@BotFather**](https://t.me/BotFather?spm=5aebb161.9aec867.0.0.7089c9212uY4m1) and copy the token.
- **GOOGLE_SPREADSHEET_ID:** Extract the ID from the URL of your Google Sheet (see instructions below).
### Step 2: Set Up Google Sheets API
1. Go to the [**Google Cloud Console**](https://console.cloud.google.com/?spm=5aebb161.9aec867.0.0.7089c9212uY4m1) .
1. Create a new project or select an existing one.
2. Enable the Google Sheets API:
    - Navigate to "APIs & Services" → "Library".
    - Find "Google Sheets API" and enable it.
4. Create credentials (Credentials):
    - Go to "APIs & Services" → "Credentials".
    - Click "Create Credentials" → "Service account".
    - Fill in the required fields and create a service account.
    - Download the JSON key file.
5. Share your Google Sheet with the email of the service account (it is specified in the JSON file).
### Step 3: Retrieve the Google Sheet ID
The ID of your Google Sheet can be found in the URL of the sheet. Here’s a step-by-step guide:

1. Open your Google Sheet in a browser.
2. Look at the URL. It will look something like this:
    ```bash
    https://docs.google.com/spreadsheets/d/1aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890/edit#gid=0
    ```
3. Find the sheet ID — it’s the long string of characters between /d/ and /edit. In this example:
    ```bash
    1aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890
    ```
4. Replace SPREADSHEET_ID in the .env file with the retrieved ID:
    ```bash
    GOOGLE_SPREADSHEET_ID='1aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890'
    ```
    
---

## Running the Bot
### Option 1: Run Locally
Start the bot by running the following command:
```bash
python bot.py
```
The bot will start polling for updates and respond to user messages.

### Option 2: Run via Docker
If you prefer to run the bot in a Docker container, follow these steps:

1. Build the Docker image:
     ```bash
    docker build -t tg-bot .
    ```
2. Run the Docker container:
    ```bash
    docker run --name tg-bot-container tg-bot
    ```
3. (Optional) Use volumes to mount the .env file and keys:
    ```bash
    docker run --name tg-bot-container -v $(pwd):/app tg-bot
    ```
    
---


## Docker Support
The project includes a Dockerfile for containerized deployment. This ensures environment consistency and simplifies deployment.
**Dockerfile Overview:**

- Base image: python:3.10-slim.
- Installs dependencies from requirements.txt.
- Copies project files into the container.
- Runs the bot using the command CMD ["python", "bot.py"].
    
---


## How It Works
### 1. User Interaction

- Users start the bot by sending the /start command.
- The bot prompts the user to enter their phone number.
- The bot processes the input, validates it, and checks for duplicates in the Google Sheet.
### 2. Phone Number Formatting

- Removes all non-digit characters (e.g., +, -, (, )).
- Replaces 00 with + for international codes.
- Converts Russian numbers starting with 8 to +7.
- Ensures the final format is +<country_code><number>.
### 3. Integration with Google Sheets

- Uses the gspread library to interact with Google Sheets.
- Adds new numbers to the first column of the sheet.
- Checks for duplicates before adding.
    
---

## Contacts
If you have any questions or need assistance, feel free to contact me:

Telegram: [@lekoncev](https://t.me/lekoncev)
