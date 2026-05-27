# M(L)ove — Dance Scoring via Pose Estimation

**Hack the North hackathon project.** A web app that compares two dance videos and generates a **frame-by-frame similarity score** using body pose keypoints and cosine similarity.

📄 **[Read the Proposal](https://github.com/woodyhoko/hackathon_HTN/blob/main/Move.pdf)**

---

## How It Works

1. **Upload two videos** — e.g. the original choreography and a learner's attempt
2. The server processes both with a **pose estimation model** (extracting 17-point skeleton per frame)
3. Per-frame **cosine similarity** between skeleton vectors produces a dance score timeline
4. Results are rendered as a score graph and overlaid on the output videos

```
Video 1 ──► Pose Extraction ──► Skeleton Vectors ──┐
                                                     ├──► Cosine Similarity ──► Score Timeline
Video 2 ──► Pose Extraction ──► Skeleton Vectors ──┘
```

---

## Stack

| Layer | Technology |
|---|---|
| Web Framework | [Plotly Dash](https://dash.plotly.com/) + Flask |
| Pose Estimation | Custom pose model (`image_demp` module) |
| Video Processing | OpenCV, imageio, ffmpeg |
| Scoring | NumPy cosine similarity |
| Hosting | Heroku (`Procfile` included) |

---

## Repository Contents

| File | Description |
|---|---|
| `app.py` | Main Dash/Flask application |
| `Move.pdf` | Project proposal and design doc |
| `M(L)ove.pptx` | Hackathon presentation slides |

---

## Run Locally

```bash
pip install dash flask opencv-python imageio numpy pandas
python app.py
# open http://localhost:8050
```

