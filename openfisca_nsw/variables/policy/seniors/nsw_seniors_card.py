# -*- coding: utf-8 -*-

# This file defines variables for the modelled legislation.
# A variable is a property of an Entity such as a Person, a Household…
# See https://openfisca.org/doc/key-concepts/variables.html

# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw.entities import *
from openfisca_nsw.variables.return_type import *


class nsw_seniors_card_works_under_20hrs(Variable):
    value_type = Enum
    possible_values = ReturnType
    entity = Person
    definition_period = MONTH
    default_value = ReturnType.unknown
    label = "Whether the person works under 20 hours a week over a 12 month period"


class nsw_seniors_card_person_is_eligible(Variable):
    value_type = Enum
    possible_values = ReturnType
    entity = Person
    definition_period = MONTH
    default_value = ReturnType.unknown
    label = "Whether the person is eligible for a NSW seniors card"

    def formula(persons, period, parameters):

        calc_age = persons('age', period)
        # calc_is_permanent_nsw_resident = persons('is_permanent_nsw_resident', period)
        calc_nsw_seniors_card_works_under_20hrs = persons('nsw_seniors_card_works_under_20hrs', period)
        calc_is_nsw_resident_enum = persons('is_nsw_resident_enum', period)

        is_disqualified = (
            (calc_age < parameters(period).nsw_seniors_card.min_age)
            + (calc_is_nsw_resident_enum == calc_is_nsw_resident_enum.possible_values.no)
            + (calc_nsw_seniors_card_works_under_20hrs == calc_nsw_seniors_card_works_under_20hrs.possible_values.no)
            )

        is_qualified = (
            (calc_age >= parameters(period).nsw_seniors_card.min_age)
            * (calc_is_nsw_resident_enum == calc_is_nsw_resident_enum.possible_values.yes)
            * (calc_nsw_seniors_card_works_under_20hrs == calc_nsw_seniors_card_works_under_20hrs.possible_values.yes)
            )

        return select(
            [is_disqualified, is_qualified],
            [ReturnType.disqualified, ReturnType.qualified], default=ReturnType.unknown)
