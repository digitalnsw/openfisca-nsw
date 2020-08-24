# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw.entities import *
from openfisca_nsw.variables.return_type import *


class has_any_seniors_card(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Holds a pensioner concession card from any Australian state or territory."

    def formula(persons, period, parameters):
        return (
            persons('has_nsw_seniors_card', period)
            + persons('has_act_seniors_card', period)
            + persons('has_nt_seniors_card', period)
            + persons('has_qld_seniors_card', period)
            + persons('has_sa_seniors_card', period)
            + persons('has_tas_seniors_card', period)
            + persons('has_vic_seniors_card', period)
            + persons('has_wa_seniors_card', period)
            )


class has_nsw_seniors_card(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Holds a pensioner concession card from New South Wales."


class has_act_seniors_card(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Holds a pensioner concession card from the Australian Capital Territory."


class has_nt_seniors_card(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Holds a pensioner concession card from the Northern Territory."


class has_qld_seniors_card(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Holds a pensioner concession card from Queensland."


class has_sa_seniors_card(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Holds a pensioner concession card from South Australia."


class has_tas_seniors_card(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Holds a pensioner concession card from Tasmania."


class has_vic_seniors_card(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Holds a pensioner concession card from Victoria."


class has_wa_seniors_card(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Holds a pensioner concession card from Western Australia."


class has_any_seniors_card_enum(Variable):
    value_type = Enum
    possible_values = ReturnType
    entity = Person
    definition_period = MONTH
    default_value = ReturnType.unknown
    label = "Holds a pensioner concession card from any Australian state or territory."

    def formula(persons, period, parameters):

        has_nsw_seniors_card_enum = persons('has_nsw_seniors_card_enum', period)
        has_nt_seniors_card_enum = persons('has_nt_seniors_card_enum', period)
        has_act_seniors_card_enum = persons('has_act_seniors_card_enum', period)
        has_qld_seniors_card_enum = persons('has_qld_seniors_card_enum', period)
        has_sa_seniors_card_enum = persons('has_sa_seniors_card_enum', period)
        has_tas_seniors_card_enum = persons('has_tas_seniors_card_enum', period)
        has_vic_seniors_card_enum = persons('has_vic_seniors_card_enum', period)
        has_wa_seniors_card_enum = persons('has_wa_seniors_card_enum', period)

        is_disqualified = (
            (has_nsw_seniors_card_enum == has_nsw_seniors_card_enum.possible_values.no)
            * (has_act_seniors_card_enum == has_act_seniors_card_enum.possible_values.no)
            * (has_nt_seniors_card_enum == has_nt_seniors_card_enum.possible_values.no)
            * (has_qld_seniors_card_enum == has_qld_seniors_card_enum.possible_values.no)
            * (has_sa_seniors_card_enum == has_sa_seniors_card_enum.possible_values.no)
            * (has_tas_seniors_card_enum == has_tas_seniors_card_enum.possible_values.no)
            * (has_vic_seniors_card_enum == has_vic_seniors_card_enum.possible_values.no)
            * (has_wa_seniors_card_enum == has_wa_seniors_card_enum.possible_values.no)
            )

        is_qualified = (
            (has_nsw_seniors_card_enum == has_nsw_seniors_card_enum.possible_values.yes)
            + (has_act_seniors_card_enum == has_act_seniors_card_enum.possible_values.yes)
            + (has_nt_seniors_card_enum == has_nt_seniors_card_enum.possible_values.yes)
            + (has_qld_seniors_card_enum == has_qld_seniors_card_enum.possible_values.yes)
            + (has_sa_seniors_card_enum == has_sa_seniors_card_enum.possible_values.yes)
            + (has_tas_seniors_card_enum == has_tas_seniors_card_enum.possible_values.yes)
            + (has_vic_seniors_card_enum == has_vic_seniors_card_enum.possible_values.yes)
            + (has_wa_seniors_card_enum == has_wa_seniors_card_enum.possible_values.yes)
            )

        return select(
            [is_disqualified, is_qualified],
            [ReturnType.no, ReturnType.yes], default=ReturnType.unknown)


class has_nsw_seniors_card_enum(Variable):
    value_type = Enum
    possible_values = ReturnType
    entity = Person
    definition_period = MONTH
    default_value = ReturnType.unknown
    label = "Holds a pensioner concession card from New South Wales."

    def formula(persons, period, parameters):

        nsw_seniors_card_person_is_eligible = persons('nsw_seniors_card_person_is_eligible', period)

        is_disqualified = (
            (nsw_seniors_card_person_is_eligible == nsw_seniors_card_person_is_eligible.possible_values.no)
            )

        is_qualified = (
            (nsw_seniors_card_person_is_eligible == nsw_seniors_card_person_is_eligible.possible_values.yes)
            )

        return select(
            [is_disqualified, is_qualified],
            [ReturnType.no, ReturnType.yes], default=ReturnType.unknown)


class has_act_seniors_card_enum(Variable):
    value_type = Enum
    possible_values = ReturnType
    entity = Person
    definition_period = MONTH
    default_value = ReturnType.unknown
    label = "Holds a pensioner concession card from the Australian Capital Territory."

    def formula(persons, period, parameters):

        calc_age = persons('age', period)

        is_disqualified = (
            (calc_age < parameters(period).seniors_cards.act_min_age)
            )

        is_qualified = (
            (calc_age >= parameters(period).seniors_cards.act_min_age)
            )

        return select(
            [is_disqualified, is_qualified],
            [ReturnType.disqualified, ReturnType.qualified], default=ReturnType.unknown)


class has_nt_seniors_card_enum(Variable):
    value_type = Enum
    possible_values = ReturnType
    entity = Person
    definition_period = MONTH
    default_value = ReturnType.unknown
    label = "Holds a pensioner concession card from the Northern Territory."

    def formula(persons, period, parameters):

        calc_age = persons('age', period)

        is_disqualified = (
            (calc_age < parameters(period).seniors_cards.nt_min_age)
            )

        is_qualified = (
            (calc_age >= parameters(period).seniors_cards.nt_min_age)
            )

        return select(
            [is_disqualified, is_qualified],
            [ReturnType.disqualified, ReturnType.qualified], default=ReturnType.unknown)


class has_qld_seniors_card_enum(Variable):
    value_type = Enum
    possible_values = ReturnType
    entity = Person
    definition_period = MONTH
    default_value = ReturnType.unknown
    label = "Holds a pensioner concession card from Queensland."

    def formula(persons, period, parameters):

        calc_age = persons('age', period)

        is_disqualified = (
            (calc_age < parameters(period).seniors_cards.qld_min_age)
            )

        is_qualified = (
            (calc_age >= parameters(period).seniors_cards.qld_min_age)
            )

        return select(
            [is_disqualified, is_qualified],
            [ReturnType.disqualified, ReturnType.qualified], default=ReturnType.unknown)


class has_sa_seniors_card_enum(Variable):
    value_type = Enum
    possible_values = ReturnType
    entity = Person
    definition_period = MONTH
    default_value = ReturnType.unknown
    label = "Holds a pensioner concession card from South Australia."

    def formula(persons, period, parameters):

        calc_age = persons('age', period)

        is_disqualified = (
            (calc_age < parameters(period).seniors_cards.sa_min_age)
            )

        is_qualified = (
            (calc_age >= parameters(period).seniors_cards.sa_min_age)
            )

        return select(
            [is_disqualified, is_qualified],
            [ReturnType.disqualified, ReturnType.qualified], default=ReturnType.unknown)


class has_tas_seniors_card_enum(Variable):
    value_type = Enum
    possible_values = ReturnType
    entity = Person
    definition_period = MONTH
    default_value = ReturnType.unknown
    label = "Holds a pensioner concession card from Tasmania."

    def formula(persons, period, parameters):

        calc_age = persons('age', period)

        is_disqualified = (
            (calc_age < parameters(period).seniors_cards.tas_min_age)
            )

        is_qualified = (
            (calc_age >= parameters(period).seniors_cards.tas_min_age)
            )

        return select(
            [is_disqualified, is_qualified],
            [ReturnType.disqualified, ReturnType.qualified], default=ReturnType.unknown)


class has_vic_seniors_card_enum(Variable):
    value_type = Enum
    possible_values = ReturnType
    entity = Person
    definition_period = MONTH
    default_value = ReturnType.unknown
    label = "Holds a pensioner concession card from Victoria."

    def formula(persons, period, parameters):

        calc_age = persons('age', period)

        is_disqualified = (
            (calc_age < parameters(period).seniors_cards.vic_min_age)
            )

        is_qualified = (
            (calc_age >= parameters(period).seniors_cards.vic_min_age)
            )

        return select(
            [is_disqualified, is_qualified],
            [ReturnType.disqualified, ReturnType.qualified], default=ReturnType.unknown)


class has_wa_seniors_card_enum(Variable):
    value_type = Enum
    possible_values = ReturnType
    entity = Person
    definition_period = MONTH
    default_value = ReturnType.unknown
    label = "Holds a pensioner concession card from Western Australia."

    def formula(persons, period, parameters):

        calc_age = persons('age', period)

        is_disqualified = (
            (calc_age < parameters(period).seniors_cards.wa_min_age)
            )

        is_qualified = (
            (calc_age >= parameters(period).seniors_cards.wa_min_age)
            )

        return select(
            [is_disqualified, is_qualified],
            [ReturnType.disqualified, ReturnType.qualified], default=ReturnType.unknown)
