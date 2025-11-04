package com.example.moodify.controller;

import com.example.moodify.dto.ResponseDTO;
import com.example.moodify.service.IeumService;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping(value = "/api", produces = MediaType.APPLICATION_JSON_VALUE)
public class ApiController {  //데이터 생성용 (FastAPI 호출)
    private final IeumService service;

    public ApiController(IeumService service) {
        this.service = service;
    }

    @GetMapping("/recommendations")
    public ResponseDTO showRecommendations() {
        return service.getSongs();
    }

    @PostMapping("/recommendations")
    public ResponseDTO getRecommendations() {
        return service.getSongs();
    }
}
