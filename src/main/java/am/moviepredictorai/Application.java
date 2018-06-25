package am.moviepredictorai;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;


//Run the application java class
@SpringBootApplication(scanBasePackages = {"am.moviepredictorai.movies.User", "am.moviepredictorai.movies.Movie"})
//@EnableOAuth2Sso
public class Application {
    public static void main(String[] args){
        SpringApplication.run(Application.class, args);
    }
}