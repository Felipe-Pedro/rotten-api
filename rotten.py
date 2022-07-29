from urllib import request
from bs4 import BeautifulSoup

def _format_link(movie_name):
    return "https://www.rottentomatoes.com/m/" + "_".join(movie_name.split(" "))

def open_link(movie_name, timeout=2):
    return request.urlopen(_format_link(movie_name), timeout=timeout)

def get_movie_page(movie_name):
    return BeautifulSoup(open_link(movie_name), features="html.parser")

def _get_page(movie_name):
    return get_movie_page(movie_name).find('score-board') if type(movie_name) != type(BeautifulSoup()) else movie_name

def get_movie_score(movie_name):
    movie_info = _get_page(movie_name)

    return (movie_info['audiencescore'], movie_info['tomatometerscore'])

def get_movie_cast(movie_name):
    movie_page = _get_page(movie_name)
    actors_link = movie_page.find_all('span', class_='characters subtle smaller')
    
    return [ actor['title'] for actor in actors_link ]

def _sanatize(input):
    clean_pieces = []

    for piece in input.split('\n '):
        clean_piece = piece.strip('\n ,')
        
        if clean_piece:
            clean_pieces.append(clean_piece)

    return clean_pieces

def _roles(movie_name):
    movie_page = _get_page(movie_name)
    caracters_link = movie_page.find_all('span', class_='characters subtle smaller')
    
    caracters_stripped_strings = [ string.stripped_strings for string in caracters_link ]

    roles = []

    for string in caracters_stripped_strings:
        roles.append([ _sanatize(sr) if '\n' in sr else sr for sr in string ])

    return roles

def get_movie_roles(movie_name):
    movie_page = _get_page(movie_name)

    return {
        actor: role for actor, role in zip(get_movie_cast(movie_page), _roles(movie_page))
    }
