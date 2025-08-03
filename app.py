import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import date

st.set_page_config(page_title="Support Request Form", layout="centered")

st.title("🛠️ Support Request Form")

# --- Form Input ---
with st.form("support_form"):
    name = st.text_input("👤 Name", max_chars=50)
    area = st.text_input("🏭 Area Name", max_chars=50)
    problem = st.text_area("📝 Problem Description", height=100)
    priority = st.selectbox("⚠️ Priority", ["Low", "Medium", "High", "Urgent"])
    support_type = st.selectbox("🔧 Type of Support", ["Technical", "Asset Care", "Electrical", "Mechanical"])
    status = st.selectbox("📌 Status", ["Open", "In Progress", "Resolved", "Closed"])
    photo = st.file_uploader("📷 Upload Photo", type=["png", "jpg", "jpeg"])

    submitted = st.form_submit_button("Submit")

# --- Submission Output ---
if submitted:
    form_data = pd.DataFrame([{
        "Date": date.today(),
        "Name": name,
        "Area": area,
        "Problem": problem,
        "Priority": priority,
        "Support Type": support_type,
        "Status": status
    }])

    st.success("✅ Form submitted successfully!")
    st.subheader("📄 Submitted Data")
    st.dataframe(form_data)

    if photo:
        st.subheader("📷 Uploaded Photo")
        st.image(photo, use_column_width=True)

    # Export to Excel
    def to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='SupportData')
        return output.getvalue()

    excel_data = to_excel(form_data)

    st.download_button(
        label="⬇️ Download Excel File",
        data=excel_data,
        file_name=f"support_form_{date.today()}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # Print instruction
    with st.expander("🖨️ Print This Page"):
        st.write("Use your browser’s **Print** feature (Ctrl+P or Share > Print on mobile) to print the filled form.")

