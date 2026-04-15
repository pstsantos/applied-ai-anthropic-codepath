# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Each **Song** in the catalog carries ten attributes: a unique id, title, and artist name, plus seven musical features — genre, mood, energy level (0–1), tempo in BPM, valence (how positive the song feels, 0–1), danceability (0–1), and acousticness (0–1).

A **UserProfile** stores what the listener cares about: their favourite genres, favourite moods, target energy level, target valence, target danceability, target tempo, and whether they lean toward acoustic music.

### Algorithm Recipe

#### Scoring Rule — rating one song at a time

When the recommender looks at a single song, it computes a weighted score across three priority tiers:

| Priority | Feature | Weight | How it's calculated |
|---|---|---|---|
| P1 | Mood match | 0.17 | Binary — 1 if song mood is in user's mood list, else 0 |
| P1 | Genre match | 0.13 | Binary — 1 if song genre is in user's genre list, else 0 |
| P2 | Energy distance | 0.175 | `1 - abs(song.energy - target_energy)` |
| P2 | Valence distance | 0.175 | `1 - abs(song.valence - target_valence)` |
| P3 | Danceability distance | 0.15 | `1 - abs(song.danceability - target_danceability)` |
| P3 | Tempo distance | 0.15 | Tempo normalised to 0–1 before subtracting |
| Penalty | Acoustic penalty | up to −0.10 | `acousticness × 0.10` subtracted when user dislikes acoustic |

**P1 total: 30% · P2 total: 35% · P3 total: 30%**

Key design decisions:
- **Mood is weighted above genre** — mood crosses genre lines more naturally. A user who wants something "nostalgic" can find that in rock, pop, or jazz.
- **P2 carries the most weight** — energy and valence are the core of discovery. A song from an unexpected genre can surface if it *feels* right.
- **No hard genre filter** — songs outside the user's stated genres are not excluded, only nudged down. This preserves the exploration aspect of music discovery.

#### Ranking Rule — choosing what to surface

Once every song has a score, the system applies four steps to decide the final list:

1. **Top-K selection** — keep only the highest-scoring songs (default K = 5)
2. **Diversity** — cap the number of songs per artist to avoid the list being dominated by one act
3. **Tie-breaking** — when two songs have equal scores, prefer higher valence as a tiebreaker
4. **Filters** — songs the user has already heard can be excluded before ranking begins

The final output is an ordered list of songs, each paired with its score and a plain-language explanation of why it was recommended.

### Expected Biases

- **Mood over genre** — because mood is weighted higher than genre, the system may surface songs from genres the user didn't list if the emotional tone is close. This is intentional for discovery but could feel surprising.
- **Energy and valence centrality** — P2 has the highest total weight, so songs that match the user's energy and emotional target will rank highly even when genre and mood miss. This may over-reward "feeling right" at the expense of stylistic fit.
- **Catalog skew** — the 20-song catalog is not evenly distributed across genres and moods. Genres with more representation (e.g. pop, rock) will appear in results more often simply because there are more candidates to score well.
- **Acoustic users are underserved** — the acoustic penalty only applies when `likes_acoustic = False`. There is no equivalent boost for users who actively prefer acoustic music, which creates an asymmetry.

---

## Sample Output

Running `python -m src.main` with the default taste profile (`genre: [pop, indie pop]`, `mood: [happy, nostalgic]`, `target_energy: 0.80`) produces:

```
==================================================
  Top 5 Recommendations for You
==================================================

#1  Sunrise City — Neon Echo
    Genre: pop  |  Mood: happy
    Score: 0.92
    Why:   mood match — happy (+0.17) · genre match — pop (+0.13) · energy fit (+0.17) · valence fit (+0.17) · danceability fit (+0.15) · tempo fit (+0.15) · acoustic penalty (-0.02)

#2  Rooftop Lights — Indigo Parade
    Genre: indie pop  |  Mood: happy
    Score: 0.89
    Why:   mood match — happy (+0.17) · genre match — indie pop (+0.13) · energy fit (+0.15) · valence fit (+0.17) · danceability fit (+0.15) · tempo fit (+0.15) · acoustic penalty (-0.03)

#3  Shape of You — Ed Sheeran
    Genre: pop  |  Mood: happy
    Score: 0.88
    Why:   mood match — happy (+0.17) · genre match — pop (+0.13) · energy fit (+0.15) · valence fit (+0.16) · danceability fit (+0.15) · tempo fit (+0.15) · acoustic penalty (-0.03)

#4  Blinding Lights — The Weeknd
    Genre: pop  |  Mood: nostalgic
    Score: 0.73
    Why:   mood match — nostalgic (+0.17) · genre match — pop (+0.13) · energy fit (+0.16) · valence fit (+0.12) · danceability fit (+0.11) · tempo fit (+0.10)

#5  Gym Hero — Max Pulse
    Genre: pop  |  Mood: intense
    Score: 0.71
    Why:   genre match — pop (+0.13) · energy fit (+0.15) · valence fit (+0.14) · danceability fit (+0.15) · tempo fit (+0.14)

==================================================
```

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

