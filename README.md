# MoviePredictor
Movie Prediction AI Project

- All html so far is to be found under the resources directory
- All controllers are mapped in HomeController

They follow the following: 

    @GetMapping("/greeting")
    public String greetingForm(Model model){
        model.addAttribute("greeting", new Greeting());
        return "greeting";
    }
  
    Will map to the greeting.html page with the /greeting url
    
    The home page is in index.html
