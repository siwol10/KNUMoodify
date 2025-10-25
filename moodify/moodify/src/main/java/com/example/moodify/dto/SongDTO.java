package com.example.moodify.dto;

public class SongDTO {
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
}
