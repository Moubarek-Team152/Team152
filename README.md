# Advanced Email Filtering and Sorting Tool

## Team152

                   ____   _____ 
                  |  _ \ |__  / 
                  | | | |  / /  
                  | |_| | / /_  
                  |____/ /____| 

                  **Team152**
               by J-moubarek
              https://t.me/team1954

---

## 📝 Description

This tool is a powerful and high-performance Python script designed for processing large email lists. It allows users to filter, sort, and segment email lists based on a predefined set of domains, in addition to other useful data handling functions. The tool is optimized to work efficiently with huge files without consuming system resources.

---

## ✨ Key Features

- **Advanced Domain Filtering**: Sorts emails belonging to a massive list of service providers (telecom companies, public email services) and saves them into separate files.
- **Large File Processing**: Optimized to read and process multi-gigabyte files line by line, without consuming RAM.
- **Email Extraction from Text**: Capable of extracting all email addresses from any unstructured text file.
- **Email Extraction from `email:pass` format**: Separates emails from combo lists.
- **User-Friendly Colorful Interface**: An interactive terminal interface with colors for better readability (works even if the `colorama` library is not installed).
- **Progress Indicators**: Displays a percentage progress bar for time-consuming operations.

---

## 📋 Requirements

For the tool to work fully, you will need to install the following libraries:

- `requests`: To send requests in the email validation function.
- `colorama`: (Optional) To support colors in the Windows terminal.

---

## ⚙️ Installation

1.  Make sure you have Python installed on your system.
2.  Open your terminal (Command Prompt or Terminal) and install the required libraries using `pip`:

    ```bash
    pip install requests colorama
    ```

---

## 🚀 How to Use

1.  Download the script file (`filter.py` or whatever name you save it as).
2.  Place the email list file you want to process in the same directory as the script.
3.  Open the terminal in that directory.
4.  Run the script with the following command:

    ```bash
    python filter.py
    ```

5.  The banner and the main menu will appear.
6.  Choose the number corresponding to the function you want to execute (1 to 4).
7.  Enter the name of your email list file (e.g., `my_list.txt`).
8.  Wait for the process to complete. You will find the output files in the same directory.

---

## 🛠️ Options Explained

1.  **Filter & Sort Corporate Emails**: Sorts the emails in your file. Emails belonging to the domains in the internal list will be saved into separate files inside the `Corporate_Emails` folder. The rest of the emails will be saved in the `Other_Domains.txt` file.
2.  **Validate Emails**: (Experimental feature) Attempts to verify the validity of emails using external services. The results may not always be accurate.
3.  **Extract Emails from Email:Pass**: Extracts only the email part from each line in a file with the `email:password` format.
4.  **Extract Emails from any Text File**: Scans an entire text file and extracts any text that matches the email format.

---

## 📞 Contact

For any inquiries or suggestions, you can get in touch via:

- **Telegram**: [https://t.me/team1954](https://t.me/team1954)
