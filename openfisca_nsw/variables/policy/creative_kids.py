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
