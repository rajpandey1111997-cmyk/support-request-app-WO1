import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import date

st.title("Support Request Form")

with st.form("support_form"):
    request_date = st.date_input("Date", value=date.today())
    name = st.text_input("Name")
    area = st.text_input("Area Name")
    problem = st.text_area("Problem Description")
    priority = st.selectbox("Priority", ["Low", "Medium", "High", "Urgent"])
    support_type = st.selectbox("Type of Support", ["Technical", "Asset Care", "Electrical", "Mechanical"])
    status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"])
    photo = st.file_uploader("Upload Photo", type=["png", "jpg", "jpeg"])
    submitted = st.form_submit_button("Submit")

if submitted:
    form_data = pd.DataFrame([
        {
            "Date": request_date,
            "Name": name,
            "Area": area,
            "Problem": problem,
            "Priority": priority,
            "Support Type": support_type,
            "Status": status,
        }
    ])
    st.success("Form submitted successfully!")
    st.subheader("Submitted Data")
    st.dataframe(form_data, use_container_width=True)

    if photo:
        st.subheader("Uploaded Photo")
        st.image(photo, use_column_width=True)

    def to_excel(df):
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='openpyxl')
        df.to_excel(writer, index=False, sheet_name='Request')
        writer.close()
        return output.getvalue()

    excel_data = to_excel(form_data)
    st.download_button(
        label="Download Excel File",
        data=excel_data,
        file_name=f"support_request_{request_date}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    with st.expander("🖨️ Print View"):
        st.write("Use your browser's print function (Ctrl+P or Share > Print on mobile).")
        st.table(form_data)
