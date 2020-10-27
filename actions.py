# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"
import re
from typing import Any, Text, Dict, List, Union
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.forms import FormAction
from rasa_sdk import Action, Tracker
from database_connectivity import DataUpdate


# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
class ActionCustomFallback(Action):

    def name(self) -> Text:
        return "action_custom_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_template('utter_custom', tracker)
        return [UserUtteranceReverted()]

class ActionEnquiryForm(FormAction):
    def name(self) -> Text:
        return "admission_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """
        A list of required slots that form has to fill
        :param tracker:
        :return:
        """
        return ["name", "contact", "email", "pcm", "cet", "jee"]

    def slot_mappings(self):
        """
        Extract Slot value from the response
        :return:
        """
        return {
            "name": [self.from_entity(entity="name", intent="name"), self.from_text()],
            "contact": [self.from_entity(entity="contact", intent="contact_number"), self.from_text()],
            "email": [self.from_entity(entity="email", intent="email"), self.from_text()],
            "pcm": [self.from_entity(entity="pcm", intent="pcm_score"), self.from_text()],
            "cet": [self.from_entity(entity="cet", intent="cet_score"), self.from_text()],
            "jee": [self.from_entity(entity="jee", intent="jee_score"), self.from_text()],
        }

    def validate_name(self,
                      value: Text,
                      dispatcher: CollectingDispatcher,
                      tracker: Tracker,
                      domain: Dict[Text, Any], ) -> Dict[Text, Any]:

        if re.fullmatch('[A-Za-z]{2,25}( [A-Za-z]{2,25})?', value):
            return {"name": value}
        else:
            dispatcher.utter_message(template="utter_wrong_name")
            return {"name": None}

    def validate_contact(self,
                         value: Text,
                         dispatcher: CollectingDispatcher,
                         tracker: Tracker,
                         domain: Dict[Text, Any], ) -> Dict[Text, Any]:

        if value.isnumeric() and len(value) == 10:
            return {"contact": value}
        else:
            dispatcher.utter_message(template="utter_wrong_contact")
            return {"contact": None}

    def validate_email(self,
                       value: Text,
                       dispatcher: CollectingDispatcher,
                       tracker: Tracker,
                       domain: Dict[Text, Any], ) -> Dict[Text, Any]:
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if (re.search(regex, value)):
            return {"email": value}
        else:
            dispatcher.utter_message(template="utter_wrong_email")
            return {"email": None}

    def validate_pcm(self,
                     value: Text,
                     dispatcher: CollectingDispatcher,
                     tracker: Tracker,
                     domain: Dict[Text, Any], ) -> Dict[Text, Any]:

        if value.isnumeric() and int(value) <= 300:
            return {"pcm": value}
        else:
            dispatcher.utter_message(template="utter_wrong_pcm")
            return {"pcm": None}

    def validate_cet(self,
                     value: Text,
                     dispatcher: CollectingDispatcher,
                     tracker: Tracker,
                     domain: Dict[Text, Any], ) -> Dict[Text, Any]:

        if (value.isnumeric() and int(value) <= 100) or value == "NA":
            return {"cet": value}
        else:
            dispatcher.utter_message(template="utter_wrong_cet")
            return {"cet": None}

    def validate_jee(self,
                     value: Text,
                     dispatcher: CollectingDispatcher,
                     tracker: Tracker,
                     domain: Dict[Text, Any], ) -> Dict[Text, Any]:

        if (float(value) <= 100) or value == "NA":
            return {"jee": value}
        else:
            dispatcher.utter_message(template="utter_wrong_jee")
            return {"jee": None}

    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any],
               ) -> List[Dict]:
        dispatcher.utter_message(template="utter_submit",
                                 name=tracker.get_slot("name"),
                                 contact=tracker.get_slot("contact"),
                                 email=tracker.get_slot("email"),
                                 pcm=tracker.get_slot("pcm"),
                                 cet=tracker.get_slot("cet"),
                                 jee=tracker.get_slot("jee"))
        DataUpdate(tracker.get_slot("name"), tracker.get_slot("contact"), tracker.get_slot("email"),
                   tracker.get_slot("pcm"), tracker.get_slot("cet"), tracker.get_slot("jee"))
        return []
