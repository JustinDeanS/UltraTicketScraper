import requests
from bs4 import BeautifulSoup
import time

# URL to check
url = "https://ultramusicfestival.com/tickets/miami/"

# Function to check availability
def check_ticket_availability():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the section containing the ticket information
    tier2_ticket_section = soup.find_all('div', class_='purchase')

    for section in tier2_ticket_section:
        # Check if it contains the specific ticket details
        sub_type = section.find_previous('p', class_='sub_type color')
        title = section.find_previous('p', class_='title')
        date = section.find_previous('p', class_='date color')
        
        if sub_type and sub_type.get_text() == 'Tier 2' and title and title.get_text() == 'GA 3-Day Ticket' and date and 'March 28, 29, 30 – 2025' in date.get_text():
            # Check if the 'COMING SOON' button is replaced with something else (e.g., 'BUY NOW')
            button = section.find('a', class_='tix soon regbtn')
            if button and 'Coming Soon' not in button.get_text():
                print("Tickets are available!")
                return True
            else:
                print("Tickets are not available yet.")
            break
    else:
        print("Ticket section not found.")
    
    return False

# Main loop to periodically check the availability
def main():
    while True:
        if check_ticket_availability():
            # Send a notification or take further action if tickets are available
            break
        # Wait for some time before checking again
        time.sleep(300)  # Check every 5 minutes

if __name__ == "__main__":
    main()
