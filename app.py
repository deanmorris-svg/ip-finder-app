import streamlit as st

# Set the page title and a brief introduction
st.set_page_config(page_title="IP Finder App", page_icon="💡")
st.title("💡 IP Finder App")
st.write("Enter a company's website and business description to identify its likely intellectual property.")

# Add input boxes for the company's website URL and business description
website_url = st.text_input("Company Website URL", help="e.g., https://www.google.com")
business_description = st.text_area("Business Description", height=150, help="e.g., A technology company specializing in artificial intelligence and machine learning solutions.")

# Create a button to submit the data. We won't add any functionality yet.
if st.button("Analyze Intellectual Property"):
    st.write("Button clicked! We'll add the analysis in Phase 3.")