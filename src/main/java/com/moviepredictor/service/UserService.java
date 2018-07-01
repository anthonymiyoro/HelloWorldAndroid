package com.moviepredictor.service;

import com.moviepredictor.model.User;

public interface UserService {

    User findUserByEmail(String email);

    void saveUser(User user);
}
