# Resume Analyzer

The **Resume Analyzer** is a backend service that processes uploaded resumes, extracts key information using OpenAI's GPT models, and stores the data in a PostgreSQL database. The workflow integrates with n8n for automation, Google Sheets for data storage, and Slack for notifications.

---

## Features

- **Authentication**: Secure login using JWT tokens.
- **Resume Upload**: Accepts PDF resumes and processes them.
- **Data Extraction**: Extracts key details like name, email, phone, skills, and experience using OpenAI.
- **Database Storage**: Stores extracted data in a PostgreSQL database.
- **Google Sheets Integration**: Appends data to a Google Sheet.
- **Slack Notifications**: Sends notifications for new resume submissions.

---

## Prerequisites

Ensure you have the following installed:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Python 3.10+](https://www.python.org/)
- [n8n](https://n8n.io/)

- download and place "tika-app-2.9.4.jar" file in teh root of the project.

# this file is used to extract the data from the pdf, must be placed at the root of the project to be coppied on the container

<!-- tika-app-2.9.4.jar -->

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd resume-analyzer

2. Configure Environment Variables
Copy the .env.example file to .env and update the values as needed:cp
[.env.example](http://_vscodecontentref_/1) .env

Key variables to configure:

Backend JWT Configuration<vscode_annotation details='%5B%7B%22title%22%3A%22hardcoded-credentials%22%2C%22description%22%3A%22Embedding%20credentials%20in%20source%20code%20risks%20unauthorized%20access%22%7D%5D'>: </vscode_annotation> - SECRET_KEY
ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES
PostgreSQL Credentials:
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_DB
OpenAI API Key:
OPENAI_API_KEY
Google OAuth Client Details:
OAUTH_CLIENT_ID
OAUTH_CLIENT_SECRET
PGAdmin Credentials:
PGADMIN_DEFAULT_EMAIL
PGADMIN_DEFAULT_PASSWORD

3. Build and Run the Project
Using Docker Compose
Build and start the services:

docker-compose up --build

Access the services:

Backend: http://localhost:8000
n8n: http://localhost:5678
PGAdmin: http://localhost:5050


4. Test the API
Use the test.http file to test the API endpoints. For example:

Login:

curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpass"

  Upload Resume:

  curl -X POST "http://localhost:8000/upload" \
  -H "Authorization: Bearer <your-token>" \
  -F "file=@/path/to/resume.pdf"


  Workflow Overview
The project uses an n8n workflow defined in workflows/resume_workflow.json:

Webhook: Receives the uploaded resume.
Apache Tika: Extracts text from the PDF.
OpenAI: Extracts structured data from the text.
PostgreSQL: Stores the extracted data.
Google Sheets: Appends the data to a Google Sheet.
Slack: Sends a notification about the new resume.


Dependencies
Python Libraries
The backend requires the following Python libraries (defined in requirements.txt):

fastapi
uvicorn
python-multipart
python-jose
python-dotenv
requests
passlib
Docker Images
Backend: Python 3.10-slim
n8n: n8nio/n8n
PostgreSQL: postgres:15
PGAdmin: dpage/pgadmin4
```
# resume-analyzer
