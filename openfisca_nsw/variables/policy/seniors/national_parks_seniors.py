# -*- coding: utf-8 -*-

# This file defines variables for the modelled legislation.
# A variable is a property of an Entity such as a Person, a Household…
# See https://openfisca.org/doc/key-concepts/variables.html

# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw.entities import *
from openfisca_nsw.variables.return_type import *


class national_parks_seniors_person_is_eligible(Variable):
    value_type = Enum
    possible_values = ReturnType
    entity = Person
    default_value = ReturnType.unknown
    definition_period = MONTH
    label = "Whether the person is eligible for seniors' discount annual park passes at approx 20% discount. https://www.nationalparks.nsw.gov.au/passes-and-fees/discount-and-concession-passes#seniors-discount-annual-park-passes"

    def formula(persons, period, parameters):
        calc_any_card = persons('has_any_seniors_card_enum', period)

        is_disqualified = (
            (calc_any_card == calc_any_card.possible_values.no)
            + (calc_any_card == calc_any_card.possible_values.disqualified)
            )

        is_qualified = (
            (calc_any_card == calc_any_card.possible_values.yes)
            )

        return select(
            [is_disqualified, is_qualified],
            [ReturnType.disqualified, ReturnType.qualified], default=ReturnType.unknown)
