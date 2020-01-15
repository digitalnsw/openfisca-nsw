# Import from openfisca-core the common Python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the Entities specifically defined for this tax and benefit system
from openfisca_nsw.entities import *

#measured_electricity_consumption input at Step 1
#measured_gas_consumption input at Step 1
#onsite_unaccounted_electricity input at Step 1
#nabers_electricity input at Step 1
#hours_per_week_with_20_percent_occupancy input at Step 3
#net_lettable_area input at Step 3
#building_area_type input at Step 3

#coal_in_KG input in unit_conversions
#coal_KG_to_kWh input in unit_conversions
#diesel_in_L input in unit_conversions
#diesel_in_kWh KG input in unit_conversions
#gas_in_MJ input in unit_conversions
#gas_MJ_to_kWh input in unit_conversions

# add from filename import function to init.py


class benchmark_star_rating(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY #need to check whether these inputs, on the NABERS reports, should all be year
    label = "The star rating for which the benchmark electricity and gas consumption is calculated against - what NABERS rating the building aims to achieve"


class number_of_computers(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "The number of computers registered as used within the NABERS rating"


class building_state_location(Variable):
	value_type = float
	entity = Building
	definition_period = ETERNITY
	label = "State within which the relevant NABERS rated building is located."


class nabers_adjusted_hours(Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "NABERS adjusted hours of building operations"

    def formula(buildings, period, parameters):
        input_hours = buildings('hours_per_week_with_20_percent_occupancy', period)
        return input_hours + 10


class elec_kWh (Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "The electricity consumption of the building, in kWh, as detailed on the NABERS report"


class gas_kWh (Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "The gas consumption of the building, in kWh, as detailed on the NABERS report"


class oil_kWh (Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "The oil consumption of the building, in kWh, as detailed on the NABERS report"


class coal_kWh (Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "The coal consumption of the building, in kWh, as detailed on the NABERS report"


class total_energy_kwh (Variable):
	value_type = float
	entity = Building
	definition_period = ETERNITY
	label = "The total kWh consumption of the building, summing electricity, gas, oil and diesel, expressed in kWh"

	def formula (buildings, period, parameters):
		return elec_kWh + gas_kWh + oil_kWh + coal_kWh


class perc_elec_kwh (Variable):
	value_type = float
	entity = Building
	definition_period = ETERNITY
	label = "The percentage of a building's energy consumption that is derived from its electricity consumption, expressed as a percentage of total energy use to 2 decimal places"

	def formula (buildings, period, parameters):
		return elec_kWh/total_energy_kwh * 100 #need to learn how to express this as a percentage


class perc_gas_kwh (Variable):
	value_type = float
	entity = Building
	definition_period = ETERNITY
	label = "The percentage of a building's energy consumption that is derived from its electricity consumption, expressed as a percentage of total energy use to 2 decimal places"

	def formula (buildings, period, parameters):
		return gas_kWh/total_energy_kwh * 100 #need to learn how to express this as a percentage


class perc_diesel_kwh (Variable):
	value_type = float
	entity = Building
	definition_period = ETERNITY
	label = "The percentage of a building's energy consumption that is derived from its diesel consumption, expressed as a percentage of total energy use to 2 decimal places"

	def formula (buildings, period, parameters):
		return diesel_kWh/total_energy_kwh * 100 #need to learn how to express this as a percentage


class perc_oil_kwh (Variable):
	value_type = float
	entity = Building
	definition_period = ETERNITY
	label = "The percentage of a building's energy consumption that is derived from its oil consumption, expressed as a percentage of total energy use to 2 decimal places"

	def formula (buildings, period, parameters):
		return oil_kWh/total_energy_kwh * 100 #need to learn how to express this as a percentage


class maximum_nabers_adjusted_hours(Variable):
	value_type = float
	entity = Building
	definition_period = ETERNITY
	label = "Maximum allowable NABERS adjusted hours of building operations - maximum number of hours in week is 168"

	def formula(buildings, period, parameters):
		condition_maximum_hours = buildings('nabers_adjusted_hours', period) > 168
		return where(condition_maximum_hours, 168, 'nabers_adjusted_hours')


class f_base_building(Variable):
	value_type = float
	entity = Building
	definition_period = ETERNITY
	label = "factor for base building NABERS calculation"

	def formula (buildings, period, parameters):
		adjusted_hours = buildings('maximum_nabers_adjusted_hours, period')
		return (1 / (0.38 + 0.0116 + 'adjusted hours'))


class SGEgas (Variable):
	value_type = float
	entity = Building
	definition_period = ETERNITY
	label = 'specific greenhouse emissions for gas for the relevant state'

	def formula (buildings, period, parameters):
		state = buildings(building_state_location, period)
		return select(
		[state == "ACT", state == "NSW", state == "NT", state == "QLD", state == "TAS", state == "VIC", state == "WA",],
		[0.23, 0.23, 0.20, 0.20, 0.21, 0.75, 0.21, 0.22] #need to check these numbers, don't think they're right
		)


class SGEelec (Variable):
	value_type = float
	entity = Building
	definition_period = ETERNITY
	label = 'specific greenhouse emissions for electricity for the relevant state'

	def formula (buildings, period, parameters):
		state = buildings(building_state_location, period)
		return select(
		[state == "ACT", state == "NSW", state == "NT", state == "QLD", state == "TAS", state == "VIC", state == "WA",],
		[0.94, 0.94, 0.69, 1.02, 0.95, 1, 1.34, 0.92]
		)


class SGEcoal (Variable):
	value_type = float
	entity = Building
	definition_period = ETERNITY
	label = 'specific greenhouse emissions for coal for the relevant state'

	def formula (buildings, period, parameters):
		state = buildings(building_state_location, period)
		return select(
		[state == "ACT", state == "NSW", state == "NT", state == "QLD", state == "TAS", state == "VIC", state == "WA",],
		[0.32, 0.32, 0.32, 0.32, 0.32, 0.7, 0.32, 0.32]
		)


class SGEoil (Variable):
	value_type = float
	entity = Building
	definition_period = ETERNITY
	label = 'specific greenhouse emissions for oil for the relevant state'

	def formula (buildings, period, parameters):
		state = buildings(building_state_location, period)
		return select(
		[state == "ACT", state == "NSW", state == "NT", state == "QLD", state == "TAS", state == "VIC", state == "WA",],
		[0.27, 0.27, 0.27, 0.27, 0.27, 0.75, 0.27, 0.27]
		)


class term_1 (Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "Term 1used in the calculation of GEclimcorr"

    def formula (buildings, period, parameters):
        SGEgas = buildings('SGEgas', period)
        return 4.12 * SGEgas


class term_2 (Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "Term 2 used in the calculation of GEclimcorr"

    def formula (buildings, period, parameters):
        SGEelec = buildings('SGEelec', period)
        return 43.6 * SGEelec


class term_3 (Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "Term 3 used in the calculation of GEclimcorr"

    def formula (buildings, period, parameters):
        SGEgas = buildings('SGEelec', period)
        HDD18 = buildings('HDD18', period)
        return (0.0016 * SGEgas * (HDD18/0.23)) #0.23 is likely SGEgas but need to check


class term_4 (Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "Term 4 used in the calculation of GEclimcorr"

    def formula (buildings, period, parameters):
        SGEelec = buildings('SGEelec', period)
        CDD15wb = buildings('CDD15wb', period)
        return (0.091 * SGEelec * (CDD15wb/0.94)) #0.94 is likely SGEelec but need to check


class term_5 (Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "Term5 used in calculating GEclimcorr"

    def formula (buildings, period, parameters):
        SGEelec = buildings('SGEelec', period)
        CDD15wb = buildings('CDD15wb', period)
        return (0.062 * SGEelec * (CDD15wb/0.94)) #0.94 is likely SGEelec but need to check


class SGE_tenancy (Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "Specific greenhouse emissions related to tenancy of a building"

    def formula (buildings, period, parameters):
        return SGEgas #want to show that SGE_tenancy and SGEgas, while being identical values, are distinct parts of formulas within the calc


class Dequip (Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "Dequip value used to weigh impact of number of computers"

    def formula (buildings, period, parameters):
        return number_of_computers * 0.2 / net_lettable_area #need to define no_of_computer and NLA here?


class GEclimcorr (Variable):
    value_type = float
    entity = Building
    definition_period = ETERNITY
    label = "climate corrected greenhouse emissions for the relevant NABERS building" #check this

    def formula (buildings, period, parameters):
        Term1 = buildings('term_1', period)
        Term2 = buildings('term_2', period)
        Term3 = buildings('term_3', period)
        Term4 = buildings('term_4', period)
        Term5 = buildings('term_5', period)
        return Term1 + Term2 + Term3 + Term4 + Term5
