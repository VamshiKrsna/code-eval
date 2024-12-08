import streamlit as st
import os
from src.llm_integrator import LLMPerformanceAnalyzer
from code_editor import code_editor

def main():
    st.set_page_config(
        page_title="Python Code Performance Analyzer",
        page_icon="🚀",
        layout="wide"
    )

    st.title("🚀 Python Code Performance Analyzer")
    st.markdown("""
    Upload your Python code and get AI-powered performance insights!
    
    ### How it works:
    1. Upload a Python file or paste your code
    2. Click "Analyze Performance"
    3. Receive detailed insights on potential performance bottlenecks
    """)

    # API Key input (mandatory to set up gemini)
    api_key = st.text_input(
        "Enter your Google Gemini API Key", 
        type="password", 
        help="You can get an API key from Google AI Studio"
    )

    input_method = st.radio(
        "Choose input method:", 
        ["Upload Python File", "Paste Code"]
    )

    code = ""
    if input_method == "Upload Python File":
        uploaded_file = st.file_uploader(
            "Choose a Python file", 
            type=["py"], 
            help="Upload a .py file to analyze"
        )
        if uploaded_file is not None:
            code = uploaded_file.getvalue().decode("utf-8")
    else:
        code = st.text_area("Write your Python Code here ")


    if st.button("🔍 Analyze Performance", type="primary"):
        if not code.strip(): 
            # if code is empty
            st.error("Please upload a file or paste some code!")
            return
        
        if not api_key and not os.getenv('GEMINI_API_KEY'):
            st.error("Please provide a Gemini API key!")
            return

        with st.spinner("Analyzing your code..."):
            try:
                analyzer = LLMPerformanceAnalyzer(api_key)
                
                performance_insights = analyzer.analyze_code_performance(code)
                
                if performance_insights:
                    st.subheader("🔬 Performance Insights")
                    
                    severity_colors = {
                        'low': 'green',
                        'medium': 'orange',
                        'high': 'red'
                    }
                    
                    for insight in performance_insights:
                        severity_color = severity_colors.get(insight.severity.lower(), 'blue')
                        
                        st.markdown(f"""
                        #### {insight.issue_type} 
                        **Severity**: <span style='color:{severity_color}'>{insight.severity.upper()}</span>
                        
                        **Description**: {insight.description}
                        
                        **Line Number**: {insight.line_number or 'N/A'}
                        
                        **Suggested Optimization**: {insight.suggested_optimization}
                        
                        ---
                        """, unsafe_allow_html=True)
                else:
                    st.info("No performance insights found. Your code looks good!")
            
            except Exception as e:
                st.error(f"An error occurred: {e}")

    st.markdown("---")
    st.markdown("*Powered by Gemini AI - Performance Insights*")

if __name__ == "__main__":
    main()