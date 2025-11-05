package com.example.moodify.controller;

import com.example.moodify.dto.ResponseDTO;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.context.annotation.Profile;
import org.springframework.core.io.ClassPathResource;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.io.IOException;
@Profile("test")
@RestController
@RequestMapping(value = "/test", produces = MediaType.APPLICATION_JSON_VALUE)
@RequiredArgsConstructor
public class TestController { // FastAPI 연동 X (웹 화면 개발 테스트용)
    private final ObjectMapper objectMapper;

    @GetMapping("/recommendations")
    public ResponseDTO get() throws IOException {
        try (var in = new ClassPathResource("test/sample_songs.json").getInputStream()) {
            return objectMapper.readValue(in, ResponseDTO.class);
        }
    }
}

