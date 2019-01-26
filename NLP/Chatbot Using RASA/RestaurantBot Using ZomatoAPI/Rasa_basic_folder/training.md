## Generated Story 5984379002978265517
* greet
    - utter_greet
* restaurant_search{"location": "rishikesh"}
    - slot{"location": "rishikesh"}
    - action_location
    - slot{"location": null}
* restaurant_search{"location": "allahabad"}
    - slot{"location": "allahabad"}
    - action_location
    - slot{"location": "allahabad"}
    - utter_ask_cuisine
* restaurant_search{"cuisine": "chinese"}
    - slot{"cuisine": "chinese"}
    - utter_ask_pricerange
* restaurant_search{"pricerange": "3"}
    - slot{"pricerange": "3"}
    - action_restaurant
    - slot{"location": "allahabad"}
    - utter_ask_emailsendconfirm
* send_email{"email": "sambitjasu@gmail.com"}
    - slot{"email": "sambitjasu@gmail.com"}
    - action_email
    - utter_goodbye_emailsent
    - action_reset
    - slot{"location": null}
    - slot{"pricerange": null}
    - slot{"email": null}
    - slot{"cuisine": null}
