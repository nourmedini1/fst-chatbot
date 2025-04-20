# FST-Chatbot 🤖

A conversational AI assistant developed during Lunar Hack 1.0 to help students and visitors navigate information about the Faculty of Science of Tunis (FST).

## 🎯 Project Overview

FST-Chatbot is an intelligent conversational agent that provides comprehensive information about the Faculty of Science of Tunis. It assists users with general inquiries, course information, and detailed guidance on master's and doctorate application processes.

## 🚀 Key Features

- General information about FST
- Course-related FAQ responses
- Detailed guidance on master's and doctorate applications
  - Required administrative documents
  - Application process walkthrough
  - Automatic document generation from LaTeX templates
- Campus navigation assistance
- Interactive responses in both French and English
- Voice interaction support
- Admin dashboard for content management

## 🛠️ Technical Architecture

### Knowledge Base Creation
1. **Data Collection**
   - Sourced from FST official website
   - Gathered from FST Facebook page
   - PDF documents conversion
   - Structured data formatting in Markdown

2. **Data Processing**
   - Implemented recursive text splitter
   - Chunk size: 1000 characters
   - Overlap: 200 characters

### Technology Stack

- **Embeddings Model**: sentence-transformers/all-mpnet-base-v2
- **Vector Database**: FAISS
- **Architecture**: RAG (Retrieval-Augmented Generation)
- **LLM**: Self-hosted Mistral via Ollama
- **Speech Processing**: Custom STT/TTS server
- **Frontend**: React.js with Material-UI
- **Backend**: FastAPI

### Query Processing Pipeline

1. User input reception (text/voice)
2. Speech-to-text conversion (if voice input)
3. Query reformulation to French using LLM
4. Vector similarity search
5. Context-aware response generation
6. Text-to-speech synthesis (if voice output requested)

## 💡 Intelligent Features

- Multilingual query handling
- Context-aware responses
- Efficient document retrieval
- Dynamic response generation
- Voice interaction capabilities
- Administrative document automation

## 🎛️ Admin Dashboard

### Knowledge Base Management
- Upload new documents to expand chatbot knowledge
- Delete outdated or irrelevant documents
- Monitor document status and usage

### LaTeX Template Management
- Upload administrative document templates
- Manage template categories
- Preview template rendering

### Document Automation
- Automatic form filling based on student data
- PDF generation from LaTeX templates
- Batch processing capabilities

## 🔧 Technical Implementation

```python
# Core Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
EMBEDDING_MODEL = "all-mpnet-base-v2"
VECTOR_DB = "FAISS"
LLM_MODEL = "mistral"
LLM_HOST = "localhost:11434"
STT_TTS_SERVER = "http://localhost:5000"
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 14+
- Ollama
- CUDA-compatible GPU (optional)

### Installation

1. Clone the repositories:
```bash
git clone https://github.com/your-username/fst-chatbot.git
git clone https://github.com/AbderrazagB/lunar-hack-frontend.git
git clone https://github.com/AbderrazagB/ai-stt-tts.git
```

2. Install backend dependencies:
```bash
cd fst-chatbot
pip install -r requirements.txt
```

3. Install frontend dependencies:
```bash
cd ../lunar-hack-frontend
npm install
```

4. Setup the STT/TTS server:
```bash
cd ../ai-stt-tts
pip install -r requirements.txt
```

## 🔗 Related Projects

- [AI Speech Server](https://github.com/AbderrazagB/ai-stt-tts) - Speech-to-Text and Text-to-Speech server
- [FST Chatbot Frontend](https://github.com/AbderrazagB/lunar-hack-frontend) - Web application interface
- [Lost & Found System](https://github.com/Karim-zitouna-01/Lost_Found_objects) - Lost items management system

## 👥 Team BlockByBlock

- **Mohamed Nour Medini** - RAG Implementation & Backend
- **Mohamed Karim Zitouna** - Lost & Found System
- **Abderrazeq Boussaid** - Frontend & Speech Processing

## 🏆 Lunar Hack 1.0

This project was developed during Lunar Hack 1.0, demonstrating innovative use of RAG architecture and natural language processing for educational institution assistance.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
