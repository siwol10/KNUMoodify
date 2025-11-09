package com.example.moodify.dto;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.List;

@Getter
@Setter
@NoArgsConstructor
public class ResponseDTO {
    private boolean selection;  // 상황이 목록에 없을 때(상황 선택 필요하면) True
    private List<String> emotions;
    private List<String> situations;
    private List<SongDTO> songs;

    // 상황이 목록에 없을 때: selection = true, emotions = [감정 분석 결과], situations = None?, songs = None
    // 상황이 목록에 있을 때: selection = false, emotions = [감정 분석 결과], situations = [상황 분석 결과], songs = 추천곡 리스트


    @Override
    public String toString() {
        return "ResponseDTO{" +
                "selection=" + selection +
                ", emotions=" + emotions +
                ", situations=" + situations +
                ", songs=" + songs +
                '}';
    }
}
