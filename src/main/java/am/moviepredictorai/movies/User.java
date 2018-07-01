package am.moviepredictorai.movies;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;

@Entity // This tells Hibernate to make a table out of this class
public class User {
    @Id
    @GeneratedValue(strategy=GenerationType.AUTO)

    private String username;
    private String likedmovies;

    public String getUsername(){
        return username;
    }

    public void setUsername(String username){
        this.username = username;
    }

    public String getLikedMovies(){
        return likedmovies;
    }

    public void setLikedMovies(String likedmovies){
        this.likedmovies = likedmovies;
    }

}
