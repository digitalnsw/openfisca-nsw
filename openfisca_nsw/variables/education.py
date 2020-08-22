# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw.entities import *

from openfisca_nsw.variables.return_type import ReturnType


class is_enrolled_in_school(Variable):
    value_type = Enum
    possible_values = ReturnType
    entity = Person
    definition_period = MONTH
    default_value = ReturnType.unknown
    label = "enrolled in school (from Kindergarten to Year 12, including those who are home-schooled or enrolled in secondary school education at TAFE NSW)"


class is_enrolled_in_nsw_school(Variable):
    value_type = Enum
    possible_values = ReturnType
    entity = Person
    definition_period = MONTH
    default_value = ReturnType.unknown
    label = "The school the person is enrolled in is in NSW"
