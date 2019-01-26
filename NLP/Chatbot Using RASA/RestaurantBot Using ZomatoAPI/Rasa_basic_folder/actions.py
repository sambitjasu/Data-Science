from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet
import zomatopy
import json

from flask import Flask
from flask_mail import Mail, Message
import logging

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    #EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = 'upgradrestaurantbot@gmail.com',
    MAIL_PASSWORD = 'Zomato@2019'
    )
mail = Mail(app)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


class ActionSearchRestaurants(Action):
    def name(self):
        return 'action_restaurant'

    def run(self, dispatcher, tracker, domain):
        citylist=["AGRA","AJMER","ALIGARH","ALLAHABAD","AMRAVATI","AMRITSAR","ASANSOL","AURANGABAD","BAREILLY","BELGAUM","BHAVNAGAR","BHIWANDI","BHOPAL","BHUBANESWAR","BIKANER","BOKARO STEEL CITY","CHANDIGARH","COIMBATORE","CUTTACK","DEHRADUN","DHANBAD","DURG-BHILAI NAGAR","DURGAPUR","ERODE","FARIDABAD","FIROZABAD","GHAZIABAD","GORAKHPUR","GULBARGA","GUNTUR","GURGAON","GUWAHATI‚ GWALIOR","HUBLI-DHARWAD","INDORE","JABALPUR","JAIPUR","JALANDHAR","JAMMU","JAMNAGAR","JAMSHEDPUR","JHANSI","JODHPUR","KANNUR","KANPUR","KAKINADA","KOCHI","KOTTAYAM","KOLHAPUR","KOLLAM","KOTA","KOZHIKODE","KURNOOL","LUCKNOW","LUDHIANA","MADURAI","MALAPPURAM","MATHURA","GOA","MANGALORE","MEERUT","MORADABAD","MYSORE","NAGPUR","NANDED","NASHIK","NELLORE","NOIDA","PALAKKAD","PATNA","PONDICHERRY","RAIPUR","RAJKOT","RAJAHMUNDRY","RANCHI","ROURKELA","SALEM","SANGLI","SILIGURI","SOLAPUR","SRINAGAR","SULTANPUR","SURAT","THIRUVANANTHAPURAM","THRISSUR","TIRUCHIRAPPALLI","TIRUNELVELI","TIRUPPUR","UJJAIN","VIJAYAPURA","VADODARA","VARANASI","VASAI-VIRAR CITY","VIJAYAWADA","VISAKHAPATNAM","WARANGAL,AHMEDABAD","BANGALORE","CHENNAI","DELHI","HYDERABAD","KOLKATA","MUMBAI","PUNE"]

        config={ "user_key":"dd6123ea663dc9965f87bcc94ef4e6be"}
        zomato = zomatopy.initialize_app(config)
        loc = tracker.get_slot('location')

        response = zomato.get_city_ID(loc)
        if(response == 'invalid_city_name'):
          dispatcher.utter_message("I couldn't find any city with name "+loc + " .Can you please tell again")
          loc=None
          return [SlotSet('location',loc)]

        if loc.upper() in citylist:
          cuisine = tracker.get_slot('cuisine')
          pricerange = tracker.get_slot('pricerange')
          location_detail=zomato.get_location(loc, 1)
          d1 = json.loads(location_detail)
          lat=d1["location_suggestions"][0]["latitude"]
          lon=d1["location_suggestions"][0]["longitude"]
          cuisines_dict={'american': 1,'chinese': 25, 'north indian': 50, 'italian': 55, 'mexican': 73, 'south indian': 85, 'thai': 95}

          results=zomato.restaurant_search("", lat, lon, str(cuisines_dict.get(cuisine)), 10)
          d = json.loads(results)
          response="Showing you top rated restaurants: \n"
          sorted_response = sorted(d.get("restaurants"), key= lambda k: float(k['restaurant']['user_rating']['aggregate_rating']), reverse=True)

          if(pricerange == '1'):
              minPrice = 0
              maxPrice = 299
          elif(pricerange == '2'):
              minPrice = 300
              maxPrice = 700
          elif(pricerange == '3'):
              minPrice = 701
              maxPrice = 100000
          elif(pricerange == '4'):
              minPrice = 0
              maxPrice = 700
          elif(pricerange == '5'):
              minPrice = 300
              maxPrice = 100000

          counter = 0
          if d['results_found'] == 0:
              response= "no results"
          else:
              for restaurantDict in sorted_response:
                  restaurant = restaurantDict['restaurant']
                  average_cost_for_two = restaurant['average_cost_for_two']
                  aggregate_rating = restaurant['user_rating']['aggregate_rating']
                  if(average_cost_for_two >= int(minPrice) and average_cost_for_two <= int(maxPrice)):
                      if(counter < 5):
                          response= response +str(counter + 1) + ". Restaurant " +  restaurant['name'] + " in " + restaurant['location']['address'] + " has been rated " + str(aggregate_rating) + "\n"
                          counter = counter + 1

                  if response is None:
                      response="No restaurants found in given pricerange"

        else:
          response="We do not operate in that area yet"
          loc=None
          cuisine=None

        if(counter == 0):
            dispatcher.utter_message("Sorry, We couldn't find any restaurants with those details. Please try again")
            return [SlotSet('location',None), SlotSet('pricerange',None), SlotSet('cuisine',None)]

        dispatcher.utter_message(response)
        return [SlotSet('location',loc)]


