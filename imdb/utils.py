from imdb.models import *
from datetime import datetime
from django.db.models import Q
from django.db.models import Avg
from django.db.models import Count
###Assignment 1
#Task 1
def get_no_of_distinct_movies_actor_acted(actor_id):
    try:
        actor = Actor.objects.get(actor_id=actor_id)
        movies = Movie.objects.filter(actor=actor)
        return len(movies)
    except Actor.DoesNotExist:
        return 0
#Task 2
def get_movies_directed_by_director(director_obj):
    try:
        direc = Director.objects.get(name=director_obj)
        return direc.movie_set.all()
    except Director.DoesNotExist:
        return 0
#Task 3
def get_average_rating_of_movie(movie_obj):
    try:
        rating_obj = movie_obj.ratings
        r1 = rating_obj.rating_one_count
        r2 = rating_obj.rating_two_count
        r3 = rating_obj.rating_three_count
        r4 = rating_obj.rating_four_count
        r5 = rating_obj.rating_five_count
        total_rating = r1 + r2 + r3 + r4 + r5
        total_points = (1 * r1) + (2 * r2) + (3 * r3) + (4 * r4) + (5 * r5)
        if total_rating == 0:
            return 0
        return total_points / total_rating, total_rating
    except Ratings.DoesNotExist:
        return 0, 0
#Task 4
def delete_movie_rating(movie_obj):
    try:
        movie_obj.ratings.delete()
    except Movie.ratings.DoesNotExist:
        return "no movie object found to delete ratings"
#Task 5
def get_all_actor_objects_acted_in_given_movies(movie_objs):
    #  return Actor.objects.filter(movie__in=movie_objs).distinct()
    try:
        actor_list = set()
        for movie_obj in movie_objs:
            actor_list.update(movie_obj.actor.all())
        return list(actor_list)
    except Exception as e:
        return e
#Task 6
def update_director_for_given_movie(movie_obj, director_obj):
    try:
        movie_obj.director = director_obj
        movie_obj.save()
        return 0
    except Exception as e:
        return e
#Task 7
def get_distinct_movies_acted_by_actor_whose_name_contains_john():
    try:
        return Movie.objects.filter(actor__name__contains="john").distinct()
    except Exception as e:
        return []
#Task 8
def remove_all_actors_from_given_movie(movie_obj):
    try:
        # for deleting single object we will use remove
        # movie_obj.actor.remove()
        movie_obj.actor.clear()
    except Exception:
        return 0
#Task 9
def get_all_rating_objects_for_given_movies(movie_objs):
    try:
        return Ratings.objects.filter(movie__in=movie_objs)
    except Exception:
        return []

### Assignment 2
#Task 1
def get_movies_by_given_movie_names(movie_names):
    movies = Movie.objects.filter(name__in = movie_names)
    movie_info_list=[]
    for movie in movies:
        director_name = movie.director.name
        average_rating, total_number_of_ratings = get_average_rating_of_movie(movie)
        cast_list = []
        for cast_member in movie.cast_set.all():
            cast_dict = {
                "actor": {
                    "name": cast_member.actor.name,
                    "actor_id": cast_member.actor.actor_id
                },
                "role": cast_member.role,
                "is_debut_movie": cast_member.is_debut_movie
            }
            cast_list.append(cast_dict)
        movie_dict = {
            "movie_id": movie.movie_id,
            "name": movie.name,
            "cast": cast_list,
            "box_office_collection_in_crores": movie.box_office_collection_in_crores,
            "release_date": movie.release_date.strftime("%Y-%m-%d"),
            "director_name": director_name,
            "average_rating": round(average_rating, 2),
            "total_number_of_ratings": total_number_of_ratings
        }
        movie_info_list.append(movie_dict)

    return movie_info_list
##Task 2
def movies_released_in_summer_in_given_years():
    try:
        return list(Movie.objects.filter(release_date__year__range= (2005,2010), release_date__month__in =[5,6,7]))
    except Exception as e:
        return e
##Task 3:
def get_movie_names_with_actor_name_ending_with_smith():
    try:
        return list(Movie.objects.filter(actor_name__iendswith = "smith").distinct())
    except Exception as e:
        return e
##Task 4:
def get_movie_names_with_ratings_in_given_range():
    try:
        return list(Movie.objects.filter(ratings__rating_five_count__lte = 3000, ratings__rating_five_count__gte = 1000))
    except Exception as e:
        return e
