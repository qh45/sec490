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
        st.write(f"**Agent Host:** ____")  # Placeholder for actual data

        # Format and display the timestamp
        st.write(f"**Timestamp:** {format_timestamp(data.get('timestamp', 'N/A'))}")

        # Checklist for other fields
        fields_to_display = st.multiselect(
            "Choose additional fields to display:",
            ["Source IP", "Dest IP", "Source Port", "Dest Port", "Bytes to Client", "Hostname"],
            default=["Source IP", "Dest IP", "Source Port", "Dest Port", "Bytes to Client", "Hostname"]
        )

        # Display selected fields
        for field in fields_to_display:
            if field == "Source IP":
                st.write(f"**Source IP:** {data.get('src_ip', 'N/A')}")
            elif field == "Dest IP":
                st.write(f"**Dest IP:** {data.get('dest_ip', 'N/A')}")
            elif field == "Source Port":
                st.write(f"**Source Port:** {data.get('src_port', 'N/A')}")
            elif field == "Dest Port":
                st.write(f"**Dest Port:** {data.get('dest_port', 'N/A')}")
            elif field == "Bytes to Client":
                st.write(f"**Bytes to Client:** {data.get('flow', {}).get('bytes_toclient', 'N/A')}")
            elif field == "Hostname":
                st.write(f"**Hostname:** {data.get('http', {}).get('hostname', 'N/A')}")

    except json.JSONDecodeError:
        st.error("Invalid JSON! Please check your input.")
else:
    st.info("Awaiting JSON input...")
