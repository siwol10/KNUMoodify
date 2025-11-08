package com.example.moodify.dto;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.List;

@Getter
@Setter
@NoArgsConstructor
public class RequestDTO {
    private String text;
    private List<String> emotions;
    private List<String> situations;

    // 첫 입력 시: text = 사용자 입력, emotions = None, situation = None
    // 상황 목록에서 선택: text = 사용자 입력, emotions = [감정 분석 결과], situations = [선택한 상황]
}
