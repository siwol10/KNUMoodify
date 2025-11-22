package com.example.moodify.controller;

import com.example.moodify.common.constans.Constant;
import com.example.moodify.dto.*;
import com.example.moodify.service.IeumService;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;
import java.util.*;
import java.util.stream.Collectors;

@Controller
@RequiredArgsConstructor
public class ViewController { //화면 표시용
    private final IeumService service;

    // 홈
    @GetMapping("/")
    public String home(Model model) {
        model.addAttribute("candidateEmotions", Constant.EMOTIONS);
        model.addAttribute("candidateSituations", Constant.SITUATIONS);
        System.out.println("log");
        return "home";
    }

    // 사용자 입력값 상황, 분석 여부 체크
    @GetMapping("/check/recommendations")
    public ResponseEntity<Map<String, Object>> checkRecommendations(@RequestParam String text) throws IOException {
        System.out.println("/check/recommendations");
        RequestDTO requestDTO = new RequestDTO();
        requestDTO.setText(text);
        ResponseDTO response = service.getAnalysisResultAndSongs(requestDTO);
        System.out.println("response : " + response);
        boolean hasEmotion = (null != response.getEmotions()) ? true : false;
        boolean hasSituation = (response.isSelection()) ? false : true;
        System.out.println("response: " + response);
        System.out.println("hasEmotion: " + hasEmotion);
        System.out.println("hasSituation: " + hasSituation);
        Map<String, Object> resp = new HashMap<>();
        resp.put("emotion", hasEmotion ? "Y" : "N");
        resp.put("situation", hasSituation ? "Y" : "N");
        resp.put("emotions", response.getEmotions());
        resp.put("response", response);
        return ResponseEntity.ok(resp);
    }


    // 팝업 -> 선택하여 재추천
    @PostMapping("/recommend") // <목록에 없는 상황이 입력된 경우> 선택한 상황에 따라 추천
    public String postRecommendations(
            @RequestParam(value = "text", required = true) String text,
            @RequestParam(value = "emotion", required = true) List<String> emotions, // 감정 선택한 경우
            @RequestParam(value = "situation", required = true) List<String> situations, // 상황 선택한 경우
            Model model) throws IOException {
        System.out.println("recommend");
        System.out.println("text : " + text);
        RequestDTO request = new RequestDTO();
        request.setText(text);
        request.setEmotions(emotions);
        request.setSituations(situations);

        List<SongDTO> songs = service.getSongs(request).getSongs();

        List<String> trackIds = songs.stream()
                .map(SongDTO::getId)
                .toList();

        model.addAttribute("songs", songs);
        model.addAttribute("inputText", text);
        model.addAttribute("emotions", emotions);
        model.addAttribute("situations", situations);
        model.addAttribute("trackIds", trackIds);

        return "result";

    }


    // 추천 결과
    @PostMapping("analyze-and-recommend") // 처음 입력 시 분석 + 추천(목록에 있는 감정/상황일 경우)
    public String analysisAndRecommendations(
            @RequestParam(value = "text", required = true) String text,
            @RequestParam(value = "analysisResult", required = true) String analysisResult,
            Model model) throws IOException {

        RequestDTO request = new RequestDTO();
        request.setText(text);
        ObjectMapper mapper = new ObjectMapper();
        ResponseDTO response = mapper.readValue(analysisResult, ResponseDTO.class);
        List<SongDTO> songs = response.getSongs();
        List<String> emotions = response.getEmotions();
        List<String> situations = response.getSituations();

        List<String> trackIds = songs.stream()
                .map(SongDTO::getId)
                .toList();

        model.addAttribute("songs", songs);
        model.addAttribute("inputText", text);
        model.addAttribute("emotions", emotions);
        model.addAttribute("situations", situations);
        model.addAttribute("trackIds", trackIds);
        return "result";
    }

}
