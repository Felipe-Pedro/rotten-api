# Rotten API

The rotten API is a open python library which provides a series of functions to extract data from Rotten Tomatoes. It is built using the urllib to make requests and BeautifulSoup to parse the html.

## What Rotten API can do for you?

### By now it can:
- Get a movie's page from Rotten Tomatoes using ```open_link(movie_name)```
- Get a BeautifulSoup object containing a movie's page from Rotten Tomatoes using ```get_movie_page(movie_name)```
- Get the audience score and rotten score from any movie using ```get_movie_score(movie_name)```
- Get the movie cast using ```get_movie_cast(movie_name)```
- Get the movie roles using ```get_movie_roles(movie_name)```

# How can i install this library?
It will be available on pip soon but until than you can do a clone from this repository to use on your projects.

# Library functions overview

## Notes

All functions, except ```open_link(movie_name)``` and ```get_movie_page(movie_name)```, can receive a BeautifulSoup object containing the Rotten movie's page as the movie_name parameter, so you can make only one request to Rotten and parse the information as you need, otherwise it will make the request each time you call a function.

### ```open_link(movie_name, timeout=2)```
```movie_name```: A string containing the movie's name which you want to get the data from.
```timeout=2```: The time it will wait for a response from the server.

It makes a request to the Rotten Tomatoes server and returns the movie's html page.

### ```get_movie_page(movie_name)```
```movie_name```: A string containing the movie's name which you want to get the data from.
```return ```: a BeautifulSoup object containing the Rotten movie's page

### ```get_movie_score(movie_name)```
```movie_name```: A string containing the movie's name which you want to get the data from, or a BeautifulSoup object.
```return ```: A tuple containing the audience and rotten score, in that order

### ```get_movie_cast(movie_name)```
```movie_name```: A string containing the movie's name which you want to get the data from, or a BeautifulSoup object.
```return```: A list containing all the movie's cast, not only actors.

### ```get_movie_roles(movie_name)```
```movie_name```: A string containing the movie's name which you want to get the data from, or a BeautifulSoup object.
```return```: A dict containing the cast as the keys and their roles as the items.