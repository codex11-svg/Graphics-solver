import streamlit as st
import solver
import google.generativeai as genai

st.title("Engineering Graphics Solver 🚀")
st.write(
    "Enter a descriptive engineering graphics problem (e.g., about pyramids, sections, projections).\n"
    "You'll receive a Gemini AI expert answer and a conceptual 2D exam-style diagram matching your question (for hexagonal pyramid problems)."
)

# Gemini API config
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
if not GEMINI_API_KEY:
    st.error("Gemini API Key missing in Streamlit secrets.")
    st.stop()
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

question = st.text_area("Enter your question:", height=140)
if st.button("Solve (Gemini Answer + 2D Conceptual Diagram)") and question.strip():
    # 1. Gemini AI solution
    with st.spinner("Gemini is analyzing your question..."):
        try:
            response = model.generate_content([question.strip()])
            st.success("Gemini AI Solution:")
            st.write(getattr(response, "text", None) or str(response))
        except Exception as e:
            st.error(f"Error from Gemini: {e}")

    # 2. Automated 2D Schematic Diagram
    if all(word in question.lower() for word in ['hexagonal', 'pyramid', 'section']):
        params = solver.parse_hex_pyramid_section(question)
        fig = solver.plot_hex_pyramid_conceptual(
            base_side=params['base_side'],
            axis_height=params['axis_height'],
            section_angle=params['section_angle']
        )
        st.markdown("**Conceptual 2D Diagram (Exam Style):**")
        st.pyplot(fig)
        st.info("2D reference schematic matches classic front/plan/true-shape layout.")
    else:
        st.info("Conceptual diagram auto-generates for hexagonal pyramid with section problems. Extendable to more figure types—let us know what you want next!")

st.markdown(
    """
    ℹ️ **Example question:**  
    "A hexagonal pyramid base 30 mm side, axis 65 mm long has its base on H.P. with an edge of base parallel to V.P. A section plane perpendicular to V.P. and inclined at 60º to H.P. bisects the axis of the pyramid. Draw front view, sectional top view and true shape of the section."
    """
)
