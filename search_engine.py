VERSION = 2.6

#=============================== IMPORTS ZONE ===============================
import requests
import debug_sys
from fuzzywuzzy import fuzz


#=============================== CHECKING ZONE ===============================
if debug_sys.VERSION != 2.2 :
    raise Exception(f'Incorrect version of the "debug_sys" python library, the current version is {debug_sys.VERSION} but the expected version is 2.2.')


#=============================== INIT ZONE ===============================
API_URL = "https://api-pokemon-fr.vercel.app/api/v1/pokemon"
API_HEADER = {
    "User-Agent": "RobotPokemon",
    "From": "adresse[at]domaine[dot]com",
    'Content-type': 'application/json'
}
LANGUAGE_SUPPORT = ["fr", "en", "jp", "all"]
# Network usage mode
ECO : bool = True
TMP = requests.get(API_URL, API_HEADER)

#=============================== MAIN ZONE ===============================
def search(input : str, language : str, url : str = API_URL, headers : str = API_HEADER, p : int = 50)-> list[int]:
    """
    This function searches for a Pokemon based on the input string and language.
    
    Parameters:
    input (str): The name of the Pokemon to search for.
    language (str): The language of the Pokemon name.
    url (str): The URL of the Pokemon API. Default is API_URL.
    headers (str): The headers to use for the API request. Default is API_HEADER.
    p (int): The minimum similarity ratio for the fuzzy search. Default is 50.
    
    Returns:
    list[int]: A list of Pokemon IDs sorted by similarity ratio in descending order.
    """
    # Checking the validity of arguments
    if language not in LANGUAGE_SUPPORT :
        debug_sys.log('INFO',f'Unsupported language "{language}+".')
    language = LANGUAGE_SUPPORT[:-1] if language == 'all' else [language]
    # Request data from API if not in ECO mode
    if ECO :
        response = TMP
        debug_sys.log('INFO', f'Request for "{input}" in ECO mode.')
    else :
        response = requests.get(url, headers)
        if response.status_code != 200:
            debug_sys.log('ERROR', f"The request failed with the status code: {response.status_code}")
    # Search
    try:
        if requests.get(url, headers).status_code == 200 :
            return [int(input)]
    except :
        pass
    # Comparison
    results = {}
    for pokemon in response.json():
        for lang in language :
            if lang in pokemon['name']:
                name = pokemon['name'][lang]
                ratio = fuzz.ratio(input.lower(), name.lower())
                if ratio >= p:
                    results[pokemon['pokedexId']] = ratio
    # Sorting
    return [id for id, ratio in sorted(results.items(), key=lambda x: x[-1], reverse=True)]

def infos_on(pokedexId : int, url : str = API_URL, headers : str = API_HEADER)-> dict :
    """
    This function retrieves information about a Pokemon based on its Pokedex ID.
    
    Parameters:
    pokedexId (int): The Pokedex ID of the Pokemon.
    url (str): The URL of the Pokemon API. Default is API_URL.
    headers (str): The headers to use for the API request. Default is API_HEADER.
    
    Returns:
    dict: A dictionary containing information about the Pokemon.
    """
    if ECO :
        try :
            debug_sys.log('INFO', f'Information request for N°{pokedexId} in ECO mode.')
            return TMP.json()[pokedexId]
        except :
            debug_sys.log('ERROR', f'Information request for N°{pokedexId} failed because not listed.')
    else :
        response = requests.get(f"{url}/{pokedexId}", headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            debug_sys.log('ERROR', f"The request failed with the status code: {response.status_code}")
