# Multi-Agent AI System for Job Screening

A complete Python system with multiple AI agents working together to enhance the job screening and recruitment process.

## 🌟 Features

- **Job Description Summarizer Agent**: Parses job descriptions into structured data
- **CV Extractor Agent**: Extracts key information from PDF resumes
- **Matching Agent**: Uses AI embeddings to calculate candidate-job match scores
- **Shortlisting Agent**: Automatically selects top candidates based on scores
- **Email Agent**: Generates personalized interview invitation emails
- **SQLite Database**: Stores all processed data for persistence
- **Streamlit Web Interface**: User-friendly web interface for easy interaction

## 🗂️ Project Structure

```
Recruit-Pro-main/
├── main.py                 # Command-line entry point
├── app.py                  # Streamlit web interface
├── agents/                 # AI Agent modules
│   ├── jd_summarizer.py    # Parse and summarize job descriptions
│   ├── cv_extractor.py     # Extract structured data from resumes
│   ├── matcher.py          # Match jobs with candidates using AI
│   ├── shortlister.py      # Shortlist top candidates
│   └── emailer.py          # Generate interview invitation emails
├── utils/                  # Utility modules
│   ├── embeddings.py       # AI embedding generation
│   ├── parser.py           # Text parsing utilities
│   └── diagram.py          # System diagram generator
├── db/                     # Database module
│   └── memory.py           # SQLite database operations
├── resumes/                # Resume PDF files directory
├── job_description.csv     # Job descriptions data file
└── requirements.txt        # Python dependencies
```

## 🚀 Installation

1. **Clone or download the project:**
   ```bash
   cd Recruit-Pro-main
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Ollama (optional for AI embeddings):**
   ```bash
   # Install Ollama from https://ollama.ai/
   # Pull the embedding model
   ollama pull nomic-embed-text
   ```

## 🖥️ How to Run

### **Streamlit Web Interface (Recommended)**

Launch the interactive web interface:

```bash
streamlit run app.py
```

Then open your browser to: **http://localhost:8501**

The web interface provides:
- **Dashboard**: System overview and pipeline execution
- **Job Management**: Upload and process job descriptions
- **Resume Processing**: Upload and analyze candidate resumes
- **AI Matching**: Run candidate-job matching with AI
- **Shortlisting**: View and manage top candidates
- **Email System**: Generate and send interview invitations
- **Database Explorer**: Browse all processed data

### **Command Line Interface**

Run the complete pipeline from command line:

```bash
python main.py
```

**Advanced options:**
```bash
python main.py --jd-file custom_jobs.csv --resumes-dir my_resumes --threshold 85 --send-emails
```

**Command line arguments:**
- `--jd-file`: Job descriptions CSV file (default: job_description.csv)
- `--resumes-dir`: Resume PDF files directory (default: resumes)
- `--threshold`: Minimum score for shortlisting (default: 80.0)
- `--send-emails`: Actually send emails (default: simulate only)
- `--db-file`: Database file path (default: memory.db)

## 🤖 How It Works

1. **Job Description Processing**:
   - Loads job descriptions from CSV file
   - Extracts requirements, skills, and key information
   - Stores structured data in database

2. **Resume Analysis**:
   - Reads PDF resume files from the resumes directory
   - Extracts candidate information (name, email, skills, experience)
   - Stores parsed data in database

3. **AI-Powered Matching**:
   - Generates AI embeddings for jobs and resumes
   - Calculates similarity scores between candidates and positions
   - Falls back to keyword matching if AI is unavailable

4. **Smart Shortlisting**:
   - Filters candidates above score threshold (default: 80%)
   - Ranks candidates by match score for each position
   - Stores shortlisted candidates in database

5. **Email Generation**:
   - Creates personalized interview invitation emails
   - Highlights matching skills and qualifications
   - Can simulate or actually send emails via SMTP

## 📋 Requirements

- Python 3.8+
- PDF resume files in the `resumes/` directory
- Job descriptions in `job_description.csv` file
- Optional: Ollama for AI embeddings

## 📊 Data Format

**Job Descriptions CSV** should have columns:
- `title`: Job title
- `description`: Full job description text

**Resume Files**:
- PDF format files in the `resumes/` directory
- System automatically extracts text and information

## 🎯 Getting Started

1. **Install dependencies:** `pip install -r requirements.txt`
2. **Add your data:**
   - Place resume PDF files in `resumes/` directory
   - Update `job_description.csv` with your job postings
3. **Run the application:** `streamlit run app.py`
4. **Open your browser:** http://localhost:8501
5. **Click "Run Full Pipeline"** to process everything!

## 📄 License

MIT License - Feel free to use and modify for your recruitment needs.

---

**Ready to streamline your recruitment process? Just run `streamlit run app.py` and get started!** 🚀 