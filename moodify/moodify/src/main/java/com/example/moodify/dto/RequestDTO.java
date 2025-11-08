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

    // 첫 입력 시에는 text = 사용자 입력, emotions = None, situation = None으로 넘어감
    // 감정/상황 분석 후, 상황이 목록에 없다면 text = 사용자 입력, emotions = 감정 분석 결과, situations = None?으로 넘어옴
    // 상황 선택 후 다시 text = 사용자 입력, emotions = 감정 분석 결과, situations = 선택한 상황으로 넘어감
}
