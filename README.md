# M(L)ove — AI Dance Coach

**Ho Ko · Rabab Azeem · Nishtha Sharma** — Hack the North

📄 **[Project Slides](https://github.com/woodyhoko/hackathon_HTN/blob/main/Move.pdf)** | **[Presentation](https://github.com/woodyhoko/hackathon_HTN/blob/main/M(L)ove.pptx)**

---

## The Problem

Dance education went fully remote during COVID-19. Online studios and video platforms have filled the gap, but they lack one critical thing: **objective, personalized feedback on technique**.

When learning choreography from YouTube, you can't tell if your arms are at the right angle, your timing is off by half a beat, or your weight transfer is wrong. Human teachers catch these things instantly. Video platforms don't.

---

## The Solution

Upload two videos — the **official choreography** and **your attempt** — and M(L)ove generates a frame-by-frame similarity score that tells you exactly where you match, and where you diverge.

```
Official Choreography Video ──► Pose Extraction ──► Skeleton Keypoints ──┐
                                                                           ├──► Cosine Similarity
Your Dance Video ─────────────► Pose Extraction ──► Skeleton Keypoints ──┘
                                                                           │
                                                                           ▼
                                                                    Score Timeline Graph
                                                                    + Annotated Output Videos
```

---

## How It Works

### Step 1 — Pose Extraction

Both videos are processed frame-by-frame using a pose estimation model that extracts **body skeleton keypoints** (34 values per frame — 17 joints × 2D coordinates). This converts the visual dance into a numerical representation of body position.

### Step 2 — Cosine Similarity Scoring

For each aligned frame pair, the skeleton vectors from both videos are compared using **cosine similarity**:

```python
score[frame] = dot(pose_a, pose_b) / (norm(pose_a) × norm(pose_b))
```

Score of 1.0 = perfect match. Score near 0 = misaligned posture.

### Step 3 — Visualization

- A matplotlib chart shows the score timeline — easy to see which parts of the choreography need work
- Both videos are rendered as annotated output files (skeleton overlaid)
- Average score summarized as a final performance grade

---

## System Architecture

```
Flask + Plotly Dash
    │
    ├── /upload-video  (POST)
    │       │
    │       ├── imageio: decode both videos frame-by-frame
    │       ├── image_demp: run pose estimation on each frame
    │       ├── NumPy: compute per-frame cosine similarity
    │       ├── OpenCV: render skeleton overlay onto frames
    │       └── ffmpeg: encode annotated output videos
    │
    └── /view-video  (GET)
            └── Displays score chart + average score
```

---

## Stack

| Component | Technology |
|---|---|
| Web framework | [Plotly Dash](https://dash.plotly.com/) + Flask |
| Pose estimation | Custom `image_demp` module |
| Video I/O | imageio + ffmpeg |
| Frame processing | OpenCV (cv2) |
| Scoring | NumPy (cosine similarity) |
| Hosting | Heroku (Procfile included) |

---

## Run Locally

```bash
pip install dash flask opencv-python imageio numpy pandas matplotlib
python app.py
# open http://localhost:8050
```

Upload two dance videos via the web interface. Processing time scales with video length — a 30-second video takes roughly 30–60 seconds to analyze.

---

## Files

| File | Description |
|---|---|
| `app.py` | Main application — Dash UI + Flask video processing routes |
| `Move.pdf` | Project concept and pitch deck |
| `M(L)ove.pptx` | Hackathon presentation slides |
| `Procfile` | Heroku deployment config |
