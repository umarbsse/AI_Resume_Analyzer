import sys
from functions import process_resume

if __name__ == "__main__":
    resume_id = sys.argv[1]
    print(f"Processing resume ID: {resume_id}")
    process_resume(resume_id)