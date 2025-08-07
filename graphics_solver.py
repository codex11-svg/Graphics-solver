import streamlit as st
import solver
import google.generativeai as genai

st.title("Engineering Graphics Solver 🚀")
st.write(
    "Input a classic engineering graphics question (e.g., pyramids, prisms, etc, with section).\n"
    "See Gemini's stepwise answer **plus all six stages** of diagram construction."
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
        stages = solver.plot_hex_pyramid_stages(**params)
        for title, fig in stages:
            st.markdown(f"**{title}**")
            st.pyplot(fig)
    elif typ == 'square_prism':
        params = solver.parse_square_prism_section(question)
        stages = solver.plot_square_prism_stages(**params)
        for title, fig in stages:
            st.markdown(f"**{title}**")
            st.pyplot(fig)
    elif typ == 'tri_prism':
        params = solver.parse_tri_prism_section(question)
        stages = solver.plot_tri_prism_stages(**params)
        for title, fig in stages:
            st.markdown(f"**{title}**")
            st.pyplot(fig)
    else:
        st.info("Staged conceptual diagrams: pyramid and prism cases supported. Tell us your next required solid/section!")
        
