
# customer.py - Handles customer data & interactions
# Author: Maurizio Gonzalez

from datetime import datetime

class Customer:
    def __init__(self, customer_id, name, email, max_rentals=3):
        """ Initialize customer details & rental limits """
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.rented_movies = {}  # Dictionary: movie -> rental_date
        self.total_rental_fees = 0
        self.max_rentals = max_rentals

    def rent_movie(self, movie):
        """ Rent a movie if under rental limit & not already rented """
        if len(self.rented_movies) < self.max_rentals:
            if any(rented.title == movie.title for rented in self.rented_movies.keys()):
                print("Movie already rented!")
                return
            self.rented_movies[movie] = datetime.today().date()
            print("Movie successfully rented!")
        else:
            print("Rental limit reached.")

    def return_movie(self, movie):
        """ Return a rented movie """
        if movie in self.rented_movies:
            self.rented_movies.pop(movie)
        else:
            print("Movie hasn't been rented.")

    def get_rented_movies(self):
        """ Return list of rented movie titles """
        return list(self.rented_movies.keys())

    def get_total_fees(self):
        """ Return total rental fees """
        return self.total_rental_fees