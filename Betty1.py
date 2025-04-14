import requests 
import json
import datetime
from bs4 import BeautifulSoup
from datetime import datetime as dt
import os
import sys
import time as tm
import keyring as kr
from urllib.parse import urlencode
from dotenv import load_dotenv
sys.path.append("/Users/ethandan/Desktop/Codes")
from Utils.communication import send_text, send_email

load_dotenv()




ToDoList = {
}
Script_Instructions = {
# Example function call shown below. Can use commas or not
##
## python3 Betty.py Ethan Dan, Black, 10-11-2024, 07:00, 10:00, 2, 4

### This script will run every 2 seconds and pull available tee times on the day and course you have listed. 
### If a time appears that is between the min and max_time called in the fucntion >= number of players listed, it will attempt to book that tee time

}
Bethpage_Rules = {
#1. 8 Cancel/Modifys per month per user
#2. 1 booking every 28 days per user on black, 1 booking every 14 days per user on Red, unlimited on Green, Blue, Yellow

## Apriil COUNT 
# Ethan: Cancellation/Modify: 3, Black: 0, Red: 0
# Marchi: Cancellation/Modify: 0, Black: 0 , Red: 0
# Richad: Cancellation/Modify: 0, Black: 0,  Red: 1
# Paolo: Cancellation/Modify: 1, Black: 1, Red: 0
# Barry: Cancellation/Modify: 0, Black: 0, Red: 0
}

## Relevant Dictionaries: Account and Course Specific
Account_Info_Dict = {
        "Alex Marchi": {
            "username": "",
            "X-Authorization": ""
        },
        "Ethan Dan": {
            "username": "ejdan98@gmail.com",
            "X-Authorization": ""
        },
        "Richad Hirani": {
            "username": "richadhirani@gmail.com",
            "X-Authorization": ""
        },
        "Paolo Olavario": {
            "username":"Prolavario@gmail.com",
            "X-Authorization": ""
        },
        "Barry Yung": {
            "username": "barrylyung@gmail.com",
            "Cookie": "PHPSESSID=o7tjo2692jt2b18gt31flrash2; __stripe_mid=f9bf1bd7-deac-48b6-bb03-1556ffa15803a794b1; _gid=GA1.2.347343975.1744669045; __stripe_sid=2bef6d26-c2a3-4bca-a3c7-27b0c3a7cffedac013; _gat_gtag_UA_101056671_2=1; _ga_Y0N3BHPPWG=GS1.1.1744669045.21.1.1744669183.0.0.0; _ga=GA1.1.651883819.1738084791; _dd_s=rum=1&id=cbe1e455-bd62-47f0-99a7-baf1e72c89d1&created=1744669044996&expire=1744670089731",
            "X-Authorization": ""
        }
    }
courses = ["Black","Red","Green","Blue","Yellow"]
num_players = 1
course = ""

course_info_dict = {
    "Black": {
        "schedule_name": "Bethpage Black Course",
        "teesheet_side_id": 1014,
        "reround_teesheet_side_id": 1015,
        "schedule_id": 2431,
        "teesheet_id": 2431,
    },
    "Red": {
        "schedule_name": "Bethpage Red Course",
        "teesheet_side_id": 1016,
        "reround_teesheet_side_id": 1017,
        "schedule_id": 2432,
        "teesheet_id": 2432
    },
    "Green": {
        "schedule_name": "Bethpage Green Course",
        "teesheet_side_id": 1020,
        "reround_teesheet_side_id": 1021,
        "schedule_id": 2434,
        "teesheet_id": 2434
    },
        
        "Blue": {
        "schedule_name": "Bethpage Blue Course",
        "teesheet_side_id": 1018,
        "reround_teesheet_side_id": 1019,
        "schedule_id": 2433,
        "teesheet_id": 2433
    },
    
        "Yellow": {
        "schedule_name": "Bethpage Yellow Course",
        "teesheet_side_id": 1022,
        "reround_teesheet_side_id": 1023,
        "schedule_id": 2435,
        "teesheet_id": 2435
    }
}

headers_template = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Api-Key": "no_limits",
        "Content-Type": "application/json",
        "Origin": "https://foreupsoftware.com",
        "Referer": "https://foreupsoftware.com/index.php/booking/19765/2431",
        "Sec-Ch-Ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"macOS\"",
        "Cookie": "",
        "X-Authorization": "",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "X-Fu-Golfer-Location": "foreup",
        "X-Requested-With": "XMLHttpRequest"
    }
