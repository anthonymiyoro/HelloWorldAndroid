package com.moviepredictor.model;


//Make setters and gettters for the liked movies
//Pass the movies to a serielizer that then sends a json object with the form results to an API

import javax.persistence.*;

@Table(name="LikedMovies")
public class LikedMovies {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private int id;
    @Column(name="Movie 1")
    private String movie1;


    public int getId(){
        return id;
    }

    public void setId(int id){
        this.id = id;
    }

    public String getMovie1(){
        return movie1;
    }

    public void setMovie1(String movie1){
        this.movie1 = movie1;
    }
}
