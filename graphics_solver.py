import streamlit as st
import solver
import google.generativeai as genai

st.title("Engineering Graphics Solver 🚀")
st.write(
    "Enter a descriptive engineering graphics problem (e.g., about hexagonal pyramids and section planes).\n"
    "You receive: (1) Gemini AI step-by-step answer, (2) an exam-style 2D conceptual diagram for classic problems."
)

# Gemini API Setup
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
if not GEMINI_API_KEY:
    st.error("Gemini API Key missing in Streamlit secrets.")
    st.stop()
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

question = st.text_area("Enter your question:", height=140)
if st.button("Solve (Gemini Answer + 2D Conceptual Diagram)") and question.strip():
    # 1. Gemini answer
    with st.spinner("Gemini is analyzing your question..."):
        try:
            response = model.generate_content([question.strip()])
            st.success("Gemini AI Solution:")
            st.write(getattr(response, "text", None) or str(response))
        except Exception as e:
            st.error(f"Error from Gemini: {e}")

    # 2. Conceptual diagram for classic cases
    if all(word in question.lower() for word in ['hexagonal', 'pyramid', 'section']):
        params = solver.parse_hex_pyramid_section(question)
        fig = solver.plot_hex_pyramid_conceptual(
            base_side=params['base_side'],
            axis_height=params['axis_height'],
            section_angle=params['section_angle']
        )
        st.markdown("**Conceptual 2D Diagram (Exam Style):**")
        st.pyplot(fig)
        st.info("Front view, sectional top view, and true shape drawn as for university/board exams.")
    else:
        st.info("Conceptual diagrams auto-generate for recognized classic hexagonal pyramid + section problems. Want more cases? Let us know!")

st.markdown(
    """
    ℹ️ **Example:**<br>
    "A hexagonal pyramid base 30 mm side, axis 65 mm long has its base on H.P. with an edge of base parallel to V.P. A section plane perpendicular to V.P. and inclined at 60º to H.P. bisects the axis of the pyramid. Draw front view, sectional top view and true shape of the section."
    """, unsafe_allow_html=True
)
