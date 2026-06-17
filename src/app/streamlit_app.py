from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

import streamlit as st

from src.pipelines.rag_pipeline import RAGPipeline


st.set_page_config(
    page_title="France Mutuelle Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Assistant Interne France Mutuelle")


if "rag_pipeline" not in st.session_state:

    st.session_state.rag_pipeline = RAGPipeline()

if "messages" not in st.session_state:

    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


question = st.chat_input(
    "Posez votre question..."
)


if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

    result = st.session_state.rag_pipeline.ask(
        question
    )

    answer = result["answer"]

    sources = result["sources"]

    final_answer = answer

    if sources:

        final_answer += "\n\n---\n\n"
        final_answer += "### 📚 Sources\n"

        for source in sources:

            file_name = source["file"]

            section = source["section"]

            if section:

                final_answer += (
                    f"- {file_name} > {section}\n"
                )

            else:

                final_answer += (
                    f"- {file_name}\n"
                )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": final_answer
        }
    )

    with st.chat_message("assistant"):

        st.markdown(final_answer)