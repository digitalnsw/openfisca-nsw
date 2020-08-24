# -*- coding: utf-8 -*-

# This file defines variables for the modelled legislation.
# A variable is a property of an Entity such as a Person, a Household…
# See https://openfisca.org/doc/key-concepts/variables.html

# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw.entities import *
from openfisca_nsw.variables.return_type import *


class gold_seniors_opal_person_is_eligible(Variable):
    value_type = Enum
    possible_values = ReturnType
    entity = Person
    default_value = ReturnType.unknown
    definition_period = ETERNITY
    label = "Person is eligible for Gold Pensioners' Opal Card"

    def formula(persons, period, parameters):

        is_disqualified = (
            (persons('nsw_seniors_card_person_is_eligible', period) == persons('nsw_seniors_card_person_is_eligible', period).possible_values.no)
            * (persons('has_nsw_seniors_card_enum', period) == persons('has_nsw_seniors_card_enum', period).possible_values.no)
            * (persons('has_act_seniors_card_enum', period) == persons('has_act_seniors_card_enum', period).possible_values.no)
            )

        is_qualified = (
            (
                (persons('nsw_seniors_card_person_is_eligible', period) == persons('nsw_seniors_card_person_is_eligible', period).possible_values.yes)
                * (persons('has_nsw_seniors_card_enum', period) == persons('has_nsw_seniors_card_enum', period).possible_values.yes)
                )
            + (persons('has_nsw_seniors_card_enum', period) == persons('has_nsw_seniors_card_enum', period).possible_values.yes)
            + (persons('has_act_seniors_card_enum', period) == persons('has_act_seniors_card_enum', period).possible_values.yes)
            )

        return select(
            [is_disqualified, is_qualified],
            [ReturnType.disqualified, ReturnType.qualified], default=ReturnType.unknown)
