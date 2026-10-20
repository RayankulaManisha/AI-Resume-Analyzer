
print("===== AI RESUME ANALYZER =====")

candidate_name = "Manisha"
target_role = "Python Developer"

resume_skills = ["Python", "SQL", "Git", "HTML", "CSS"]
job_skills = ["Python", "SQL", "Git", "REST APIs", "Docker"]

# Find matching skills
matching_skills = []

for skill in job_skills:
    if skill in resume_skills:
        matching_skills.append(skill)

# Find missing skills
missing_skills = []

for skill in job_skills:
    if skill not in resume_skills:
        missing_skills.append(skill)

# Calculate match percentage
total_job_skills = len(job_skills)
total_matching_skills = len(matching_skills)

if total_job_skills > 0:
    match_percentage = (
        total_matching_skills / total_job_skills
    ) * 100
else:
    match_percentage = 0

# Display results
print("\nCandidate:", candidate_name)
print("Target Job:", target_role)

print("\nResume Skills:", resume_skills)
print("Required Job Skills:", job_skills)

print("\nMatching Skills:", matching_skills)
print("Missing Skills:", missing_skills)

print("Match Percentage:", match_percentage, "%")
