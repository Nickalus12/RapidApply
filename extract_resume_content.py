#!/usr/bin/env python3
"""
Extract resume content from PDF file
"""

import sys
import json
import re
from modules.resumes.extractor import extract_text_from_pdf

def extract_resume_info(text):
    """Extract structured information from resume text"""
    
    # Initialize results
    results = {
        "technical_skills": [],
        "programming_languages": [],
        "frameworks_tools": [],
        "databases": [],
        "certifications": [],
        "work_experience": []
    }
    
    # Convert text to lowercase for case-insensitive matching
    text_lower = text.lower()
    
    # Common programming languages
    languages = [
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'go', 'golang',
        'rust', 'swift', 'kotlin', 'scala', 'r', 'matlab', 'php', 'perl', 'bash', 'shell',
        'powershell', 'sql', 'html', 'css', 'xml', 'json', 'yaml', 'vb.net', 'objective-c',
        'dart', 'lua', 'groovy', 'clojure', 'elixir', 'haskell', 'julia', 'fortran', 'cobol'
    ]
    
    # Common frameworks and tools
    frameworks_tools = [
        'react', 'angular', 'vue', 'django', 'flask', 'spring', 'express', 'node.js', 'nodejs',
        '.net', 'laravel', 'rails', 'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas',
        'numpy', 'matplotlib', 'docker', 'kubernetes', 'jenkins', 'git', 'github', 'gitlab',
        'aws', 'azure', 'gcp', 'google cloud', 'terraform', 'ansible', 'puppet', 'chef',
        'maven', 'gradle', 'webpack', 'babel', 'jest', 'mocha', 'selenium', 'cypress',
        'redux', 'graphql', 'rest api', 'microservices', 'kafka', 'rabbitmq', 'elasticsearch',
        'spark', 'hadoop', 'airflow', 'tableau', 'power bi', 'jira', 'confluence', 'slack'
    ]
    
    # Common databases
    databases = [
        'mysql', 'postgresql', 'mongodb', 'redis', 'cassandra', 'dynamodb', 'oracle',
        'sql server', 'sqlite', 'mariadb', 'couchdb', 'neo4j', 'influxdb', 'firestore',
        'cosmos db', 'aurora', 'redshift', 'bigquery', 'snowflake', 'hbase', 'memcached'
    ]
    
    # Extract programming languages
    for lang in languages:
        # Use word boundaries for more accurate matching
        pattern = r'\b' + re.escape(lang) + r'\b'
        if re.search(pattern, text_lower):
            results["programming_languages"].append(lang.upper() if len(lang) <= 3 else lang.title())
    
    # Extract frameworks and tools
    for tool in frameworks_tools:
        pattern = r'\b' + re.escape(tool) + r'\b'
        if re.search(pattern, text_lower):
            results["frameworks_tools"].append(tool.title())
    
    # Extract databases
    for db in databases:
        pattern = r'\b' + re.escape(db) + r'\b'
        if re.search(pattern, text_lower):
            results["databases"].append(db.upper() if db in ['mysql', 'sql', 'aws', 'gcp'] else db.title())
    
    # Extract certifications (common patterns)
    cert_patterns = [
        r'certified\s+[\w\s]+',
        r'certification[s]?\s*:?\s*[\w\s,]+',
        r'aws\s+certified[\w\s]+',
        r'microsoft\s+certified[\w\s]+',
        r'google\s+certified[\w\s]+',
        r'cisco\s+certified[\w\s]+',
        r'oracle\s+certified[\w\s]+',
        r'pmp\b', r'scrum\s+master', r'ccna\b', r'ccnp\b', r'cissp\b',
        r'comptia\s+[\w\+]+', r'itil\b', r'togaf\b'
    ]
    
    for pattern in cert_patterns:
        matches = re.finditer(pattern, text_lower)
        for match in matches:
            cert = match.group().strip()
            if len(cert) > 5:  # Filter out too short matches
                results["certifications"].append(cert.title())
    
    # Extract work experience and companies
    # Look for common patterns like "Company Name (Year-Year)" or "at Company Name"
    company_patterns = [
        r'at\s+([A-Z][\w\s&,.\'-]+)(?:\s*\(|\s*-|\s*,)',
        r'([A-Z][\w\s&,.\'-]+)\s*\(\d{4}',
        r'([A-Z][\w\s&,.\'-]+)\s*\|\s*\d{4}',
        r'([A-Z][\w\s&,.\'-]+)\s*-\s*\d{4}',
        r'([A-Z][\w\s&,.\'-]+)\s*•\s*\d{4}'
    ]
    
    # Also look for job titles
    job_patterns = [
        r'(software\s+engineer|developer|programmer|architect|manager|analyst|consultant|designer|administrator|specialist|lead|senior|junior|intern)[\w\s]*(?:\s*at|\s*-|\s*\|)',
    ]
    
    # Extract companies
    companies_found = set()
    for pattern in company_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            company = match.group(1).strip()
            if len(company) > 3 and len(company) < 50:  # Reasonable company name length
                companies_found.add(company)
    
    # Extract work experience sections
    work_section_pattern = r'(work\s+experience|professional\s+experience|employment\s+history|experience)[:\s]*(.+?)(?=education|skills|certifications|projects|$)'
    work_match = re.search(work_section_pattern, text, re.IGNORECASE | re.DOTALL)
    
    if work_match:
        work_text = work_match.group(2)
        # Split by common delimiters for job entries
        job_entries = re.split(r'\n{2,}|\r\n{2,}', work_text)
        
        for entry in job_entries[:10]:  # Limit to first 10 entries
            if len(entry.strip()) > 20:  # Skip very short entries
                results["work_experience"].append(entry.strip())
    
    # Add companies to work experience if not already captured
    for company in companies_found:
        results["work_experience"].append(f"Company: {company}")
    
    # Combine all technical skills
    results["technical_skills"] = (
        results["programming_languages"] + 
        results["frameworks_tools"] + 
        results["databases"]
    )
    
    # Remove duplicates
    for key in results:
        if isinstance(results[key], list):
            results[key] = list(set(results[key]))
    
    return results

