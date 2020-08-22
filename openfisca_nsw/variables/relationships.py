# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw.entities import *


class RelationshipType(Enum):
    parent = u"Parent of children in family"
    guardian = u"Parent of children in family"
    carer = u"Carer of children in family"
    respite_carer = u"Respite carer of children in family"
    short_term_carer = u"Carer providing short term placement of more than 3 months"
    unknown = u"Relationship status unknown"
    other = u"Other relationship"
    none = u"No relationship"


class relationship(Variable):
    value_type = Enum
    possible_values = RelationshipType
    default_value = RelationshipType.unknown
    entity = Person
    definition_period = MONTH
    label = "is parent of children in family"


class is_parent(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "is parent of children in family"


class is_guardian(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "is parent of children in family"


class is_carer(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "is parent of children in family"


class is_respite_carer(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "person is a respite carer"


class is_carer_providing_short_term_placement(Variable):
    value_type = bool
    entity = Person
    definition_period = MONTH
    label = "carer providing short term placement of more than 3 months"
