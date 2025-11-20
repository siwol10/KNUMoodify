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
    private String id; // 해당 곡 ID
    private String url; // 해당 곡으로 연결되는 링크

    @Override
    public String toString() {
        return "SongDTO{" +
                "artist='" + artist + '\'' +
                ", title='" + title + '\'' +
                ", emotion='" + emotion + '\'' +
                ", length='" + length + '\'' +
                ", isrc='" + isrc + '\'' +
                ", party=" + party +
                ", work=" + work +
                ", relaxation=" + relaxation +
                ", exercise=" + exercise +
                ", running=" + running +
                ", stretching=" + stretching +
                ", driving=" + driving +
                ", gathering=" + gathering +
                ", morning=" + morning +
                ", id=" + id +
                ", url=" + url +
                '}';
    }
}
