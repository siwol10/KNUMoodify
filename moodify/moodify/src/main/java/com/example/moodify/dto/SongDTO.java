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

/*
    private String title;
    private String artist;
    private String image;      // 썸네일 URL
    private String spotifyUrl; // 외부 링크

    public SongDTO() {}

    public SongDTO(String title, String artist, String image, String spotifyUrl) {
        this.title = title;
        this.artist = artist;
        this.image = image;
        this.spotifyUrl = spotifyUrl;
    }

    public String getTitle() { return title; }
    public String getArtist() { return artist; }
    public String getImage() { return image; }
    public String getSpotifyUrl() { return spotifyUrl; }

    public void setTitle(String title) { this.title = title; }
    public void setArtist(String artist) { this.artist = artist; }
    public void setImage(String image) { this.image = image; }
    public void setSpotifyUrl(String spotifyUrl) { this.spotifyUrl = spotifyUrl; }
*/
}
