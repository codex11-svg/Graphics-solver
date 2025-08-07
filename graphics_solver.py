import streamlit as st
import solver
import google.generativeai as genai

st.title("Engineering Graphics Solver 🚀")
st.write(
    "Input a classic engineering graphics question (e.g., pyramids, prisms, cones, cylinders, frustums, intersection, with section planes)."
    "\nYou get:\n"
    "(1) Gemini AI - expert, stepwise text solution\n"
    "(2) Automated conceptual exam-style 2D diagrams: Front/Elevation, Top/Plan (hatched if cut), True Shape (if inclined cut), with labels\n"
)

GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

question = st.text_area("Enter your question:", height=140)

if st.button("Solve") and question.strip():
    # Gemini answer
    with st.spinner("Gemini is analyzing your question..."):
        try:
            response = model.generate_content([question.strip()])
            st.success("Gemini AI Solution / Steps:")
            st.write(getattr(response, "text", None) or str(response))
        except Exception as e:
            st.error(f"Error from Gemini: {e}")

    # Classification + diagram selection
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
    # elif typ == "cylinder": ... (to be added)
    # elif typ == "cone": ... (to be added)
    # elif typ == "frustum": ... (to be added)
    # elif typ == "sphere": ... (to be added)
    # elif typ == "combined": ... (to be added)

    else:
        st.info("Conceptual diagrams auto-generate for standard solids/sections; more types coming on request!")

st.markdown("""
**Currently supported:**<br>
- Hexagonal pyramid, square prism, triangular prism—with section planes.<br>
**Just ask to add cylinders, cones, frustums, spheres, intersecting solids and more!**
""", unsafe_allow_html=True)
