import sys
import json
import time
from urllib.request import urlopen, Request
from urllib.error import URLError

# Try importing phonenumbers for Option 3 tracking
try:
    import phonenumbers
    from phonenumbers import geocoder, carrier, timezone
except ImportError:
    phonenumbers = None

# Terminal Color Codes
RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"

art = f"""                      .::^~~~~~^::.                      
                 .:^!7?????????7!^:.                 
              .:!7?????????????????7!:.              
            .^7???????????????????????7^.            
          .^7????????7!^:. .::^!7????????7^.          
         :7??????7!:.             .:!7??????7:       
       .!??????!:.                   .:!??????!.     
      :7?????^                           ^?????7:    
     :7????^             .::::.           ^????7:    
    .7????:          .:^!7????7!^:.        :????7.   
    7????^         .:!7??????????7!:.       ^????7   
   :????7         :7????????????????7:       7????:  
   7????:        !????????????????????!        :????7  
  .????7        7???????7!^::^!7???????7        7????. 
  :????!       :??????7:.      .:7??????:       !????: 
  :????!       !?????!.   (O)    .!?????!       !????: 
  .????7       :??????7:.      .:7??????:       7????. 
   7????:        !????????????????????!        :????7  
   :????7         :7????????????????7:       7????:  
    7????^         .:!7??????????7!:.       ^????7   
    .7????:          .:^!7????7!^:.        :????7.   
     :7????^             .::::.           ^????7:    
      :7?????^                           ^?????7:    
       .!??????!:.                   .:!??????!.     
         :7??????7!:.             .:!7??????7:       
          .^7????????7!^:. .::^!7????????7^.          
            .^7???????????????????????7^.            
              .:!7?????????????????7!:.              
                 .:^!7?????????7!^:.                 
                      .::^~~~~~^::.                      

{RED} ____  _______     _____ _       _______   _______ 

|  _ \| ____\ \   / /_ _| |     | ____\ \ / / ____|
| | | |  _|  \ \ / / | || |     |  _|  \ V /|  _|  
| |_| | |___  \ V /  | || |___  | |___  | | | |___ 
|____/|_____|  \_/  |___|_____| |_____| |_| |_____|

                     ____   ___  
                    |___ \ / _ \ 
                      __) | | | |
                     / __/| |_| |

                    |_____|\___/

=======================================================
   CREATED AND DEVELOPED BY SYRUS@PARTHAA
======================================================={RESET}"""

menu = f"""
{GREEN}[ 1 ] IP Tracker
[ 2 ] Show Your IP
[ 3 ] Phone Number Tracker
[ 4 ] Username Tracker
[ 0 ] Exit

[ + ] Select Option : {RESET}"""

print(art)

