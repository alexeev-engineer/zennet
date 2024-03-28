"""Returns the address based on the passed coordinates. The coordinates
must be transmitted as a list. That is, take into account the
possibility of the user passing it to the script as a 
comma-separated list, but to send it to the function it is necessary
to form a list.
"""
from geopy.geocoders import Nominatim


def get_addr(location=None) -> (str, bool):
	"""Get address by coordinates.

	Arguments:
	---------
	localion=None - coordinates

	Return:
	------
	(str, bool)
	
	"""
	if location is None:
		return
	try:
		return Nominatim(user_agent="GetLoc").reverse(location).address
	except Exception:
		return
