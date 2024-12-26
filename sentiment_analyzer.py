from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI

class SentimentAnalyzer:
    """
    Initializes the SentimentAnalyzer

    Args:
        keywords (str, optional): Keywords associated with complaints. Defaults to None.
        model_name (str): Name of the LLM model. Defaults to "gpt-3.5-turbo-instruct".
        temperature (float): Sampling temperature. Defaults to 0.
    """
    def __init__(self,keywords=None,model_name="gpt-3.5-turbo-instruct", temperature=0,max_tokens = 500):
        self.llm = OpenAI(model_name=model_name, temperature=temperature,max_tokens=max_tokens)
        self.keywords = keywords or ''

    def lang_sentiment_analysis(self, subject, body):
        """
        Basic sentiment analysis using langchain.
        """
        # Define the prompt
        extract_prompt = PromptTemplate(
            input_variables=["subject", "body",'keywords'],
            template="""
            You are an assistant that reviews information in emails to detect complaints.
            Analyze the subject and body of the email to determine the topic, customer sentiment, and urgency level. 
            When determining sentiment consider these keywords to be associated with a complaint: {keywords}
            Based on this review classify if the message is a complaint and report as Decision.

            Email:
            Subject: {subject}
            Body: {body}

            Output:
            - Topic: ...
            - Sentiment: ...
            - Urgency: ...
            - Decision: ...
            
            """
        )

        # Build the pipeline
        pipeline = extract_prompt | self.llm

        # Run the pipeline
        response = pipeline.invoke({"subject": subject, "body": body, "keywords": self.keywords})
        return response

    def cot_sentiment_analysis(self, subject, body):
        """
        User defined Chain of Thought (CoT) sentiment analysis.
        """
        # Define the prompts
        extract_prompt = PromptTemplate(
            input_variables=["subject", "body","keywords"],
            template="""
            You are an intelligent assistant that extracts key information from emails.
            Extract the main topic, customer sentiment, urgency level, and summarize email with at most 25 words.
            When determining sentiment consider these keywords to be associated with a complaint: {keywords}
            The information will be used by a judge to determine if an email is a complaint or not.

            Email:
            Subject: {subject}
            Body: {body}

            Output:
            - Topic: ...
            - Sentiment: ...
            - Urgency: ...
            - Summary: ...
            """
        )

        complaint_prompt = PromptTemplate(
            input_variables=["report"],
            template="""
            You are an intelligent analyst and have been provide the following report: 
            - Report: {report}

            Given the report provide reasoning for a judge to classify whether the email is a complaint or not.
            """
        )

        classifier_prompt = PromptTemplate(
            input_variables=["decision_documentation"],
            template="""
            You are expert logician and judge. 
            An analyst documented the following reasoning for you to classify if an email is a complaint or not:
            - Complaint Decision Documentation: {decision_documentation}

            Use the decision documentation to make a binary classification. The output classes can be either:
            {{Complaint, Not Complaint}}
            """
        )

        # Build the pipeline
        pipeline = (
            extract_prompt | self.llm |
            (lambda result: {
                "report": result.split("- Sentiment:")[1].split("\n")[0].strip()
            }) |
            complaint_prompt | self.llm |
            (lambda result: {
                "decision_documentation": result.strip()
            }) |
            classifier_prompt | self.llm
        )

        # Run the pipeline
        response = pipeline.invoke({"subject": subject, "body": body, "keywords": self.keywords})
        return response

