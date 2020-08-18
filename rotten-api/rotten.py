import urllib.request
from bs4 import BeautifulSoup

class Rotten:
    def __init__(self):
        self.base_link = "https://www.rottentomatoes.com"
    
    def split_name(self, name):
        return name.split(" ")

    def format_name_to_link(self, movie_name):
        formated_name = ""
        name_splited = self.split_name(movie_name)

        for name_part in name_splited:
            formated_name += name_part

            if name_splited.index(name_part) >= len(name_splited) - 1: #If it is the last name part in array
                break                                                 #it will not put _ after the name part
            formated_name += "_"
    
        return formated_name

    def open_link(self, movie_name):
        formated_name = self.format_name_to_link(movie_name)
        return urllib.request.urlopen(f"{self.base_link}/m/{formated_name}")

    def get_page(self, movie_name):
        return BeautifulSoup(self.open_link(movie_name), features="html.parser")

    def search_movie(self, movie_name):
        try:
            return Rotten_movie(self.get_page(movie_name))
        except urllib.error.HTTPError:
            return Rotten_movie(None)

class Rotten_movie:
    def __init__(self, page):

        self.page = page
        self.rotten_rating_value = self.get_rotten_rating()
        self.audience_rating_value = self.get_audience_rating()
        self.movie_name = self.get_movie_name()
        self.movie_cast = self.get_movie_cast()
        self.movie_poster = self.get_movie_poster()

    def try_get_info(self, tag, attributes, string="yes"):
        try:
            if string == "yes":
                return self.page.find(tag, attrs=attributes).string 
            return self.page.find(tag, attrs=attributes)
        except AttributeError:
            return 0

    def get_rotten_rating(self):
        return self.try_get_info('span', {'class': 'mop-ratings-wrap__percentage'})
    
    def get_audience_rating(self):
        audience_div = self.try_get_info('div', {'class': 'mop-ratings-wrap__half audience-score'}, string="no")
        return audience_div.find('span', attrs={'class': 'mop-ratings-wrap__percentage'}).string

    def get_movie_name(self):
        return self.try_get_info('h1', {'class': 'mop-ratings-wrap__title mop-ratings-wrap__title--top'})

    def get_cast_div(self):
        return self.try_get_info('div', {'class': 'castSection'}, string="no")

    def dictionary_generator(self, array):
            dictionary = {}
            for i in range(0, len(array), 2):
                dictionary[array[i]['title']] = array[i+1]['title']
            return dictionary

    def get_movie_cast(self):
        try:
            cast_div = self.get_cast_div()
            
            cast_name_span = cast_div.find_all('span')
            cast_name_span.pop()

            cast_name = self.dictionary_generator(cast_name_span)
            
            return cast_name
        except AttributeError:
            return 0

    def get_movie_poster(self):
        image_link = self.try_get_info('img', {'class': 'posterImage js-lazyLoad'}, string="no")
        if image_link == 0:
            return 0

        return urllib.request.urlretrieve(image_link["data-src"])[0]