##Task 5:
def get_movie_names_with_ratings_above_given_minimum():
    try:
        return list(Movie.objects.filter(Q(release_date__gte = 2000)&Q(Q(ratings__rating_five_count__gte = 500) | Q(ratings__rating_four_count__gte = 1000) | Q(ratings__rating_three_count__gte = 2000) | Q(ratings__rating_two_count__gte = 4000) | Q(ratings__rating_one_count__gte = 8000))))
    except Exception as e:
        return e
##Task 6:
def get_movie_directors_in_given_year():
    try:
        return list(Movie.objects.filter(release_date__year = 2000).values_list('director__name'))
    except Exception as e:
        return e
##Task 7:
def get_actor_names_debuted_in_21st_century():
    try:
        return list(Movie.objects.filter(cast__is_debut_movie = True, cast__movie__release_date__year__gt = 2000))
    except Exception as e:
        return e
##Task 8:
def get_director_names_containing_big_and_movie_in_may():
    try:
        return list(Movie.objects.filter(name__contains = "big", release_date__months = 5).values_list('director__name'))
    except Exception as e:
        return e
##Task 9:(same as task 8)
## Task 10:
def reset_ratings_for_movies_in_this_year():
    try:
        rating_objs = Ratings.objects.filter(movie__release_date__year = 2000)
        rating_objs.update(
            rating_one_count=0,
            rating_two_count=0,
            rating_three_count=0,
            rating_four_count=0,
            rating_five_count=0
        )
    except Exception as e:
        return e

##Assignment 3
##Task 1:
def get_average_box_office_collections():
    try:
        collection = Movie.objects.aggregate(Avg("box_office_collection_in_crores"))
        result = collection['box_office_collection_in_crores__avg']
        return round(result, 3) if result is not None else 0
    except Exception as e:
        return e
#Task 2:
def get_movies_with_distinct_actors_count():
    try:
        movie_actor_count = Movie.objects.annotate(actors_count = Count("actor", distinct = True))
        return movie_actor_count
    except Exception as e:
        return e
#Task 3:
def get_male_and_female_actors_count_for_each_movie():
    # try:
    #     female_actor_count = Movie.objects.filter(movie__actor__gender = "Female").count()
    #     male_actor_count = Movie.objects.filter(movie__actor__gender = "Male").count()
    #     return female_actor_count, male_actor_count
    # except Exception as e:
    #     return e
    try:
        actor_count = Movie.objects.annotate(female_actor_count = Count("actor", filter = Q(actor__gender = "Female")), male_actor_count = Count("actor", filter = Q(actor__gender = "Male")))
        return actor_count
    except Exception as e:
        return e
#Task 4:
def get_roles_count_for_each_movie():
    try:
        role_count = Movie.objects.annotate(roles = Count("cast__role", distinct =True))
        return role_count
    except Exception as e:
        return e
#Task 5:
def get_role_frequency():
    try:
        role_freq = Cast.objects.values("role").annotate(actor = Count("actor", distincy=True))
        role_freq_dict = {
            item["role"]: item["actor_count"] for item in role_freq
        }
        return role_freq_dict
    except Exception as e:
        return e
#Task 6:
def get_role_frequency_in_order():
    try:
        role_freq = Movie.objects.values('role').annotate(count = Count('role')).order_by('movie__release_date').values_list('role', 'count')
        return role_freq
    except Exception as e:
        return e
#Task 7:
def get_no_of_movies_and_distinct_roles_for_each_actor():
    try:
        no_of_movies = Actor.objects.annotate(movie_count = Count("cast__movie", distinct =True) , role_count =Count("cast__role", distinct =True))
        return no_of_movies
    except Exception as e:
        return e
#Task 8:
def get_movies_with_atleast_forty_actors():
    try:
        actors_count = Movie.objects.annotate(fourty_actors = Count("actor", distinct =True)).filter(fourty_actors__gte = 40)
        return actors_count
    except Exception as e:
        return e
#Task 9:
def get_average_no_of_actors_for_all_movies():
    try:
        average = Movie.objects.annotate(all_actors= Count("actor", distinct =True))
        avg_result = average.aggregate(avg_actor = Avg("all_actors"))
        final = avg_result["avg_actor"]
        return round(final, 3) if average is not None else 0
    except Exception as e:
        return e

