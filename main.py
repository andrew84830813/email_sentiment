import logging
from config import CLIENT_ID, TENANT, SCOPES, GRAPH_ENDPOINT, MAX_EMAIl_BODY_CHARACTERS
from authenicator import acquire_token
from email_retriever import fetch_emails
from utils import *
from sentiment_analyzer import SentimentAnalyzer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    keywords = ','.join(read_keywords('complaint_keywords.txt'))
    analyzer = SentimentAnalyzer(keywords=keywords)

    if not CLIENT_ID or not TENANT or not SCOPES:
        logger.error("CLIENT_ID or TENANT or Scope missing from configuration.")
        return

    # Authenticate and acquire an access token
    access_token = acquire_token(CLIENT_ID, TENANT, SCOPES)
    if not access_token:
        logger.error("Unable to retrieve access token. Exiting.")
        return

    try:
        # Fetch and display emails
        desired_email_count = 25
        emails = fetch_emails(access_token, GRAPH_ENDPOINT, desired_email_count=desired_email_count)

        logger.info(f"Total Emails Retrieved: {len(emails)}")
        for idx, msg in enumerate(emails, start=1):
            subject = msg.get('subject', 'No Subject')
            email_body = msg['body']['content']
            content_type = msg['body']['contentType']
            if content_type  in ['text','html']:
                email_body_parsed = extract_email_content(email_body,content_type, max_chars = MAX_EMAIl_BODY_CHARACTERS)
                complaint_decision = analyzer.lang_sentiment_analysis(subject=subject[:MAX_EMAIl_BODY_CHARACTERS], body=email_body_parsed)
            else:
                complaint_decision = 'Unable to Parse Email'

            sender = msg.get('from', {}).get('emailAddress', {}).get('name', 'Unknown Sender')
            sender_email = msg.get('from', {}).get('emailAddress', {}).get('address', 'Unknown Address')
            received = msg.get('receivedDateTime', 'Unknown Time')
            # classify email

            logger.info(f"Email #{idx}\nSubject: {subject}\nFrom: {sender} <{sender_email}>\nReceived: {received}\n{'-' * 40}\nComplaint_Decision: {complaint_decision} \n")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()