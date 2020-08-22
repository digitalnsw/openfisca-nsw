# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw.entities import *


class ReturnType(Enum):
    qualified = u"All criteria met"
    disqualified = u"At least 1 criteria not met"
    unknown = u"Calculation incomplete, or variable not asked"
    yes = u"Variable confirmed as positive/true"
    no = u"Variable confirmed as negative/false"
    ignored = u"Variable answer declined or ignored"


class return_type(Variable):
    value_type = Enum
    possible_values = ReturnType
    default_value = ReturnType.unknown
    entity = Person
    definition_period = ETERNITY
    label = u""
    reference = 'Status for calculations'
