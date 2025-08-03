import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import date

st.set_page_config(page_title="Support Request Form", layout="centered")
st.title("🛠️ Support Request Form")

# Form section
with st.form("support_form"):
    request_date = st.date_input("Date", value=date.today())
    name = st.text_input("Name")
    area = st.text_input("Area Name")
    problem = st.text_area("Problem Description")
    priority = st.selectbox("Priority", ["", "Low", "Medium", "High", "Urgent"])
    support_type = st.selectbox("Type of Support", ["", "Technical", "Asset Care", "Electrical", "Mechanical"])
    status = st.selectbox("Status", ["", "Open", "In Progress", "Resolved", "Closed"])
    photo = st.file_uploader("Upload Photo", type=["jpg", "jpeg", "png"])  # Optional

    submitted = st.form_submit_button("Submit")

# Submission logic
if submitted:
    # Validation check
    if not all([name.strip(), area.strip(), problem.strip(), priority, support_type, status]):
        st.warning("❗ Please fill out all required fields before submitting.")
    else:
        form_data = pd.DataFrame([{
            "Date": request_date,
            "Name": name,
            "Area": area,
            "Problem": problem,
            "Priority": priority,
            "Support Type": support_type,
            "Status": status,
        }])

        st.success("✅ Form submitted successfully!")
        st.subheader("Submitted Data")
        st.dataframe(form_data, use_container_width=True)

        if photo:
            st.subheader("Uploaded Photo")
            st.image(photo, use_column_width=True)

        # Export to Excel
        def to_excel(df):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name="SupportRequest")
            return output.getvalue()

        excel_data = to_excel(form_data)
        st.download_button(
            label="⬇️ Download Excel File",
            data=excel_data,
            file_name=f"support_request_{request_date}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        with st.expander("🖨️ Print View"):
            st.write("Use your browser’s print feature (Ctrl+P or mobile share > Print).")
            st.table(form_data)
