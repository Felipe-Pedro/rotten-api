# Rotten API

The rotten API is a open python library which provides a series of functions to extract data from Rotten Tomatoes. It is built using the urllib to make requests and BeautifulSoup to parse the html.

## What Rotten API can do for you?

### By now it can:
- Get a movie's page from Rotten Tomatoes using ```python
                                                   open_link(movie_name)
                                                   ```
- Get a BeautifulSoup object containing a movie's page from Rotten Tomatoes using ```python
                                                   get_movie_page(movie_name)
                                                   ```
- Get the audience score and rotten score from any movie using ```python
                                        get_movie_score(movie_name)
                                        ```
- Get the movie cast using ```python
                              get_movie_cast(movie_name)
                              ```
- Get the movie roles using ```python
                               get_movie_roles(movie_name)
                            ```
# How can i install this library?
It will be available on pip soon but until than you can do a clone from this repository to use on your projects.

# Library functions overview

## Notes

All functions, except ```py 
                        open_link(movie_name) 
                        ``` and 
                        ```python 
                        get_movie_page(movie_name) 
                        ```
                        , can receive a BeautifulSoup object containing the Rotten movie's page as the movie_name parameter, so you can make only one request to Rotten and parse the information as you need, otherwise it will make the request each time you call a function.

### ```python open_link(movie_name, timeout=2) ```
```python movie_name```: A string containing the movie's name which you want to get the data from.
```python timeout=2```: The time it will wait for a response from the server.

It makes a request to the Rotten Tomatoes server and returns the movie's html page.

### ```python get_movie_page(movie_name) ```
```python movie_name```: A string containing the movie's name which you want to get the data from.
```python return ```: a BeautifulSoup object containing the Rotten movie's page

### ```python get_movie_score(movie_name) ```
```python movie_name```: A string containing the movie's name which you want to get the data from, or a BeautifulSoup object.
```python return ```: A tuple containing the audience and rotten score, in that order

### ```python get_movie_cast(movie_name) ```
```python movie_name```: A string containing the movie's name which you want to get the data from, or a BeautifulSoup object.
```python return ```: A list containing all the movie's cast, not only actors.

### ```python get_movie_roles(movie_name) ```
```python movie_name```: A string containing the movie's name which you want to get the data from, or a BeautifulSoup object.
```python return ```: A dict containing the cast as the keys and their roles as the items.