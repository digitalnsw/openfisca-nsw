# -*- coding: utf-8 -*-

# This file defines variables for the modelled legislation.
# A variable is a property of an Entity such as a Person, a Household…
# See https://openfisca.org/doc/key-concepts/variables.html

# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw.entities import *

from openfisca_nsw.variables.return_type import *


class creative_kids__already_issued_in_calendar_year(Variable):
    value_type = Enum
    possible_values = ReturnType
    entity = Person
    definition_period = YEAR
    set_input = set_input_dispatch_by_period
    default_value = ReturnType.unknown
    label = "Whether the child has already had an creative kids voucher this calendar year"


class creative_kids__voucher_amount(Variable):
    value_type = int
    entity = Person
    definition_period = MONTH
    label = "Calculates voucher amount for Creative Kids"

    def formula(persons, period, parameters):
        rt = persons('return_type', period)
        RT = rt.possible_values
        return (persons('creative_kids__child_meets_criteria', period) == RT.qualified) \
            * parameters(period).creative_kids.voucher


class creative_kids__child_meets_criteria(Variable):
    value_type = Enum
    possible_values = ReturnType
    entity = Person
    definition_period = MONTH
    default_value = ReturnType.unknown
    label = "child meets criteria for Creative Kids"
    reference = 'https://www.service.nsw.gov.au/campaign/creative-kids'

    def formula(persons, period, parameters):
        min_age_in_months = 12 * parameters(period).creative_kids.min_age
        max_age_in_months = 12 * parameters(period).creative_kids.max_age
        age_in_months = persons('age_in_months', period)

        calc_is_nsw_resident_enum = persons('is_nsw_resident_enum', period)
        calc_is_enrolled_in_school = persons('is_enrolled_in_school', period)
        calc_creative_kids__already_issued_in_calendar_year = persons('creative_kids__already_issued_in_calendar_year', period.this_year)
        calc_has_valid_medicare_card = persons('has_valid_medicare_card', period)

        is_disqualified = ((calc_is_nsw_resident_enum == calc_is_nsw_resident_enum.possible_values.no)
            + (calc_is_enrolled_in_school == calc_is_enrolled_in_school.possible_values.no)
            + (calc_creative_kids__already_issued_in_calendar_year == calc_creative_kids__already_issued_in_calendar_year.possible_values.yes)
            + (calc_has_valid_medicare_card == calc_has_valid_medicare_card.possible_values.no)
            + (age_in_months < min_age_in_months)
            + (age_in_months >= max_age_in_months))

        is_qualified = ((calc_is_nsw_resident_enum == calc_is_nsw_resident_enum.possible_values.yes)
            * (calc_is_enrolled_in_school == calc_is_enrolled_in_school.possible_values.yes)
            * (calc_creative_kids__already_issued_in_calendar_year == calc_creative_kids__already_issued_in_calendar_year.possible_values.no)
            * (calc_has_valid_medicare_card == calc_has_valid_medicare_card.possible_values.yes)
            * (age_in_months >= min_age_in_months)
            * (age_in_months < max_age_in_months))

        return select(
            [is_disqualified, is_qualified],
            [ReturnType.disqualified, ReturnType.qualified], default=ReturnType.unknown)


class creative_kids__is_eligible(Variable):
    value_type = Enum
    possible_values = ReturnType
    entity = Person
    definition_period = MONTH
    default_value = ReturnType.unknown
    label = "person is a parent/carer/guardian and is entitled to 1 or more Creative Kids vouchers for their family"

    def formula(persons, period, parameters):
        calc_relationship = persons('relationship', period)
        parent = (calc_relationship == calc_relationship.possible_values.parent)
        guardian = (calc_relationship == calc_relationship.possible_values.guardian)
        carer = (calc_relationship == calc_relationship.possible_values.carer)
        rel_unknown = (calc_relationship == calc_relationship.possible_values.unknown)
        return select(
            [((parent + guardian + carer) * persons.family('creative_kids__family_has_children_eligible', period)),
            (not_(persons.family('creative_kids__family_has_children_eligible', period))
            + (not_(parent) * not_(guardian) * not_(carer) * not_(rel_unknown)))],
            [ReturnType.qualified, ReturnType.disqualified],
            default=ReturnType.unknown)


class creative_kids__family_has_children_eligible(Variable):
    value_type = bool
    entity = Family
    definition_period = MONTH
    label = "family has 1 or more children eligible for Creative Kids vouchers"

    def formula(families, period, parameters):
        eligible = (families.members('creative_kids__child_meets_criteria', period) == families.members('creative_kids__child_meets_criteria', period).possible_values.qualified)
        eligible = eligible.astype('bool')
        return families.any(eligible, role=Family.CHILD)

# # -*- coding: utf-8 -*-
#
# # This file defines variables for the modelled legislation.
# # A variable is a property of an Entity such as a Person, a Household…
# # See https://openfisca.org/doc/key-concepts/variables.html
#
# # Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
# from openfisca_core.model_api import *
# # Import the Entities specifically defined for this tax and benefit system
# from openfisca_nsw.entities import *
#
#
# class creative_kids__already_issued_in_calendar_year(Variable):
#     value_type = bool
#     entity = Person
#     definition_period = YEAR
#     set_input = set_input_dispatch_by_period
#     label = "Whether the child has already had a creative kids voucher this calendar year"
#
#
# class creative_kids__voucher_amount(Variable):
#     value_type = int
#     entity = Person
#     definition_period = MONTH
#     label = "Calculates voucher amount for Creative Kids"
#
#     def formula(persons, period, parameters):
#         return (persons('creative_kids__child_meets_criteria', period)
#                 * parameters(period).creative_kids.voucher)
#
#
# class creative_kids__child_meets_criteria(Variable):
#     value_type = bool
#     entity = Person
#     definition_period = MONTH
#     label = "child meets criteria for Creative Kids"
#     reference = 'https://www.service.nsw.gov.au/campaign/creative-kids'
#
#     def formula(persons, period, parameters):
#         min_age_in_months = 12 * parameters(period).creative_kids.min_age
#         max_age_in_months = 12 * parameters(period).creative_kids.max_age
#         age_in_months = persons('age_in_months', period)
#         return (persons('is_nsw_resident', period)
#                * persons('is_enrolled_in_school', period)
#                * not_(persons('creative_kids__already_issued_in_calendar_year', period.this_year))
#                * persons('has_valid_medicare_card', period)
#                * (age_in_months >= min_age_in_months)
#                * (age_in_months < max_age_in_months))
#
#
# class creative_kids__is_eligible(Variable):
#     value_type = bool
#     entity = Person
#     definition_period = MONTH
#     label = "person is a parent/carer/guardian and is entitled to 1 or more Creative Kids vouchers for their family"
#
#     def formula(persons, period, parameters):
#         parent = persons('is_parent', period)
#         guardian = persons('is_guardian', period)
#         carer = persons('is_carer', period)
#         return (parent + guardian + carer) * persons.family('creative_kids__family_has_children_eligible', period)
#
#
# class creative_kids__family_has_children_eligible(Variable):
#     value_type = bool
#     entity = Family
#     definition_period = MONTH
#     label = "family has 1 or more children eligible for Creative Kids vouchers"
#
#     def formula(families, period, parameters):
#         eligible = families.members('creative_kids__child_meets_criteria', period)
#         return families.any(eligible, role=Family.CHILD)
