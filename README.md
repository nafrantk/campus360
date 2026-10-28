# Campus360 – Student Academic Companion 🌿

## About the Project

Campus360 is a student-focused web application developed using Python and Streamlit. It provides a centralized dashboard to help students monitor academic performance, organize tasks, plan study sessions, explore career-related skills, and access student support information.

## Objectives

- Provide a dashboard for monitoring academic progress.
- Help students track subjects, marks, and attendance.
- Organize assignments, tasks, and examinations.
- Generate study recommendations and weekly study plans.
- Support skill exploration and career suggestions.
- Provide a simple interface for accessing student-related information.

## Features

- **Dashboard:** Displays an overview of academic progress.
- **My Academics:** Helps students view and manage subject-related information.
- **Tasks & Exams:** Supports task tracking and completion status.
- **AI Study Mentor:** Provides rule-based study recommendations and a sample quiz.
- **Skills & Career:** Offers skill assessments and career suggestions.
- **Ask Campus360:** Provides responses to common queries using predefined rules.
- **My Profile:** Allows students to manage profile information.

## Technologies Used

- Python
- Streamlit
- Pandas
- CSV for dataset input
- JSON for local application data storage

## Project Structure

```text
campus360/
├── app.py
├── requirements.txt
├── README.md
└── student_performance_updated_1000.csv
```

The CSV file should be included only if the application requires it and the dataset license permits redistribution. Do not upload confidential or sensitive student information.

The application may also create a `campus360_data.json` file to store local application data.

## Installation and Setup

1. Install Python.

2. Download or clone this repository.

3. Open a terminal in the project directory.

4. Install the dependencies:

   `pip install -r requirements.txt`

5. Start the application:

   `streamlit run app.py`

6. Open the local URL displayed in the terminal.

## Requirements

The `requirements.txt` file contains the Python packages required to run the application.

## Deployment

Campus360 can be deployed using Streamlit Community Cloud by connecting the GitHub repository and selecting `app.py` as the main application file.

## Future Enhancements

- Integration with a real AI model for personalized study assistance.
- Secure student authentication and data storage.
- Improved academic analytics and visualizations.
- Integration with institutional academic systems.
- More personalized study plans and career guidance.

## Dataset Acknowledgment

The project uses the *Student Performance Predictions* dataset created by **Muhammad Haseeb**, obtained from Kaggle and described as synthetic data.

- **Owner/Creator:** Muhammad Haseeb
- **Source:** [https://www.kaggle.com/datasets/haseebindata/student-performance-predictions/data](https://www.kaggle.com/datasets/haseebindata/student-performance-predictions/data)
- **License:** Apache License 2.0, as listed on the dataset page.

The dataset creator is acknowledged, and applicable license conditions should be followed.

## Project Status

Campus360 is a prototype developed for educational and academic project purposes. Features and implementation may evolve as the project is updated.

## Author

Student Project – Data Science

