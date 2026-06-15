# Email-Summerizer Project

## Overview
The Email-Summerizer is a Python-based application designed to automate the process of fetching unread newsletter emails, summarizing their content using the Gemini API, and delivering the formatted summaries to a Google Doc. It streamlines information consumption by providing concise daily digests of subscribed content.

## Features
*   Automated fetching of unread emails from Gmail based on a whitelist.
*   Intelligent summarization of newsletter content using the Gemini API.
*   Automated creation of daily Google Docs with formatted summaries.
*   Web dashboard for monitoring the summarization process status.
*   Modular and extensible architecture.

## Email Pipeline Functionality

The project operates through a four-stage pipeline, orchestrated by `pilot_main.py`:

1.  **Extraction**:
    *   `fetch_unread.py` is responsible for connecting to Gmail and retrieving unread emails.
    *   It filters emails based on a `whitelist.txt` to ensure only desired newsletters are processed.
    *   For emails containing links to full articles, `web_extractor.py` is used to extract the main content.

2.  **Summarization**:
    *   `batch_summarize.py` takes the extracted content.
    *   It utilizes the Gemini API to generate concise summaries of each newsletter.
    *   The summaries are structured and ready for delivery.

3.  **Delivery**:
    *   `append_to_doc.py` handles the publishing of summaries.
    *   It creates a new Google Doc for the day.
    *   The formatted summaries are then appended to this document, creating a daily digest.

4.  **Cleanup**:
    *   After successful summarization and delivery, `fetch_unread.py` marks the processed emails as read in Gmail to prevent reprocessing.

## Data Flow to Google Docs

The summarized content is seamlessly integrated into Google Docs as follows:

1.  After summarization by `batch_summarize.py`, the structured summary data is passed to `append_to_doc.py`.
2.  `append_to_doc.py` uses the Google Docs API to create a new document for the current day or append to an existing one.
3.  Authentication for Google services (Gmail and Google Docs) is managed centrally by `google_auth_util.py`, which securely handles OAuth 2.0 credentials. The project expects a client secret file for this purpose.
4.  The summaries are then written into the Google Doc, often with appropriate formatting (e.g., headings, bullet points) to ensure readability.

## Directory Structure

The project has a clear and organized directory structure:

```
.
├── .gitignore
├── B.L.A.S.T. Master System Prompt.md
├── GOOGLE_CLOUD_SETUP.md          # Guide for setting up Google Cloud services
├── requirements.txt               # Python dependencies
├── summary.txt                    # Placeholder for recent summary output
├── TROUBLESHOOTING_JOURNEY.md     # Documentation of troubleshooting steps
├── whitelist.txt                  # List of whitelisted email addresses
├── .git/...                       # Git version control
├── architecture/                  # Architectural documentation and SOPs
│   ├── 01_extraction_sop.md
│   ├── 02_summarization_sop.md
│   └── 03_delivery_sop.md
├── dashboard/                     # Web-based status dashboard
│   ├── index.html
│   └── status.json
├── protocol_0/                    # Project-specific documentation and progress
│   ├── cli_handoff.md
│   ├── findings.md
│   ├── gemini.md
│   ├── progress.md
│   └── task_plan.md
└── tools/                         # Main application logic and scripts
    ├── append_to_doc.py           # Handles writing summaries to Google Docs
    ├── batch_summarize.py         # Summarizes content using Gemini API
    ├── fetch_unread.py            # Fetches and filters unread emails
    ├── google_auth_util.py        # Centralized Google API authentication
    ├── link_test.py               # Utility for testing links
    ├── pilot_main.py              # Main orchestration script
    ├── read_doc.py                # Utility for reading Google Docs (if needed)
    ├── web_extractor.py           # Extracts content from web articles
    └── __pycache__/               # Python compiled bytecode cache
```

## Setup Guide

To get the Email-Summerizer project up and running, follow these steps:

### Prerequisites

*   Python 3.8+
*   `pip` (Python package installer)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd Email-Summerizer
    ```
2.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Google Cloud Project Setup

1.  **Create a Google Cloud Project:**
    Follow the instructions in `GOOGLE_CLOUD_SETUP.md` for detailed steps.
2.  **Enable APIs:**
    *   Google Gmail API
    *   Google Docs API
    *   Google Drive API (often required for Docs management)
3.  **Download OAuth 2.0 Client Configuration:**
    *   From the Google Cloud Console, create OAuth 2.0 Client IDs.
    *   Download the `client_secret.json` file and save it in your project's root directory or a secure location.
    *   Set the `GOOGLE_CLIENT_SECRET_FILE` environment variable to the path of this file.

### Gemini API Key

1.  **Obtain a Gemini API Key:**
    *   Visit the Google AI Studio or Google Cloud Console to generate your Gemini API key.
2.  **Set the environment variable:**
    ```bash
    export GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
    ```

### Environment Variables

The following environment variables are required:

*   `GOOGLE_CLIENT_SECRET_FILE`: The absolute path to your `client_secret.json` file for Google OAuth.
    *   Example: `/path/to/your/client_secret.json`
*   `GEMINI_API_KEY`: Your API key for accessing the Gemini service.
    *   Example: `your_gemini_api_key_here`
*   `GMAIL_WHITELIST_FILE`: The absolute path to your `whitelist.txt` file, containing allowed sender email addresses (one per line).
    *   Example: `/path/to/your/whitelist.txt`

### Running the Application

After setting up all prerequisites and environment variables, you can run the main orchestration script:

```bash
python tools/pilot_main.py
```
