import streamlit as st
import warnings

warnings.filterwarnings("ignore")

from researcher_demo.crew import generate_content

# Streamlit page config
st.set_page_config(page_title="Conetent Researcher & Writer", layout="wide")

# Title and description
st.title("Content Researcher & Writer, powered by CrewAI")
st.markdown("Generate blog posts about any topic using AI agents.")

# Sidebar
with st.sidebar:
    st.header("Content Settings")

    # Make the text input take up more space
    topic = st.text_area("Enter your topic", height=100, placeholder="Enter the topic")

    # Add more sidebar controls if needed
    st.markdown("### LLM Settings")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.5)

    # Add some spacing
    st.markdown("---")

    # Make the generate button more prminent in the sidebar
    generate_button = st.button(
        "Generate Conent", type="primary", use_container_width=True
    )

    # Add some helpful information
    with st.expander("ℹ️ How to use"):
        st.markdown(
            """
            1. Enter your desired content topic
            2. Play with the temperture
            3. Click 'Generate Content' to start
            4. Wait for the AI to generate your article
            5. Download the result as a markdown file            
            """
        )

# Main content area
if generate_button:
    with st.spinner("generating content... This may take a moment."):
        try:
            result = generate_content(topic)
            st.markdown("### Generated Content")
            st.markdown(result)

            # Add download button
            st.download_button(
                label="Download Content",
                data=result.raw,
                file_name=f"{topic.lower().replace(' ', '_')}_article.md",
                mime="text/markdown",
            )
        except Exception as e:
            st.error(f"An error occured: \n{str(e)}")

# Footer
st.markdown("---")
st.markdown("Built with CrewAI, Streamlit and Openai")
