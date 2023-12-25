<div align="center">
    <h1>--// Linkedin Connect Bot //--</h1>
    <img src="https://img.shields.io/github/last-commit/klpod221/linkedin-connect-bot?style=for-the-badge&color=ffb4a2&labelColor=201a19">
    <img src="https://img.shields.io/github/stars/klpod221/linkedin-connect-bot?style=for-the-badge&color=e6c419&labelColor=1d1b16">
    <img src="https://img.shields.io/github/repo-size/klpod221/linkedin-connect-bot?style=for-the-badge&color=a8c7ff&labelColor=1a1b1f">
</div>

## About

This is a bot that automatically connects to people on LinkedIn. It uses Selenium to automate the process of logging in and connecting to people.

## Prerequisites

- Python 3.6+
- Selenium (`pip install selenium`)
- python-dotenv (`pip install python-dotenv`)
- ChromeDriver (Recommend using driver from this repo as it is already configured to work with the bot or download the latest version [here](https://chromedriver.chromium.org/downloads))

## Usage

1. Clone the [repo](https://github.com/klpod221/linkedin-connect-bot)
2. Install the [prerequisites](#prerequisites)
3. Copy the `.env.example` file and rename it to `.env` and fill in the required fields (see [below](#env-variables))
4. Run the bot (`python main.py`)
5. Enter the keywords you want to search for
6. Enter the location you want to search in (leave blank for no filter, split multiple locations with a comma (`,`) and no spaces e.g. `London,United Kingdom`)
7. It will open a Chrome window and start connecting to people
8. Once it has finished it will close the Chrome window and stop the bot
9. You can find the people it connected to in the `./connections` folder
10. Enjoy!

## Env Variables

- `MY_NAME` - Your name (this is used to send notes to the people you connect to)
- `COMPANY_NAME` - The name of your company (this is used to send notes to the people you connect to)
- `COMPANY_DESCRIPTION` - A short description of your company (this is used to send notes to the people you connect to)
- `EMAIL` - Your LinkedIn email
- `PASSWORD` - Your LinkedIn password (this will be stored in plain text in the `.env` file so make sure to keep it safe)
- `SEND_WITH_NOTE` - Whether to send a note with the connection request (set to `true` or `false`) (only set to `true` if your account has LinkedIn Premium)