class SendMail(Action):
    def name(self):
      return 'action_email'

    def run(self, dispatcher, tracker, domain):
      citylist=["AGRA","AJMER","ALIGARH","ALLAHABAD","AMRAVATI","AMRITSAR","ASANSOL","AURANGABAD","BAREILLY","BELGAUM","BHAVNAGAR","BHIWANDI","BHOPAL","BHUBANESWAR","BIKANER","BOKARO STEEL CITY","CHANDIGARH","COIMBATORE","CUTTACK","DEHRADUN","DHANBAD","DURG-BHILAI NAGAR","DURGAPUR","ERODE","FARIDABAD","FIROZABAD","GHAZIABAD","GORAKHPUR","GULBARGA","GUNTUR","GURGAON","GUWAHATI‚ GWALIOR","HUBLI-DHARWAD","INDORE","JABALPUR","JAIPUR","JALANDHAR","JAMMU","JAMNAGAR","JAMSHEDPUR","JHANSI","JODHPUR","KANNUR","KANPUR","KAKINADA","KOCHI","KOTTAYAM","KOLHAPUR","KOLLAM","KOTA","KOZHIKODE","KURNOOL","LUCKNOW","LUDHIANA","MADURAI","MALAPPURAM","MATHURA","GOA","MANGALORE","MEERUT","MORADABAD","MYSORE","NAGPUR","NANDED","NASHIK","NELLORE","NOIDA","PALAKKAD","PATNA","PONDICHERRY","RAIPUR","RAJKOT","RAJAHMUNDRY","RANCHI","ROURKELA","SALEM","SANGLI","SILIGURI","SOLAPUR","SRINAGAR","SULTANPUR","SURAT","THIRUVANANTHAPURAM","THRISSUR","TIRUCHIRAPPALLI","TIRUNELVELI","TIRUPPUR","UJJAIN","VIJAYAPURA","VADODARA","VARANASI","VASAI-VIRAR CITY","VIJAYAWADA","VISAKHAPATNAM","WARANGAL,AHMEDABAD","BANGALORE","CHENNAI","DELHI","HYDERABAD","KOLKATA","MUMBAI","PUNE"]

      loc = tracker.get_slot('location')

      if loc.upper() in citylist:
        config={ "user_key":"dd6123ea663dc9965f87bcc94ef4e6be"}
        zomato = zomatopy.initialize_app(config)
        cuisine = tracker.get_slot('cuisine')
        pricerange = tracker.get_slot('pricerange')
        mailid = tracker.get_slot('email')
        location_detail=zomato.get_location(loc, 1)
        d1 = json.loads(location_detail)
        lat=d1["location_suggestions"][0]["latitude"]
        lon=d1["location_suggestions"][0]["longitude"]
        cuisines_dict={'american': 1,'chinese': 25, 'north indian': 50, 'italian': 55, 'mexican': 73, 'south indian': 85, 'thai': 95}
        results=zomato.restaurant_search("", lat, lon, str(cuisines_dict.get(cuisine)), 20)
        d = json.loads(results)
        response="Showing you top rated restaurants: \n"

        sorted_response = sorted(d.get("restaurants"), key= lambda k: float(k['restaurant']['user_rating']['aggregate_rating']), reverse=True)

        if(pricerange == '1'):
            minPrice = 0
            maxPrice = 299
        elif(pricerange == '2'):
            minPrice = 300
            maxPrice = 700
        elif(pricerange == '3'):
            minPrice = 701
            maxPrice = 100000
        elif(pricerange == '4'):
            minPrice = 0
            maxPrice = 700
        elif(pricerange == '5'):
            minPrice = 300
            maxPrice = 100000

        counter = 0

        if d['results_found'] == 0:
            response= "no results"
        else:
            for restaurantDict in sorted_response:
                restaurant = restaurantDict['restaurant']
                average_cost_for_two = restaurant['average_cost_for_two']
                aggregate_rating = restaurant['user_rating']['aggregate_rating']
                if(average_cost_for_two >= int(minPrice) and average_cost_for_two <= int(maxPrice)):
                    if(counter < 10):
                        response= response + str(counter + 1) + ". Found " + restaurant['name'] + " in " + restaurant['location']['address'] + ", average price for two people here is " + str(average_cost_for_two) +" with Zomato rating as: " + str(aggregate_rating) + "\n"
                        counter = counter + 1

                if response is None:
                    response="No restaurants found in given pricerange"

      else:
          response="We do not operate in that area yet"
          loc=None
          cuisine=None
          dispatcher.utter_message(response)
          return

