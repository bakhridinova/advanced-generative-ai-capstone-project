import os
import requests
from dotenv import load_dotenv

load_dotenv()


def get_github_auth():
    auth_token = os.getenv("GITHUB_TOKEN")
    repository_name = os.getenv("GITHUB_REPO")
    account_username = os.getenv("GITHUB_USER")
    return auth_token, repository_name, account_username


def build_ticket_payload(ticket_title, customer_name, customer_email, issue_details):
    formatted_body = (
        f"**Customer Name:** {customer_name}\n"
        f"**Contact Email:** {customer_email}\n\n"
        f"**Issue Description:**\n{issue_details}"
    )

    return {
        "title": f"[Customer Support Ticket] {ticket_title}",
        "body": formatted_body,
        "labels": ["support-ticket", "customer-inquiry"]
    }


def build_api_headers(authentication_token):
    return {
        "Authorization": f"Bearer {authentication_token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }


def post_github_issue(api_endpoint, request_headers, issue_data):
    try:
        api_response = requests.post(
            api_endpoint,
            json=issue_data,
            headers=request_headers,
            timeout=10
        )

        if api_response.status_code in (200, 201):
            issue_link = api_response.json().get("html_url")
            print(f"[TICKET_MODULE] Successfully created issue: {issue_link}")
            return True, f"Support ticket created successfully!\n\nTrack your ticket here: {issue_link}"
        else:
            error_description = api_response.json().get("message", "Unknown error occurred")
            print(f"[TICKET_MODULE] API Error: {api_response.status_code} – {error_description}")
            return False, f"Ticket creation failed: {api_response.status_code} – {error_description}"

    except requests.exceptions.Timeout:
        print("[TICKET_MODULE] Request timeout")
        return False, "Ticket creation failed: Request timeout. Please try again."
    except Exception as error:
        print(f"[TICKET_MODULE] Unexpected error: {error}")
        return False, f"Ticket creation error: {str(error)}"


def create_support_ticket(summary: str, name: str, email: str, description: str) -> str:
    auth_token, repo_name, username = get_github_auth()

    if not auth_token or not repo_name or not username:
        print("[TICKET_MODULE] Missing required GitHub credentials")
        return "Configuration error: GitHub credentials are incomplete. Please contact administrator."

    api_url = f"https://api.github.com/repos/{username}/{repo_name}/issues"
    headers = build_api_headers(auth_token)
    payload = build_ticket_payload(summary, name, email, description)

    print(f"[TICKET_MODULE] Submitting ticket to repository: {repo_name}")
    success, message = post_github_issue(api_url, headers, payload)

    return message

