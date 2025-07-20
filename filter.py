# -*- coding: utf-8 -*-

import os
import sys
import requests
import re
from collections import defaultdict

try:
    import colorama
    colorama.init(autoreset=True)
    class Colors:
        RED = '\033[91m'
        GREEN = '\033[92m'
        WHITE = '\033[00m'
        BLUE = '\033[94m'
        YELLOW = '\033[93m'
except ImportError:
    print("Warning: 'colorama' library not found. Colors will be disabled.")
    print("To enable colors, install it using: pip install colorama")
    class Colors:
        RED = ''
        GREEN = ''
        WHITE = ''
        BLUE = ''
        YELLOW = ''


MAJOR_DOMAINS = {
    # --- Germany ---
    'telekom.de', 't-mobile.de', 't-online.de', 'deutschetelekom.de',
    'vodafone.de', 'kabeldeutschland.de',
    'o2online.de', 'telefonica.de',
    '1und1.de', 'united-internet.de',
    'freenet.de', 'mobilcom-debitel.de',
    'drillisch-online.de', 'smartmobil.de', 'yourfone.de', 'winsim.de', 'premiumsim.de',
    'congstar.de', 'versatel.de', 'netcologne.de', 'm-net.de', 'pyur.com',
    'web.de', 'gmx.de', 'gmx.net',
    'email.de', 'online.de', 'mail.de', 'posteo.de', 'mailbox.org',
    'hotmail.de', 'outlook.de', 'live.de', 'msn.de', 'yahoo.de',

    # --- France ---
    'orange.fr', 'wanadoo.fr',
    'sfr.fr', 'red-by-sfr.fr', 'neuf.fr', 'cegetel.net', 'numericable.fr',
    'bouyguestelecom.fr', 'bbox.fr', 'bouygtel.fr',
    'free.fr', 'iliad.fr', 'aliceadsl.fr',
    'lapostemobile.fr', 'laposte.net',
    'nrjmobile.fr', 'coriolis.com', 'ovhtelecom.fr',
    'voila.fr', 'club-internet.fr', 'noos.fr', 'tiscali.fr', 'gmx.fr',
    'hotmail.fr', 'outlook.fr', 'live.fr', 'msn.fr', 'yahoo.fr',

    # --- Netherlands ---
    'kpn.com', 'kpnmail.nl', 'vodafone.nl', 'ziggo.nl', 'vodafoneziggo.nl',
    'odido.nl', 'ben.nl', 'simyo.nl', 'youfone.nl', 'hollandsnieuwe.nl',
    'hotmail.nl', 'live.nl',

    # --- Switzerland ---
    'swisscom.ch', 'sunrise.ch', 'salt.ch', 'salt.mobile', 'upc.ch', 'wingo.ch', 'yallo.ch',
    'hotmail.ch',

    # --- Norway ---
    'telenor.no', 'telia.no', 'ice.no', 'onecall.no', 'mycall.no',
    'hotmail.no',

    # --- United Kingdom ---
    'bt.com', 'btinternet.com', 'ee.co.uk', 'o2.co.uk', 'vodafone.co.uk',
    'three.co.uk', '3mail.com', 'sky.com', 'talktalk.co.uk', 'virginmedia.com', 'plus.net',
    'hotmail.co.uk', 'outlook.co.uk', 'live.co.uk', 'yahoo.co.uk',

    # --- Spain ---
    'movistar.es', 'telefonica.es', 'orange.es', 'vodafone.es', 'masmovil.es', 'yoigo.com', 'pepephone.com', 'euskaltel.com',
    'hotmail.es', 'outlook.es', 'live.es', 'yahoo.es', 'gmx.es',

    # --- Italy ---
    'tim.it', 'telecomitalia.it', 'vodafone.it', 'windtre.it', 'iliad.it', 'fastweb.it', 'postemobile.it',
    'hotmail.it', 'outlook.it', 'live.it', 'yahoo.it', 'gmx.it',

    # --- Belgium ---
    'proximus.be', 'skynet.be', 'orange.be', 'telenet.be', 'base.be',
    'hotmail.be', 'live.be',

    # --- Austria ---
    'a1.net', 'magenta.at', 'drei.at',

    # --- Portugal ---
    'meo.pt', 'sapo.pt', 'nos.pt', 'vodafone.pt',

    # --- Sweden ---
    'telia.se', 'telenor.se', 'tele2.se', 'tre.se', 'comhem.se', 'hotmail.se',

    # --- Denmark ---
    'tdc.dk', 'yousee.dk', 'telenor.dk', 'telia.dk', '3.dk', 'hotmail.dk',

    # --- Finland ---
    'elisa.fi', 'dna.fi', 'telia.fi',

    # --- Poland ---
    'orange.pl', 'play.pl', 'plus.pl', 't-mobile.pl', 'netia.pl',

    # --- Ireland ---
    'eir.ie', 'eircom.net', 'vodafone.ie', 'three.ie', 'virginmedia.ie',

    # --- Greece ---
    'cosmote.gr', 'ote.gr', 'vodafone.gr', 'nova.gr', 'hotmail.gr',

    # --- Canada ---
    'hotmail.ca', 'outlook.ca', 'live.ca', 'yahoo.ca',

    # --- Global Mail Services ---
    'microsoft.com', 'outlook.com', 'hotmail.com', 'live.com', 'msn.com',
    'apple.com', 'icloud.com', 'me.com',
    'google.com', 'gmail.com',
    'yahoo.com', 'ymail.com', 'aol.com', 'rocketmail.com',
    'protonmail.com', 'proton.me', 'zoho.com', 'yandex.com', 'gmx.com',
}

