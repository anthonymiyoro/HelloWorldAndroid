package am.moviepredictorai.movies;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;

@Entity // This tells Hibernate to make a table out of this class
public class Movie {
    @Id
    @GeneratedValue(strategy=GenerationType.AUTO)

    private long id;
    private String title;
    private int length;
    private int year;

    public void setId(long id){
        this.id = id;
    }

    public long getId(){
        return id;
    }

    public void setTitle (String title){
        this.title = title;
    }

    public String getTitle(){
        return title;
    }

    public void setLength(){
        this.length = length;
    }

    public int getLength(){
        return length;
    }

    public void setYear() {
        this.year = year;
    }

    public int getYear() {
        return year;
    }

}
