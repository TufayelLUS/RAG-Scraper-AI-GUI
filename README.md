# RAG Scraper

A Python-based RAG (Retrieval Augmented Generation) application that allows you to ask questions about web content or PDF documents using Ollama's local LLMs.

---

## GUI Software Guideline
Download this repository as a zipped file and inside build folder, you'll find the compiled executable file. No need to install anything except Ollama and the required models.

---
## Software Preview
![image](https://github.com/TufayelLUS/RAG-Scraper-AI-GUI/blob/main/ss.png?raw=true)

---

## Prerequisites

### 1. Install Ollama

#### **Windows**
1. Download Ollama from the official website: [Ollama Downloads](https://ollama.ai/download)
2. Run the installer.
3. After installation, Ollama will run as a service in the background.

#### **Linux**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

#### **macOS**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

---

### 2. Install Required Ollama Models

After installing Ollama, open a terminal/command prompt and run:

```bash
# Install the base LLM model
ollama pull llama2

# Install the embeddings model
ollama pull all-minilm
```

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/TufayelLUS/RAG-Scraper-AI-GUI.git
   cd RAG-Scraper
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:

   **Windows:**
   ```bash
   venv\Scripts\activate
   ```

   **Linux/MacOS:**
   ```bash
   source venv/bin/activate
   ```

4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

1. Make sure Ollama is running in the background.
2. Run the application:
   ```bash
   python "RAG Scraper.py"
   ```

### Using the Interface:

a. **Select Loader Type:**
   - **Web Loader:** For scraping web content.
   - **PDF Loader:** For reading PDF files.

b. **Select Models:**
   - **Base Model:** Choose the LLM for answering questions (e.g., llama2).
   - **Embeddings Model:** Choose the model for text embeddings (e.g., all-minilm).

c. **For Web Loader:**
   - Enter URLs (one per line).
   - Enter the CSS class name of the content area to narrow down the context. Leave empty if not applicable.
     - Example: For a blog post, you might use `"article-content"` or `"post-content"`.

d. **For PDF Loader:**
   - Click **"Browse"** to select a PDF file.

e. **Ask Questions:**
   - Enter your question in the question field.
   - Click **"ASK AI"** to get answers.

---

## Features

- Support for both web pages and PDF documents.
- Dynamic model selection from available Ollama models.
- Persistent settings saved in an INI file.
- Customizable content extraction for web pages.
- Error handling and user-friendly warnings.

---

## Configuration

The application saves your preferences in `settings.ini`:
- Last used loader type
- Selected base model
- Selected embeddings model

---

## Troubleshooting

- **"Could not connect to Ollama API" error:**
  - Ensure Ollama is running.
  - Check if the Ollama service is active.
  - Restart Ollama if necessary.

- **Models not showing up:**
  - Make sure you've pulled the models using `ollama pull [model-name]`.
  - Check Ollama's status.
  - Restart the application.

- **Web scraping not working:**
  - Verify the URL is accessible.
  - Check if the CSS class name is correct.
  - Some websites may block scraping.

- **PDF loading issues:**
  - Ensure the PDF is not password-protected.
  - Check if the file is accessible.
  - Image based PDFs may not work.
  - Verify the PDF file is not corrupted.

---

## Notes

- The application uses local LLMs through Ollama, ensuring privacy.
- Processing time depends on your hardware capabilities.
- Model performance varies based on the selected models.
- First-time model downloads may take time depending on your internet connection.

---

## Requirements

- Python 3.8 or higher
- Ollama installed and running
- Sufficient disk space for models
- Internet connection for web scraping
- Adequate RAM (16GB minimum recommended)

---

## Looking for a Software Engneer?
Reach out to me on [Fiverr](https://www.fiverr.com/thechoyon).