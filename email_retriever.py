import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_emails(access_token, graph_endpoint, desired_email_count=50, top=25):
    """
    Fetch emails using Microsoft Graph API with pagination.

    :param access_token: Access token for Microsoft Graph API.
    :param graph_endpoint: Base URL for Microsoft Graph API.
    :param desired_email_count: Total number of emails to retrieve.
    :param top: Number of emails per API request.
    :return: List of emails.
    """
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    params = {
        '$top': top,
        '$select': 'subject,from,receivedDateTime,body'
    }
    emails = []
    next_link = graph_endpoint

    while len(emails) < desired_email_count:
        # Use params only for the initial request, not when following next_link
        if next_link == graph_endpoint:
            response = requests.get(next_link, headers=headers, params=params)
        else:
            response = requests.get(next_link, headers=headers)  # next_link already contains params

        if response.status_code == 200:
            data = response.json()
            emails.extend(data.get('value', []))  # Append new emails to the list
            next_link = data.get('@odata.nextLink')  # Get the next page URL
            if not next_link:  # Exit if there are no more pages
                break
        else:
            logger.error(f"Failed to retrieve emails: {response.status_code}")
            logger.error(response.text)
            break

    return emails