# Sophos Brute Login IDs

ID and paswword extraction accomplished for `21` batch and `22` batch
`NOTE:` not tested for `23`, `24` batch

**Todo**

- [x] get sophos internet portal login ids

#### Requirements

    pandas,
    python-dotenv,
    requests

#### Run the script

```bash
python -m venv .venv
source .venv/bin/activate
pip install pandas, python-dotenv, requests
```

**make a .env file**
`EXPLOIT_ID` = "your-enrollment-number"
`EXPLOIT_PASS` = "your-password-sophos"

```bash
python main.py
```
