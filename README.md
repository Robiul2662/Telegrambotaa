# BD School Info Bot — fixed package layout

## Render setup
Upload the *contents* of this folder to the root of a GitHub repository, so `bot.py`, `requirements.txt`, `school_data.py`, and `render.yaml` are visible at the repository top level.

Recommended: create a **Background Worker** from this repository. Build command:
`pip install -r requirements.txt`
Start command:
`python bot.py`

In Render > Environment, set:
- Key: `BOT_TOKEN`
- Value: your Telegram BotFather token (keep it secret)

## Commands
`/start`, `/help`, `/search school name or area`, `/eiin 123456`, `/district`, `/about`

## Data
This package does not contain a complete government school database. Add only verified public school/professional data in `school_data.py`; the bot intentionally returns no result when no verified record exists. Do not add private phone numbers, home addresses, NID numbers, or secret account data.

## Security
Never commit the actual token to GitHub. If a token was exposed in a screenshot, revoke it with BotFather and use a new token in Render Environment.
