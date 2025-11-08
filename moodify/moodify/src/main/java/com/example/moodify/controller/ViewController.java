package com.example.moodify.controller;

import com.example.moodify.service.TestService;
import lombok.RequiredArgsConstructor;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;

@Controller
@Profile("test")  // 웹 화면 테스트용
@RequiredArgsConstructor
public class ViewController { //화면 표시용
    private final TestService testService;

    @GetMapping("/")
    public String home() {
        return "home";
    }

    @GetMapping("/recommendations")
    public String recommendations(Model model) throws IOException {
        model.addAttribute("songs", testService.read().getSongs());
        return "result"; // 추천 결과 화면 템플릿
    }

    @PostMapping("/recommendations")
    public String postRecommendations(@RequestParam("text") String text, Model model) throws IOException {
        model.addAttribute("songs", testService.read().getSongs());
        model.addAttribute("inputText",text);

//        model.addAttribute("needsSelection", true);
//
//        // 모달에 표시될 감정/상황 후보 (하드코딩)
//        model.addAttribute("candidateEmotions",
//                java.util.List.of("joy", "anger", "fear", "sadness", "surprise"));
//        model.addAttribute("candidateSituations",
//                java.util.List.of("party", "work", "relaxation", "exercise", "running", "stretching", "driving", "gathering", "morning"));
//
//        // 노래 리스트는 비워두기
//        model.addAttribute("songs", java.util.Collections.emptyList());
        return "result";
    }
}
