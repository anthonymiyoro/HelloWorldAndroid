package am.moviepredictorai.controllers;

import org.springframework.web.bind.annotation.*;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;


@Controller
public class HomeController {
//    View that adds name to greeting
    @GetMapping("/greeting1")
        public String greeting(@RequestParam(name="name", required=false, defaultValue="World") String name, Model model){
        model.addAttribute("name", name);
        return "greeting1";
    }

    @GetMapping("/greeting")
    public String greetingForm(Model model){
        model.addAttribute("greeting", new Greeting());
        return "greeting";
    }

    @PostMapping("/greeting")
    public String greetingSubmit(@ModelAttribute Greeting greeting){
        return "result";
    }
}