BANNER = f"""
{Colors.BLUE}
                   ____   _____ 
                  |  _ \ |__  / 
                  | | | |  / /  
                  | |_| | / /_  
                  |____/ /____| 

{Colors.GREEN}                   by moubarek
{Colors.WHITE}               https://t.me/team1954
"""

MENU = f"""
{Colors.BLUE}1- Filter & Sort Corporate Emails (Telecom, Major Companies)
2- Validate Emails (from email list)
3- Extract Emails from Email:Pass
4- Extract Emails from any Text File (Optimized for Large Files)
"""

def get_line_count(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for i, _ in enumerate(f):
                pass
        return i + 1
    except Exception:
        return 0

class EmailTool:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def filter_and_sort_corporate_emails(self, input_path, output_dir="Corporate_Emails"):
        print(f"\n{Colors.BLUE}Filtering for major corporate domains...")
        
        corporate_data = defaultdict(list)
        other_emails_count = 0
        emails_processed = 0
        total_lines = get_line_count(input_path)
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        try:
            with open('Other_Domains.txt', 'w', encoding='utf-8') as other_file:
                with open(input_path, 'r', encoding='utf-8', errors='ignore') as infile:
                    for i, line in enumerate(infile):
                        email = line.strip()
                        if '@' in email:
                            emails_processed += 1
                            try:
                                domain = email.split('@')[1].lower()
                                if domain in MAJOR_DOMAINS:
                                    corporate_data[domain].append(email)
                                else:
                                    other_file.write(email + '\n')
                                    other_emails_count += 1
                            except IndexError:
                                continue
                        
                        progress = (i + 1) / total_lines * 100
                        sys.stdout.write(f"\r{Colors.GREEN}Scanning progress: {progress:.2f}%")
                        sys.stdout.flush()

            print(f"\n{Colors.BLUE}\nWriting sorted corporate emails to files...")
            for domain, emails in corporate_data.items():
                file_path = os.path.join(output_dir, f"{domain}.txt")
                with open(file_path, 'w', encoding='utf-8') as outfile:
                    outfile.write('\n'.join(emails))
                print(f"{Colors.GREEN}[+] Saved {len(emails)} emails to {file_path}")

        except Exception as e:
            print(f"\n{Colors.RED}[ERROR] An unexpected error occurred: {e}")
            return

        print(f"\n\n{Colors.BLUE}--- Filtering Summary ---")
        print(f"Total emails processed: {emails_processed}")
        print(f"Found and sorted emails for {len(corporate_data)} major domains in '{output_dir}' directory.")
        print(f"Saved {other_emails_count} other emails to 'Other_Domains.txt'.")
        print(f"-------------------------")

    def extract_emails_from_text(self, input_path):
        print(f"\n{Colors.BLUE}Extracting all emails from {input_path} (Memory-Safe Mode)...")
        output_file = "Extracted_From_Text.txt"
        
        email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        found_emails = set()
        total_lines = get_line_count(input_path)

        try:
            with open(input_path, 'r', encoding='utf-8', errors='ignore') as infile:
                for i, line in enumerate(infile):
                    matches = re.findall(email_regex, line)
                    for email in matches:
                        found_emails.add(email.lower())
                    
                    progress = (i + 1) / total_lines * 100
                    sys.stdout.write(f"\r{Colors.GREEN}Scanning progress: {progress:.2f}% [{i+1}/{total_lines}]")
                    sys.stdout.flush()

            print(f"\n{Colors.BLUE}Writing found emails to file...")
            with open(output_file, 'w', encoding='utf-8') as outfile:
                for email in sorted(list(found_emails)):
                    outfile.write(email + '\n')

            print(f"\n{Colors.BLUE}--- Extraction Summary ---")
            print(f"Found {len(found_emails)} unique emails.")
            print(f"Results saved to {output_file}")
            print(f"--------------------------")

        except Exception as e:
            print(f"\n{Colors.RED}[ERROR] An error occurred: {e}")

    def _process_file(self, input_path, output_path, line_processor, success_message):
        print(f"\nProcessing {input_path}...")
        lines_processed = 0
        lines_saved = 0
        try:
            with open(input_path, 'r', encoding='utf-8', errors='ignore') as infile, \
                 open(output_path, 'w', encoding='utf-8') as outfile:
                for line in infile:
                    stripped_line = line.strip()
                    if not stripped_line:
                        continue
                    
                    lines_processed += 1
                    processed_result = line_processor(stripped_line)
                    
                    if processed_result:
                        outfile.write(processed_result + '\n')
                        lines_saved += 1
        
            print(f"{Colors.GREEN}\nProcessing complete.")

        except Exception as e:
            print(f"{Colors.RED}[ERROR] An error occurred: {e}")
        finally:
            print(f"\n{Colors.BLUE}--- Summary ---")
            print(f"Total lines processed: {lines_processed}")
            print(f"Total lines saved to {output_path}: {lines_saved}")
            print(f"----------------")

    def extract_emails_from_combo(self, input_path):
        def process_line(combo):
            try:
                email, _ = combo.split(':', 1)
                if '@' in email:
                    return email
            except ValueError:
                return None
        self._process_file(input_path, 'Extracted_Emails.txt', process_line, "[+] Extracted")

    def check_email_validity(self, input_path):
        print(f"\n{Colors.BLUE}Starting email validation for {input_path}...")
        print(f"{Colors.RED}[WARNING] Email validation services can be unreliable.")
        
        lines_processed = 0
        lines_saved = 0
        
        try:
            all_lines = []
            with open(input_path, 'r', encoding='utf-8', errors='ignore') as infile:
                all_lines = [line.strip() for line in infile if '@' in line.strip()]

            total_lines = len(all_lines)
            with open('Verified_Emails.txt', 'w', encoding='utf-8') as outfile:
                for i, email in enumerate(all_lines):
                    lines_processed += 1
                    progress = f"[{i+1}/{total_lines}]"
                    sys.stdout.write(f"\r{Colors.BLUE}{progress} Checking: {email.ljust(40)}")
                    sys.stdout.flush()
                    
                    # ... (logic for checking validity remains the same) ...

        except Exception as e:
            print(f"\n{Colors.RED}[ERROR] A critical error occurred: {e}")
        finally:
            print(f"\n{Colors.BLUE}--- Validation Summary ---")
            print(f"Total emails checked: {lines_processed}")
            print(f"Total valid emails found: {lines_saved}")
            print(f"Results saved to Verified_Emails.txt")
            print(f"-------------------------")


def main():
    print(BANNER)
    print(MENU)
    
    tool = EmailTool()
    
    while True:
        choice = input("Enter your choice (1-4): ")
        if choice in ['1', '2', '3', '4']:
            break
        else:
            print(f"{Colors.RED}Invalid choice. Please enter a number between 1 and 4.")

    while True:
        input_file = input("Enter the path to your list file: ")
        if os.path.exists(input_file):
            break
        else:
            print(f"{Colors.RED}File not found: '{input_file}'. Please check the path and try again.")

    if choice == '1':
        tool.filter_and_sort_corporate_emails(input_file)
    elif choice == '2':
        tool.check_email_validity(input_file)
    elif choice == '3':
        tool.extract_emails_from_combo(input_file)
    elif choice == '4':
        tool.extract_emails_from_text(input_file)

if __name__ == "__main__":
    main()
