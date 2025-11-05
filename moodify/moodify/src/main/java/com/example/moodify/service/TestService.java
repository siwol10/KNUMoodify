package com.example.moodify.service;

import com.example.moodify.dto.ResponseDTO;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.context.annotation.Profile;
import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Service;

import java.io.IOException;

@Service
@Profile("test")
@RequiredArgsConstructor
public class TestService {
    private final ObjectMapper objectMapper;

    public ResponseDTO read() throws IOException {
        try (var in = new ClassPathResource("test/sample_songs.json").getInputStream()) {
            return objectMapper.readValue(in, ResponseDTO.class);
        }
    }
}
