import streamlit as st
import requests
import time

API_BASE = "https://tax-gst-chatbot-v1-a83103c3-600d-4622-9f11--bf126ac7.crewai.com"
BEARER_TOKEN = "16c64f95cb7e"
HEADERS = {"Authorization": f"Bearer {BEARER_TOKEN}"}


def get_required_inputs():
    url = f"{API_BASE}/inputs"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()


def start_crew(payload):
    url = f"{API_BASE}/kickoff"
    headers = HEADERS.copy()
    headers["Content-Type"] = "application/json"
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()


def check_status(kickoff_id):
    url = f"{API_BASE}/status/{kickoff_id}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()


def main():
    st.title("Tax & GST Chatbot")

    user_query = st.text_area("Enter your query:", height=100)
    start_button = st.button("Ask")

    if start_button:
        if not user_query.strip():
            st.error("Please enter a query!")
            return

        # Get required inputs schema (optional display)
        try:
            required_inputs = get_required_inputs()
        except Exception as e:
            st.error(f"Error fetching required inputs: {e}")
            return

        payload = {
            "inputs": {
                "user_query": user_query
            }
        }

        try:
            kickoff_response = start_crew(payload)
        except Exception as e:
            st.error(f"Error starting crew: {e}")
            return

        kickoff_id = kickoff_response.get("kickoff_id")
        if not kickoff_id:
            st.error("No kickoff_id returned; aborting.")
            return

        result_placeholder = st.empty()
        while True:
            try:
                status_response = check_status(kickoff_id)
            except Exception as e:
                result_placeholder.error(f"Error checking status: {e}")
                break

            status = status_response.get("status")

            if status == "completed" or ("result" in status_response and status_response["result"]):
                answer = status_response.get("result") or ""
                result_placeholder.success("Answer:")
                result_placeholder.text(answer)
                break
            elif status == "failed" or ("error" in status_response and status_response["error"]):
                error_msg = status_response.get("error") or "Unknown error"
                result_placeholder.error(f"Task failed: {error_msg}")
                break
            else:
                time.sleep(2)


if __name__ == "__main__":
    main()
