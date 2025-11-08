package com.example.moodify.service;

import com.example.moodify.dto.ResponseDTO;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

@Service
public class IeumService {
    private final WebClient fastApi;

    public IeumService(WebClient.Builder fastApiWebClient) {
        this.fastApi = fastApiWebClient.baseUrl("http://localhost:8000").build();
    }

    public ResponseDTO getSongs() {
        return fastApi.post()
                .uri("/recommendations")
                .accept(MediaType.APPLICATION_JSON)
                .retrieve()
                .bodyToMono(ResponseDTO.class)
                .block(); //mono
    }

}
