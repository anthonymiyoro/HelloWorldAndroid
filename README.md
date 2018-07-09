# MoviePredictor
### Movie Prediction AI Project

Consists of a java Spring client (Because we have to use it for school) that interacts with an AI written in Python (Django API wrapper) that tries its best to predict the next movie you should watch.


## TO DO

- [x] Install Bootstrap
- [x] Create Navbar
- [x] Install a HTML theme
- [x] Create a Beautiful Homepage
- [x] Install MySQl
- [x] Create user login pages
- [x] Create user sign-up pages
- [ ] Build form that allows for a selection of predefined movies
    - [ ] Build form that collects user input and pases it to the controller
    - [ ] Build controller that converts form input to json and posts it to API
- [ ] Create user input pages
- [ ] Add AI data source
- [ ] Build Pipeline
- [ ] Create AI strategy
- [ ] Create and Host AI Python site


================================================================================
## ADDITIONAL NOTES

- All html so far is to be found under the resources directory
- All controllers are mapped in userController under the controller folder
- All security permissions are handled in configuration under Security Ccnfiguration


## TO RUN THIS THING: (Guess who uses Maven now :p )

- mvn clean install
- mvn spring-boot:run
