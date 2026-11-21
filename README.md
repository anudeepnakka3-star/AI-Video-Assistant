# AI Video Assistant

AI Video Assistant converts YouTube videos or local audio/video recordings into meeting notes. It transcribes the media, generates a summary, extracts action items and decisions, identifies open questions, and supports transcript-based chat.

The application provides a Streamlit interface and an interactive command-line interface.

## Features

- Import media from YouTube or upload local audio/video files
- Transcribe English audio locally with OpenAI Whisper
- Transcribe Hindi or Hinglish audio through the Sarvam AI speech-to-text API
- Generate meeting titles and summaries
- Extract action items, key decisions, and open questions
- Ask follow-up questions using a ChromaDB retrieval pipeline
- Download results as PDF or TXT
- Support 10-minute audio chunking for longer recordings

## Tech Stack

- Python and Streamlit
- OpenAI Whisper
- Sarvam AI
- Groq and LangChain
- ChromaDB and Hugging Face embeddings
- yt-dlp and FFmpeg
- PyDub
- ReportLab

## Requirements

- Python 3.10 or newer
- FFmpeg available in the system `PATH`
- Groq API key
- Sarvam API key only for Hindi/Hinglish transcription
- Internet access for YouTube downloads and hosted model/API services

## Installation

Clone the repository:

```bash
git clone https://github.com/anudeepnakka3-star/AI-Video-Assistant.git
cd AI-Video-Assistant
```

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Install FFmpeg for Windows. FFmpeg must be accessible from the command prompt:

```bash
ffmpeg -version
```

## Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
SARVAM_API_KEY=your_sarvam_api_key
WHISPER_MODEL=small
SARVAM_STT_MODEL=saaras:v2.5
```

- `GROQ_API_KEY` is required for summaries, extraction, titles, and chat.
- `SARVAM_API_KEY` is required only when selecting Hindi/Hinglish transcription.
- `WHISPER_MODEL` defaults to `small`.
- `SARVAM_STT_MODEL` defaults to `saaras:v2.5`.

Do not commit the `.env` file or API keys.

## Run the Streamlit Application

```bash
streamlit run app.py
```

Open the local URL shown by Streamlit. Paste a public YouTube link or upload a supported local media file, choose the spoken language, and select **Create meeting notes**.

Supported local formats include MP3, WAV, M4A, AAC, FLAC, OGG, MP4, MOV, MKV, and WebM.

## Run from the Command Line

```bash
python main.py
```

Enter a YouTube URL or local file path when prompted. The CLI will print the title, summary, action items, decisions, open questions, and an interactive transcript chat session.

## Project Structure

```text
.
├── app.py                  # Streamlit web interface
├── main.py                 # CLI entry point and processing pipeline
├── theme.py                # Streamlit styling components
├── requirements.txt        # Python dependencies
├── core/
│   ├── extractor.py        # Action item and decision extraction
│   ├── rag_engine.py       # Retrieval and question-answer pipeline
│   ├── summarizer.py       # Title and summary generation
│   ├── transcriber.py      # Whisper and Sarvam transcription
│   └── vector_store.py     # ChromaDB vector storage
└── utils/
    ├── audio_processor.py  # Downloading, conversion, and chunking
    └── report.py           # PDF and TXT export
```

## Processing Pipeline

1. Download YouTube audio or convert a local media file to WAV.
2. Split the audio into chunks of approximately 10 minutes.
3. Transcribe chunks with Whisper or Sarvam AI.
4. Generate a title and summary.
5. Extract action items, key decisions, and open questions.
6. Create a ChromaDB vector index of the transcript.
7. Use retrieval to answer follow-up questions.

## Generated and Ignored Files

Runtime data is excluded through `.gitignore`, including:

- `.env` and virtual environments
- Downloaded media and audio chunks
- The `vector_db` database
- Python cache, coverage, build, and IDE files

## Troubleshooting

- `ffmpeg` not found: install FFmpeg and ensure its `bin` directory is in `PATH`.
- Sarvam transcription fails: verify `SARVAM_API_KEY` and use the Hinglish option.
- Groq requests fail: verify `GROQ_API_KEY` and account access.
- YouTube download fails: confirm that the URL is public and supported.
- Local uploads fail: verify that the file is valid and FFmpeg supports its format.

## Repository

https://github.com/anudeepnakka3-star/AI-Video-Assistant
