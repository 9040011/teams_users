import streamlit as st
import csv
import phonenumbers


def process_data(emails, phones, region_code="CA"):
    emails_lower = [email.lower().strip() for email in emails if email.strip()]
    phones_e164 = []
    for phone in phones:
        if phone.strip():
            try:
                parsed_phone = phonenumbers.parse(phone, region_code)
                if phonenumbers.is_valid_number(parsed_phone):
                    phones_e164.append(phonenumbers.format_number(parsed_phone, phonenumbers.PhoneNumberFormat.E164))
                else:
                    st.write(f"Invalid phone number: {phone}")
            except phonenumbers.NumberParseException:
                st.write(f"Invalid phone number: {phone}")
    return emails_lower, phones_e164


st.title("Email & Phone Processor")

emails_input = st.text_area("Paste Email Addresses:")
phones_input = st.text_area("Paste Phone Numbers:")
region_code = st.text_input("Region Code (e.g., US, CA, GB - default: CA):", value="CA")

if st.button("Process and Download"):
    emails = emails_input.splitlines()
    phones = phones_input.splitlines()

    emails_lower, phones_e164 = process_data(emails, phones, region_code)

    csv_data = [["TeamsUserID", "DirectRoutingNumber"]] + list(zip(emails_lower, phones_e164))
    st.download_button(
        label="Download CSV",
        data="\n".join([",".join(row) for row in csv_data]),
        file_name="processed_data.csv",
        mime="text/csv",
    )
