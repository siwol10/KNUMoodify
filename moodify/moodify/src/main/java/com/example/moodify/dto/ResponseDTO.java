package com.example.moodify.dto;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.List;

@Getter
@Setter
@NoArgsConstructor
public class ResponseDTO {
    private boolean selection;
    private List<String> emotions;
    private List<String> situations;
    private List<SongDTO> songs;
}
