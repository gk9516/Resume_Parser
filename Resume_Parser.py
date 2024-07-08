import json
import fitz  # PyMuPDF

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()
    return text

# Extracted text from the provided resume PDF
pdf_path = "Ganesh_Resume_Final.pdf"
resume_text = extract_text_from_pdf(pdf_path)

# Function to parse the resume text into JSON format
def parse_resume_to_json(resume_text):
    resume_json = {
        "name": "",
        "location": "",
        "contact": {},
        "education": [],
        "projects": [],
        "experience": [],
        "achievements": {
            "certifications": [],
            "hackathons": []
        },
        "technical_skills": {
            "languages": [],
            "relevant_coursework": [],
            "technologies_and_tools": [],
            "soft_skills": []
        },
        "areas_of_interest": []
    }

    lines = resume_text.split('\n')
    current_section = None

    for line in lines:
        line = line.strip()
        if line == "Education:":
            current_section = "education"
            continue
        elif line == "Projects:":
            current_section = "projects"
            continue
        elif line == "Experience:":
            current_section = "experience"
            continue
        elif line == "Achievements:":
            current_section = "achievements"
            continue
        elif line == "Technical Skills:":
            current_section = "technical_skills"
            continue

        if current_section == "education":
            if line.startswith("- "):
                parts = line[2:].split(", ")
                education = {
                    "institution": parts[0],
                    "duration": parts[1],
                    "course": parts[2],
                    "score": parts[3] if len(parts) > 3 else None
                }
                resume_json["education"].append(education)
        elif current_section == "projects":
            if line.startswith("- "):
                project_name = line[2:]
                technologies = None
                date = None
                description = None
                github_link = None
            elif line.startswith("  - "):
                if "Utilized" in line or "Developed" in line:
                    description = line[4:]
                elif "GitHub Link:" in line:
                    github_link = line.split("GitHub Link: ")[1]
                elif not technologies:
                    technologies = line.split(", ")
            if project_name and technologies and date and description and github_link:
                project = {
                    "name": project_name,
                    "technologies": technologies,
                    "date": date,
                    "description": description,
                    "github_link": github_link
                }
                resume_json["projects"].append(project)
        elif current_section == "experience":
            if line.startswith("- "):
                parts = line[2:].split(", ")
                experience = {
                    "company": parts[0],
                    "role": parts[1],
                    "duration": parts[2],
                    "location": parts[3] if len(parts) > 3 else None
                }
                resume_json["experience"].append(experience)
        elif current_section == "achievements":
            if line.startswith("- Certifications:"):
                certifications = line[len("- Certifications:"):].split(", ")
                resume_json["achievements"]["certifications"].extend(certifications)
            elif line.startswith("- Intracollege Hackathons:"):
                hackathons = line[len("- Intracollege Hackathons:"):].split(", ")
                resume_json["achievements"]["hackathons"].extend(hackathons)
        elif current_section == "technical_skills":
            if line.startswith("- Languages:"):
                languages = line[len("- Languages:"):].split(", ")
                resume_json["technical_skills"]["languages"].extend(languages)
            elif line.startswith("- Relevant Coursework:"):
                coursework = line[len("- Relevant Coursework:"):].split(", ")
                resume_json["technical_skills"]["relevant_coursework"].extend(coursework)
            elif line.startswith("- Technologies and Developer Tools:"):
                tools = line[len("- Technologies and Developer Tools:"):].split(", ")
                resume_json["technical_skills"]["technologies_and_tools"].extend(tools)
            elif line.startswith("- Soft Skills:"):
                soft_skills = line[len("- Soft Skills:"):].split(", ")
                resume_json["technical_skills"]["soft_skills"].extend(soft_skills)
        elif current_section is None:
            if line.startswith("Ganesh K"):
                resume_json["name"] = line
            elif line.startswith("East Tambaram,"):
                resume_json["location"] = line
            elif line.startswith("Phone:"):
                resume_json["contact"]["phone"] = line.split("Phone: ")[1]
            elif line.startswith("Email:"):
                resume_json["contact"]["email"] = line.split("Email: ")[1]
            elif line.startswith("LinkedIn:"):
                resume_json["contact"]["linkedin"] = line.split("LinkedIn: ")[1]
            elif line.startswith("GitHub:"):
                resume_json["contact"]["github"] = line.split("GitHub: ")[1]

    return resume_json

# Parse the resume text to JSON
resume_json = parse_resume_to_json(resume_text)

# Save the parsed JSON to a file
output_path = "Ganesh_Resume.json"
with open(output_path, "w") as json_file:
    json.dump(resume_json, json_file, indent=4)

print("Resume parsed and saved to Ganesh_Resume.json")
