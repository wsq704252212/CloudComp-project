import requests
import json
import boto3
import datetime
import decimal
import random
from faker import Faker
import pandas as pd
import time

apiKey = 'PQNXZrV3FcfBac6IKhtbu5oiPsBasUTuzIoUuy8ANtl_qq3ANl5luvPwlKf1YeeDVgZqruJ26IN2awnga9GJJErunQBwHCKof8K9CARi1oh8NfEULuZE6nyab97SZXYx'
EventType = ["badminton", "bars", "restaurants", "movietheaters",
		"citywalk", "hiking", "coffee", "escapegames", "dog_parks",
		"basketballcourts", "climbing", "fishing", "galleries", "museums", "musicvenues"]
userNumber = 500
eventNumberPerType = 40

fake = Faker()
Faker.seed(2)
random.seed(5)


def generateUser():
    uid = 0
    users = []
    for u in range(userNumber):
        numberOfInterest = random.randint(2, 5)
        interests = []
        for i in range(numberOfInterest):
            interest = EventType[random.randint(0, len(EventType)-1)]
            if interest not in interests:
                interests.append(interest)

        email = fake.email()
        user = {
            #'Uid': email,
            'Email': email,
            'Interests': interests
        }
        uid = uid + 1
        users.append(user)

    with open('user-v2.json', 'w') as f:
        json.dump(users, f)

    return users


def generateEvent(users):
    events = []
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + apiKey
    }

    eid = 0
    for e in EventType:
        url = "https://api.yelp.com/v3/businesses/search?location=Manhattan&categories=" + e + "&sort_by=best_match&limit=" + str(eventNumberPerType)
        response = requests.get(url, headers=headers)
        parsed = json.loads(response.text)  

        for res in parsed["businesses"]:
            # generate participants
            numberOfPeople = random.randint(2, 7)
            participants = []
            for i in range(numberOfPeople - random.randint(1, numberOfPeople-1)): 
                participantsID = random.randint(0, userNumber-1)
                if users[participantsID]['Email'] not in participants:
                    participants.append(users[participantsID]['Email'])

            # generate event
            event = {
                'Eid': eid,
                'Type': e,
                'Address': res['location']['address1'],
                'Latitude': res['coordinates']['latitude'],
                'Longitude': res['coordinates']['longitude'],
                'NumberOfPeople': numberOfPeople,
                'StartTime': fake.date_time_between_dates(datetime_start=datetime.date(2024, 5, 14),
                                                        datetime_end=datetime.date(2024, 5, 28)).isoformat(),
                'Participants': participants,
            }
            eid = eid + 1

            #jsonEvent = json.dumps(event)
            #print(jsonEvent)
            #dbEvent = json.loads(jsonEvent, parse_float=decimal.Decimal)

            events.append(event)
    
    with open('event-v2.json', 'w') as f:
        json.dump(events, f)

    return events


def generateInteraction(events):
    interactions = []
    for e in events:
        dt = datetime.datetime.fromisoformat(e['StartTime'])
        timestamp = round(time.mktime(dt.timetuple()))

        for u in e['Participants']:
            action = {
                'USER_ID': u,
                'ITEM_ID': e['Eid'],
                'TIMESTAMP': timestamp
            }
            interactions.append(action)

    df = pd.DataFrame(interactions)
    df.head()
    df.to_csv('interaction-dataset-v2.csv', index=False)

def generateEventsDataset(events):
    eventDS = []
    for e in events:
        event = {
            'ITEM_ID': e['Eid'],
            'TYPE': e['Type']
        }
        eventDS.append(event)

    df = pd.DataFrame(eventDS)
    df.head()
    df.to_csv('event-dataset-v2.csv', index=False)


def generateUserDataset(users):
    usersDS = []
    for u in users:
        user = {
            'USER_ID': u['Email'],
            'INTERESTS': '|'.join(u['Interests'])
        }
        usersDS.append(user)

    df = pd.DataFrame(usersDS)
    df.head()
    df.to_csv('user-dataset-v2.csv', index=False)


users = generateUser()
events = generateEvent(users)
print(len(users), len(events))
generateInteraction(events)
generateEventsDataset(events)
generateUserDataset(users)


