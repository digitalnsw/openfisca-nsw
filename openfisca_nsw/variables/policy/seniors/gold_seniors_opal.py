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
        calc_nsw_eligible = persons('nsw_seniors_card_person_is_eligible', period)
        calc_has_nsw_seniors = persons('has_nsw_seniors_card_enum', period)
        calc_has_act_seniors = persons('has_act_seniors_card_enum', period)

        is_disqualified = (
            (calc_nsw_eligible == calc_nsw_eligible.possible_values.no)
            * (calc_has_nsw_seniors == calc_has_nsw_seniors.possible_values.no)
            * (calc_has_act_seniors == calc_has_act_seniors.possible_values.no)
            )

        is_disqualified_by_default = (
            (calc_nsw_eligible == calc_nsw_eligible.possible_values.disqualified)
            * (calc_has_nsw_seniors == calc_has_nsw_seniors.possible_values.disqualified)
            * (calc_has_act_seniors == calc_has_act_seniors.possible_values.disqualified)
            )

        is_qualified = (
            (
                (calc_nsw_eligible == calc_nsw_eligible.possible_values.yes)
                * (calc_has_nsw_seniors == calc_has_nsw_seniors.possible_values.yes)
                )
            + (calc_has_nsw_seniors == calc_has_nsw_seniors.possible_values.yes)
            + (calc_has_act_seniors == calc_has_act_seniors.possible_values.yes)
            )

        return select(
            [is_disqualified, is_disqualified_by_default, is_qualified],
            [ReturnType.disqualified, ReturnType.disqualified, ReturnType.qualified], default=ReturnType.unknown)
