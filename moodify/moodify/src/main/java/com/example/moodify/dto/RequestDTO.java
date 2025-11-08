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
}