def main():
    pdf_path = "/mnt/c/Users/Nicka/RapidApply/all resumes/default/resume.pdf"
    
    print(f"Extracting text from: {pdf_path}")
    
    # Extract text from PDF
    text = extract_text_from_pdf(pdf_path)
    
    if not text or text.startswith("["):
        print("Failed to extract text from PDF. The file might be corrupted or PyPDF2/pdfplumber might not be installed.")
        print("\nRaw output:", text)
        return
    
    print("\n=== EXTRACTED TEXT ===")
    print(text[:1000], "..." if len(text) > 1000 else "")
    print(f"\nTotal characters extracted: {len(text)}")
    
    # Extract structured information
    print("\n=== EXTRACTED INFORMATION ===")
    info = extract_resume_info(text)
    
    print("\n1. PROGRAMMING LANGUAGES:")
    for lang in sorted(info["programming_languages"]):
        print(f"   - {lang}")
    
    print("\n2. FRAMEWORKS AND TOOLS:")
    for tool in sorted(info["frameworks_tools"]):
        print(f"   - {tool}")
    
    print("\n3. DATABASES:")
    for db in sorted(info["databases"]):
        print(f"   - {db}")
    
    print("\n4. ALL TECHNICAL SKILLS:")
    for skill in sorted(info["technical_skills"]):
        print(f"   - {skill}")
    
    print("\n5. CERTIFICATIONS:")
    for cert in sorted(set(info["certifications"])):
        print(f"   - {cert}")
    
    print("\n6. WORK EXPERIENCE AND COMPANIES:")
    for exp in info["work_experience"][:10]:  # Show first 10 entries
        print(f"   - {exp[:100]}..." if len(exp) > 100 else f"   - {exp}")
    
    # Save to JSON file for further use
    output_path = "/mnt/c/Users/Nicka/RapidApply/extracted_resume_data.json"
    with open(output_path, 'w') as f:
        json.dump(info, f, indent=2)
    print(f"\n\nExtracted data saved to: {output_path}")

if __name__ == "__main__":
    main()