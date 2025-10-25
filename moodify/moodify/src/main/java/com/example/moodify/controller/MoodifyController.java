package com.example.moodify.controller;

import com.example.moodify.dto.SongDTO;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.List;

@Controller
public class MoodifyController {
    @GetMapping("/")
    public String home() {
        return "home";
    }

    @PostMapping("/analyze")
    public String analyze(@RequestParam("text") String userText, Model model) {
        // ▼ TODO: 여기에 실제 감정/상황 분석 로직을 붙이면 됩니다.
        String emotion   = "sadness";
        String situation = "party";

        // ▼ 예시 추천곡 (스텁)
        List<SongDTO> songs = List.of(
                new SongDTO(
                        "봄날", "BTS",
                        "https://i.scdn.co/image/ab67616d0000b273a92e7b99b0f6f1af97d9f1a6",
                        "https://open.spotify.com/track/2m6Ko3CY1qXNNja8AlugNc"
                ),
                new SongDTO(
                        "Blue & Grey", "BTS",
                        "https://i.scdn.co/image/ab67616d0000b2738ea26e1531e5a3bfa2a343b2",
                        "https://open.spotify.com/track/4hDok0OAJd57SGIT8xuWJH"
                ),
                new SongDTO(
                        "Someone Like You", "Adele",
                        "https://i.scdn.co/image/ab67616d0000b273a5c2b3a2ee6f4b4c8bdb0f20",
                        "https://open.spotify.com/track/4kflIGfjdZJW4ot2ioixTB"
                ),
                new SongDTO(
                        "Someone Like You", "Adele",
                        "https://i.scdn.co/image/ab67616d0000b273a5c2b3a2ee6f4b4c8bdb0f20",
                        "https://open.spotify.com/track/4kflIGfjdZJW4ot2ioixTB"
                ),
                new SongDTO(
                        "Someone Like You", "Adele",
                        "https://i.scdn.co/image/ab67616d0000b273a5c2b3a2ee6f4b4c8bdb0f20",
                        "https://open.spotify.com/track/4kflIGfjdZJW4ot2ioixTB"
                ),
                new SongDTO(
                        "Someone Like You", "Adele",
                        "https://i.scdn.co/image/ab67616d0000b273a5c2b3a2ee6f4b4c8bdb0f20",
                        "https://open.spotify.com/track/4kflIGfjdZJW4ot2ioixTB"
                ),
                new SongDTO(
                        "Someone Like You", "Adele",
                        "https://i.scdn.co/image/ab67616d0000b273a5c2b3a2ee6f4b4c8bdb0f20",
                        "https://open.spotify.com/track/4kflIGfjdZJW4ot2ioixTB"
                ),
                new SongDTO(
                        "Someone Like You", "Adele",
                        "https://i.scdn.co/image/ab67616d0000b273a5c2b3a2ee6f4b4c8bdb0f20",
                        "https://open.spotify.com/track/4kflIGfjdZJW4ot2ioixTB"
                ),
                new SongDTO(
                        "Someone Like You", "Adele",
                        "https://i.scdn.co/image/ab67616d0000b273a5c2b3a2ee6f4b4c8bdb0f20",
                        "https://open.spotify.com/track/4kflIGfjdZJW4ot2ioixTB"
                ),
                new SongDTO(
                        "Someone Like You", "Adele",
                        "https://i.scdn.co/image/ab67616d0000b273a5c2b3a2ee6f4b4c8bdb0f20",
                        "https://open.spotify.com/track/4kflIGfjdZJW4ot2ioixTB"
                ),
                new SongDTO(
                        "Someone Like You", "Adele",
                        "https://i.scdn.co/image/ab67616d0000b273a5c2b3a2ee6f4b4c8bdb0f20",
                        "https://open.spotify.com/track/4kflIGfjdZJW4ot2ioixTB"
                ),
                new SongDTO(
                        "Someone Like You", "Adele",
                        "https://i.scdn.co/image/ab67616d0000b273a5c2b3a2ee6f4b4c8bdb0f20",
                        "https://open.spotify.com/track/4kflIGfjdZJW4ot2ioixTB"
                ),
                new SongDTO(
                        "Someone Like You", "Adele",
                        "https://i.scdn.co/image/ab67616d0000b273a5c2b3a2ee6f4b4c8bdb0f20",
                        "https://open.spotify.com/track/4kflIGfjdZJW4ot2ioixTB"
                ),
                new SongDTO(
                        "Someone Like You", "Adele",
                        "https://i.scdn.co/image/ab67616d0000b273a5c2b3a2ee6f4b4c8bdb0f20",
                        "https://open.spotify.com/track/4kflIGfjdZJW4ot2ioixTB"
                ),
                new SongDTO(
                        "Someone Like You", "Adele",
                        "https://i.scdn.co/image/ab67616d0000b273a5c2b3a2ee6f4b4c8bdb0f20",
                        "https://open.spotify.com/track/4kflIGfjdZJW4ot2ioixTB"
                ),
                new SongDTO(
                        "Someone Like You", "Adele",
                        "https://i.scdn.co/image/ab67616d0000b273a5c2b3a2ee6f4b4c8bdb0f20",
                        "https://open.spotify.com/track/4kflIGfjdZJW4ot2ioixTB"
                ),
                new SongDTO(
                        "Someone Like You", "Adele",
                        "https://i.scdn.co/image/ab67616d0000b273a5c2b3a2ee6f4b4c8bdb0f20",
                        "https://open.spotify.com/track/4kflIGfjdZJW4ot2ioixTB"
                ),
                new SongDTO(
                        "Someone Like You", "Adele",
                        "https://i.scdn.co/image/ab67616d0000b273a5c2b3a2ee6f4b4c8bdb0f20",
                        "https://open.spotify.com/track/4kflIGfjdZJW4ot2ioixTB"
                ),
                new SongDTO(
                        "Someone Like You", "Adele",
                        "https://i.scdn.co/image/ab67616d0000b273a5c2b3a2ee6f4b4c8bdb0f20",
                        "https://open.spotify.com/track/4kflIGfjdZJW4ot2ioixTB"
                ),
                new SongDTO(
                        "Someone Like You", "Adele",
                        "https://i.scdn.co/image/ab67616d0000b273a5c2b3a2ee6f4b4c8bdb0f20",
                        "https://open.spotify.com/track/4kflIGfjdZJW4ot2ioixTB"
                ),
                new SongDTO(
                        "Someone Like You", "Adele",
                        "https://i.scdn.co/image/ab67616d0000b273a5c2b3a2ee6f4b4c8bdb0f20",
                        "https://open.spotify.com/track/4kflIGfjdZJW4ot2ioixTB"
                )
        );

        model.addAttribute("userText", userText);
        model.addAttribute("emotion", emotion);
        model.addAttribute("situation", situation);
        model.addAttribute("songs", songs);

        return "result"; // templates/result.html
    }
}
