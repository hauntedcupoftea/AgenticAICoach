import sys
from time import sleep
import streamlit as st
import streamlit.web.cli as stcli
import logging
from agentic_cv_advisor.sqlite import (
    get_chat_history,
    init_db,
    save_chat_to_db,
    save_cv_to_db,
    get_all_cvs,
    get_cv_content,
)

# Setup logging to direct output to terminal
logging.basicConfig(level=logging.INFO)


# App logic
def Agentic_CV_Coach():
    st.header("Agentic")
    st.warning(
        "This is a prototype with no safety and authentication implementations, use at own risk."
    )
    st.info(
        "This application stores your data, included any uploaded CVs, but does not share it with anyone."
    )

    # Initialize the database
    init_db()

    # Sidebar for CV upload and selection
    with st.sidebar:
        uploaded_file = st.file_uploader(
            "Upload your CV (PDF or DOCX)", type=["pdf", "docx"]
        )
        if uploaded_file and st.button("Save CV"):
            save_cv_to_db(uploaded_file)
            st.sidebar.success("CV uploaded successfully!")

        st.sidebar.markdown("### Uploaded CVs")
        cvs = get_all_cvs()
        if cvs:
            for cv_id, filename, uploaded_at in cvs:
                st.sidebar.write(f"**{filename}** (Uploaded: {uploaded_at})")
                if st.sidebar.button(f"Select {filename}", key=f"select_{cv_id}"):
                    # Clear previous messages and load new chat history
                    st.session_state.selected_cv_id = cv_id
                    st.session_state.messages = [
                        {
                            "role": "assistant",
                            "content": f"Currently offering help on CV: **{filename}** (Uploaded: {uploaded_at}). Feel free to ask me questions.",
                        }
                    ]

                    # Retrieve chat history for this specific CV
                    saved_history = get_chat_history(cv_id)
                    saved_history = get_chat_history(cv_id)
                    for user_msg, assistant_msg, _ in saved_history:
                        if user_msg:
                            st.session_state.messages.append(
                                {"role": "user", "content": user_msg}
                            )
                        if assistant_msg:
                            st.session_state.messages.append(
                                {"role": "assistant", "content": assistant_msg}
                            )
        else:
            st.sidebar.info("No CVs uploaded yet.")

    # Initialize session state for chat history if not exists
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Welcome to the CV Coach. I will help you improve and tailor your CV according to your needs.",
            }
        ]

    # Display previous conversation
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Handle chat input
    if "selected_cv_id" in st.session_state:
        selected_cv_content = get_cv_content(st.session_state.selected_cv_id)
        if selected_cv_content:
            if prompt := st.chat_input("Your question"):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.write(prompt)

                # Simulate assistant response
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        try:
                            sleep(3)
                            # Placeholder for agent logic
                            response = f"Analyzing CV and responding to: {prompt}"
                            st.session_state.messages.append(
                                {"role": "assistant", "content": response}
                            )
                            st.write(response)

                            # Save conversation to database with CV ID
                            save_chat_to_db(
                                user_message=prompt,
                                assistant_message=response,
                                cv_id=st.session_state.selected_cv_id,
                            )
                        except Exception as e:
                            logging.error(f"Error processing query: {e}")
                            st.error(
                                "An error occurred while processing your request. Please try again."
                            )
        else:
            st.warning("Selected CV could not be loaded. Please choose another.")
    else:
        st.info("Please upload or select a CV to start.")


def run():
    init_db()
    sys.argv = ["streamlit", "run", "src/agentic_cv_advisor/main.py"]
    sys.exit(stcli.main())


if __name__ == "__main__":
    Agentic_CV_Coach()
