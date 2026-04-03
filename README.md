# Extract-whatsapp_web_numbers
A script that retrieves all the phone numbers you've messaged via WhatsApp Web with the click of a button.

<img width="1920" height="1027" alt="image" src="https://github.com/user-attachments/assets/ed22e00f-74c9-44a1-9e77-e137336661f8" />


# What does this script do?

It opens WhatsApp Web in the Chrome browser using Selenium.

It saves the login session (optional) to the chrome_profile folder so you don't have to scan a QR code every time.

It waits until WhatsApp Web loads and the chat list appears.

It scrolls through the chat list several times to load more conversations on the page.

Then it takes the entire page content (page_source) and searches it for anything resembling a phone number using Regex.

It cleans up the numbers (removing spaces, dashes, and brackets) and ensures the number length is reasonable (from 8 to 5000 digits). Then:
It sums the numbers without duplicates and saves them to the file: wa_web_numbers.txt

# Requirements

Python 3 is installed.

Google Chrome is installed.

Selenium is installed.

pip install selenium


# How to download the tool:

pip install selenium

git clone https://github.com/joker-gaza/Extract-whatsapp_web_numbers

pytohn wa_web_numbers.py
----------------------------------------------------------------------------------------

# Contact us to purchase a better copy:

https://t.me/JOKER_PLSTAEEN_1

https://www.facebook.com/JOKERGAZA222
