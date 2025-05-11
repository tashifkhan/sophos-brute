import pandas as pd
import os
import dotenv

dotenv.load_dotenv()
expoit_id = os.getenv("EXPLOIT_ID")
expoit_pass = os.getenv("EXPLOIT_PASS")

def main():
    print("Hello from sophos-brute!")


if __name__ == "__main__":
    main()
