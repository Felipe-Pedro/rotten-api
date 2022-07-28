from urllib import request
from bs4 import BeautifulSoup

def format_link(movie_name):
    return "https://www.rottentomatoes.com/m/" + "_".join(movie_name.split(" "))

def open_link(movie_name, timeout=2):
    return request.urlopen(format_link(movie_name), timeout=timeout)

def get_movie_page(movie_name):
    return BeautifulSoup(open_link(movie_name), features="html.parser")

def get_movie_score(movie_name):
    movie_info = get_movie_page(movie_name, ).find('score-board')

    return (movie_info['audiencescore'], movie_info['tomatometerscore'])

def get_movie_actors(movie_name):
    movie_page = get_movie_page(movie_name) if type(movie_name) != type(BeautifulSoup()) else movie_name
    actors_link = movie_page.find_all('span', class_='characters subtle smaller')
    
    return [ actor['title'] for actor in actors_link ]

def _sanatize(input):
    if '\n' not in input:
        return input
    
    clean_pieces = []

    for piece in input.split('\n '):
        clean_piece = piece.strip('\n ,')
        
        if not clean_piece:
            continue
        
        clean_pieces.append(clean_piece)

    return clean_pieces

def _roles(movie_name):
    movie_page = get_movie_page(movie_name) if type(movie_name) != type(BeautifulSoup()) else movie_name
    caracters_link = movie_page.find_all('span', class_='characters subtle smaller')
    
    caracters_stripped_strings = [ string.stripped_strings for string in caracters_link ]

    roles = []

    for string in caracters_stripped_strings:
        roles.append([ _sanatize(sr) for sr in string ])

    return roles

def get_movie_cast(movie_name):
    movie_page = get_movie_page(movie_name)

    return {
        actor: role for actor, role in zip(get_movie_actors(movie_page), _roles(movie_page))
    }