# Sending Mail ##################
      with app.app_context():
        try:
          msg = Message(subject="Hey! Here is your list of restaurants..",
                     sender="upgradrestaurantbot@gmail.com",
                     recipients=[mailid])

          msg.body = response
          mail.send(msg)

          #dispatcher.utter_message("Mail Sent. Thanks")
        except Exception as e:
          return(str(e))


class CheckLocation(Action):
    def name(self):
      return 'action_location'

    def run(self, dispatcher, tracker, domain):
      citylist=["AGRA","AJMER","ALIGARH","ALLAHABAD","AMRAVATI","AMRITSAR","ASANSOL","AURANGABAD","BAREILLY","BELGAUM","BHAVNAGAR","BHIWANDI","BHOPAL","BHUBANESWAR","BIKANER","BOKARO STEEL CITY","CHANDIGARH","COIMBATORE","CUTTACK","DEHRADUN","DHANBAD","DURG-BHILAI NAGAR","DURGAPUR","ERODE","FARIDABAD","FIROZABAD","GHAZIABAD","GORAKHPUR","GULBARGA","GUNTUR","GURGAON","GUWAHATI‚ GWALIOR","HUBLI-DHARWAD","INDORE","JABALPUR","JAIPUR","JALANDHAR","JAMMU","JAMNAGAR","JAMSHEDPUR","JHANSI","JODHPUR","KANNUR","KANPUR","KAKINADA","KOCHI","KOTTAYAM","KOLHAPUR","KOLLAM","KOTA","KOZHIKODE","KURNOOL","LUCKNOW","LUDHIANA","MADURAI","MALAPPURAM","MATHURA","GOA","MANGALORE","MEERUT","MORADABAD","MYSORE","NAGPUR","NANDED","NASHIK","NELLORE","NOIDA","PALAKKAD","PATNA","PONDICHERRY","RAIPUR","RAJKOT","RAJAHMUNDRY","RANCHI","ROURKELA","SALEM","SANGLI","SILIGURI","SOLAPUR","SRINAGAR","SULTANPUR","SURAT","THIRUVANANTHAPURAM","THRISSUR","TIRUCHIRAPPALLI","TIRUNELVELI","TIRUPPUR","UJJAIN","VIJAYAPURA","VADODARA","VARANASI","VASAI-VIRAR CITY","VIJAYAWADA","VISAKHAPATNAM","WARANGAL,AHMEDABAD","BANGALORE","CHENNAI","DELHI","HYDERABAD","KOLKATA","MUMBAI","PUNE"]

      loc = tracker.get_slot('location')
      config={"user_key":"dd6123ea663dc9965f87bcc94ef4e6be"}
      zomato = zomatopy.initialize_app(config)
      response = zomato.get_city_ID(loc)
      if(response == 'invalid_city_name'):
        dispatcher.utter_message("I couldn't find any city with name "+loc + " .Can you please tell again")
        loc=None
      elif(loc.upper() not in citylist):
        dispatcher.utter_message("Sorry, we don’t operate in this city. Can you please specify some other location")
        loc=None

      return [SlotSet('location',loc)]


class Reset(Action):
    def name(self):
        return 'action_reset'

    def run(self, dispatcher, tracker, domain):
        return [SlotSet('location',None), SlotSet('pricerange',None),SlotSet('email',None), SlotSet('cuisine',None)]
