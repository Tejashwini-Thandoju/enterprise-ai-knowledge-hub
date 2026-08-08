import streamlit as st

from src.retriever.retriever import (
    retrieve_chunks,
    collection
)

from src.llm.groq_client import (
    generate_answer,
    rewrite_query
)


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Enterprise AI Knowledge Hub",
    page_icon="📚",
    layout="wide"
)


# --------------------------------------------------
# Helper: Get Document Count
# --------------------------------------------------

def get_document_count():

    try:

        results = collection.get(
            include=["metadatas"]
        )

        sources = set()

        for metadata in results["metadatas"]:

            if metadata and "source" in metadata:

                sources.add(
                    metadata["source"]
                )

        return len(sources)

    except Exception:

        return 0


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.title("📚 Knowledge Hub")

    st.write(
        "Enterprise AI assistant powered by "
        "Retrieval-Augmented Generation."
    )

    st.divider()

    document_count = get_document_count()

    st.metric(
        "Knowledge Base Documents",
        document_count
    )

    st.divider()

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()

    st.divider()

    st.caption(
        "The assistant answers questions using "
        "information retrieved from company documents."
    )


# --------------------------------------------------
# Main Title
# --------------------------------------------------

st.title("📚 Enterprise AI Knowledge Hub")

st.write(
    "Ask questions about company policies and get "
    "answers based on the organization's documents."
)


# --------------------------------------------------
# Initialize Chat History
# --------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []


# --------------------------------------------------
# Display Previous Messages
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

        # ------------------------------------------
        # Display Sources
        # ------------------------------------------

        if (
            message["role"] == "assistant"
            and message.get("sources")
        ):

            st.caption("Sources:")

            for source in message["sources"]:

                st.caption(
                    f"📄 {source}"
                )


# --------------------------------------------------
# Chat Input
# --------------------------------------------------

question = st.chat_input(
    "Ask a question about company policies..."
)


# --------------------------------------------------
# Process Question
# --------------------------------------------------

if question:

    # ----------------------------------------------
    # Save User Message
    # ----------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    # ----------------------------------------------
    # Display User Question
    # ----------------------------------------------

    with st.chat_message("user"):

        st.markdown(question)


    # ----------------------------------------------
    # Generate Assistant Response
    # ----------------------------------------------

    with st.chat_message("assistant"):

        try:

            # --------------------------------------
            # Query Rewriting
            # --------------------------------------

            with st.spinner(
                "Understanding your question..."
            ):

                chat_history = (
                    st.session_state.messages[:-1]
                )

                standalone_question = rewrite_query(
                    question,
                    chat_history
                )


            # --------------------------------------
            # Retrieve Relevant Documents
            # --------------------------------------

            with st.spinner(
                "Searching company documents..."
            ):

                results = retrieve_chunks(
                    standalone_question,
                    top_k=1
                )


            # --------------------------------------
            # Extract Retrieval Results
            # --------------------------------------

            documents = results.get(
                "documents",
                [[]]
            )

            metadatas = results.get(
                "metadatas",
                [[]]
            )


            # --------------------------------------
            # Check Whether Documents Were Found
            # --------------------------------------

            if (
                not documents
                or not documents[0]
            ):

                answer = (
                    "I couldn't find this information "
                    "in the company documents."
                )

                sources = []


            else:

                # ----------------------------------
                # Build Context
                # ----------------------------------

                context = "\n\n".join(
                    documents[0]
                )


                # ----------------------------------
                # Generate Grounded Answer
                # ----------------------------------

                with st.spinner(
                    "Generating answer..."
                ):

                    answer = generate_answer(
                        context,
                        standalone_question
                    )


                # ----------------------------------
                # Check If Answer Was Found
                # ----------------------------------

                answer_not_found = (
                    "I couldn't find this information "
                    "in the company documents."
                    in answer
                )


                # ----------------------------------
                # Collect Sources
                # ----------------------------------

                sources = set()

                if not answer_not_found:

                    if (
                        metadatas
                        and metadatas[0]
                    ):

                        for metadata in metadatas[0]:

                            if (
                                metadata
                                and "source"
                                in metadata
                            ):

                                sources.add(
                                    metadata["source"]
                                )


            # --------------------------------------
            # Display Answer
            # --------------------------------------

            st.markdown(answer)


            # --------------------------------------
            # Display Sources
            # --------------------------------------

            if sources:

                st.caption("Sources:")

                for source in sources:

                    st.caption(
                        f"📄 {source}"
                    )


            # --------------------------------------
            # Save Assistant Message
            # --------------------------------------

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                    "sources": list(sources)
                }
            )


        except Exception as e:

            # --------------------------------------
            # Error Handling
            # --------------------------------------

            error_message = (
                "Something went wrong while "
                "processing your question."
            )

            st.error(error_message)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": error_message,
                    "sources": []
                }
            )