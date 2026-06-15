# 📖 SOP 02: Two-Pass Summarization

## 🎯 Goal
Transform raw, noisy newsletter text into a high-signal research document focusing on entrepreneurial relevance.

## 📥 Inputs
- Raw extraction payload (from SOP 01).
- `keywords.md`: (Optional) Custom focus areas for the user.

## ⚙️ Logic
### Pass 1: Relevance Check
- Pass the text to Gemini to determine if it contains high-value news or is just promotional filler.
- Filter out ads, sponsor pitches, and generic greetings.

### Pass 2: Structured Synthesis
- For relevant items, generate:
    - **Title**: Impactful headline.
    - **Summary**: Concise explanation of the news.
    - **"So What?"**: Direct implication for the user's workflow/business.
    - **Citations**: Clean URL to the source.

## ⚠️ Edge Cases
- **Oversized inputs**: Truncate raw text to fit Gemini context window limits (though usually not an issue for individual newsletters).
- **Ambiguous relevance**: Default to "relevant" if unsure, prioritizing info retention over aggressive filtering.

## 🛠️ Tooling
- `tools/batch_summarize()`: Gemini API interaction.
