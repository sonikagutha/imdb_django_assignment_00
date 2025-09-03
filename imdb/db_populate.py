from imdb.models import Director, Actor, Movie, Cast, Ratings
from datetime import datetime

def run():
    # Directors
    d1, _ = Director.objects.get_or_create(name="Director 1")

    # Actors
    a1, _ = Actor.objects.get_or_create(actor_id="actor_1", name="Actor 1")
    a2, _ = Actor.objects.get_or_create(actor_id="actor_2", name="Actor 2")


    # Movie
    m1, _ = Movie.objects.get_or_create(
        movie_id="movie_1",
        defaults={
            "name": "Movie 1",
            "release_date": datetime.strptime("2020-03-03", "%Y-%m-%d").date(),
            "box_office_collection_in_crores": 12.3,
            "director": d1,
        }
    )

    # Cast
    Cast.objects.get_or_create(movie=m1, actor=a1, role="Hero", is_debut_movie=True)
    Cast.objects.get_or_create(movie=m1, actor=a2, role="Villain", is_debut_movie=False)

    # Ratings
    Ratings.objects.get_or_create(
        movie=m1,
        defaults={
            "rating_one_count": 2,
            "rating_two_count": 3,
            "rating_three_count": 4,
            "rating_four_count": 5,
            "rating_five_count": 6,
        }
    )

    print("✅ Database populated successfully")
