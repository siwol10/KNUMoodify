package com.example.moodify.controller;

import com.example.moodify.dto.RequestDTO;
import com.example.moodify.dto.ResponseDTO;
import com.example.moodify.service.IeumService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;


@RestController
@RequestMapping(value = "/api", produces = MediaType.APPLICATION_JSON_VALUE)
@RequiredArgsConstructor
public class ApiController {  //데이터 생성용 (FastAPI 호출)
    private final IeumService service;

    @PostMapping("/analyze-and-recommend") // 처음 입력 시 분석 + 추천(목록에 있는 감정/상황일 경우)
    public ResponseDTO getAnalysisAndRecommendations(@RequestBody RequestDTO requestDTO) {
        return service.getAnalysisResultAndSongs(requestDTO);
    }

    @PostMapping("/recommend") // <목록에 없는 상황이 입력된 경우> 선택한 상황에 따라 추천
    public ResponseDTO getRecommendations(@RequestBody RequestDTO requestDTO) {
        return service.getAnalysisResultAndSongs(requestDTO);
    }
}
