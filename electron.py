import requests
from utils import solver
import time
from playwright.sync_api import sync_playwright
import colorama
import random, string
import concurrent.futures

"""
curl "https://ryo.sh/download_token.php?token=" ^
  -H "authority: ryo.sh" ^
  -H "accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7" ^
  -H "accept-language: en-US,en;q=0.9" ^
  -H "cache-control: max-age=0" ^
  -H "content-type: application/x-www-form-urlencoded" ^
  -H "origin: https://ryo.sh" ^
  -H "referer: https://ryo.sh/download_token.php?token=" ^
  -H "sec-ch-ua-mobile: ?0" ^
  -H "sec-ch-ua-platform: ^\^"Windows^\^"" ^
  -H "sec-fetch-dest: document" ^
  -H "sec-fetch-mode: navigate" ^
  -H "sec-fetch-site: same-origin" ^
  -H "sec-fetch-user: ?1" ^
  


  Made by Nano, i didn't make the slover tho <3
"""

colorama.init()

class Electron:
    electron_url = "https://ryo.sh/download_token.php?token="

    def __init__(self):
        ...

    def __solver__(self):
        print(f"{colorama.Fore.WHITE}[{colorama.Fore.GREEN}+{colorama.Fore.WHITE}] Started with 4 threads")
        with sync_playwright() as playwright:
            s = solver.Solver(playwright, headless=True)
            while True:
                current_time = time.time()
                electron_key = self.genkey()
                captcha = s.solve(f"https://ryo.sh/download_token.php?token={electron_key}", "0x4AAAAAAAOE-pbn1T-JGNjg", invisible=False) 
                
                if "failed" in captcha:
                    print(f"{colorama.Fore.WHITE}[{colorama.Fore.RED}-{colorama.Fore.WHITE}] Failed to solve captcha")
                    continue
                
                print(f"{colorama.Fore.WHITE}[{colorama.Fore.GREEN}+{colorama.Fore.WHITE}] Solved {captcha[0:40]} in {colorama.Fore.GREEN}{time.time() - current_time}{colorama.Fore.WHITE} seconds")
                
                self.__requester__(captcha, electron_key)


    def genkey(self):
        characters = string.ascii_lowercase + string.digits
        random_string = ''.join(random.choice(characters) for _ in range(6))
        return random_string


    def __requester__(self, auth_token, electron_key):
        build_auth_token = {"cf-turnstile-response": auth_token}
        electron_key_request = requests.post(self.electron_url + electron_key, build_auth_token)
        
        print(f"{colorama.Fore.WHITE}[{colorama.Fore.GREEN}+{colorama.Fore.WHITE}] Trying Key {electron_key_request.url} ...")
        
        if "Invalid token" in electron_key_request.text:
            print(f"{colorama.Fore.WHITE}[{colorama.Fore.RED}!{colorama.Fore.WHITE}] Invalid Electron Key: {electron_key}")
        else:
            print(f"{colorama.Fore.WHITE}[{colorama.Fore.GREEN}+{colorama.Fore.WHITE}] Correct Key {electron_key_request.url}")
            print(f"{colorama.Fore.WHITE}[{colorama.Fore.GREEN}+{colorama.Fore.WHITE}] Now Downloading Electron... {electron_key_request.url} ...")
            with open("Electron.zip", 'wb') as file:
                file.write(electron_key_request.content)

       
    



if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
            electrons = [Electron() for _ in range(4)]
            futures = [executor.submit(electron.__solver__) for electron in electrons]

            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Exception in thread: {e}")
