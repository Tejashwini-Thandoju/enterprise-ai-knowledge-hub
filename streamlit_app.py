import streamlit as st

from src.retriever.retriever import (
    retrieve_chunks,
    collection
)

from src.llm.groq_client import (
    generate_answer,
    rewrite_query
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Enterprise AI Knowledge Hub",
    page_icon="📚",
    layout="wide"
)


# ============================================================
# HELPER: GET DOCUMENT COUNT
# ============================================================

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


# ============================================================
# SIDEBAR
# ============================================================

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


# ============================================================
# MAIN TITLE
# ============================================================

st.title("📚 Enterprise AI Knowledge Hub")

st.write(
    "Ask questions about company policies and get "
    "answers based on the organization's documents."
)


# ============================================================
# INITIALIZE CHAT HISTORY
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# ============================================================
# DISPLAY PREVIOUS MESSAGES
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

        # -----------------------------------------------
        # Display Sources
        # -----------------------------------------------

        if (
            message["role"] == "assistant"
            and message.get("sources")
        ):

            st.caption("Sources:")

            for source in message["sources"]:

                st.caption(
                    f"📄 {source}"
                )


# ============================================================
# CHAT INPUT
# ============================================================

question = st.chat_input(
    "Ask a question about company policies..."
)


# ============================================================
# PROCESS QUESTION
# ============================================================

if question:

    # --------------------------------------------------------
    # Save User Message
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    # --------------------------------------------------------
    # Display User Question
    # --------------------------------------------------------

    with st.chat_message("user"):

        st.markdown(question)


    # --------------------------------------------------------
    # Generate Assistant Response
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        try:

            # ==================================================
            # QUERY REWRITING
            # ==================================================

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


            # ==================================================
            # RETRIEVE RELEVANT DOCUMENTS
            # ==================================================

            with st.spinner(
                "Searching company documents..."
            ):

                results = retrieve_chunks(
                    standalone_question,
                    top_k=5
                )


            # ==================================================
            # EXTRACT RESULTS
            # ==================================================

            documents = results.get(
                "documents",
                [[]]
            )

            metadatas = results.get(
                "metadatas",
                [[]]
            )


            # ==================================================
            # CHECK DOCUMENTS
            # ==================================================

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

                # ==================================================
                # BUILD CONTEXT
                # ==================================================

                context_parts = []

                for document in documents[0]:

                    if (
                        document
                        and document.strip()
                    ):

                        context_parts.append(
                            document.strip()
                        )

                context = "\n\n---\n\n".join(
                    context_parts
                )


                # ==================================================
                # GENERATE GROUNDED ANSWER
                # ==================================================

                with st.spinner(
                    "Generating answer..."
                ):

                    answer = generate_answer(
                        context,
                        standalone_question
                    )


                # ==================================================
                # CHECK IF ANSWER WAS FOUND
                # ==================================================

                fallback_message = (
                    "I couldn't find this information "
                    "in the company documents."
                )

                answer_not_found = (
                    fallback_message.lower()
                    in answer.lower()
                )


                # ==================================================
                # COLLECT SOURCES
                # ==================================================

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


            # ==================================================
            # DISPLAY ANSWER
            # ==================================================

            st.markdown(answer)


            # ==================================================
            # DISPLAY SOURCES
            # ==================================================

            if sources:

                st.caption("Sources:")

                # Show only the most relevant source
                # instead of all retrieved documents.

                displayed_sources = list(sources)[:1]

                for source in displayed_sources:

                    st.caption(
                        f"📄 {source}"
                    )


            # ==================================================
            # SAVE ASSISTANT MESSAGE
            # ==================================================

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                    "sources": list(sources)
                }
            )


        except Exception as e:

            # ==================================================
            # ERROR HANDLING
            # ==================================================

            error_message = (
                "Something went wrong while "
                "processing your question."
            )

            st.error(
                error_message
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": error_message,
                    "sources": []
                }
            )