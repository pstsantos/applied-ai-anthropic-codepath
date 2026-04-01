# Model Card: Mood Machine

This model card is for the Mood Machine project, which includes **two** versions of a mood classifier:

1. A **rule based model** implemented in `mood_analyzer.py`
2. A **machine learning model** implemented in `ml_experiments.py` using scikit learn

## 1. Model Overview

**Model type:**
I compared both models — a rule-based model (`mood_analyzer.py`) and an ML model (`ml_experiments.py`).

**Intended purpose:**
Classify short text messages (social media posts, messages) into mood labels: positive, negative, neutral, or mixed.

**How it works (brief):**
- **Rule-based:** Preprocesses text (strips whitespace, maps emojis to words, removes punctuation, lowercases), then scores each token by checking it against positive and negative word lists. Handles negation by checking the previous word, and detects sarcasm using known phrases and context patterns. The final score maps to a label.
- **ML model:** Uses `CountVectorizer` to convert text into word-count vectors, then trains a `LogisticRegression` classifier on those vectors and the true labels. It learns word-to-label patterns automatically from the training data.

## 2. Data

**Dataset description:**
The dataset contains 11 posts total — 6 original starter posts plus 5 that I added. New posts were appended to `SAMPLE_POSTS` and `TRUE_LABELS` in `dataset.py`.

Added posts:
- `”not me crying at work lol 💀”` — negative
- `”I absolutely LOVE getting stuck in traffic”` — negative (sarcasm)
- `”finally finished my project 😭😂✨”` — mixed
- `”tired but grateful”` — positive
- `”going to grab lunch”` — neutral

**Labeling process:**
Labels were chosen based on the overall intent of the message, not just individual words. For example, `”tired but grateful”` was labeled positive because the dominant feeling is gratitude despite tiredness. `”I absolutely LOVE getting stuck in traffic”` was labeled negative because it is clearly sarcastic.

Hard-to-label posts:
- `”finally finished my project 😭😂✨”` — could be positive (relief/accomplishment) or mixed (emotional exhaustion + joy). Labeled mixed.
- `”Feeling tired but kind of hopeful”` — negative emotion paired with a hopeful outlook. Labeled mixed.

**Important characteristics of your dataset:**
- Contains Unicode emojis (😭, 😂, ✨, 💀) and text emoticons (:), :()
- Includes sarcasm (`”I absolutely LOVE getting stuck in traffic”`)
- Some posts express mixed feelings with opposing sentiment words
- Contains short, ambiguous messages (`”This is fine”`, `”going to grab lunch”`)
- Uses internet-style phrasing (`”not me crying at work lol”`)

**Possible issues with the dataset:**
- Very small (11 examples) — not enough to generalize well
- Label imbalance: more negative examples than mixed or neutral
- No slang like “lowkey”, “bussin”, “mid” — missing an entire register of language
- All posts are short (under 10 words) — longer text may behave differently
- Labels are subjective — another person might label some posts differently

## 3. How the Rule Based Model Works

**Your scoring rules:**
- **Word matching:** Each token is checked against a positive word set (10 words) and a negative word set (10 words). Positive matches add +1 to the score, negative matches add -1.
- **Negation handling:** Before scoring a word, the system checks if the previous token is a negation word (“not”, “never”, “no”, “neither”, “nor”). If so, the score contribution is flipped — e.g., “not happy” scores -1 instead of +1.
- **Emoji mapping:** Before tokenization, emojis are replaced with sentiment words (e.g., 😂 → “amazing”, 🥲 → “sad”, 🔥 → “awesome”). This converts non-text signals into scorable tokens.
- **Sarcasm detection:** A `_detect_sarcasm` method checks for known sarcastic phrases (“oh great”, “absolutely love”, “thanks for nothing”) and sarcasm markers (“totally”, “absolutely”) near negative topics (“traffic”, “monday”, “meetings”). If sarcasm is detected, the entire score is flipped.
- **Label thresholds:**
  - Score > 0 → “positive”
  - Score < 0 → “negative”
  - Score == 0 with equal positive and negative word counts (both > 0) → “mixed”
  - Score == 0 otherwise → “neutral”

**Strengths of this approach:**
- Transparent and explainable — you can trace exactly why a label was chosen
- Handles negation well for simple cases (“not happy”, “not bad”)
- Catches common sarcasm patterns that an ML model with little data might miss
- No training required — works immediately with any input

