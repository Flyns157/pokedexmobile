VERSION = 1.2
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


#=============================== MAIN ZONE ===============================
def create_search_index()-> dict[int:dict[str:str]]:
    """
    Crée un index de recherche en récupérant les données de l'API Pokemon.
    
    Retourne:
        Un dictionnaire qui associe un id de pokedex à un nom de pokemon.
    """
    return {pokemon['pokedexId']:pokemon['name'] for pokemon in requests.get(API_URL, headers=API_HEADER).json()}

def create_search_index2()-> dict[str:int]:
    """
    Crée un index de recherche en récupérant les données de l'API Pokemon.
    
    Retourne:
        Un dictionnaire qui associe un nom de pokemon à un id de pokedex.
    """
    return {pokemon_name:pokemon['pokedexId'] for pokemon in requests.get(API_URL, headers=API_HEADER).json() for pokemon_name in pokemon['name'].values()}

register = create_search_index()

def search_engine(input : str, data : dict[int:dict[str:str]] = register, language  : str = 'fr', p : int = 1)-> dict[int:int]:
    """
    Recherche une correspondance entre la chaîne d'entrée et les noms de Pokemon dans l'index de recherche.
    
    Args:
        input (str): La chaîne d'entrée à rechercher.
        data (dict): L'index de recherche à utiliser. Par défaut, utilise l'index créé par `create_search_index`.
        language (str): La langue à utiliser pour la recherche. Par défaut, utilise le français ('fr').
        p (int): Le pourcentage minimum de correspondance pour qu'un résultat soit retourné. Par défaut, est 1.
        
    Retourne:
        Un dictionnaire qui associe un id de pokedex à un pourcentage de correspondance.
    """
    try:
        return {int(input):100}
    except:
        results = {}
        for id, name_dict in data.items():
            if language in name_dict:
                name = name_dict[language]
                ratio = fuzz.ratio(input.lower(), name.lower())
                if ratio >= p:
                    results[id] = ratio
        return results

def search_result(result_data : dict[int,int])-> list[tuple[int,int]]:
    """
    Trie les résultats de la recherche par ordre décroissant de pourcentage de correspondance.
    
    Args:
        result_data (dict): Les résultats de la recherche à trier.
        
    Retourne:
        Une liste de tuples, où chaque tuple contient un id de pokedex et un pourcentage de correspondance.
    """
    return sorted(result_data.items(), key=lambda x: x[-1], reverse=True)

def suggest(input : str, size : int = 5, language : str = 'fr', data : dict[int:dict[str:str]]= register)-> list[str]:
    """
    Suggère des noms de Pokemon basés sur une chaîne d'entrée.
    
    Args:
        input (str): La chaîne d'entrée à utiliser pour la suggestion.
        size (int): Le nombre maximum de suggestions à retourner. Par défaut, est 5.
        language (str): La langue à utiliser pour la suggestion. Par défaut, utilise le français ('fr').
        data (dict): L'index de recherche à utiliser. Par défaut, utilise l'index créé par `create_search_index`.
        
    Retourne:
        Une liste des noms suggérés de Pokemon.
    """
    return [data[id][language] for id,_ in search_result(search_engine(input,data,language))[:size]]