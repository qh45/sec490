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

# Function to convert bytes to KB or MB (no decimals)
def convert_bytes(value):
    try:
        kb_value = value // 1024
        if kb_value > 9999:  # Convert to MB if KB > 9999
            return f"{kb_value // 1024} MB"
        else:
            return f"{kb_value} KB"
    except (TypeError, ValueError):
        return "N/A"

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
            "Bytes to Client": convert_bytes(data.get('flow', {}).get('bytes_toclient')),
            "Bytes to Server": convert_bytes(data.get('flow', {}).get('bytes_toserver')),
            "Hostname": data.get('http', {}).get('hostname', 'N/A'),
            "Signature": data.get('alert', {}).get('signature', 'N/A'),
            "Category": data.get('alert', {}).get('category', 'N/A'),
            "MITRE Technique Name": data.get('alert', {}).get('metadata', {}).get('mitre_technique_name', ['N/A'])[0],
            "HTTP User Agent": data.get('http', {}).get('http_user_agent', 'N/A'),
            "HTTP Refer": data.get('http', {}).get('http_refer', 'N/A'),
            "URL": data.get('http', {}).get('url', 'N/A'),
            "Application Protocol": data.get('app_proto', 'N/A')
        }

        # Automatically select only fields with values (not N/A), excluding app_proto if "http"
        default_fields = [
            field for field, value in all_fields.items()
            if value != 'N/A' and not (field == "Application Protocol" and value == "http")
        ]

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