### Assignment 4:
#Task 6:
def get_female_cast_details_from_movies_having_more_than_five_female_cast():
    try:
        movies = Movie.objects.annotate(female_act = Count("actor", distinct = True, filter = Q(actor__gender = "F"))).filter(female_act__gte = 5)
        movie_details_list=[]

        for movie in movies:
            average_rating, total_number_of_ratings = get_average_rating_of_movie(movie)
            cast_list=[]
            for cast_member in movie.cast_set.all():
                if cast_member.actor.gender == "F":
                    cast_dict={
                        "actor": {
                            "name": cast_member.actor.name,
                            "actor_id": cast_member.actor.actor_id,
                            "gender": cast_member.actor.gender
                        },
                        "role": cast_member.role,
                        "is_debut_movie": cast_member.is_debut_movie
                    }
            cast_list.append(cast_dict)
            movie_dict={
                "movie_id": movie.movie_id,
                "name": movie.name,
                "cast": cast_list,
                "box_office_collection_in_crores":movie.box_office_collection_in_crores ,
                "release_date": movie.release_date,
                "director_name": movie.director.name,
                "average_rating":average_rating,
                "total_number_of_ratings": total_number_of_ratings
            }
            movie_details_list.append(movie_dict)
        return movie_details_list
    except Exception as e:
        return e
#Task 7:
def get_actor_movies_released_in_year_greater_than_or_equal_to_2000():
    try:
        all_actors = Actor.objects.all()
        actor_movies_list = []
        for actor in all_actors:
            movies = Movie.object.filter(actor = actor, release_date__year__gte = 2000)
            for movie in movies:
                average_rating, total_number_of_ratings = get_average_rating_of_movie(movie)
                cast_list = []
                for cast_member in movie.cast_set.all():
                    cast_dict = {
                        "actor": {
                            "name": cast_member.actor.name,
                            "actor_id": cast_member.actor.actor_id,
                            "gender": cast_member.actor.gender
                        },
                        "role": cast_member.role,
                        "is_debut_movie": cast_member.is_debut_movie
                    }
                cast_list.append(cast_dict)
                movie_dict = {
                    "movie_id": movie.movie_id,
                    "name": movie.name,
                    "cast": cast_list,
                    "box_office_collection_in_crores": movie.box_office_collection_in_crores,
                    "release_date": movie.release_date,
                    "director_name": movie.director.name,
                    "average_rating": average_rating,
                    "total_number_of_ratings": total_number_of_ratings
                }
                actor_movies_list.append(movie_dict)
        return actor_movies_list

    except Exception as e:
        return e
#Task 8:
def reset_ratings_for_movies_in_given_year(year):
    try:
        target_reset_rating = Ratings.objects.filter(movie__release_date__year = year)
        target_reset_rating.update(
            rating_five_count = 0,
            rating_four_count = 0,
            rating_three_count = 0,
            rating_two_count = 0,
            rating_one_count = 0
        )

    except Exception as e:
        return e


def populate_database(actors_list, movies_list, directors_list, movie_rating_list):
    """
    Populates the DB using the given dictionaries.
    """

    # Step 1: Create Directors
    director_objects = {}
    for director_name in directors_list:
        director_obj, _ = Director.objects.get_or_create(name=director_name)
        director_objects[director_name] = director_obj

    # Step 2: Create Actors
    actor_objects = {}
    for actor in actors_list:
        actor_obj, _ = Actor.objects.get_or_create(
            actor_id=actor["actor_id"],
            defaults={"name": actor["name"]}
        )
        actor_objects[actor["actor_id"]] = actor_obj

    # Step 3: Create Movies
    movie_objects = {}
    for movie in movies_list:
        director = director_objects[movie["director_name"]]
        movie_obj, _ = Movie.objects.get_or_create(
            movie_id=movie["movie_id"],
            defaults={
                "name": movie["name"],
                "release_date": datetime.strptime(movie["release_date"], "%Y-%m-%d").date(),
                "box_office_collection_in_crores": float(movie["box_office_collection_in_crores"]),
                "director": director,
            }
        )
        movie_objects[movie["movie_id"]] = movie_obj

        # Step 4: Create Cast (link movie ↔ actors)
        for actor in movie["actors"]:
            Cast.objects.get_or_create(
                movie=movie_obj,
                actor=actor_objects[actor["actor_id"]],
                role=actor["role"],
                is_debut_movie=actor.get("is_debut_movie", False)
            )

    # Step 5: Create Ratings
    for rating in movie_rating_list:
        movie_obj = movie_objects[rating["movie_id"]]
        Ratings.objects.get_or_create(
            movie=movie_obj,
            defaults={
                "rating_one_count": rating["rating_one_count"],
                "rating_two_count": rating["rating_two_count"],
                "rating_three_count": rating["rating_three_count"],
                "rating_four_count": rating["rating_four_count"],
                "rating_five_count": rating["rating_five_count"],
            }
        )

