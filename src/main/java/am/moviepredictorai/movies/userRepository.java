package am.moviepredictorai.movies;

import org.springframework.data.repository.CrudRepository;

import am.moviepredictorai.movies.User;
// This will be AUTO IMPLEMENTED by Spring into a Bean called userRepository
// CRUD refers Create, Read, Update, Delete

public interface userRepository extends CrudRepository<User, Long> {

}