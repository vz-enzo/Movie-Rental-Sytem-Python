
# system.py - Manages the movie rental system
# Author: Maurizio Gonzalez

import random
import csv
from datetime import datetime
from movie import Movie, ProductionCompany
from customer import Customer

class MovieManagementSystem:
    """ Movie Rental System that allows customers to rent, return, and manage movies. """

    def __init__(self):
        """ Initialize system with empty databases. """
        self.movies = {}  # Dictionary: title -> Movie object
        self.productionCompany = {}  # Dictionary: name -> production company object
        self.customers = {}  # Dictionary: customerID -> Customer object
        self.genre_classification = {}  # Dictionary: Genre -> {set of movie titles}
        self.waitlist = {}  # Dictionary: movie titles -> [list of customerIDs]

    def add_movie(self, title, director_name, production_company, year, copies, genre, rental_fee, founded_year):
        """ Add a new movie to the system. """
        movie = Movie(title, director_name, year, copies, genre, production_company, rental_fee) 
        self.movies[title] = movie 

        if production_company not in self.productionCompany: 
            newproduction = ProductionCompany(production_company, founded_year) 
            self.productionCompany[production_company] = newproduction 
    
        self.productionCompany[production_company].add_movie(movie) 

        if genre not in self.genre_classification: 
            self.genre_classification[genre] = set() 
        self.genre_classification[genre].add(title) 


    def register_customer(self, name, email):
        """ Register a new customer and assign a unique ID. """
        customer_id = random.randint(0, 100000) 

        if customer_id in self.customers:
            customer = Customer(customer_id, name, email) 
            self.customers[customer_id] = customer  
        else:
            while customer_id in self.customers: 
                customer_id = random.randint(0, 100000)
            
            customer = Customer(customer_id, name, email) 
            self.customers[customer_id] = customer
            
        return customer_id 
    

    def rent_movie(self, title, customer_id):
        """ Process movie rental for a customer. """

        if customer_id not in self.customers:
            print("Customer ID Doens't exist")
            return

        if len(self.customers[customer_id].rented_movies) >= self.customers[customer_id].max_rentals: 
            print("Max rentals reached")
            return

        if title in self.movies: 
            if self.movies[title].available_copies == 0: 
                print("No copies Available")
            else:
                movie = self.movies[title]   
                self.movies[title].available_copies -= 1  
                self.customers[customer_id].rent_movie(movie)  

        elif title not in self.movies: 
            print("Movie not Available")
        
        elif customer_id not in self.customers: 
            print("Customer ID Does'nt exists")
            
        else:
            print("Movie not available")
        

    def return_movie(self, title, customer_id):
        """ Process returning a rented movie. """

        if title not in self.movies: 
            print("Movie not Available")
            return
        
        if customer_id not in self.customers: 
            print("Customer ID Doesn't exists")
            return

        if self.movies[title] not in self.customers[customer_id].rented_movies: 
            print("User hasn't rented this movie")
            return
    
        else:           
            movie = self.movies[title]  
            self.customers[customer_id].return_movie(movie) 
            self.movies[title].available_copies += 1  
            
            rating = int(input("Rate the Movie (1-5 stars): "))  
            while rating < 1 or rating > 5:
                print("Invalid rating please enter a number in the range 1-5") 
                rating = int(input("Rate the Movie (1-5 stars): "))

            print("Movie Succesfully Returned")


    def search_movie(self, query):
        """ Search movies by title, genre, or director. """
        matches  = [] 

        for i in self.movies.values():
            if query == i.title or query == i.genre or query == i.director: 
                matches.append(str(i))
        
        return matches 
    

    def display_available_movies(self):
        """ Display all available movies for rent. """
        available_movies = [] 

        for i in self.movies.values(): 
            if i.available_copies > 0:      
                available_movies.append(str(i))  
        
        return available_movies 
    

    def display_customer_movies(self, customer_id):
        """ Show all movies rented by a specific customer. """

        if len(self.customers[customer_id].rented_movies) < 1: 
            return []  
        else:
            display_rented = {str(movie): date for movie, date in self.customers[customer_id].rented_movies.items()} 
            return display_rented
        

    def recommend_movies(self, customer_id):
        """ Recommend movies based on customer's rental history. """

        list_recommends = [] 
        genres = set() 

        for i in self.customers[customer_id].rented_movies.keys(): 
            genres.add(i.genre)    

        for movie in self.movies.values():  
            if len(list_recommends) >= 5:   
                return list_recommends
            if movie.genre in genres:    
                list_recommends.append(str(movie)) 
        
        return list_recommends 

    def add_to_waitlist(self, title, customer_id):
        """ Add customer to waitlist if a movie is unavailable. """
        if self.movies[title].available_copies == 0: 
            if title not in self.waitlist: 
                self.waitlist[title] = [] 
                self.waitlist[title].append(customer_id) 
            else:
                self.waitlist[title].append(customer_id) 


    def check_late_returns(self, days_threshold=14):
        """ Check for customers who have kept movies past the rental period. """
        late_returns = [] 

        for i in self.customers.values(): 
            for j, rental_date in i.rented_movies.items(): 
                days_rented = (datetime.today().date() - rental_date).days 

                if days_rented > days_threshold: 
                    late_returns.append(j) 
        
        return late_returns 
                

    def display_top_rated_movies(self):
        """ Display the top 3 highest-rated movies. """
        highest_three = [] 
       
        for i in self.movies.values(): 
            highest_three.append((i.average_rating, i)) 
        
        
        def get_rating(movie_tuple):
            return movie_tuple[0]
        
        final = sorted(highest_three, key = get_rating, reverse = True)

        top_3 = [] 
        for movie in final[:3]: 
            top_3.append(str(movie[1])) 
        
        return top_3 
 

    def read_file(self, filename = "data.csv"):
        """ Read movie data from a CSV file. """

        try:
            with open(filename, mode = 'r')as file: 
                csvFile = csv.reader(file)
                next(csvFile) 
                
                for i in csvFile:
                     
                    title, director, year, copies, genre, production_company, rental_fee, founded_year = i
                    
                    year = int(year)
                    copies = int(copies)
                    rental_fee = float(rental_fee)
                    founded_year = int(founded_year)
                    
                    movie = Movie(title, director, year, copies, genre, production_company, rental_fee)
                    self.movies[title] = movie
                    
                    if production_company not in self.productionCompany:
                        self.productionCompany[production_company] = ProductionCompany(production_company, founded_year)
                    
                    self.productionCompany[production_company].add_movie(movie)
                    
                    if genre not in self.genre_classification:
                        self.genre_classification[genre] = set() 
                    self.genre_classification[genre].add(title) 
        except:
            print("The file was not found, check if its in the correct folder")
                
    def run(self):
        """ Run the console-based Movie Rental System. """
        while True:
            print("\nWELCOME TO VZ'S MOVIES CORNER")
            print("1. Add Movie")
            print("2. Register Customer")
            print("3. Rent Movie")
            print("4. Return Movie")
            print("5. Search Movies")
            print("6. Display Available Movies")
            print("7. Display Customer's Rented Movies")
            print("8. Recommend Movies")
            print("9. Check Late Returns")
            print("10. Exit")

            try:
                user_input = int(input("Please Enter your choice: ")) 
            except:
                print("X Invalid input, Please enter a number 1-10: ")
                continue 

            if user_input < 1 or user_input > 10:
                print("Invalid input, Please enter valid number 1-10:")
                continue 
            
            if user_input == 1: 
                 title = input("Enter movie title: ")
                 director = input("Enter director name: ")
                 production_company = input("Enter production company: ")
                 try:
                     year = int(input("Enter release year: "))
                     copies = int(input("Enter number of copies: "))
                     rental_fee = float(input("Enter rental fee: "))
                     founded_year = int(input("Enter production company founded year: "))
                 except:
                     print("Invalid number input")
                     continue
                 genre = input("Enter movie genre:")

                 
                 self.add_movie(title, director, production_company, year, copies, genre, rental_fee, founded_year)
                 print("Movie Succesfully registered =)")

            elif user_input == 2: 

                name = input("Enter customer username:")
                email = input("Enter customer email: ")
                customer_id = self.register_customer(name, email)
                print("Customer succesfully regireted, Your Customer ID is:", customer_id)

            elif user_input == 3:
                try:
                    customer_id = int(input("Enter your Customer ID: "))

                    customer_id = int(customer_id)  

                    title =  input('Enter Movie Title: ')

                    self.rent_movie(title, customer_id)
                except ValueError:
                    print("Customer ID must be a number")

            elif user_input == 4:
                try:
                    customer_id = int(input("Enter customer ID: "))
                    title = input("Enter Movie Title please: ")
                    self.return_movie(title, customer_id)
                except:
                    print("Invalid input, customer id must be a number")

            elif user_input == 5:
                query = input("Enter the movie title, genre or director: ")
                results = self.search_movie(query)
                print("Search Results:", results)

            elif user_input == 6:
                available_movies = self.display_available_movies()
                print("Available Movies:", available_movies)

            elif user_input == 7:
                try:
                    customer_id = int(input("Enter Customer ID: ")) 
                    rented_movies =  self.display_customer_movies(customer_id)

                    if not rented_movies: 
                        print("Customer hasn't rented any movies yet")
                        continue 

                    print("Movies rented by Customer: ")
                    for movie, date in rented_movies.items(): 
                        print(f" {movie} (was rented on: {date})") 
                except:
                    print("Invalid input, customer ID must be a number")

            elif user_input == 8:
                try:
                    customer_id = int(input("Enter Customer ID: ")) 

                    if customer_id not in self.customers:
                        print("Customer ID doesn't exist")
                        continue 

                    top_3 = self.display_top_rated_movies()

                    print("\n -- TOP 3 ROTTEN VICHENZO'S HIGHEST RATED MOVIES: --")
                    for movie in top_3:
                        print(f"- {movie}")

                    
                    recommendations =  self.recommend_movies(customer_id)

                    if not recommendations:
                        print("There are no recommendations available =(")
                    else:
                        print("\n Recommended Movies to customer:")
                        for movie in recommendations:  
                            print(f" {movie}") 

                except:
                    print("Invalid input, customer ID must be a number")
                    
            elif user_input == 9:
                late_movies = self.check_late_returns()
                print("Your Late Returns:",  late_movies)

            elif user_input == 10:
                print("THANK YOU FOR USING VZ'S MOVIE RENTAL")
                break 
            else:
                print("Invalid Choice, please try again")

