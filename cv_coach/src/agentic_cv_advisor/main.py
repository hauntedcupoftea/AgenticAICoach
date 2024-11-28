import streamlit as st
import logging
from agentic_cv_advisor.sqlite import get_chat_history, init_db, save_chat_to_db, save_cv_to_db, get_all_cvs, get_cv_content

# Setup logging to direct output to terminal
logging.basicConfig(level=logging.INFO)

# App logic
def Agentic_CV_Coach():
    st.header("Agentic CV Coach with SQLite Integration")

    # Initialize the database
    init_db()

    # Sidebar for CV upload and selection
    with st.sidebar:
        uploaded_file = st.file_uploader("Upload your CV (PDF or DOCX)", type=["pdf", "docx"])
        if uploaded_file and st.button("Save CV"):
            save_cv_to_db(uploaded_file)
            st.sidebar.success("CV uploaded successfully!")

        st.sidebar.markdown("### Uploaded CVs")
        cvs = get_all_cvs()
        if cvs:
            for cv_id, filename, uploaded_at in cvs:
                st.sidebar.write(f"**{filename}** (Uploaded: {uploaded_at})")
                if st.sidebar.button(f"Select {filename}", key=f"select_{cv_id}"):
                    st.session_state.selected_cv_id = cv_id
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"You've selected CV: {filename}. You can now ask questions about it."
                    })
        else:
            st.sidebar.info("No CVs uploaded yet.")

    # Initialize session state for chat history
    if "messages" not in st.session_state:
        # Fetch chat history from the database
        saved_history = get_chat_history()
        st.session_state.messages = [
            {"role": "user", "content": user_msg} if user_msg else 
            {"role": "assistant", "content": assistant_msg}
            for user_msg, assistant_msg, _ in saved_history
        ]
        # Add a welcome message if no history is found
        if not st.session_state.messages:
            st.session_state.messages = [
                {"role": "assistant", "content": "Welcome! Please upload a CV to start."}
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
                    with st.spinner("Analyzing..."):
                        try:
                            # Placeholder for agent logic
                            response = f"Analyzing CV and responding to: {prompt}"
                            st.session_state.messages.append({"role": "assistant", "content": response})
                            st.write(response)

                            # Save conversation to database
                            save_chat_to_db(prompt, response)
                        except Exception as e:
                            logging.error(f"Error processing query: {e}")
                            st.error("An error occurred while processing your request. Please try again.")
        else:
            st.warning("Selected CV could not be loaded. Please choose another.")
    else:
        st.info("Please upload or select a CV to start.")

if __name__ == "__main__":
    Agentic_CV_Coach()
