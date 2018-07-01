package am.moviepredictorai.movies;

import org.springframework.data.repository.CrudRepository;

import am.moviepredictorai.movies.Movie;
// This will be AUTO IMPLEMENTED by Spring into a Bean called userRepository
// CRUD refers Create, Read, Update, Delete

public interface movieRepository extends CrudRepository<User, Long> {

}