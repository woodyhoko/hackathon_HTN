# M(L)ove — AI Dance Coach

*Computer-vision–based choreography feedback system: pose estimation + cosine similarity scoring, built in 36 hours at Hack the North.*

**Ho Ko · Rabab Azeem · Nishtha Sharma** — Hack the North

📄 **[Project Slides](https://github.com/woodyhoko/hackathon_HTN/blob/main/Move.pdf)** | **[Presentation](https://github.com/woodyhoko/hackathon_HTN/blob/main/M(L)ove.pptx)** | **[▶ Live Demo](demo.html)**

---

## 1. The problem

Dance education went remote during COVID-19. Video platforms can deliver choreography — but they cannot deliver feedback. When learning from a YouTube tutorial, you can't tell whether your arm angle is off by 20°, your timing is a half-beat late, or your weight transfer is reversed. Human instructors catch these things frame by frame. Video platforms don't.

**M(L)ove** closes this gap with a two-video comparison pipeline: upload the reference choreography and your attempt, get a frame-by-frame similarity score that locates exactly where you diverge.

---

## 2. Technical approach

### 2.1 Pose estimation

Each video is processed frame-by-frame through a **pose estimation model** that outputs 17 body keypoints per frame (COCO keypoint schema: nose, eyes, ears, shoulders, elbows, wrists, hips, knees, ankles) as 2D pixel coordinates:

```
frame → pose_model → keypoints ∈ ℝ^{17×2}    (34 values per frame)
```

The keypoint vector is **mean-centered and L2-normalized** before comparison, making the similarity score invariant to the dancer's position in frame and body scale:

```python
kp = keypoints - keypoints.mean(axis=0)
kp = kp / (np.linalg.norm(kp) + 1e-6)
```

### 2.2 Temporal alignment

Before comparison, both videos are **resampled to the same frame rate** and optionally aligned with a cross-correlation offset to handle timing differences between the reference start and the dancer's start.

### 2.3 Cosine similarity scoring

For each aligned frame pair (reference **a**, student **b**):

```
score(t) = cos(â, b̂) = (â · b̂) / (||â|| · ||b̂||)    ∈ [−1, 1]
```

A score of **1.0** means perfect posture match. Near **0** means orthogonal (unrelated) body configurations. In practice, scores range from ~0.7 (rough match) to ~0.98 (near-perfect). The average score over all frames is reported as a final performance grade.

### 2.4 Per-joint breakdown

Beyond the holistic cosine score, per-joint Euclidean distances identify *which body part* diverges most:

```python
joint_error[j] = ||kp_ref[j] − kp_stu[j]||₂    for j in 0..16
```

High error on joint 9 (left wrist) means the left arm movement needs work; high error on joints 13–16 (knees, ankles) means footwork is off.

---

## 3. System architecture

```
Flask + Plotly Dash (web UI)
    │
    ├── POST /upload-video
    │       ├── imageio: decode both videos frame-by-frame
    │       ├── pose_model: extract 34-value keypoint vector per frame
    │       ├── NumPy: center, normalize, compute cosine similarity
    │       ├── OpenCV: render skeleton overlay on output frames
    │       └── ffmpeg: encode annotated output videos
    │
    └── GET /view-video
            ├── Plotly: score timeline chart
            └── Average score + per-joint breakdown table
```

---

## 4. Stack

| Component | Technology |
|---|---|
| Web framework | Plotly Dash + Flask |
| Pose estimation | Custom `image_demp` module |
| Video I/O | imageio + ffmpeg |
| Frame processing | OpenCV (cv2) |
| Similarity scoring | NumPy (cosine similarity, broadcasting) |
| Deployment | Heroku (Procfile included) |

---

## 5. Run locally

```bash
pip install dash flask opencv-python imageio numpy pandas matplotlib
python app.py
# open http://localhost:8050
```

Upload two dance videos via the web interface. Processing time is roughly equal to the video length (30-second video ≈ 30–60 seconds to analyze).

---

## 6. Files

| File | Description |
|---|---|
| `app.py` | Main application — Dash UI + Flask video processing routes |
| `Move.pdf` | Project concept and pitch deck |
| `M(L)ove.pptx` | Hackathon presentation slides |
| `Procfile` | Heroku deployment config |
| `demo.html` | Browser demo — animated skeleton pose comparison |

---

## 7. Limitations & future work

- **2D pose only** — depth ambiguity means the 2D keypoints cannot distinguish, e.g., an arm raised toward the camera vs. to the side. A 3D pose model (e.g. VideoPose3D) would resolve this.
- **Rigid temporal alignment** — cross-correlation alignment handles a constant offset but not tempo variation (the student dancing slightly faster or slower throughout).
- **No audio synchronization** — beat-matched alignment using the audio track's BPM would dramatically improve temporal correspondence.
- **Per-joint feedback UI** — a color-coded skeleton overlay highlighting problem joints in red/green would make the feedback more actionable.
