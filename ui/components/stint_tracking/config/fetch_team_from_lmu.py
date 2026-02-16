from core.errors import log, log_exception
import requests

"""
fetch_team_from_lmu.py

Fetches team and driver information from LMU shared memory.
"""

def fetch_team_from_lmu():
    """
    Fetch team and driver information from LMU shared memory.
    Returns:
        dict: Team info with driver names, or None if unavailable.
    """
    try:
        url = "http://localhost:6397/rest/garage/UIScreen/TireManagement"
        headers = {
            "accept": "application/json",
        }

        response = requests.get(url, headers=headers, timeout=2)
        response.raise_for_status()

        log('DEBUG', 'Successfully retrieved tire management data',
            category='config_options', action='get_tire_management_data')
        res_json = response.json()
        driver_names = res_json.get('teamInfo', {}).get('driverNames', [])
        decoded_names = []
        for name_bytes in driver_names:
            # Convert list of ints to bytes, then decode, strip nulls and whitespace
            if isinstance(name_bytes, list):
                name = bytes(name_bytes).decode('utf-8', errors='ignore').rstrip('\x00').strip()
                decoded_names.append(name)
            else:
                decoded_names.append(str(name_bytes))
        print("Decoded Driver Names:", decoded_names)
        return decoded_names

        
    except requests.RequestException as e:
        log('WARNING', f'Failed to retrieve tire management data: {str(e)}',
            category='config_options', action='get_tire_management_data')
        return None
    except Exception as e:
        log_exception(e, 'Unexpected error retrieving tire management data',
                     category='config_options', action='get_tire_management_data')