**Weaknesses of this approach:**
- Only recognizes words in the predefined lists — “grateful”, “hopeful”, “euphoric” are invisible
- Negation only checks one word back — “not really happy” or “I don't think this is good” are missed
- Sarcasm detection is a hardcoded list — novel sarcasm slips through
- Ignores intensifiers — “very happy” and “happy” score the same
- Cannot handle slang, double meanings (“this is sick”), or tone from punctuation/caps

## 4. How the ML Model Works

**Features used:**
Bag of words using `CountVectorizer` — each word becomes a numeric feature representing how many times it appears in the text.

**Training data:**
The model trained on the same 11 `SAMPLE_POSTS` and `TRUE_LABELS` from `dataset.py`.

**Training behavior:**
The ML model achieved higher accuracy than the rule-based model on the training data. It correctly classified posts like `”I absolutely LOVE getting stuck in traffic”` as negative, likely because it learned the word pattern from that specific training example. However, with only 11 examples, it is essentially memorizing the training set rather than learning generalizable patterns.

**Strengths and weaknesses:**
- **Strengths:** Learns patterns automatically from data without manual word lists. Considers all words in the vocabulary, not just a predefined set. Can pick up multi-word patterns that co-occur with certain labels.
- **Weaknesses:** With only 11 training examples, it overfits heavily — it performs well on training data but fails on unseen inputs. Unknown words (not in training vocabulary) are completely ignored by `CountVectorizer`. Cannot learn sarcasm, slang, or complex language patterns from so few examples.

## 5. Evaluation

**How you evaluated the model:**
Both models were evaluated on the 11 labeled posts in `dataset.py` using `main.py` (rule-based) and `ml_experiments.py` (ML). The rule-based model achieved approximately 8/11 correct (73% accuracy). The ML model achieved a higher accuracy on the same training data.

**Examples of correct predictions:**
- `”I love this class so much”` → predicted positive, true positive — “love” is in the positive word list, straightforward match
- `”I am not happy about this”` → predicted negative, true negative — negation handling correctly flipped “happy” to negative
- `”I absolutely LOVE getting stuck in traffic”` → predicted negative, true negative — sarcasm detection caught “absolutely love” and flipped the score

**Examples of incorrect predictions (rule-based):**
- `”Feeling tired but kind of hopeful”` → predicted negative, true mixed — “hopeful” is not in the positive word list, so only “tired” (-1) was scored
- `”tired but grateful”` → predicted negative, true positive — “grateful” is not in the positive word list, so only “tired” (-1) was counted
- `”finally finished my project 😭😂✨”` → predicted positive, true mixed — 😭 is not in the emoji map, so only the positive emojis (😂, ✨) were counted

Both failures share the same root cause: missing words/emojis in the predefined lists. The ML model handled some of these correctly because it learned from all words in context, not just a fixed list.

## 6. Limitations

- **Tiny dataset:** 11 examples is far too few for the ML model to generalize, and too few to capture the diversity of real language
- **Limited vocabulary:** The rule-based model only knows 10 positive and 10 negative words — common sentiment words like “grateful”, “hopeful”, “disappointed”, “frustrated” are invisible
- **Shallow negation:** Only checks one word back — multi-word negation (“do not really think”, “I wish I could”) is missed
- **Sarcasm is hardcoded:** The rule-based sarcasm detector only catches phrases explicitly listed — novel sarcasm patterns are missed entirely
- **No slang support:** Modern internet language (“lowkey”, “bussin”, “mid”, “no cap”) is not recognized by either model
- **No context understanding:** Both models treat words independently — they cannot understand that “sick” means different things in “I feel sick” vs “that trick was sick”
- **Evaluated on training data only:** There is no held-out test set, so reported accuracy is inflated and does not reflect real-world performance

## 7. Ethical Considerations

- **Misclassifying distress:** A message like “I can't do this anymore” might be classified as neutral due to missing vocabulary, when it could indicate someone in crisis. Using mood detection in mental health contexts without human oversight is dangerous.
- **Cultural and linguistic bias:** The word lists and sarcasm patterns reflect a narrow slice of English. Different communities, dialects, and cultural contexts express mood differently — the model could systematically misinterpret certain groups.
- **Privacy:** Analyzing personal messages for mood raises significant privacy concerns. Users may not consent to or be aware of sentiment analysis on their communications.
- **False confidence:** A simple model producing clean labels (“positive”, “negative”) can create a false sense of accuracy. Decision-makers might trust these labels more than warranted, especially when the underlying system is this limited.

