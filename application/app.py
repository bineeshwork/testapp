import streamlit as st
import boto3
import json
import uuid
from datetime import datetime
import os

# Set up S3 client using environment variables
s3 = boto3.client('s3',
                  aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                  aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
                  region_name=os.environ.get('AWS_DEFAULT_REGION')
                  )

# Get S3 bucket name from environment variable
S3_BUCKET_NAME = "awsbin-studentfeedback-files"

st.title("Student Feedback Form")

with st.form("feedback_form"):
    student_id = str(uuid.uuid4())[:8]  # Generate anonymized ID
    st.write(f"Your anonymized Student ID: {student_id}")

    program_name = st.text_input("Program Name")

    course_satisfaction = st.slider("Course Satisfaction", 1, 5, 3)
    learning_outcomes = st.slider("Learning Outcomes Achievement", 1, 5, 3)
    support_services = st.slider("Support Services Rating", 1, 5, 3)

    engagement_level = st.selectbox("Engagement Level", ["High", "Medium", "Low"])

    feedback = st.text_area("Open-ended Feedback")

    future_plans = st.selectbox("Future Plans", ["Continue", "Transfer", "Undecided"])

    submitted = st.form_submit_button("Submit Feedback")

if submitted:
    feedback_data = {
        "Student ID": student_id,
        "Program Name": program_name,
        "Course Satisfaction": course_satisfaction,
        "Learning Outcomes Achievement": learning_outcomes,
        "Support Services Rating": support_services,
        "Engagement Level": engagement_level,
        "Open-ended Feedback": feedback,
        "Future Plans": future_plans,
        "Timestamp": datetime.now().isoformat()
    }

    # Convert data to JSON string
    feedback_json = json.dumps(feedback_data)

    # Generate a unique filename
    filename = f"feedback_{student_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"

    try:
        # Upload to S3
        s3.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=filename,
            Body=feedback_json
        )
        st.success("Thank you! Your feedback has been submitted successfully.")
    except Exception as e:
        st.error(f"An error occurred while saving your feedback: {str(e)}")
