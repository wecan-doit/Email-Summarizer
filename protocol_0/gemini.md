# 📜 Project Constitution: AI Newsletter Digest

## 🚀 Mission (North Star)
A deterministic daily intelligence feed that transforms high-volume newsletters into a structured, actionable research document for content creation.

## 🛠️ Architectural Invariants (The Law)
1. **Data-First:** Coding only begins once JSON schemas are confirmed.
2. **Determinism:** Business logic must be deterministic Python scripts in `tools/`.
3. **Layered Separation:** Separation of Architecture (SOPs), Navigation (Reasoning), and Tools (Execution).
4. **Self-Annealing:** Failures must be analyzed, patched, and documented in Architecture to prevent recurrence.
5. **Auto-Progress Tracking:** The system must automatically update `protocol_0/task_plan.md` and `protocol_0/progress.md` immediately following the completion of any task or implementation.


## 📊 Data Schemas

### 📥 Gmail Extraction (Input to Reasoning)
```json
{
  "message_id": "string",
  "thread_id": "string",
  "sender_email": "string",
  "sender_name": "string",
  "date": "iso-8601",
  "subject": "string",
  "body_text": "string",
  "source_url": "string"
}
```

### 🧠 Summarization Payload (Gemini Output)
```json
{
  "is_relevant": "boolean",
  "title": "string",
  "executive_summary": "string",
  "key_points": ["string"],
  "so_what": "string",
  "sentiment": "neutral | positive | negative",
  "tags": ["string"]
}
```

### 📤 Google Doc Batch Update (Tool Payload)
```json
{
  "document_id": "string",
  "requests": [
    {
      "insertText": {
        "location": { "index": "integer" },
        "text": "string"
      }
    },
    {
      "updateParagraphStyle": {
        "range": { "startIndex": "integer", "endIndex": "integer" },
        "paragraphStyle": { "namedStyleType": "HEADING_1 | HEADING_2 | NORMAL_TEXT" },
        "fields": "namedStyleType"
      }
    }
  ]
}
```

## 📋 Behavioral Rules
1. **Strict Curation:** Ignore promotional material, sponsor pitches, or filler text.
2. **Action-Oriented Tone:** Focus on impact on workflows, tools, or business strategies.
3. **Citation:** Always include original title and source link.
4. **Halt Execution:** Do not run if no new newsletters are found in the last 24 hours.
5. **Time-Bound Fetching:** Only fetch new emails from the last 48 hours for the given `whitelist.txt`.


## 🛰️ Trigger & Deployment
- **Frequency:** Once-daily morning execution.
- **Post-Processing:** Mark processed emails as 'READ'.

---
*Last Updated: 2026-05-07*
