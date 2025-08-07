import streamlit as st
import solver
import google.generativeai as genai

st.title("Engineering Graphics Solver 🚀")
st.write(
    "Input a classic engineering graphics question (e.g., pyramids, prisms, sections, with section planes).\n"
    "You'll get:\n"
    "1. Gemini AI detailed answer\n"
    "2. Automated 2D exam-style diagram: FV, TV (sectioned/hatch), true shape\n"
)

GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

question = st.text_area("Enter your question:", height=140)

if st.button("Solve") and question.strip():
    with st.spinner("Gemini is analyzing your question..."):
        try:
            response = model.generate_content([question.strip()])
            st.success("Gemini AI Solution / Steps:")
            st.write(getattr(response, "text", None) or str(response))
        except Exception as e:
            st.error(f"Error from Gemini: {e}")

    typ = solver.classify_problem_type(question)
    if typ == 'hex_pyramid':
        params = solver.parse_hex_pyramid_section(question)
        fig = solver.plot_hex_pyramid_conceptual(**params)
        st.markdown("**Hexagonal Pyramid – Conceptual Views (Exam Style):**")
        st.pyplot(fig)
    elif typ == 'square_prism':
        params = solver.parse_square_prism_section(question)
        fig = solver.plot_square_prism_conceptual(**params)
        st.markdown("**Square Prism – Conceptual Views (Exam Style):**")
        st.pyplot(fig)
    elif typ == 'tri_prism':
        params = solver.parse_tri_prism_section(question)
        fig = solver.plot_tri_prism_conceptual(**params)
        st.markdown("**Triangular Prism – Conceptual Views (Exam Style):**")
        st.pyplot(fig)
    # Placeholders for more: cylinder, cone, frustum, sphere, combined:
    else:
        st.info("Conceptual diagrams auto-generate for pyramids/prisms with sections; more solids and views coming soon. Tell us your shape to add next!")

st.markdown("""
**Current support:** Hexagonal pyramid, square prism, triangular prism (with section planes, all views).<br>
More solids (cylinder, cone, frustum, sphere, penetration) can be added immediately—just ask!
""", unsafe_allow_html=True)
