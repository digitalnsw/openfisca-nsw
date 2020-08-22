# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw.entities import *
from openfisca_nsw.variables.return_type import *


class is_nsw_resident_enum(Variable):
    value_type = Enum
    possible_values = ReturnType
    entity = Person
    definition_period = MONTH
    default_value = ReturnType.unknown
    label = "is a resident of New South Wales"


class is_nsw_resident(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "is a resident of New South Wales"


class is_act_resident(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "is a resident of the Australian Capital Territory"


class is_permanent_nsw_resident(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "is a permanent resident of the New South Wales"
