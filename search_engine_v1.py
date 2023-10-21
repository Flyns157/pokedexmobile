import requests
from fuzzywuzzy import fuzz

API_URL = "https://api-pokemon-fr.vercel.app/api/v1/pokemon"
API_HEADER = {
    "User-Agent": "RobotPokemon",
    "From": "adresse[at]domaine[dot]com",
    'Content-type': 'application/json'
}

def create_search_index()-> dict[dict:int]:
    return {pokemon['pokedexId']:pokemon['name'] for pokemon in requests.get(API_URL, headers=API_HEADER).json()}
def create_search_index2()-> dict[dict:int]:
    return {pokemon_name:pokemon['pokedexId'] for pokemon in requests.get(API_URL, headers=API_HEADER).json() for pokemon_name in pokemon['name'].values()}

register = create_search_index()

def search_engine(input, data = register, language = 'fr')-> dict[int:int]:
    try:
        return {int(input):100}
    except:
        results = {}
        for id, name_dict in data.items():
            if language in name_dict:
                name = name_dict[language]
                ratio = fuzz.ratio(input.lower(), name.lower())
                if ratio >= 1:  # Vous pouvez ajuster ce seuil en fonction de vos besoins
                    results[id] = ratio
        return results

def search_result(result_data : dict[int,int])-> list[tuple[int,int]]:
    return sorted(result_data.items(), key=lambda x: x[-1], reverse=True)

def suggest(input : str, size : int = 5, language = 'fr', data = register)-> list[str]:
    return [data[id][language] for id,_ in search_result(search_engine(input,data,language))[:size]]