payload_template = {
        "time": "",
        "course_id": 19765,
        "airQuotesCart": [
            {
                "type": "item", 
                "description": "Green Fee", 
                "price": 28, 
                "quantity": 1, 
                "subtotal": 28
            }
            ],
        "allow_mobile_checkin": 0,
        "allowed_group_sizes": ["1", "2", "3", "4"],
        "availableHoles": "18",
        "available_duration": None,
        "available_spots": 1,
        "available_spots_9": 0,
        "available_spots_18": 1,
        "blockReservationDueToExistingReservation": False,
        "booking_class_id": 0,
        "booking_fee_per_person": False,
        "booking_fee_price": False,
        "booking_fee_required": False,
        "captchaid": "PHPSESSID=o7tjo2692jt2b18gt31flrash2; __stripe_mid=f9bf1bd7-deac-48b6-bb03-1556ffa15803a794b1; _gid=GA1.2.1211452850.1741121338; _ga_Y0N3BHPPWG=GS1.1.1741121337.8.1.1741121399.0.0.0; _ga=GA1.1.651883819.1738084791; __stripe_sid=49975532-e257-404e-88e6-0349a0dba59b48719e; _dd_s=rum=1&id=756387a5-e6e5-48b5-b485-e981a6f393c7&created=1741121337893&expire=1741123468731",
        "cart_fee": 0,
        "cart_fee_9": 0,
        "cart_fee_18": 0,
        "cart_fee_tax": 0,
        "cart_fee_tax_9": 0,
        "cart_fee_tax_18": 0,
        "cart_fee_tax_rate": False,
        "carts": False,
        "course_name": "Bethpage State Park",
        "customer_message": "",
        "details": "",
        "discount": 0,
        "discount_percent": 0,
        "duration": 1,
        "estimatedTax": 0,
        "foreup_discount": False,
        "foreup_trade_discount_information": [],
        "foreup_trade_discount_rate": 0,
        "green_fee": 28,
        "green_fee_9": 0,
        "green_fee_18": 28,
        "green_fee_tax": 0,
        "green_fee_tax_9": 0,
        "green_fee_tax_18": 0,
        "green_fee_tax_rate": False,
        "group_id": False,
        "guest_cart_fee": 0,
        "guest_cart_fee_9": 0,
        "guest_cart_fee_18": 0,
        "guest_cart_fee_tax": 0,
        "guest_cart_fee_tax_9": 0,
        "guest_cart_fee_tax_18": 0,
        "guest_cart_fee_tax_rate": False,
        "guest_green_fee": 28,
        "guest_green_fee_9": 0,
        "guest_green_fee_18": 28,
        "guest_green_fee_tax": 0,
        "guest_green_fee_tax_9": 0,
        "guest_green_fee_tax_18": 0,
        "guest_green_fee_tax_rate": False,
        "has_special": False,
        "holes": "18",
        "increment_amount": None,
        "maximum_players_per_booking": "4",
        "minimum_players": "1",
        "notes": [],
        "paid_player_count": 0,
        "pay_carts": False,
        "pay_online": "no",
        "pay_players": num_players,
        "players": num_players,
        "pay_subtotal": 28,
        "pay_total": 28,
        "player_list": False,
        "preTaxSubtotal": 28,
        "promo_code": "",
        "promo_discount": 0,
        "purchased": False,
        "rate_type": "walking",
        "require_credit_card": False,
        "reround_teesheet_side_id": 1015,
        "reround_teesheet_side_name": "Back",
        "schedule_id": 2431,
        "schedule_name": course,
        "special_discount_percentage": 0,
        "special_id": False,
        "special_was_price": None,
        "subtotal": 28,
        "teesheet_holes": 18,
        "teesheet_id": 2431,
        "teesheet_side_id": 1014,
        "teesheet_side_name": "Front",
        "teesheet_side_order": 1,
        "total": 28,
        "trade_available_players": 0,
        "trade_cart_requirement": "riding",
        "trade_hole_requirement": "18",
        "trade_min_players": 8
    }

def BookTeeTime(user, course, date_and_booking_time, players):
    url = "https://foreupsoftware.com/index.php/api/booking/users/reservations"

    headers = headers_template.copy()
    #headers["Cookie"] = Account_Info_Dict[user]["Cookie"]
    headers["X-Authorization"] = Account_Info_Dict[user]["X-Authorization"]

    payload = payload_template.copy()
    for param in ['schedule_name','teesheet_side_id','reround_teesheet_side_id','schedule_id','teesheet_id']:
        payload[param] = course_info_dict[course][param]
    payload["time"] = date_and_booking_time
    payload["players"] = players
    payload["pay_players"]= players
    
    response = requests.post(url, headers=headers, data = json.dumps(payload))
    response_content = json.loads(response.content)
    print(response.status_code, response_content)

    if response.status_code == 200 and 'teetime_id' in response_content and 'start_datetime' in response_content:
        subject, text = "Betty" , f"Time was booked on {course} for {date_and_booking_time} under {user}"
        my_email = os.getenv("EMAIL_USERNAME")
        password = os.getenv("EMAIL_APP_PASSWORD")
        send_email(send_from = my_email, send_to =[my_email], subject=subject, text=text, files=None, server="smtp.gmail.com", port=587, username=my_email, password=password)
        return True
    else:
        return False