while True:
    try:
        choice = input(menu).strip()
        
        # ----------------------------------------------------
        # OPTION 1: IP TRACKER
        # ----------------------------------------------------
        if choice == "1":
            ip_target = input(f"\n{GREEN}[+] Enter Target IP Address: {RESET}").strip()
            print(f"{GREEN}[*] Scanning IP parameters...{RESET}")
            time.sleep(1)
            try:
                # Direct API lookup via http://ip-api.com
                req = Request(f"http://ip-api.com{ip_target}", headers={'User-Agent': 'Mozilla/5.0'})
                with urlopen(req) as response:
                    data = json.loads(response.read().decode())
                
                if data.get("status") == "success":
                    print(f"\n{GREEN}--- IP ANALYSIS REPORT ---")
                    print(f"[•] Target IP   : {data.get('query')}")
                    print(f"[•] Country     : {data.get('country')} ({data.get('countryCode')})")
                    print(f"[•] Region/State: {data.get('regionName')}")
                    print(f"[•] City        : {data.get('city')}")
                    print(f"[•] ISP         : {data.get('isp')}")
                    print(f"[•] Organization: {data.get('org')}")
                    print(f"[•] Latitude    : {data.get('lat')}")
                    print(f"[•] Longitude   : {data.get('lon')}{RESET}\n")
                else:
                    print(f"\n{RED}[!] Error: Could not resolve target IP data.{RESET}\n")
            except Exception as e:
                print(f"\n{RED}[!] Connection error or API limit reached.{RESET}\n")
            
        # ----------------------------------------------------
        # OPTION 2: SHOW YOUR IP
        # ----------------------------------------------------
        elif choice == "2":
            print(f"\n{GREEN}[*] Contacting external network gateways...{RESET}")
            try:
                req = Request("https://api.ipify.org?format=json", headers={'User-Agent': 'Mozilla/5.0'})
                with urlopen(req) as response:
                    my_ip = json.loads(response.read().decode()).get("ip")
                print(f"{GREEN}[✓] Your Public IP Address is: {RED}{my_ip}{RESET}\n")
            except Exception:
                print(f"\n{RED}[!] Offline. Unable to fetch your public IP address.{RESET}\n")
            
        # ----------------------------------------------------
        # OPTION 3: PHONE NUMBER TRACKER
        # ----------------------------------------------------
        elif choice == "3":
            if not phonenumbers:
                print(f"\n{RED}[!] Error: 'phonenumbers' module not installed! Please run: pip install phonenumbers{RESET}\n")
                continue
                
            phone_in = input(f"\n{GREEN}[+] Enter Number with Country Code (e.g., +14155552671): {RESET}").strip()
            print(f"{GREEN}[*] Parsing international databases...{RESET}")
            time.sleep(1)
            try:
                parsed_num = phonenumbers.parse(phone_in, None)
                if phonenumbers.is_valid_number(parsed_num):
                    # Fetching country name, carrier information and target timezones
                    country = geocoder.description_for_number(parsed_num, "en")
                    srv_provider = carrier.name_for_number(parsed_num, "en")
                    time_zones = timezone.time_zone_for_number(parsed_num)
                    
                    print(f"\n{GREEN}--- PHONE TRACKER REPORT ---")
                    print(f"[•] Clean Format: {phonenumbers.format_number(parsed_num, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}")
                    print(f"[•] Country     : {RED}{country if country else 'Unknown'}{GREEN}")
                    print(f"[•] Carrier/ISP : {srv_provider if srv_provider else 'Unknown/Virtual Phone'}")
                    print(f"[•] Timezone    : {', '.join(time_zones)}{RESET}\n")
                else:
                    print(f"\n{RED}[!] Error: The structural format of this phone number is invalid.{RESET}\n")
            except Exception as e:
                print(f"\n{RED}[!] Check your target format. Ensure it includes '+' and country code.{RESET}\n")
            
        # ----------------------------------------------------
        # OPTION 4: USERNAME TRACKER
        # ----------------------------------------------------
        elif choice == "4":
            username = input(f"\n{GREEN}[+] Enter Target Username to Scan: {RESET}").strip()
            print(f"{GREEN}[*] Scanning popular platforms for profiles...{RESET}\n")
            
            # Common target platform lists for OSINT scanning
            targets = {
                "GitHub": f"https://github.com/{username}",
                "Instagram": f"https://instagram.com/{username}",
                "Twitter/X": f"https://x.com{username}",
                "Reddit": f"https://reddit.com{username}",
                "Pinterest": f"https://pinterest.com{username}"
            }
            
            for platform, url in targets.items():
                try:
                    req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
                    with urlopen(req, timeout=3) as resp:
                        if resp.getcode() == 200:
                            print(f"{GREEN}[✓] Found on {platform}: {url}{RESET}")
                except URLError as e:
                    # Explicit checking for standard HTTP 404 meaning account doesn't exist
                    if hasattr(e, 'code') and e.code == 404:
                        print(f"\033[90m[-] Not Found on {platform}\033[0m")
                    else:
                        print(f"\033[90m[-] Error/Blocked on {platform}\033[0m")
                except Exception:
                    print(f"\033[90m[-] Skipping {platform}\033[0m")
            print()
            
        # ----------------------------------------------------
        # OPTION 0: EXIT
        # ----------------------------------------------------
        elif choice == "0":
            print(f"\n{RED}[!] Exiting DEVIL-EYE. Goodbye!{RESET}\n")
            sys.exit(0)
            
        else:
            print(f"\n{RED}[!] Invalid Option. Please choose between 0 and 4.{RESET}\n")
            
    except KeyboardInterrupt:
        print(f"\n\n{RED}[!] Forced Shutdown detected.{RESET}\n")
        sys.exit(0)
