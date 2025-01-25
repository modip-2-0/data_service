import requests
import json
from colorama import init, Fore, Style

# Initialize colorama
init()

class ApiClient:
    def __init__(self, base_url="http://0.0.0.0:8000"):
        self.base_url = base_url
    
    def download_data(self, query):
        """Make a download request"""
        url = f"{self.base_url}/download/{query}"
        response = requests.post(url)
        return response.json()
    
    def list_bioassays(self):
        """Query bioassay database"""
        url = f"{self.base_url}/bioassay/"
        response = requests.get(url)
        return response
    
    def list_compounds(self):
        """Query compound database"""
        url = f"{self.base_url}/compound/"
        response = requests.get(url)
        return response
    
    def get_bioassay(self, aid):
        """Get a specific bioassay by its ID"""
        url = f"{self.base_url}/bioassay/get/{aid}"
        response = requests.get(url)
        return response.json()
    
    def get_compound(self, cid):
        """Get a specific compound by its ID"""
        url = f"{self.base_url}/compound/get/{cid}"
        response = requests.get(url)
        return response.json()

def main():
    client = ApiClient()
    print(Fore.GREEN + "Welcome to the MODIP 2.0 Data Service Client. Type 'help' for a list of commands." + Style.RESET_ALL)
    
    while True:
        command = input(Fore.BLUE + "> " + Style.RESET_ALL).strip()
        
        if command.startswith("query "):
            query_text = command[len("query "):]
            result = client.download_data(query_text)            
        
        elif command == "list bioassays":
            result = client.list_bioassays()
            print(result.text)
        
        elif command == "list compounds":
            result = client.list_compounds()
            print(result.text)
        
        elif command.startswith("bioassay "):
            aid = command[len("bioassay "):]
            result = client.get_bioassay(aid)
            print(json.dumps(result, indent=2))
        
        elif command.startswith("compound "):
            cid = command[len("compound "):]
            result = client.get_compound(cid)
            print(json.dumps(result, indent=2))
        
        elif command == "help":
            print(Fore.CYAN + "Available commands:" + Style.RESET_ALL)
            print(Fore.CYAN + "  query <query_text>  - Download data with the specified query" + Style.RESET_ALL)
            print(Fore.CYAN + "  list bioassays      - List all bioassays" + Style.RESET_ALL)
            print(Fore.CYAN + "  list compounds      - List all compounds" + Style.RESET_ALL)
            print(Fore.CYAN + "  bioassay <aid>      - Get a specific bioassay by its ID" + Style.RESET_ALL)
            print(Fore.CYAN + "  compound <cid>      - Get a specific compound by its ID" + Style.RESET_ALL)
            print(Fore.CYAN + "  exit                - Exit the client" + Style.RESET_ALL)
        
        elif command == "exit":
            print(Fore.RED + "Exiting the client." + Style.RESET_ALL)            
            break
        
        else:
            print(Fore.RED + "Unknown command. Type 'help' for a list of commands." + Style.RESET_ALL)

if __name__ == "__main__":
    main()