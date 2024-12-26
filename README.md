# Email Complaint Detection Application

## Introduction

The **Email Complaint Detection Application** fetches emails from your Outlook account using the Microsoft Graph API and analyzes them to determine whether they are complaints or non-complaints using sentiment analysis. This automation helps businesses efficiently identify and address customer complaints.

## Features

- **Authentication with Microsoft Graph API** using MSAL.
- **Email Retrieval**: Fetch recent emails from your Outlook inbox.
- **Sentiment Analysis**: Classify emails as complaints or non-complaints based on predefined keywords.
- **Logging**: Track the application's operations and analysis results.

## Prerequisites

Before you begin, ensure you have the following:

- **Python 3.7+** installed via [Anaconda](https://www.anaconda.com/).
- **Conda** environment manager.
- An **Azure Active Directory (Azure AD)** tenant to create and configure an application for MSAL.
- A **Microsoft account** with access to Outlook emails.

## Setting Up Microsoft Authentication Library (MSAL) Application

To authenticate and access your Outlook emails, you need to register an application in Azure AD.

### Step 1: Register an Application in Azure AD

1. **Sign in to the Azure Portal**: [Azure Portal](https://portal.azure.com/).

2. **Navigate to Azure Active Directory**:
   - Click on **"Azure Active Directory"** in the left-hand menu.

3. **Register a New Application**:
   - Go to **"App registrations"**.
   - Click **"New registration"**.
   - **Name**: Enter a name (e.g., `EmailComplaintDetector`).
   - **Supported Account Types**: Choose **"Accounts in this organizational directory only"**.
   - **Redirect URI**: Set to `http://localhost` for a desktop application.
   - Click **"Register"**.

4. **Note Important IDs**:
   - **Application (client) ID**: Copy this value.
   - **Directory (tenant) ID**: Copy this value.

### Step 2: Configure API Permissions

1. **Navigate to API Permissions**:
   - In your registered application, click **"API permissions"**.

2. **Add Permissions**:
   - Click **"Add a permission"**.
   - Select **"Microsoft Graph"**.
   - Choose **"Delegated permissions"**.
   - Add **`Mail.Read`** permission.
   - Click **"Add permissions"**.

3. **Grant Admin Consent**:
   - Click **"Grant admin consent for [Your Tenant]"** and confirm.

### Step 3: Create a Client Secret

1. **Navigate to Certificates & Secrets**:
   - Click **"Certificates & secrets"**.

2. **Create a New Client Secret**:
   - Click **"New client secret"**.
   - **Description**: Enter a description (e.g., `EmailComplaintDetectorSecret`).
   - **Expires**: Choose a duration.
   - Click **"Add"**.

3. **Copy Client Secret**:
   - Copy the generated client secret value. **Store it securely**; you won't be able to retrieve it again.

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/EmailComplaintDetector.git
cd EmailComplaintDetector

Step 2: Create and Activate a Conda Environment

conda create -n email_complaint_detector python=3.8
conda activate email_complaint_detector

Step 3: Install Dependencies

Ensure you have a requirements.txt file with the necessary packages. If not, install the required packages directly:

pip install langchain openai requests python-dotenv

Alternatively, if requirements.txt exists:

pip install -r requirements.txt

Configuration

Step 1: Create a .env File

In the project root directory, create a file named .env and add the following content:

# .env

CLIENT_ID=your_client_id_here
TENANT_ID=your_tenant_id_here
CLIENT_SECRET=your_client_secret_here
SCOPES=https://graph.microsoft.com/.default
GRAPH_ENDPOINT=https://graph.microsoft.com/v1.0/me/messages
MAX_EMAIL_BODY_CHARACTERS=1000

Step 2: Update config.py to Load Environment Variables

Ensure your config.py reads from the .env file. Here’s a sample config.py:

# config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
TENANT = os.getenv("TENANT_ID")
SCOPES = os.getenv("SCOPES").split(",")
GRAPH_ENDPOINT = os.getenv("GRAPH_ENDPOINT")
MAX_EMAIL_BODY_CHARACTERS = int(os.getenv("MAX_EMAIL_BODY_CHARACTERS", 1000))

Security Note: Ensure that .env is added to your .gitignore file to prevent sensitive information from being committed to version control.

Step 3: Create complaint_keywords.txt

Create a file named complaint_keywords.txt and list keywords that identify complaints, one per line. Example:

dissatisfied
unacceptable
problem
issue
delay
refund
complaint
disappointed
inconvenience

Running the Application

Ensure your Conda environment is activated and run the application using:

python main.py

Authentication Flow

	1.	Browser Prompt: A browser window will open asking you to sign in to your Microsoft account and grant permissions.
	2.	Permissions Grant: Allow the application to access your emails.
	3.	Processing: The application will fetch and analyze the specified number of emails, logging the results in the console.

Sample Output

INFO:__main__:Total Emails Retrieved: 25
INFO:__main__:Email #1
Subject: Extremely Disappointed with Your Service
From: John Doe <john.doe@example.com>
Received: 2023-10-15T14:30:00Z
----------------------------------------
Complaint_Decision: Complaint 

Project Structure

EmailComplaintDetector/
├── main.py
├── config.py
├── authenticator.py
├── email_retriever.py
├── sentiment_analyzer.py
├── utils.py
├── complaint_keywords.txt
├── requirements.txt
├── .env
└── README.md

File Descriptions

	•	main.py: The entry point of the application. Handles authentication, email retrieval, and analysis.
	•	config.py: Contains configuration variables loaded from the .env file.
	•	authenticator.py: Manages the authentication process using MSAL to acquire access tokens.
	•	email_retriever.py: Contains functions to fetch emails from Microsoft Graph API.
	•	sentiment_analyzer.py: Implements sentiment analysis logic to classify emails.
	•	utils.py: Utility functions for tasks like reading keywords and extracting email content.
	•	complaint_keywords.txt: A list of keywords used to identify complaints in emails.
	•	requirements.txt: Lists all Python dependencies required for the project.
	•	.env: Environment variables file containing sensitive configuration details.
	•	README.md: This documentation file.

Troubleshooting

Common Errors

	1.	Missing Configuration Variables
	•	Error Message: “CLIENT_ID or TENANT or Scope missing from configuration.”
	•	Solution: Ensure that the .env file contains valid CLIENT_ID, TENANT_ID, and SCOPES. Verify that the MSAL application is correctly set up in Azure AD with the necessary permissions.
	2.	Token Acquisition Failure
	•	Error Message: “Unable to retrieve access token. Exiting.”
	•	Solution: Check your internet connection, ensure that the Azure AD application is properly configured, and that the API permissions have been granted admin consent.
	3.	API Request Errors
	•	Error Message: Varies based on the issue (e.g., permission denied, rate limits).
	•	Solution: Review the error details in the logs. Ensure that the application has the necessary permissions and that you’re not exceeding API rate limits.
	4.	Token Limit Exceeded
	•	Error Message: “This model’s maximum context length is 4097 tokens…”
	•	Solution: Reduce the size of the prompt by limiting the number of emails processed at once or truncating lengthy email bodies. Ensure that supplementary data is concise.

Steps to Resolve Issues

	1.	Check Configuration
	•	Verify that all necessary fields in the .env file are correctly populated.
	2.	Review Logs
	•	Examine the logs for detailed error messages and stack traces.
	3.	Validate Permissions
	•	Ensure that the Azure AD application has the correct API permissions and that admin consent has been granted.
	4.	Internet Connectivity
	•	Ensure that your machine has a stable internet connection to communicate with Azure and OpenAI APIs.
	5.	Update Dependencies
	•	Make sure all Python packages are up-to-date by running:

pip install --upgrade -r requirements.txt


	6.	Seek Help
	•	If issues persist, consider reaching out to support forums or consulting the official documentation for Microsoft Graph API and LangChain.

License

This project is licensed under the MIT License.

