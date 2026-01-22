from .get_tire_index import get_tire_index
from .get_compound_from_index import get_compound_from_index
from .get_tire_mgmt import get_tire_mgmt

def get_tire_compound(tire, data):
  index = get_tire_index(tire)

  compound_index = data['wheelInfo']['wheelLocs'][index]['compound']

  return get_compound_from_index(compound_index)
