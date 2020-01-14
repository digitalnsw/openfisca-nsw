# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw.entities import *


class coal_in_KG(Variable):
    value_type = float
    entity = Building
    definition_period = YEAR
    label = "The amount of coal consumed at the site throughout the NABERS rating period, as indicated on the NABERS Rating Report, in kg per annum"


class coal_KG_to_KWh(Variable):
    value_type = float
    entity = Building
    definition_period = YEAR
    label = "Formula for converting coal from kg to kwh"

    def formula(buildings, period, parameters):
        return ((buildings('coal_in_KG', period) * 22.1) / 3.6)


class diesel_in_litres(Variable):
    value_type = float
    entity = Building
    definition_period = YEAR
    label = "The amount of diesel comnsumed at the site throughout the NABERS rating period, as indicated on the NABERS Rating Report, in Litres per annum"


class diesel_litres_to_KWh(Variable):
    value_type = float
    entity = Building
    definition_period = YEAR
    label = "Formula for converting diesel from litres to kwh"

    def formula(buildings, period, parameters):
        return ((buildings('diesel_in_litres', period) * 38.6) / 3.6)


class gas_in_MJ(Variable):
    value_type = float
    entity = Building
    definition_period = YEAR
    label = "The amount of gas consumed at the site throughout the NABERS rating period, as indicated on the NABERS Rating Report, in MJ per annum"


class gas_MJ_to_KWh(Variable):
    value_type = float
    entity = Building
    definition_period = YEAR
    label = "Formula for converting gas from MJ to KwH"

    def formula(buildings, period, parameters):
        return ((buildings('gas_in_MJ', period) / 3.6))
