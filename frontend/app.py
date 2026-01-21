import streamlit as st
import requests
import json
from PIL import Image
import os
from datetime import datetime

API_BASE = "http://localhost:8000"

st.title("Chronicle AI - Institutional Memory Agent")
st.markdown("**Preserve institutional knowledge, learn from the past, and make evidence-based decisions.**")

st.sidebar.header("Navigation")
page = st.sidebar.radio("Choose Action", ["Search Institutional Memory", "Add Institutional Memory"])

if page == "Search Institutional Memory":
    st.header("Search Institutional Memory")

    query = st.text_input("Query", placeholder="e.g., What lessons were learned from past flood response failures?")

    st.subheader("Optional Filters")
    col1, col2 = st.columns(2)

    with col1:
        department_filter = st.selectbox("Department Filter", ["", "Emergency Management", "Finance", "Infrastructure", "Other"], index=0)
        outcome_filter = st.selectbox("Outcome Filter", ["", "success", "failure", "mixed"], index=0)
        data_type = st.selectbox("Data Type", ["both", "text", "image"], index=0)

    with col2:
        date_from = st.date_input("Date From", value=None)
        date_to = st.date_input("Date To", value=None)
        location_filter = st.text_input("Location Filter")

    tags_filter = st.multiselect("Tags Filter", ["policy", "budget", "flood", "infrastructure", "emergency", "monitoring", "evacuation", "cybersecurity"])

    st.subheader("Advanced Options")
    col3, col4 = st.columns(2)

    with col3:
        top_k = st.slider("Top K Results", 3, 10, 5)
        reasoning_mode = st.selectbox("Reasoning Mode", ["summary", "comparison", "recommendation"], index=0)

    with col4:
        evidence_strictness = st.slider("Evidence Strictness", 1, 10, 7)
        include_images = st.checkbox("Include Visual Evidence", value=True)

    if st.button("Search", type="primary"):
        if query:
            filters = {}
            if department_filter:
                filters["department"] = department_filter
            if outcome_filter:
                filters["outcome"] = outcome_filter
            if location_filter:
                filters["location"] = location_filter
            if tags_filter:
                filters["tags"] = tags_filter
            if date_from:
                filters["date_from"] = str(date_from)
            if date_to:
                filters["date_to"] = str(date_to)

            payload = {
                "query": query,
                "filters": filters if filters else None,
                "limit": top_k,
                "data_type": data_type,
                "reasoning_mode": reasoning_mode,
                "include_images": include_images,
                "evidence_strictness": evidence_strictness
            }

            with st.spinner("Searching institutional memory..."):
                try:
                    response = requests.post(f"{API_BASE}/query", json=payload)
                    if response.status_code == 200:
                        result = response.json()

                        st.success("Search completed!")

                        st.subheader("Summary")
                        st.write(result.get("summary", "No summary available"))

                        st.subheader("Reasoning")
                        st.write(result.get("reasoning", "No reasoning available"))

                        st.subheader("Retrieved Memories")
                        memories = result.get("memories", [])
                        if memories:
                            for i, memory in enumerate(memories, 1):
                                with st.expander(f"#{i} {memory['department']} - {memory['date']} ({memory['outcome']})"):
                                    st.write(f"**Type:** {memory['type']}")
                                    if memory.get('text'):
                                        st.write(f"**Content:** {memory['text'][:500]}{'...' if len(memory['text']) > 500 else ''}")
                                    if memory.get('image_url'):
                                        try:
                                            image = Image.open(memory['image_url'])
                                            st.image(image, caption=f"Visual Evidence - {memory['image_url']}", use_column_width=True)
                                        except:
                                            st.write(f"**Image:** {memory['image_url']}")
                                    if memory.get('location'):
                                        st.write(f"**Location:** {memory['location']}")
                                    if memory.get('tags'):
                                        st.write(f"**Tags:** {', '.join(memory['tags'])}")
                        else:
                            st.info("No memories found matching your criteria.")
                    else:
                        st.error(f"Search failed: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"Connection error: {str(e)}")
        else:
            st.warning("Please enter a query")

elif page == "Add Institutional Memory":
    st.header("Add Institutional Memory")

    content_type = st.radio("Content Type", ["Text", "Image"], horizontal=True)

    if content_type == "Text":
        st.subheader("Required Information")
        col1, col2 = st.columns(2)

        with col1:
            document_text = st.text_area("Document Text", height=200)
            department = st.selectbox("Department", ["Emergency Management", "Finance", "Infrastructure", "Other"])

        with col2:
            date = st.date_input("Date")
            outcome = st.selectbox("Outcome", ["success", "failure", "mixed"])
            location = st.text_input("Location")

        tags_input = st.multiselect("Tags", ["policy", "budget", "flood", "infrastructure", "emergency", "monitoring", "evacuation", "cybersecurity"])

        st.subheader("Optional Information")
        col3, col4 = st.columns(2)

        with col3:
            document_type = st.selectbox("Document Type", ["", "Policy", "Report", "Decision", "Incident"], index=0)
            confidence = st.selectbox("Confidence Level", ["", "low", "medium", "high"], index=0)

        with col4:
            source = st.text_input("Source / Reference")
            notes = st.text_area("Notes (Internal)", height=100)

        if st.button("Ingest Text Document", type="primary"):
            if document_text and department:
                tags = tags_input if tags_input else None

                payload = {
                    "type": "text",
                    "text": document_text,
                    "department": department,
                    "date": str(date),
                    "outcome": outcome,
                    "location": location if location else None,
                    "tags": tags,
                    "document_type": document_type if document_type else None,
                    "confidence": confidence if confidence else None,
                    "source": source if source else None,
                    "notes": notes if notes else None
                }

                with st.spinner("Ingesting text document..."):
                    try:
                        response = requests.post(f"{API_BASE}/ingest", json=payload)
                        if response.status_code == 200:
                            st.success("Text document ingested successfully!")
                        else:
                            st.error(f"Ingestion failed: {response.status_code} - {response.text}")
                    except Exception as e:
                        st.error(f"Connection error: {str(e)}")
            else:
                st.warning("Please fill in the required fields (Document Text and Department)")

    else:
        st.subheader("Required Information")
        uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg", "gif", "bmp"])

        if uploaded_file is not None:
            st.image(uploaded_file, caption="Preview", use_column_width=True)

            image_description = st.text_area("Image Description", height=100)

            col1, col2 = st.columns(2)
            with col1:
                department = st.selectbox("Department", ["Emergency Management", "Finance", "Infrastructure", "Other"])
                date = st.date_input("Date")

            with col2:
                location = st.text_input("Location")
                tags_input = st.multiselect("Tags", ["policy", "budget", "flood", "infrastructure", "emergency", "monitoring", "evacuation", "cybersecurity"])

            st.subheader("Optional Information")
            col3, col4 = st.columns(2)

            with col3:
                image_category = st.selectbox("Image Category", ["", "Map", "Dashboard", "Chart", "Photo", "Diagram"], index=0)
                related_event = st.text_input("Related Event / Policy")

            with col4:
                source = st.text_input("Source")
                notes = st.text_area("Notes (Internal)", height=80)

            if st.button("Ingest Image", type="primary"):
                if image_description and department:
                    temp_path = f"temp_{uploaded_file.name}"
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    tags = tags_input if tags_input else None

                    payload = {
                        "image_path": temp_path,
                        "description": image_description,
                        "department": department,
                        "date": str(date),
                        "location": location if location else None,
                        "tags": tags,
                        "image_category": image_category if image_category else None,
                        "related_event": related_event if related_event else None,
                        "source": source if source else None,
                        "notes": notes if notes else None
                    }

                    with st.spinner("Ingesting image..."):
                        try:
                            response = requests.post(f"{API_BASE}/ingest", json=payload)
                            if response.status_code == 200:
                                st.success("Image ingested successfully!")
                            else:
                                st.error(f"Ingestion failed: {response.status_code} - {response.text}")
                        except Exception as e:
                            st.error(f"Connection error: {str(e)}")
                        finally:
                            if os.path.exists(temp_path):
                                os.remove(temp_path)
                else:
                    st.warning("Please provide an image description and select a department")
        else:
            st.info("Please upload an image file to get started")

st.markdown("---")
st.markdown("*Chronicle AI - Preserving institutional memory for evidence-based governance*")