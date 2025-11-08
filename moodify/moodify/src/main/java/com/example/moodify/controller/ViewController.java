package com.example.moodify.controller;

import com.example.moodify.common.constans.Constant;
import com.example.moodify.dto.RequestDTO;
import com.example.moodify.dto.ResponseDTO;
import com.example.moodify.dto.SongDTO;
import com.example.moodify.service.IeumService;
import com.example.moodify.service.TestService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;
import java.util.*;
import java.util.stream.Collectors;

@Controller
//@Profile("test")  // 웹 화면 테스트용
@RequiredArgsConstructor
public class ViewController { //화면 표시용
    private final TestService testService;
    private final IeumService service;

    @GetMapping("/")
    public String home(Model model) {
        model.addAttribute("candidateEmotions", Constant.EMOTIONS);
        model.addAttribute("candidateSituations", Constant.SITUATIONS);
        System.out.println("log");
        return "home";
    }
/*
    @GetMapping("/recommendations")
    public String recommendations(Model model) throws IOException {
        List<SongDTO> songs = testService.read().getSongs();
        System.out.println(songs.toString());
        model.addAttribute("songs", songs);


        return "result"; // 추천 결과 화면 템플릿
    }*/

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

    @PostMapping("analyze-and-recommend") // 처음 입력 시 분석 + 추천(목록에 있는 감정/상황일 경우)
    public String analysisAndRecommendations(@RequestParam(value = "text", required = false) String text, Model model) throws IOException{
        RequestDTO requestDTO = new RequestDTO();
        requestDTO.setText(text);

        ResponseDTO response = service.getAnalysisResultAndSongs(requestDTO);
        if (response.isSelection()) { // 목록에 없는 상황이 입력된 경우 -> 상황 선택
            List<String> emotions = response.getEmotions();
            List<String> situations = response.getSituations();

            model.addAttribute("inputText", text);
            model.addAttribute("emotions", emotions);
            //model.addAttribute("situations", situations);

            return "home"; // 상황 선택할 페이지 (상황 선택 후 /recommend로 이동하면 됨)
        } else {  // 목록에 있는 상황/감정 -> 추천 리스트 보여줌
            List<SongDTO> songs = response.getSongs();
            List<String> emotions = response.getEmotions();
            List<String> situations = response.getSituations();

            /*
            Set<String> uniqueEmotions = getUniqueEmotions(songs);
            Set<String> activeSituation = getActiveSituation(songs);
            System.out.println("uniqueEmotions : " + uniqueEmotions.toString());
            System.out.println("activeSituation : " + activeSituation.toString());

            model.addAttribute("emotions", uniqueEmotions);
            model.addAttribute("situations", activeSituation);
            */

            model.addAttribute("songs", songs);
            model.addAttribute("inputText", text);
            model.addAttribute("emotions", emotions);
            model.addAttribute("situations", situations);

            return "result";
        }

    }

    @PostMapping("/recommend") // <목록에 없는 상황이 입력된 경우> 선택한 상황에 따라 추천
    public String postRecommendations(
            @RequestParam(value = "text", required = false) String text,
            @RequestParam(value = "emotion", required = false) List<String> emotions, // 감정 선택한 경우
            @RequestParam(value = "situation", required = false) List<String> situations, // 상황 선택한 경우
            Model model) throws IOException {

        RequestDTO requestDTO = new RequestDTO();
        requestDTO.setText(text);
        requestDTO.setEmotions(emotions);
        requestDTO.setSituations(situations);

        List<SongDTO> songs = service.getSongs(requestDTO).getSongs();
        model.addAttribute("songs", songs);
        model.addAttribute("inputText", text);
        model.addAttribute("emotions", emotions);
        model.addAttribute("situations", situations);


        /*
        System.out.println("text : " + text);
        System.out.println("emotion : " + emotion);
        System.out.println("situation : " + situation);

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
        */

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
