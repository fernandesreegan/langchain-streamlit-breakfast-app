import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pprint import pformat

# Load environment variables from .env file (automatically reads OPENAI_API_KEY)
load_dotenv()

# Streamlit Page Configuration
st.set_page_config(page_title="LangChain Breakfast Generator", layout="wide")

# CSS snippet to force code blocks and text areas to soft-wrap lines instead of horizontally scrolling
st.markdown("""
    <style>
    code, pre {
        white-space: pre-wrap !important;
        word-break: break-word !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🍳 LangChain Healthy Breakfast Assignment")
st.caption("Assignment | learn. build. operate")

# Initialize LLM with low temperature for consistency
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Define Tabs
tab1, tab2 = st.tabs(["Stage 1: Raw invoke() Object", "Stage 2: Refined & Formatted Output"])

# =====================================================================
# STAGE 1: Unfiltered / Raw Invoke Output
# =====================================================================
with tab1:
    st.header("Stage 1: Unfiltered Model Response")
    st.write(
        "Calling `llm.invoke()` directly hands back a full LangChain `AIMessage` object, "
        "not just a string text."
    )
    
    if st.button("Run Stage 1 (Raw Object)", type="primary"):
        with st.spinner("Invoking model..."):
            raw_response = llm.invoke("Give me 5 healthy breakfast ideas.")
            
        st.subheader("Raw `AIMessage` Object Inspection:")
        
        # Method 1: Pretty-printed object representation with word wrapping
        formatted_object = pformat(raw_response, width=80)
        st.code(formatted_object, language="python")
        
        # Method 2: Structured dictionary view via st.json
        with st.expander("View as Formatted JSON / Dictionary"):
            st.json({
                "type": raw_response.__class__.__name__,
                "content": raw_response.content,
                "response_metadata": raw_response.response_metadata,
                "id": raw_response.id
            })
        
        st.info(
            "💡 **Observation:** The output is an `AIMessage` instance containing `content`, "
            "`response_metadata` (token counts, finish reason), and `id`."
        )

# =====================================================================
# STAGE 2: Refined Prompt with Specific Constraints
# =====================================================================
with tab2:
    st.header("Stage 2: Refined Prompt & Formatted Output")
    st.write(
        "Here we explicitly define the criteria for 'healthy' in the system prompt "
        "and access `.content` for clean UI rendering."
    )
    
    # Allow user to tweak parameters live
    col1, col2 = st.columns(2)
    with col1:
        min_protein = st.number_input("Min Protein (g)", value=15)
        min_fiber = st.number_input("Min Fiber (g)", value=5)
    with col2:
        max_sugar = st.number_input("Max Added Sugar (g)", value=5)
        meal_type = st.selectbox("Context", ["Quick weekday morning", "Post-workout", "Weekend brunch"])

    refined_prompt = ChatPromptTemplate.from_messages([
        ("system", 
         "You are a clinical nutritionist. A 'healthy breakfast' must strictly meet these criteria:\n"
         f"- High protein (>= {min_protein}g)\n"
         f"- High fiber (>= {min_fiber}g)\n"
         f"- Low added sugar (< {max_sugar}g)\n"
         "- Contains complex carbohydrates and healthy fats\n\n"
         "Always format each item clearly with name, short description, and estimated macro profile."),
        ("user", "Give me 5 healthy breakfast ideas for a {context}.")
    ])

    chain = refined_prompt | llm

    if st.button("Generate Refined Ideas"):
        with st.spinner("Generating nutritionist-backed ideas..."):
            response = chain.invoke({"context": meal_type})
            
        st.subheader("Clean Text Output (`response.content`):")
        # Extract strictly the text content attribute
        st.markdown(response.content)

# =====================================================================
# CONCEPTUAL QUESTIONS RECAP
# =====================================================================
st.divider()
with st.expander("📝 Assignment Q&A Summary"):
    st.markdown("""
    * **1. What do you see printing `invoke()` directly?**  
      `invoke()` returns an `AIMessage` wrapper object. To get the text, you must access `.content` or pipe into a `StrOutputParser()`.
    * **2. How to ensure the same 5 ideas every single run?**  
      Set `temperature=0` (and optionally a fixed `seed` in `ChatOpenAI`), and make your prompt constraints completely explicit.
    * **3. Did you define 'healthy' or let the model decide?**  
      In Stage 1, the LLM decides based on generic training patterns. In Stage 2, we define exact macro thresholds (protein, fiber, sugar limits) in the system prompt.
    """)