package com.example.moodify.dto;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
public class PlaylistResponseDTO {
    private String authorize_url; // 스포티파이 로그인 + 권한 동의
}
