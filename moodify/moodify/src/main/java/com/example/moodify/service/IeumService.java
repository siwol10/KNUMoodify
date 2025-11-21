package com.example.moodify.service;

import com.example.moodify.dto.PlaylistRequestDTO;
import com.example.moodify.dto.LoginResponseDTO;
import com.example.moodify.dto.RequestDTO;
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

    public ResponseDTO getAnalysisResultAndSongs(RequestDTO requestDTO) { // 처음 입력 시 분석 + 추천(목록에 있는 감정/상황일 경우)
        return fastApi.post()
                .uri("/analyze-and-recommend")
                .accept(MediaType.APPLICATION_JSON)
                .bodyValue(requestDTO)
                .retrieve()
                .bodyToMono(ResponseDTO.class)
                .block();
    }

    public ResponseDTO getSongs(RequestDTO requestDTO) { // <목록에 없는 상황이 입력된 경우> 선택한 상황에 따라 추천
        return fastApi.post()
                .uri("/recommend")
                .accept(MediaType.APPLICATION_JSON)
                .bodyValue(requestDTO)
                .retrieve()
                .bodyToMono(ResponseDTO.class)
                .block();
    }

    public LoginResponseDTO startSpotifyLogin(PlaylistRequestDTO playlistRequestDTO) { // 스포티파이에 플레이리스트 생성
        return fastApi.post()
                .uri("/spotify-login")
                .bodyValue(playlistRequestDTO)
                .retrieve()
                .bodyToMono(LoginResponseDTO.class)
                .block();
    }
}
