from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import os
import json
import asyncio
from typing import List, Optional
import pandas as pd
from pathlib import Path

# Import existing agents
from agents.cv_extractor import CVExtractorAgent
from agents.jd_summarizer import JDSummarizerAgent
from agents.matcher import MatcherAgent
from agents.shortlister import ShortlisterAgent
from agents.emailer import EmailerAgent
from db.memory import Memory

app = FastAPI(title="Recruit Pro API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
memory = Memory()

# Global state for session data
session_data = {
    "job_descriptions": [],
    "resumes": [],
    "matches": [],
    "shortlisted": [],
    "emails_sent": []
}

@app.get("/")
async def root():
    return {"message": "Recruit Pro API is running"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "Recruit Pro API is operational"}

@app.get("/api/stats")
async def get_stats():
    """Get system statistics"""
    try:
        # Get counts from database
        jd_count = len(memory.get_job_descriptions())
        resume_count = len(memory.get_resumes())
        match_count = len(memory.get_matches())
        shortlist_count = len(memory.get_shortlisted())
        
        return {
            "job_descriptions": jd_count,
            "resumes": resume_count,
            "matches": match_count,
            "shortlisted": shortlist_count,
            "total_candidates": resume_count,
            "active_jobs": jd_count,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting stats: {str(e)}")

@app.post("/api/upload/job-descriptions")
async def upload_job_descriptions(file: UploadFile = File(...)):
    """Upload job descriptions CSV file"""
    try:
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Only CSV files are supported")
        
        # Read CSV file
        df = pd.read_csv(file.file)
        
        # Process job descriptions
        jd_agent = JDSummarizerAgent()
        job_descriptions = []
        
        for _, row in df.iterrows():
            jd_data = {
                "title": row.get("title", ""),
                "company": row.get("company", ""),
                "location": row.get("location", ""),
                "description": row.get("description", ""),
                "requirements": row.get("requirements", ""),
                "type": row.get("type", "Full-time"),
                "experience": row.get("experience", ""),
            }
            
            # Process with JD agent
            processed_jd = jd_agent.process(jd_data)
            memory.add_job_description(processed_jd)
            job_descriptions.append(processed_jd)
        
        session_data["job_descriptions"].extend(job_descriptions)
        
        return {
            "message": f"Successfully uploaded {len(job_descriptions)} job descriptions",
            "count": len(job_descriptions),
            "job_descriptions": job_descriptions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading job descriptions: {str(e)}")

@app.post("/api/upload/resumes")
async def upload_resumes(files: List[UploadFile] = File(...)):
    """Upload resume PDF files"""
    try:
        cv_agent = CVExtractorAgent()
        processed_resumes = []
        
        for file in files:
            if not file.filename.endswith('.pdf'):
                continue
            
            # Save file temporarily
            temp_path = f"temp_{file.filename}"
            with open(temp_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            
            try:
                # Process with CV agent
                resume_data = cv_agent.process(temp_path)
                memory.add_resume(resume_data)
                processed_resumes.append(resume_data)
            finally:
                # Clean up temp file
                if os.path.exists(temp_path):
                    os.remove(temp_path)
        
        session_data["resumes"].extend(processed_resumes)
        
        return {
            "message": f"Successfully processed {len(processed_resumes)} resumes",
            "count": len(processed_resumes),
            "resumes": processed_resumes
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading resumes: {str(e)}")

@app.post("/api/matching/run")
async def run_matching():
    """Run candidate matching"""
    try:
        matcher = MatcherAgent()
        
        # Get job descriptions and resumes from database
        job_descriptions = memory.get_job_descriptions()
        resumes = memory.get_resumes()
        
        if not job_descriptions:
            raise HTTPException(status_code=400, detail="No job descriptions available")
        if not resumes:
            raise HTTPException(status_code=400, detail="No resumes available")
        
        # Run matching
        matches = matcher.process(job_descriptions, resumes)
        
        # Store matches in database
        for match in matches:
            memory.add_match(match)
        
        session_data["matches"] = matches
        
        return {
            "message": f"Successfully matched {len(matches)} candidates",
            "count": len(matches),
            "matches": matches
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error running matching: {str(e)}")

@app.post("/api/shortlisting/run")
async def run_shortlisting(threshold: float = Form(0.7)):
    """Run candidate shortlisting"""
    try:
        shortlister = ShortlisterAgent()
        
        # Get matches from database
        matches = memory.get_matches()
        
        if not matches:
            raise HTTPException(status_code=400, detail="No matches available. Run matching first.")
        
        # Run shortlisting
        shortlisted = shortlister.process(matches, threshold)
        
        # Store shortlisted candidates in database
        for candidate in shortlisted:
            memory.add_shortlisted(candidate)
        
        session_data["shortlisted"] = shortlisted
        
        return {
            "message": f"Successfully shortlisted {len(shortlisted)} candidates",
            "count": len(shortlisted),
            "shortlisted": shortlisted
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error running shortlisting: {str(e)}")

@app.post("/api/emails/send")
async def send_emails(simulate: bool = Form(True)):
    """Send emails to shortlisted candidates"""
    try:
        emailer = EmailerAgent(simulate=simulate)
        
        # Get shortlisted candidates from database
        shortlisted = memory.get_shortlisted()
        
        if not shortlisted:
            raise HTTPException(status_code=400, detail="No shortlisted candidates available")
        
        # Send emails
        email_results = emailer.process(shortlisted)
        
        session_data["emails_sent"] = email_results
        
        return {
            "message": f"Successfully sent {len(email_results)} emails",
            "count": len(email_results),
            "results": email_results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending emails: {str(e)}")

@app.post("/api/pipeline/run")
async def run_full_pipeline(
    simulate_emails: bool = Form(True),
    shortlist_threshold: float = Form(0.7)
):
    """Run the complete recruitment pipeline"""
    try:
        results = {
            "steps": [],
            "total_time": 0
        }
        
        # Step 1: Check if we have data
        job_descriptions = memory.get_job_descriptions()
        resumes = memory.get_resumes()
        
        if not job_descriptions:
            results["steps"].append({
                "step": "job_descriptions",
                "status": "error",
                "message": "No job descriptions available"
            })
            return results
        
        if not resumes:
            results["steps"].append({
                "step": "resumes",
                "status": "error",
                "message": "No resumes available"
            })
            return results
        
        # Step 2: Run matching
        try:
            matcher = MatcherAgent()
            matches = matcher.process(job_descriptions, resumes)
            for match in matches:
                memory.add_match(match)
            
            results["steps"].append({
                "step": "matching",
                "status": "success",
                "message": f"Matched {len(matches)} candidates",
                "count": len(matches)
            })
        except Exception as e:
            results["steps"].append({
                "step": "matching",
                "status": "error",
                "message": str(e)
            })
            return results
        
        # Step 3: Run shortlisting
        try:
            shortlister = ShortlisterAgent()
            shortlisted = shortlister.process(matches, shortlist_threshold)
            for candidate in shortlisted:
                memory.add_shortlisted(candidate)
            
            results["steps"].append({
                "step": "shortlisting",
                "status": "success",
                "message": f"Shortlisted {len(shortlisted)} candidates",
                "count": len(shortlisted)
            })
        except Exception as e:
            results["steps"].append({
                "step": "shortlisting",
                "status": "error",
                "message": str(e)
            })
            return results
        
        # Step 4: Send emails
        try:
            emailer = EmailerAgent(simulate=simulate_emails)
            email_results = emailer.process(shortlisted)
            
            results["steps"].append({
                "step": "emails",
                "status": "success",
                "message": f"Sent {len(email_results)} emails",
                "count": len(email_results)
            })
        except Exception as e:
            results["steps"].append({
                "step": "emails",
                "status": "error",
                "message": str(e)
            })
        
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error running pipeline: {str(e)}")

@app.get("/api/job-descriptions")
async def get_job_descriptions():
    """Get all job descriptions"""
    try:
        job_descriptions = memory.get_job_descriptions()
        return {
            "job_descriptions": job_descriptions,
            "count": len(job_descriptions)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting job descriptions: {str(e)}")

@app.get("/api/resumes")
async def get_resumes():
    """Get all resumes"""
    try:
        resumes = memory.get_resumes()
        return {
            "resumes": resumes,
            "count": len(resumes)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting resumes: {str(e)}")

@app.get("/api/matches")
async def get_matches():
    """Get all matches"""
    try:
        matches = memory.get_matches()
        return {
            "matches": matches,
            "count": len(matches)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting matches: {str(e)}")

@app.get("/api/shortlisted")
async def get_shortlisted():
    """Get all shortlisted candidates"""
    try:
        shortlisted = memory.get_shortlisted()
        return {
            "shortlisted": shortlisted,
            "count": len(shortlisted)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting shortlisted candidates: {str(e)}")

@app.delete("/api/clear")
async def clear_database():
    """Clear all data from database"""
    try:
        memory.clear_all()
        session_data.clear()
        session_data.update({
            "job_descriptions": [],
            "resumes": [],
            "matches": [],
            "shortlisted": [],
            "emails_sent": []
        })
        return {"message": "Database cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing database: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 