import streamlit as st
import scraper
import google.generativeai as genai
import os
import json
import pandas as pd
import re

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

def get_ip_analysis(text):
    """
    Analyzes the provided text using an AI to identify intellectual property.
    """
    prompt = f"""
    You are a seasoned intellectual property analyst. Your task is to analyze a company's business
    description and website content to identify its key intangible assets and intellectual property (IP).

    The output should be a single JSON object. The JSON should contain a key called "intellectual_properties"
    which is a list of objects. Each object in the list must contain the following keys:
    - name: (string, the name of the IP, e.g., "Brand", "Patents", "Know-how")
    - description: (string, a brief 25-word description of the IP)
    - importance_score: (integer, 1-10, with 10 being the most critical to the company's value proposition)
    - actions: (object with boolean keys: develops, enhances, maintains, protects, exploits)

    Sort the list of IP from highest to lowest importance_score.

    Use the following provided text:
    {text}
    """

    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    
    # Extract the JSON string from the response using a regular expression
    json_match = re.search(r'```json\s*(\{.*?\})\s*```', response.text, re.DOTALL)
    
    if json_match:
        # Return the clean JSON string
        return json_match.group(1)
    else:
        # Return the raw text if no JSON is found
        return response.text

# Rest of the app.py file

def parse_and_format_ip_data(json_string):
    """
    Parses the JSON string, sorts the data, and returns a DataFrame.
    """
    try:
        data = json.loads(json_string)
        df = pd.DataFrame(data['intellectual_properties'])

        # Now we sort the DataFrame by importance_score in descending order
        df = df.sort_values(by='importance_score', ascending=False)

        # The 'actions' column contains a dictionary, so we need to expand it
        actions_df = pd.json_normalize(df['actions'])
        df = pd.concat([df.drop('actions', axis=1), actions_df], axis=1)

        return df
    except (json.JSONDecodeError, KeyError) as e:
        st.error(f"Error parsing AI output: {e}")
        return None

# Set the page title and a brief introduction
st.set_page_config(page_title="IP Finder App", page_icon="💡")
st.title("💡 IP Finder App")
st.write("Enter a company's website and business description to identify its likely intellectual property.")

# Add input boxes for the company's website URL and business description
website_url = st.text_input("Company Website URL", help="e.g., https://www.google.com")
business_description = st.text_area("Business Description", height=150, help="e.g., A technology company specializing in artificial intelligence and machine learning solutions.")

# The lines above this are correct
# ...
# Here is the correct indentation for your button block

if st.button("Analyze Intellectual Property", key="analyze_button"):
    if website_url and business_description:
        with st.spinner('Analyzing...'):
            all_text = scraper.get_text_from_url(website_url)
            
            links_to_scrape = scraper.get_links_from_url(website_url)
            for link in links_to_scrape[:2]:
                all_text += " " + scraper.get_text_from_url(link)
            
            # This is where we call the AI and get the result
            combined_text = all_text + " " + business_description
            ai_output = get_ip_analysis(combined_text)

            # This block of code is now correctly indented
            formatted_df = parse_and_format_ip_data(ai_output)

            if formatted_df is not None:
                st.subheader("Intellectual Property Analysis")
                st.dataframe(formatted_df, use_container_width=True)
                
            st.success("Analysis complete!")
    else:
        st.warning("Please enter both a website URL and a business description.")