VERSION = 2
#=============================== IMPORTS ZONE ===============================
import requests
from fuzzywuzzy import fuzz


#=============================== INIT ZONE ===============================
API_URL = "https://api-pokemon-fr.vercel.app/api/v1/pokemon"
API_HEADER = {
    "User-Agent": "RobotPokemon",
    "From": "adresse[at]domaine[dot]com",
    'Content-type': 'application/json'
}
LANGUAGE_SUPPORT = ["fr", "en", "jp"]


#=============================== MAIN ZONE ===============================
def search(input : str, language : str, url : str = API_URL, headers : str = API_HEADER, p : int = 50)-> list[int]:
    # Vérification de la valliditée des arguments
    if language not in LANGUAGE_SUPPORT :
        raise Exception(f'/!\ Unsupported language "{language}+".')
    # Demande des données à l'API
    response = requests.get(url, headers)
    if response.status_code != 200:
        raise Exception("/!\ La requête a échoué avec le code d'état: ", response.status_code)
    # Recherche    
    if requests.get(url, headers).status_code == 200 :
        return [int(input)]
    else :
        # comparaison
        results = {}
        for pokemon in response.json():
            if language in pokemon['name']:
                name = pokemon['name'][language]
                ratio = fuzz.ratio(input.lower(), name.lower())
                if ratio >= p:
                    results[pokemon['pokedexId']] = ratio
        # trie
        return sorted(results.items(), key=lambda x: x[-1], reverse=True)

def infos_on(pokedexId : int, url : str = API_URL, headers : str = API_HEADER)-> dict :
    response = requests.get(f"{url}/{pokedexId}", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("/!\ La requête a échoué avec le code d'état: ", response.status_code)