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
}