### Bias and Scope

**Who is this model optimized for?**
The dataset and word lists reflect a narrow demographic: English-speaking, internet-literate, likely young and US-centric. The positive/negative word lists use standard American English vocabulary (“awesome”, “terrible”), and the sarcasm patterns assume a specific tone common in online spaces (“oh great”, “absolutely love”).

**Who might it misinterpret?**
- **AAVE and other dialects:** Expressions like “I'm dead”, “that's fire”, or “she ate that” carry strong positive sentiment in AAVE but would be misclassified or ignored entirely. The word lists have zero coverage of these patterns.
- **Non-native English speakers:** Simpler or more literal phrasing may lack the sentiment words the model expects, leading to false neutrals.
- **Different cultural contexts:** Sarcasm, humor, and emotional expression vary across cultures. British understatement (“not bad” meaning “excellent”), indirect expression common in many Asian cultures, or the use of diminutives in Spanish-influenced English would all be missed.
- **Older or more formal speakers:** The emoji map and sarcasm patterns skew young and informal. Someone writing “I am quite displeased” would get a neutral label.
- **Neurodivergent communication styles:** Flat or literal tone does not mean neutral mood. The model assumes emotional expression follows neurotypical patterns.

Both models inherit the biases of whoever wrote the word lists and training labels — in this case, a single person. Real-world mood detection would need diverse annotators and a dataset that represents the full range of people who would use it.

## 8. Rule-Based vs ML Model Comparison

**Did the ML model behave differently?**
Yes. The ML model achieved higher accuracy on the training data than the rule-based model. Where the rule-based model relies on explicit word lists and hand-written rules, the ML model learned its own associations between words and labels. It effectively built its own "word list" from the training data — one that included every word, not just the ones we thought to add.

**What did the ML model fix?**
- Posts with sentiment words missing from our lists (e.g., "tired but grateful") — the ML model could learn that "grateful" correlates with positive labels from context, while the rule-based model had no idea "grateful" was a positive word.
- The ML model handled some sarcasm (e.g., "I absolutely LOVE getting stuck in traffic") without needing a hardcoded sarcasm detector — it memorized that specific training example and its label.

**What new failures did the ML model introduce?**
- When tested on unseen inputs with unfamiliar words ("I feel euphoric", "this slaps fr fr", "lowkey mid tbh"), the ML model failed because `CountVectorizer` ignores words it has never seen. At least the rule-based model has a predictable failure mode — you know exactly which words it recognizes. The ML model's blind spots are harder to predict.
- Emojis-only inputs (😂😂😂) produced unpredictable results since the ML model has no emoji preprocessing — unlike the rule-based model which maps emojis to sentiment words.

**How sensitive was it to the labels?**
Very. With only 11 training examples, each label has an outsized influence. Changing a single label (e.g., flipping "tired but grateful" from positive to mixed) could shift the model's decision boundary enough to change predictions on other posts too. The ML model doesn't "understand" mood — it memorizes correlations between word patterns and labels. When the dataset is this small, those correlations are fragile and one mislabeled example can cascade into multiple wrong predictions.

## 9. Ideas for Improvement

- **Expand word lists:** Add more positive words (“grateful”, “hopeful”, “proud”, “relieved”) and negative words (“frustrated”, “disappointed”, “overwhelmed”, “anxious”)
- **Add more training data:** Grow the dataset to 50-100+ labeled examples covering diverse language styles, slang, sarcasm, and mixed feelings
- **Use TF-IDF instead of CountVectorizer:** Weight words by importance rather than just counting occurrences
- **Improve emoji coverage:** Add missing emojis (😭, 👍, 👎, 😤) to the preprocessing map
- **Multi-word negation:** Expand negation handling to check a wider window (2-3 words back) instead of just the previous token
- **Create a real test set:** Split data into training and test sets so accuracy reflects generalization, not memorization
- **Use a pretrained model:** A transformer-based model (like a fine-tuned BERT or a small language model) would understand context, sarcasm, and slang far better than either approach here
