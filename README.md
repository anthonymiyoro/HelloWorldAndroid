# MoviePredictor
### Movie Prediction AI Project


## TO DO

- [ ] Install Bootstrap
- [ ] Create Navbar
- [ ] Install a HTML theme
- [ ] Create a Beautiful Homepage
- [ ] Install MySQl
- [ ] Create user login pages
- [ ] Create user sign-up pages
- [ ] Create user input pages
- [ ] Add AI data source
- [ ] Build Pipeline
- [ ] Create AI strategy


================================================================================
## ADDITIONAL NOTES

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



