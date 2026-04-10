# Resume Analytics Platform

A production-style AI-powered hiring system that automates resume screening, candidate ranking, and shortlisting using intelligent matching algorithms.

---

## Overview

Resume Analytics Platform enables recruiters to:

* Upload job descriptions and resumes
* Automatically parse candidate information from PDFs
* Rank candidates based on relevance
* Identify top matches instantly
* Generate interview-ready outreach drafts

Built as a full-stack application using **FastAPI (backend)** and **React + Tailwind (frontend)**.

---

## Features

* **Resume Parsing**
  Extracts structured data (skills, experience, education) from real PDF resumes

* **Intelligent Candidate Matching**
  Combines semantic similarity, skill overlap, and experience fit

* **Ranking & Shortlisting**
  Automatically ranks candidates and highlights top matches

* **Interview Draft Generation**
  Generates personalized outreach emails for shortlisted candidates

* **Dashboard Analytics**
  Clean UI with candidate metrics and match breakdowns

* **Batch Processing**
  Upload and process multiple resumes in a single workflow

---

## Tech Stack

**Frontend**

* React (Vite)
* Tailwind CSS

**Backend**

* FastAPI
* SQLite

**Core Capabilities**

* Resume parsing (PDF)
* Embedding-based similarity
* Hybrid scoring system

---

## Architecture

```text
            ┌────────────────────┐
            │   React Frontend   │
            │  (Dashboard + UI)  │
            └─────────┬──────────┘
                      │ REST API
                      ▼
            ┌────────────────────┐
            │   FastAPI Backend  │
            │  (Core Services)   │
            ├────────────────────┤
            │ Resume Parsing     │
            │ Embedding Engine   │
            │ Matching Logic     │
            │ Shortlisting       │
            │ Email Generator    │
            └─────────┬──────────┘
                      ▼
            ┌────────────────────┐
            │     SQLite DB      │
            │  (Candidates/Data) │
            └────────────────────┘
