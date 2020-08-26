# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw.entities import *
import requests
import json


class start_with_a_num(Variable):
    value_type = int
    entity = Person
    definition_period = MONTH
    label = "Number to sent to the API"
    reference = ''


class get_another_num(Variable):
    value_type = int
    entity = Person
    definition_period = MONTH
    label = "Number to sent to the API"
    reference = ''


class add_them_up(Variable):
    value_type = int
    entity = Person
    definition_period = MONTH
    label = "Gets a calculation from a REST API"
    reference = ''

    def formula(persons, period, parameters):
        headers = {
            'Content-Type': 'text/plain'
            }
        url = "http://api.mathjs.org/v4/?expr={}%2B{}".format(persons('start_with_a_num', period), persons('get_another_num', period))
        response = requests.request("GET", url, headers=headers)
        getNumber = json.loads(response.text)
        theNumber = getNumber[0]
        return int(theNumber)
