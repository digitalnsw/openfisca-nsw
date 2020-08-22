# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw.entities import *


class ReturnType(Enum):
    qualified = u"You are eligible for this"
    disqualified = u"You are not eligible for this"
    unknown = u"Based on what we know, you may be eligible for this"


class return_type(Variable):
    value_type = Enum
    possible_values = ReturnType
    default_value = ReturnType.unknown
    entity = Person
    definition_period = ETERNITY
    label = u""
    reference = 'Active Kids'
