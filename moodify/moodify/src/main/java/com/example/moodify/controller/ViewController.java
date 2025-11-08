package com.example.moodify.controller;

import com.example.moodify.common.constans.Constant;
import com.example.moodify.dto.SongDTO;
import com.example.moodify.service.TestService;
import io.netty.util.internal.StringUtil;
import lombok.RequiredArgsConstructor;
import org.springframework.context.annotation.Profile;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;
import java.util.*;
import java.util.function.BinaryOperator;
import java.util.stream.Collectors;

@Controller
@Profile("test")  // 웹 화면 테스트용
@RequiredArgsConstructor
public class ViewController { //화면 표시용
    private final TestService testService;

    @GetMapping("/")
    public String home(Model model) {
        model.addAttribute("candidateEmotions", Constant.EMOTIONS);
        model.addAttribute("candidateSituations", Constant.SITUATIONS);
        System.out.println("log");
        return "home";
    }

    @GetMapping("/recommendations")
    public String recommendations(Model model) throws IOException {
        List<SongDTO> songs = testService.read().getSongs();
        System.out.println(songs.toString());
        model.addAttribute("songs", songs);

        return "result"; // 추천 결과 화면 템플릿
    }

    @GetMapping("/check/recommendations")
    public ResponseEntity<Map<String, String>> checkRecommendations(@RequestParam String text) throws IOException {
        System.out.println("호출 테스트");
        // 아래 코드 -> 서비스로 뺴야됨
//        List<SongDTO> songs = testService.read().getSongs(); // 추후에 text로 변경해야됨
        boolean hasEmotion = false;
        boolean hasSituation = false;


        Map<String, String> resp = new HashMap<>();
        resp.put("emotion", hasEmotion ? "Y" : "N");
        resp.put("situation", hasSituation ? "Y" : "N");
        return ResponseEntity.ok(resp);
    }

    @PostMapping("/recommendations")
    public String postRecommendations(
            @RequestParam(value = "text", required = false) String text,
            @RequestParam(value = "emotion", required = false) String emotion, // 감정 선택한 경우
            @RequestParam(value = "situation", required = false) String situation, // 상황 선택한 경우
            Model model) throws IOException {

        System.out.println("text : " + text);
        System.out.println("emotion : " + emotion);
        System.out.println("situation : " + situation);
        List<SongDTO> songs = testService.read().getSongs();
        Set<String> uniqueEmotions = getUniqueEmotions(songs);
        Set<String> activeSituation = getActiveSituation(songs);
        System.out.println("uniqueEmotions : " +uniqueEmotions.toString());
        System.out.println("activeSituation : " +activeSituation.toString());


        model.addAttribute("emotions", uniqueEmotions);
        model.addAttribute("situations", activeSituation);
        model.addAttribute("songs", songs);
        model.addAttribute("inputText",text);
        return "result";
    }

    /**
     * 감정 중복제거
     * @param songs
     * @return
     */
    private Set<String> getUniqueEmotions(List<SongDTO> songs) {
        Set<String> uniqueEmotions = songs.stream()
                .map(SongDTO::getEmotion)
                .collect(Collectors.toSet());
        return uniqueEmotions;

    }

    private Set<String> getActiveSituation(List<SongDTO> songs) {
        Set<String> activeFields = new HashSet<>();
        for (SongDTO song : songs) {
            if (song.getParty() == 1) activeFields.add("party");
            if (song.getWork() == 1) activeFields.add("work");
            if (song.getRelaxation() == 1) activeFields.add("relaxation");
            if (song.getExercise() == 1) activeFields.add("exercise");
            if (song.getRunning() == 1) activeFields.add("running");
            if (song.getStretching() == 1) activeFields.add("stretching");
            if (song.getDriving() == 1) activeFields.add("driving");
            if (song.getGathering() == 1) activeFields.add("gathering");
            if (song.getMorning() == 1) activeFields.add("morning");
        }
        return activeFields;
    }


}
