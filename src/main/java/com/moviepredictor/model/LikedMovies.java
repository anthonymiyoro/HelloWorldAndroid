package com.moviepredictor.model;


//Make setters and gettters for the liked movies
//Pass the movies to a serielizer that then sends a json object with the form results to an API

import javax.persistence.Column;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;

@Table(name="LikedMovies")
public class LikedMovies {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private int id;

    @Column(name="Movie 1")
    private String movie1;

    @Column(name="Movie 2")
    private String movie2;

    @Column(name="Movie 3")
    private String movie3;

    @Column(name="Movie 4")
    private String movie4;

}
