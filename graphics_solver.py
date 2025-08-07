import streamlit as st
import solver
import google.generativeai as genai

st.title("Engineering Graphics Solver 🚀")
st.write(
    "Enter any classic engineering graphics question (e.g., about pyramids, sections, projections). "
    "You'll receive a Gemini AI solution and an automated 3D diagram for recognized solids (e.g., sectioned hexagonal pyramid)."
)

# Gemini API config
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
if not GEMINI_API_KEY:
    st.error("Gemini API Key is missing. Add it to Streamlit secrets.")
    st.stop()
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

question = st.text_area("Enter your question:", height=140)
if st.button("Solve (Gemini Answer + 3D Diagram)") and question.strip():
    # 1. Gemini AI solution
    with st.spinner("Gemini is analyzing your question..."):
        try:
            response = model.generate_content([question.strip()])
            st.success("Gemini AI Solution:")
            st.write(getattr(response, "text", None) or str(response))
        except Exception as e:
            st.error(f"Error from Gemini: {e}")

    # 2. Automated 3D Diagram (hexagonal pyramid with inclined section)
    if all(word in question.lower() for word in ['hexagonal', 'pyramid', 'section']):
        params = solver.parse_hex_pyramid_section(question)
        fig = solver.plot_hex_pyramid_section(
            base_side=params['base_side'],
            axis_height=params['axis_height'],
            section_angle_deg=params['section_angle']
        )
        st.markdown("**Automated 3D Diagram:**")
        st.pyplot(fig)
        st.info("3D diagram auto-generates for classic hexagonal pyramid with inclined section questions. More cases coming soon!")
    else:
        st.info("Diagram generation supports classic hexagonal pyramid + section problems. To extend, specify other solid/section features you want.")

st.markdown(
    """
    ℹ️ **Example:**  
    "A hexagonal pyramid base 30 mm side, axis 65 mm long has its base on H.P. with an edge of base parallel to V.P. A section plane perpendicular to V.P. and inclined at 60º to H.P. bisects the axis of the pyramid. Draw front view, sectional top view and true shape of the section."
    """
)
