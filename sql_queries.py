class FilmQueries:
    GET_ALL = "SELECT title, description, release_year FROM sakila.film;"

    @staticmethod
    def get_films_by_keyword(keyword):
        return (
            "SELECT title, release_year "
            "FROM sakila.film "
            "WHERE title LIKE %s OR description LIKE %s"
            "LIMIT 10;",
            ('%' + keyword + '%', '%' + keyword + '%')
        )
    @staticmethod
    def get_films_by_genre_and_year(genre, year):
        return (
            "SELECT f.title, f.release_year, c.name "
            "FROM sakila.film AS f "
            "JOIN sakila.film_category AS fc ON f.film_id = fc.film_id "
            "JOIN sakila.category AS c ON c.category_id = fc.category_id "
            "WHERE c.name = %s AND f.release_year = %s;",
            (genre, year)
        )

    @staticmethod
    def get_all_films(limit=100):
        return (
            "SELECT title, description, release_year FROM sakila.film LIMIT %s;",
            (limit,)
        )