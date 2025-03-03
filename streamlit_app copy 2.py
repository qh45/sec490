import streamlit as st
import json
from datetime import datetime

# Function to format the timestamp
def format_timestamp(timestamp):
    try:
        dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f%z")
        return dt.strftime("%-m/%-d/%y %H:%M")
    except ValueError:
        return "Invalid Timestamp"

# Streamlit app
st.title("Interactive JSON Viewer")

# Text area for JSON input
st.subheader("Input JSON Data")
json_input = st.text_area("Paste your JSON data here:", height=200)

if json_input:
    try:
        # Parse the input JSON
        data = json.loads(json_input)

        st.success("JSON loaded successfully!")

        # Always display Agent Host
        st.subheader("Field Values")
        st.markdown(f"**Agent Host:** ____")  # Placeholder for actual data
        st.markdown(f"**Timestamp:** {format_timestamp(data.get('timestamp', 'N/A'))}")

        # Define fields with dynamic default selection based on values
        all_fields = {
            "Source IP": data.get('src_ip', 'N/A'),
            "Dest IP": data.get('dest_ip', 'N/A'),
            "Source Port": data.get('src_port', 'N/A'),
            "Dest Port": data.get('dest_port', 'N/A'),
            "Bytes to Client": data.get('flow', {}).get('bytes_toclient', 'N/A'),
            "Hostname": data.get('http', {}).get('hostname', 'N/A'),
            "Signature": data.get('alert', {}).get('signature', 'N/A'),
            "Category": data.get('alert', {}).get('category', 'N/A'),
            "MITRE Technique Name": data.get('alert', {}).get('metadata', {}).get('mitre_technique_name', ['N/A'])[0],
            "HTTP User Agent": data.get('http', {}).get('http_user_agent', 'N/A')
        }

        # Automatically select only the fields with values (not N/A) as defaults
        default_fields = [field for field, value in all_fields.items() if value != 'N/A']

        # Checklist for other fields
        fields_to_display = st.multiselect(
            "Choose additional fields to display:",
            list(all_fields.keys()),
            default=default_fields
        )

        # Display selected fields without empty lines
        for field in fields_to_display:
            st.markdown(f"**{field}:** {all_fields[field]}")

    except json.JSONDecodeError:
        st.error("Invalid JSON! Please check your input.")
else:
    st.info("Awaiting JSON input...")