def PullTeeTimes(user, course, date, min_time, max_time, min_players, max_players):
    booking_success = False
    holes = 'all'
    players = min_players
    booking_class = '50297'
    schedule_id = str(course_info_dict[course]["schedule_id"])
    schedule_ids = "2517&schedule_ids[]=2431&schedule_ids[]=2433&schedule_ids[]=2539&schedule_ids[]=2538&schedule_ids[]=2434&schedule_ids[]=2432&schedule_ids[]=2435"
    specials_only =  '0'
    api_key = 'no_limits'

    #make user specific header adjustments
    headers = headers_template.copy()
    #headers["Cookie"] = Account_Info_Dict[user]["Cookie"]
    headers["X-Authorization"] = Account_Info_Dict[user]["X-Authorization"]

    t = datetime.datetime.now()
    s = t.strftime('%Y-%m-%d %H:%M:%S.%f')
    print(f"Time: {s[:-4]}, checking for {course}, {date}")

    url = f"https://foreupsoftware.com/index.php/api/booking/times?time=all&date={date}&holes={holes}&players={players}&booking_class={booking_class}&schedule_id={schedule_id}&schedule_ids[]={schedule_ids}&specials_only={specials_only}&api_key={api_key}"    
    response = requests.get(url, headers=headers)
    if response.content:
        tee_times = json.loads(response.content)
    else:
        print("Empty response content")
        tee_times = []
    
    for tee_time in tee_times:
        course_name = tee_time['schedule_name'].split(' ')[1]
        official_tee_time = tee_time['time'].split(' ')[1]
        consolidated_tee_time_des = f"{course_name}, {official_tee_time}, {tee_time['available_spots']}"
        print(consolidated_tee_time_des)

        if  official_tee_time >= min_time and official_tee_time <= max_time:

            full_booking_time = f"{date} {official_tee_time}"
            reformatted_booking_time = datetime.datetime.strptime(full_booking_time, '%m-%d-%Y %H:%M').strftime('%Y-%m-%d %H:%M')
            available_spots = int(tee_time['available_spots'])
            if available_spots >= int(min_players):
                num_players = min(available_spots,int(max_players))
                consolidated_booking_des = f"{course_name}, {official_tee_time}, {num_players}"
                print(f"Booking tee time: {consolidated_booking_des}")
                booking_success = BookTeeTime(user, course, reformatted_booking_time, num_players)

                if booking_success:
                    print(f"{consolidated_tee_time_des} Tee time booked successfully, exiting loop.")
                    break  
                else:
                    print("Booking failed, continuing to next tee time.")
    tm.sleep(2)
    return booking_success





def CancelTeeTime(user, tee_time_id):

    url = f"https://foreupsoftware.com/index.php/api/booking/users/reservations/{tee_time_id}"

    headers = headers_template.copy()
    headers["X-Authorization"] = Account_Info_Dict[user]["X-Authorization"]

    response = requests.delete(url, headers=headers)

    # Print the response
    if response.content:
        cancellation_message = json.loads(response.content)
        print(cancellation_message)
    else:
        print("Empty response content")


def Login(user):
    url = "https://foreupsoftware.com/index.php/api/booking/users/login"

    username = Account_Info_Dict[user]["username"]
    if not username:
        print("No username stored in Account_Info_Dict. Please set one and ensure credentials are in keyring as well. Exiting...")
        exit()
    password = kr.get_password("Bethpage", username)
    if not password:
        print("No stored password found. Please set them using keyring. Exiting...")
        exit()

    headers = headers_template.copy()
    headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'


    payload = {
    "username": username,
    "password": password,
    "booking_class_id": "",
    "api_key": "no_limits",
    "course_id": "19765",
}

    payload_encoded = urlencode(payload)

    response = requests.post(url, data=payload_encoded, headers=headers)

    if response.status_code == 200:
        response_data = response.json()  
        print("Login successful!")
    

        jwt = response_data.get('jwt') 
        booking_class_ids = response_data.get('booking_class_ids')
    
        print(f"Booking Class IDs: {booking_class_ids}")

        Account_Info_Dict[user]["X-Authorization"] = f"Bearer {jwt}"
    else:
        print(f"Login failed with status code: {response.status_code}")
        print("Response content:", response.content)
        print("Exiting...")


   

def PullTeeTimesLoop(args):
    while True:
        project_sucess = PullTeeTimes(f"{args[1]} {args[2]}", args[3], args[4], args[5], args[6], args[7], args[8])
        if project_sucess:
            print("Acheived Assigned Booking, no longer checking for times.")
            break

       


if __name__ == '__main__':
    args = sys.argv
    for i in range(len(args)):
        args[i] = args[i].replace(',','')
    Login(f"{args[1]} {args[2]}")
    PullTeeTimesLoop(args)
    
    #CancelTeeTime("Ethan Dan", "TTID_03041622232p0ac")