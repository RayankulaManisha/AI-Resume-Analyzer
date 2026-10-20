
with open("sample_resume.txt", "r") as file:
    resume_text = file.read()

with open("job_description.txt", "r") as file:
    job_text = file.read()

print("===== RESUME CONTENT =====")
print(resume_text)

print("\n===== JOB DESCRIPTION =====")
print(job_text)
