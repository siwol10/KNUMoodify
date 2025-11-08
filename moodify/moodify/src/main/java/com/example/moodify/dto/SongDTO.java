package com.example.moodify.dto;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
public class SongDTO {
    private String artist;
    private String title;
    private String emotion;
    private String length;
    private String isrc;
    private int party;
    private int work;
    private int relaxation;
    private int exercise;
    private int running;
    private int stretching;
    private int driving;
    private int gathering;
    private int morning;
}
