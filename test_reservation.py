from typing import Pattern
from unittest.case import SkipTest, skip
import requests, unittest, datetime, re
from decouple import config
from parameterized import parameterized
from enum import Enum

"""
Important Caveat:
This unittest tests the logging branch of the WCG project.


Please create your own env file and add configurations
to make running this test possible (See README).
"""

base_url = config("BASE_URL", default="https://wcg-apis.herokuapp.com")
# print(base_url)

# REGISTRATION = "/registration"
# RESERVATION = "/reservation"
# CITIZEN = "/citizen"
# REPORT_TAKEN = "/report_taken"

registration_url = base_url+"/registration"
reservation_url = base_url+"/reservation"
report_url = base_url+"/report_taken"
citizen_url = base_url+"/citizen"


class FeedBack(Enum):
    FINISHED_ALL_VACCINE = "reservation failed: you finished all vaccinations"
    ONE_VACCINE_OPTION_LEFT = "reservation failed: your next vaccine can be {vaccines} only"
    VACCINE_OPTIONS_LEFT = "reservation failed: your available vaccines are only {vaccines}"
    INVALID_CITIZEN_ID = "reservation failed: invalid citizen ID"
    INVALID_VACCINE = "report failed: invalid vaccine name"
    CITIZEN_NOT_REGISTERED = "reservation failed: citizen ID is not registered"
    ALREADY_HAVE_RESERVATION = "reservation failed: there is already a reservation for this citizen"
    RESERVATION_SUCCESS = "reservation success!"


def create_citizen_dict(citizen_id, name, surname, birth_date, occupation, address):
    return dict(citizen_id=citizen_id, name=name, surname=surname,
        birth_date=birth_date, occupation=occupation, address=address)

def create_reservation_dict(citizen_id, site_name, vaccine_name):
    return dict(citizen_id=citizen_id, site_name=site_name, vaccine_name=vaccine_name)

def create_report_dict(citizen_id, vaccine_name, option):
    return dict(citizen_id=citizen_id, vaccine_name=vaccine_name, option=option)


class ReservationTest(unittest.TestCase):
    """Test the reservation API endpoint.
    
    Since the latest version (master branch) has many errors,
    such as not being able to reset the whole or delete one data from
    the database, then the latest version of the logging branch will be used.
    """

    def setUp(self) -> None:
        self.citizen1 = create_citizen_dict("1006210546650", "Raymoo", "Fumo",
            "21-01-2001", "going for a schwim", "::1")
        self.citizen2 = create_citizen_dict("1016210546650", "Yucurri", "Fumo",
            "21-01-1988", "used Astrazeneca", "::1")
        self.citizen3 = create_citizen_dict("1026210546650", "Patchy", "Fumo",
            "21-01-1997", "double Astrazeneca", "::1")
        self.citizen4 = create_citizen_dict("9996210546650", "Cirno", "Fumo",
            "09-09-1999", "fully immunized!", "9::9")

        requests.post(registration_url, data=self.citizen1)
        requests.post(registration_url, data=self.citizen2)
        requests.post(registration_url, data=self.citizen3)
        requests.post(registration_url, data=self.citizen4)

        report2 = create_report_dict(self.citizen2["citizen_id"], "Astra", "walk-in")
        report3 = create_report_dict(self.citizen3["citizen_id"], "Astra", "walk-in")
        report4 = create_report_dict(self.citizen4["citizen_id"], "Pfizer", "walk-in")

        requests.post(report_url, data=report2)
        requests.post(report_url, data=report3)
        requests.post(report_url, data=report3)
        requests.post(report_url, data=report4)
        requests.post(report_url, data=report4)



    def test_correct_reservation(self):
        reservation1 = create_reservation_dict(self.citizen1["citizen_id"], "OGYH", "Sinovac")
        r = requests.post(reservation_url, data=reservation1)
        feedback = r.json()["feedback"]
        # self.assertEqual(201, r.status_code)
        self.assertEqual(FeedBack.RESERVATION_SUCCESS.value, feedback)

    def test_same_citizen_reserve_twice(self):
        reserve_astra = create_reservation_dict(self.citizen1["citizen_id"], "OGYH", "Astra")
        reserve_sinovac = create_reservation_dict(self.citizen1["citizen_id"], "OGYH", "Sinovac")
        r1 = requests.post(reservation_url, data=reserve_astra)
        r2 = requests.post(reservation_url, data=reserve_sinovac)
        feedback1 = r1.json()["feedback"]
        feedback2 = r2.json()["feedback"]

        # self.assertEqual(201, r1.status_code)
        self.assertEqual(FeedBack.RESERVATION_SUCCESS.value, feedback1)
        # self.assertEqual(400, r2.status_code)
        self.assertEqual(FeedBack.ALREADY_HAVE_RESERVATION.value, feedback2)

    def test_reserve_invalid_vaccine(self):
        reserve_vodka = create_reservation_dict(self.citizen1["citizen_id"], "OGYH", "Vodka")
        r = requests.post(reservation_url, data=reserve_vodka)
        feedback = r.json()["feedback"]
        # self.assertEqual(400, r.status_code)
        self.assertEqual(FeedBack.INVALID_VACCINE.value, feedback)

    def test_reserve_unavailable_vaccine_option(self):
        reserve_sinofarm = create_reservation_dict(self.citizen2["citizen_id"], "OGYH", "Sinofarm")
        r = requests.post(reservation_url, data=reserve_sinofarm)
        feedback = r.json()["feedback"]
        # self.assertEqual(400, r.status_code)
        expected_feedback = FeedBack.VACCINE_OPTIONS_LEFT.value.format(vaccines=["Astra","Pfizer"])
        self.assertEqual(expected_feedback, feedback)
        
    def test_only_one_vaccine_option_available(self):
        reserve_astra = create_reservation_dict(self.citizen3["citizen_id"], "OGYH", "Sinofarm")
        r = requests.post(reservation_url, data=reserve_astra)
        feedback = r.json()["feedback"]
        # self.assertEqual(400, r.status_code)
        expected_feedback = FeedBack.ONE_VACCINE_OPTION_LEFT.value.format(vaccines=["Pfizer"])
        self.assertEqual(expected_feedback, feedback)

    def test_finished_all_vaccine_option(self):
        reserve_pfizer = create_reservation_dict(self.citizen4["citizen_id"], "OGYH", "Sinofarm")
        r = requests.post(reservation_url, data=reserve_pfizer)
        feedback = r.json()["feedback"]
        # self.assertEqual(400, r.status_code)
        self.assertEqual(FeedBack.FINISHED_ALL_VACCINE.value, feedback)

    def test_reserve_unregistered_citizen(self):
        reserve_sinofarm = create_reservation_dict("5556210546650", "Suchon", "Sinofarm")
        r = requests.post(reservation_url, data=reserve_sinofarm)
        feedback = r.json()["feedback"]
        # self.assertEqual(400, r.status_code)
        self.assertEqual(FeedBack.CITIZEN_NOT_REGISTERED.value, feedback)

    def test_reserve_button_site(self):
        reserve_at_click_me_site = create_reservation_dict(
            self.citizen1["citizen_id"],
            "<button type=\"button\">Click Me Site!</button>",
            "Sinovac"
        )
        r = requests.post(reservation_url, data=reserve_at_click_me_site)
        feedback = r.json()["feedback"]
        self.assertEqual(400, r.status_code)
        pattern = r"(?i)(script|scripts) .* (?i)(not allow|not allowed)"
        self.assertRegex(feedback, pattern)
    

    def tearDown(self) -> None:
        requests.delete(citizen_url)


    