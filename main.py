import os
import time

import requests
import datetime as dt
import dotenv
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

dotenv.load_dotenv()

#######################
# Set these variables #
#######################
FROM_EMAIL = ""  # must be a registered from email in sendgrid
TO_EMAILS = []  # where to send notifications. I used my email and  <phone>@vtext.com for a text
BOOKING_CODE = ""  # the booking code from the URL of the ticketing site, a uuid
TICKET_URL = ""  # the URL you got for tickets
PARTY_SIZE = 6  # the number of people in your party


unavailable_dates = [
    dt.date(2024, 2, 26),
    dt.date(2024, 2, 27),
    dt.date(2024, 2, 28),
    dt.date(2024, 2, 29),
    dt.date(2024, 3, 1),
]

####################
# End of variables #
####################

def send_message(msg):
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=TO_EMAILS,
        subject='Date Available at Casa Bonita',
        html_content=msg + f"<br /><br />{TICKET_URL}"
    )
    sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)


def check_dates():
    url = "https://casatix-api.casabonitadenver.com/api/v2/search"
    params = {

        "booking_code": BOOKING_CODE,
        "fc_token": "",
        "party_size": PARTY_SIZE,
        "res_date": "",
        "service": "dinner"
    }

    session = requests.Session()

    date = dt.date.today()
    messages = []
    while True:
        # print(date)
        logger.info(f"Checking date {date}")
        date += dt.timedelta(days=1)
        if date in unavailable_dates:
            continue
        params["res_date"] = date.isoformat()
        res = session.get(url, params=params, timeout=10)
        if res.status_code != 200:
            if "This code cannot be used for visits after" in res.json().get("display_error", ""):
                print(f"No more dates after {date}")
                break
            print(f"Error: {res.status_code}\n{res.text}")
            continue
        data = res.json()
        if data['times_available']:
            # the results look like this: {'times_available': [{'time': '2024-02-27T20:30', 'experiences': [{'id': 171289, 'name': 'Traditional Dining'}]}], 'experiences_by_id': {'171289': {'item_id': 2, 'name': 'Traditional Dining', 'description': 'The traditional Casa Bonita experience with the opportunity to sit in multiple dining areas such as the Plaza, Gold Mine, Limestone Caverns, etc.', 'description_detail': '<ul>\r\n<li> Each ticket includes an entree of incredible Mexican food, chips & salsa, a soft drink, and of course, sopaipillas!</li>\r\n<li> Everyone age 3 and up must purchase a ticket to enter the restaurant.</li>\r\n<li> Alcoholic beverages and other menu items are sold separately.</li>\r\n<li> Ticket holder must show ID to enter.</li>\r\n</ul>', 'price_description': '$39.99 / Adults<br>$24.99 / Kids (age 3-12)', 'prices': {'adult': '39.99', 'child': '24.99', 'baby': '0.00', 'flex': '10.00'}, 'flex_allowed': True, 'skus': {'adult': 'ga_dinner_adult', 'child': 'ga_dinner_child', 'baby': 'baby'}, 'id': 171289, 'version': 4}, '171306': {'item_id': 3, 'name': 'Cliffside Dining', 'description': 'A premium dining experience for those who wish to skip the line and sit cliffside with dedicated table service.', 'description_detail': '<ul>\r\n<li> Each ticket includes an entree of incredible Mexican food, chips & salsa, a soft drink, and of course, sopaipillas!</li>\r\n<li> Everyone age 3 and up must purchase a ticket to enter the restaurant.</li>\r\n<li> Alcoholic beverages and other menu items are sold separately.</li>\r\n<li> Ticket holder must show ID to enter.</li>\r\n</ul>', 'price_description': '$44.99 / per person', 'prices': {'adult': '44.99', 'child': '44.99', 'baby': '0.00', 'flex': '10.00'}, 'flex_allowed': True, 'skus': {'adult': 'premium_dinner_adult', 'child': 'premium_dinner_child', 'baby': 'baby'}, 'id': 171306, 'version': 2}, '204321': {'item_id': 6, 'name': 'Traditional Dining - Lunch', 'description': "The traditional Casa Bonita experience with the opportunity to sit in multiple dining areas such as the Plaza, Governor's Palace, Gold Mine, Limestone Caverns, etc.", 'description_detail': '<ul>\r\n<li> Each ticket includes an entree of incredible Mexican food, chips & salsa, a soft drink, and of course, sopaipillas!</li>\r\n<li> Everyone age 3 and up must purchase a ticket to enter the restaurant.</li>\r\n<li> Alcoholic beverages and other menu items are sold separately.</li>\r\n<li> Ticket holder must show ID to enter.</li>\r\n</ul>', 'price_description': '$29.99 / Adults<br>$19.99 / Kids (age 3-12)', 'prices': {'adult': '29.99', 'child': '19.99', 'baby': '0.00', 'flex': '10.00'}, 'flex_allowed': True, 'skus': {'adult': 'ga_lunch_adult', 'child': 'ga_lunch_child', 'baby': 'baby'}, 'id': 204321, 'version': 1}, '204323': {'item_id': 5, 'name': 'Cliffside Dining - Lunch', 'description': 'A premium dining experience for those who wish to skip the line and sit cliffside with dedicated table service.', 'description_detail': '<ul>\r\n<li> Each ticket includes an entree of incredible Mexican food, chips & salsa, a soft drink, and of course, sopaipillas!</li>\r\n<li> Everyone age 3 and up must purchase a ticket to enter the restaurant.</li>\r\n<li> Alcoholic beverages and other menu items are sold separately.</li>\r\n<li> Ticket holder must show ID to enter.</li>\r\n</ul>', 'price_description': '$34.99 / per person', 'prices': {'adult': '34.99', 'child': '34.99', 'baby': '0.00', 'flex': '10.00'}, 'flex_allowed': True, 'skus': {'adult': 'premium_lunch_adult', 'child': 'premium_lunch_child', 'baby': 'baby'}, 'id': 204323, 'version': 1}}}
            # get a list of names of experiences from all times_available
            experiences = []
            for _time in data['times_available']:
                for exp in _time['experiences']:
                    experiences.append(exp['name'])
            print(experiences, date)
            if "Cliffside Dining" in experiences:
                print(f"{date} has Cliffside Dining")
                print()
                messages.append(f"{date} has Cliffside Dining")
                # send_message(f"{date} has Cliffside Dining")
            # check if any of the options are not Traditional Dining
            elif any(exp not in ["Traditional Dining"] for exp in experiences):
                print(f"{date} has other options")
                print()
                messages.append(f"{date} has other options")
                # send_message(f"{date} has other options")
            else:
                print(f"{date} has Traditional Dining")
                print()
                # if you want to be notified of Traditional Dining, uncomment the next line
                # messages.append(f"{date} has Traditional Dining")

    if messages:
        send_message("<br />".join(messages))
        # print()


if __name__ == '__main__':
    while True:
        print(f"### {dt.datetime.now()} ###")
        logger.info(f"Checking dates")
        check_dates()
        time.sleep(600)
