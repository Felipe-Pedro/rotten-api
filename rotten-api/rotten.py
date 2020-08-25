import urllib.request
from bs4 import BeautifulSoup

class Rotten:
    def __init__(self, timeout=2):
        self.base_link = "https://www.rottentomatoes.com"
        self.timeout = timeout

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
        return urllib.request.urlopen(f"{self.base_link}/m/{formated_name}", timeout=self.timeout)

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
        self.movie_synopsis = self.get_movie_synopsis()
        self.movie_info = self.get_movie_info()

    def try_get_info(self, tag, attributes, string=True, html=None):
        if html is None:
            html = self.page
        try:
            if string:
                return html.find(tag, attrs=attributes).string
            return html.find(tag, attrs=attributes)
        except AttributeError:
            return 0

    def get_rotten_rating(self):
        return self.try_get_info('span', {'class': 'mop-ratings-wrap__percentage'})
    
    def get_audience_rating(self):
        audience_div = self.try_get_info('div', {'class': 'audience-score'}, string=False)
        return self.try_get_info('span', {'class': 'mop-ratings-wrap__percentage'}, html=audience_div)

    def get_movie_name(self):
        return self.try_get_info('h1', {'class': 'mop-ratings-wrap__title mop-ratings-wrap__title--top'})

    def get_cast_div(self):
        return self.try_get_info('div', {'class': 'castSection'}, string=False)

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
        image_link = self.try_get_info('img', {'class': 'posterImage js-lazyLoad'}, string=False)
        if image_link == 0:
            return 0

        return urllib.request.urlretrieve(image_link["data-src"])[0]

    def get_movie_synopsis(self):
        return self.try_get_info('div', {'id': 'movieSynopsis'})

    def dictionary_info_generator(self, array):
        dictonary = {}
        for i in range(0, len(array), 2):
            dictonary[array[i]] = array[i+1]
        return dictonary 
    
    def check_item_type(self, item):
        if type(item) == type([]):
            return True
        return False

    def strip_item(self, item):
        for i in range(0, 3):
            item = item.strip()
        return item

    def movie_info_organizer(self, array):
        
        organized_array = []
        
        for info in array:
            organized_array.append(info) if self.check_item_type(info) else organized_array.append(self.strip_item(info))
        return organized_array

    def get_info_list(self):
        info_div = self.try_get_info('ul', {'class': 'content-meta info'}, string=False)
        if info_div == 0:
            return 0
        return info_div.find_all('li', attrs={'class': 'meta-row clearfix'})

    def organize_genre(self, genre):
        gender_array = []
        genre_splited = genre.split(" ")
        for genre in genre_splited:
            if genre != "" and genre != "\n" and genre != "&":
                genre = genre.strip(",")
                gender_array.append(genre)

        return gender_array

    def get_movie_info(self):
        info_list = self.get_info_list()

        if info_list == 0:
            return 0

        info_array = []

        for info in info_list:
            info_value = info.find('div', attrs={'class': 'meta-value'})
            
            info_array.append(info.find('div', attrs={'class': 'meta-label subtle'}).string)

            if info_value.string is not None:
                info_array.append(info_value.string)
                
            if info_value.find('time') is not None:
                info_array.append(info_value.find('time').string)

            if info_value.find('a') is not None:
                name_array = []
                for info2 in info_value.find_all('a'):
                    name_array.append(info2.string)
                info_array.append(name_array)
        
        organized_array = self.movie_info_organizer(info_array)
        
        right_genre = self.organize_genre(organized_array[3])
        organized_array[3] = right_genre
        info_dict = self.dictionary_info_generator(organized_array)
        
        return info_dict