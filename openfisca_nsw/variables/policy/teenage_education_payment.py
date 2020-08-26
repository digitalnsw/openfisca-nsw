# -*- coding: utf-8 -*-

# This file defines variables for the modelled legislation.
# A variable is a property of an Entity such as a Person, a Household…
# See https://openfisca.org/doc/key-concepts/variables.html

# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw.entities import *


# This is used to calculate whether the youth is eligible for Teenage Education Payment
class teenage_education_payments__youth_meets_payment_criteria(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Youth meets criteria for Teenage Education Payment"
    reference = 'https://www.facs.nsw.gov.au/__data/assets/pdf_file/0004/319954/teenage_education_payment_guidelines.pdf'

    def formula(persons, period, parameters):
        age = persons('age', period)

        return (
            ((age >= parameters(period).teenage_education_payment.min_age) * (age <= parameters(period).teenage_education_payment.upper_age))
            + ((age == parameters(period).teenage_education_payment.max_age) * persons('teenage_education_payments__turned_18_this_school_year', period))
            )


# This is used to calculate whether persons over 17 are still eligible for Teenage Education Payment
class teenage_education_payments__turned_18_this_school_year(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "Youth turned 18 this school year"


class teenage_education_payments__adult_meets_payment_criteria (Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "person is a carer / short-term carer / guardian who is entitled to the Teenage Education Payment"

    def formula(persons, period, parameters):
        return (
            (persons('is_carer', period) + persons('is_guardian', period) + persons('is_carer_providing_short_term_placement', period))
            * not_(persons('is_respite_carer', period))
            * persons('teenage_education_payments__is_family_tax_benefit_recipient_partA_youth15', period)
            )


class teenage_education_payments__is_family_tax_benefit_recipient_partA_youth15 (Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "carer or guardian received Family Tax Benefit part A when young person was 15 years old"


class teenage_education_payments__amount (Variable):
    value_type = int
    entity = Person
    definition_period = MONTH
    label = "Teenage Education Paymnent amount"

    def formula(persons, period, parameters):
        return select(
            [(persons('teenage_education_payments__adult_meets_payment_criteria', period) * persons.family('teenage_education_payments__family_has_children_eligible', period)), not_(persons('teenage_education_payments__adult_meets_payment_criteria', period) * persons.family('teenage_education_payments__family_has_children_eligible', period))],
            [parameters(period).teenage_education_payment.amount, 0]
            )


class teenage_education_payments__family_has_children_eligible(Variable):
    value_type = bool
    entity = Family
    definition_period = MONTH
    label = "family has 1 or more children and adults who meet the criteria for Teenage Education Payments AND one ofthe NSW criteria is met"

    def formula(families, period, parameters):
        return (
            families.any(families.members('teenage_education_payments__youth_meets_payment_criteria', period), role=Family.CHILD)
            * (
                families.any(families.members('is_enrolled_in_nsw_school', period), role=Family.CHILD)
                + families.any(families.members('is_nsw_resident', period), role=Family.PARENT)
                )
            )


class teenage_education_payments__is_eligible(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "child meets criteria and person is a carer/guardian and is entitled to teenage education payment"

    def formula(persons, period, parameters):
        return (
            persons('teenage_education_payments__adult_meets_payment_criteria', period)
            * persons.family('teenage_education_payments__family_has_children_eligible', period)
            )
