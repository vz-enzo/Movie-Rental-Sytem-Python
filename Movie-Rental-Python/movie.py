
# movie.py - Defines Movie & ProductionCompany classes
# Author: Maurizio Gonzalez

class ProductionCompany:
    def __init__(self, name, founded_year):
        """ Initialize production company details """
        self.name = name
        self.founded_year = founded_year
        self.movies = set()

    def add_movie(self, movie):
        """ Add a new movie to the company's catalog """
        if movie not in self.movies:
            self.movies.add(movie)

class Movie:
    def __init__(self, title, director, year, copies, genre, production_company, rental_fee):
        """ Initialize movie details """
        self.title = title
        self.director = director
        self.year = year
        self.copies = copies
        self.available_copies = copies
        self.genre = genre
        self.production_company = production_company
        self.rental_fee = rental_fee
        self.user_ratings = []
        self.average_rating = 0

    def __str__(self):
        """ Return string representation of the movie """
        return f"{self.title} by {self.production_company} ({self.year}) {self.average_rating}/5 stars"

    def add_rating(self, rating):
        """ Add a rating (1-5) to the movie """
        if 1 <= rating <= 5:
            self.user_ratings.append(rating)
        else:
            print("Invalid rating. Enter a number between 1-5.")

    def update_average_rating(self):
        """ Calculate and update the movie's average rating """
        if not self.user_ratings:
            print("No ratings yet.")
            return
        self.average_rating = sum(self.user_ratings) / len(self.user_ratings)

    def get_average_rating(self):
        """ Return the average rating of the movie """
        return self.average_rating