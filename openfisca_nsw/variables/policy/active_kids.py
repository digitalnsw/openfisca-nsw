# -*- coding: utf-8 -*-

# This file defines variables for the modelled legislation.
# A variable is a property of an Entity such as a Person, a Household…
# See https://openfisca.org/doc/key-concepts/variables.html

# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw.entities import *

from openfisca_nsw.variables.return_type import ReturnType


class active_kids__already_issued_in_calendar_year(Variable):
    value_type = bool
    entity = Person
    definition_period = YEAR
    set_input = set_input_dispatch_by_period
    label = "Whether the child has already had an active kids voucher this calendar year"


class active_kids__voucher_amount(Variable):
    value_type = int
    entity = Person
    definition_period = MONTH
    label = "Calculates voucher amount for Active Kids"

    def formula(persons, period, parameters):
        return persons('active_kids__child_meets_criteria', period) \
            * parameters(period).active_kids.voucher


class active_kids__child_meets_criteria(Variable):
    value_type = Enum
    possible_values = ReturnType
    entity = Person
    definition_period = MONTH
    default_value = ReturnType.unknown
    label = "child meets criteria for Active Kids"
    reference = 'https://sport.nsw.gov.au/sectordevelopment/activekids'

    def formula(persons, period, parameters):
        rt = persons('return_type', period)
        RT = rt.possible_values
        min_age_in_months = 12 * parameters(period).active_kids.min_age
        max_age_in_months = 12 * parameters(period).active_kids.max_age
        age_in_months = persons('age_in_months', period)

        return select(
            [(persons('is_nsw_resident', period)
            * persons('is_enrolled_in_school', period)
            * not_(persons('active_kids__already_issued_in_calendar_year', period.this_year))
            * persons('has_valid_medicare_card', period)
            * (age_in_months >= min_age_in_months) * (age_in_months < max_age_in_months)),
            (not_(persons('is_nsw_resident', period))
            * not_(persons('is_enrolled_in_school', period))
            * (persons('active_kids__already_issued_in_calendar_year', period.this_year))
            * not_(persons('has_valid_medicare_card', period))
            * not_(age_in_months >= min_age_in_months) * (age_in_months < max_age_in_months))],
            [RT.qualified, RT.disqualified])


class active_kids__is_eligible(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "person is a parent/carer/guardian and is entitled to 1 or more Active Kids vouchers for their family"

    def formula(persons, period, parameters):
        parent = persons('is_parent', period)
        guardian = persons('is_guardian', period)
        carer = persons('is_carer', period)
        return (parent + guardian + carer) * persons.family('active_kids__family_has_children_eligible', period)


class active_kids__family_has_children_eligible(Variable):
    value_type = bool
    entity = Family
    definition_period = MONTH
    label = "family has 1 or more children eligible for Active Kids vouchers"

    def formula(families, period, parameters):
        eligible = families.members('active_kids__child_meets_criteria', period)
        return families.any(eligible, role=Family.CHILD)
