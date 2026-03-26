import streamlit as st
import pandas as pd
import base64
from io import BytesIO
import time
import plotly.express as px
import plotly.graph_objects as go

# Page configuration with custom theme and layout
st.set_page_config(
    page_title="DataSync Pro",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    /* Global Styles */
    body {font-family: 'Inter', sans-serif;}
    .main {padding: 0 !important; max-width: 100% !important;}

    /* Header Styling */
    .header-container {
        background-color: #1a1f2b;
        padding: 1rem 2rem;
        border-radius: 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: -5px -5px 20px -5px;
        color: white;
    }
    .logo-text {font-size: 24px; font-weight: 600; color: white;}
    .header-nav {display: flex; gap: 2rem;}
    .nav-item {color: #ccc; text-decoration: none; font-weight: 500;}
    .nav-item:hover {color: white; text-decoration: none;}
    .active-nav {color: #3498db; font-weight: 600;}
    .dashboard-button {
        background-color: #3498db;
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 500;
    }

    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #1a1f2b 0%, #2c3e50 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    .hero-title {font-size: 2.5rem; font-weight: 700; margin-bottom: 1rem;}
    .hero-subtitle {font-size: 1.2rem; opacity: 0.8; margin-bottom: 2rem;}

    /* Card Styling */
    .card {
        background-color: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        height: 100%;
    }
    .card-header {
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 1rem;
        color: #1a1f2b;
    }

    /* Metrics Card */
    .metric-container {display: flex; justify-content: space-between; margin-bottom: 1rem;}
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        flex: 1;
        margin: 0 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .metric-value {font-size: 1.8rem; font-weight: 700; color: #3498db; margin-bottom: 0.5rem;}
    .metric-label {font-size: 0.9rem; color: #6c757d;}

    /* Chat UI */
    .chat-messages-box {
        height: 300px;
        overflow-y: auto;
        padding: 1rem;
        background-color: #f8f9fa;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin-bottom: 0.5rem;
    }
    .user-message {
        background-color: #3498db;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 18px;
        margin-bottom: 0.5rem;
        max-width: 80%;
        margin-left: auto;
        text-align: right;
    }
    .bot-message {
        background-color: #e9ecef;
        color: #212529;
        padding: 0.5rem 1rem;
        border-radius: 18px;
        margin-bottom: 0.5rem;
        max-width: 80%;
    }

    /* Button Styling */
    .primary-button {
        background-color: #3498db;
        color: white !important;
        border-radius: 6px !important;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        border: none;
        text-decoration: none;
    }
    .primary-button:hover {background-color: #2980b9;}
    .secondary-button {
        background-color: #f8f9fa;
        color: #495057 !important;
        border-radius: 6px !important;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        border: 1px solid #dee2e6;
        text-decoration: none;
    }
    .secondary-button:hover {background-color: #e9ecef;}

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        margin-bottom: 1rem;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 0px;
        font-weight: 500;
    }

    /* Remove Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Custom Header
st.markdown("""
<div class="header-container">
    <div class="logo-text">DataSync Pro</div>
    <div class="header-nav">
        <a href="#" class="nav-item active-nav">Dashboard</a>
        <a href="#" class="nav-item">Analytics</a>
        <a href="#" class="nav-item">Campaigns</a>
        <a href="#" class="nav-item">Settings</a>
    </div>
    <div class="dashboard-button">Premium Plan</div>
</div>
""", unsafe_allow_html=True)

# ===== Configuration =====
COUNTRY_INFO = {
    '1': {'name': 'USA/Canada', 'length': 10},
    '44': {'name': 'United Kingdom', 'length': 10},
    '60': {'name': 'Malaysia', 'length': 9},
    '65': {'name': 'Singapore', 'length': 8},
    '971': {'name': 'UAE', 'length': 9},
    '966': {'name': 'Saudi Arabia', 'length': 9},
    '61': {'name': 'Australia', 'length': 9},
    '91': {'name': 'India', 'length': 10},
    '880': {'name': 'Bangladesh', 'length': 8}
}

currency_mapping = {
    'USD': {'code': '1', 'length': 10, 'name': 'US Dollar'},
    'GBP': {'code': '44', 'length': 10, 'name': 'British Pound'},
    'MYR': {'code': '60', 'length': 9, 'name': 'Malaysian Ringgit'},
    'SGD': {'code': '65', 'length': 8, 'name': 'Singapore Dollar'},
    'AED': {'code': '971', 'length': 9, 'name': 'UAE Dirham'},
    'SAR': {'code': '966', 'length': 9, 'name': 'Saudi Riyal'},
    'AUD': {'code': '61', 'length': 9, 'name': 'Australian Dollar'},
    'CAD': {'code': '1', 'length': 10, 'name': 'Canadian Dollar'},
    'INR': {'code': '91', 'length': 10, 'name': 'Indian Rupee'},
    'BDT': {'code': '880', 'length': 8, 'name': 'Bangladeshi Taka'}
}

# ===== Phone processing functions =====
def process_snippet1_data(df):
    results = []
    if 'Email' not in df.columns:
        return pd.DataFrame(columns=['Email', 'Formatted_Number'])
    for _, row in df.iterrows():
        try:
            email = str(row['Email']).strip()
            if pd.isna(email) or '@' not in email:
                continue
            if any(domain in email.lower() for domain in ['@hoichoi.tv', '@hoichoitv.com']):
                phone_part = email.split('@')[0].strip()
                formatted_number = phone_part
                if phone_part.startswith('+'):
                    for code, info in COUNTRY_INFO.items():
                        if phone_part[1:].startswith(code):
                            number_part = ''.join(filter(str.isdigit, phone_part[1+len(code):]))
                            formatted_number = f"{code} {number_part[-info['length']:]}" if number_part else phone_part
                            break
                results.append({'Email': email, 'Formatted_Number': formatted_number})
        except Exception:
            continue
    return pd.DataFrame(results) if results else pd.DataFrame(columns=['Email', 'Formatted_Number'])


def process_snippet2_data(df):
    try:
        email_col = 'Email'
        phone_col = 'Phone'
        currency_col = 'currency'

        required_cols = [email_col, phone_col, currency_col]
        for col in required_cols:
            if col not in df.columns:
                return pd.DataFrame(columns=['Email', 'clean_phone'])

        filtered_df = df[
            ~df[email_col].fillna('').str.lower().str.endswith(('@hoichoi.tv', '@hoichoitv.com'))
        ].copy()

        filtered_df = filtered_df[
            filtered_df[phone_col].notnull() &
            (filtered_df[phone_col].astype(str).str.strip() != '') &
            (filtered_df[phone_col].astype(str).str.replace(r'\D', '', regex=True).str.len() >= 5)
        ].copy()

        if filtered_df.empty:
            return pd.DataFrame(columns=['Email', 'clean_phone'])

        def format_phone(row):
            phone = ''.join(filter(str.isdigit, str(row[phone_col])))
            currency = str(row[currency_col]).strip()
            if currency in currency_mapping:
                code = currency_mapping[currency]['code']
                length = currency_mapping[currency]['length']
                if phone.startswith(code):
                    phone = phone[len(code):]
                return f"{code} {phone[:length]}"
            return ''

        filtered_df['clean_phone'] = filtered_df.apply(format_phone, axis=1)
        return filtered_df[[email_col, 'clean_phone']].rename(columns={email_col: 'Email'})
    except Exception as e:
        st.error(f"Error in snippet 2 processing: {e}")
        return pd.DataFrame(columns=['Email', 'clean_phone'])


def combine_results(df1, df2):
    frames = []
    if not df1.empty and 'Formatted_Number' in df1.columns:
        frames.append(df1[['Email', 'Formatted_Number']].rename(columns={'Formatted_Number': 'Phone'}))
    if not df2.empty and 'clean_phone' in df2.columns:
        frames.append(df2[['Email', 'clean_phone']].rename(columns={'clean_phone': 'Phone'}))

    if not frames:
        return pd.DataFrame(columns=['Email', 'Phone'])

    combined = pd.concat(frames)
    combined = combined[combined['Phone'].astype(str).str.strip() != '']
    combined = combined.drop_duplicates(subset=['Email', 'Phone'])
    final_result = combined.groupby('Email')['Phone'].apply(lambda x: ', '.join(filter(None, x))).reset_index()
    return final_result


def get_table_download_link(df, filename, text):
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)
    excel_data = buffer.getvalue()
    b64 = base64.b64encode(excel_data).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}" class="primary-button">{text}</a>'
    return href


def generate_sample_data(num_records=1000):
    import random
    import string

    countries = list(currency_mapping.keys())
    domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hoichoi.tv', 'hotmail.com', 'company.com']

    data = []
    for _ in range(num_records):
        name = ''.join(random.choice(string.ascii_lowercase) for _ in range(6))
        domain = random.choice(domains)
        email = f"{name}@{domain}"

        currency = random.choice(countries)
        country_code = currency_mapping[currency]['code']
        phone_length = currency_mapping[currency]['length']
        phone = country_code + ''.join(random.choice(string.digits) for _ in range(phone_length))

        data.append({
            'Email': email,
            'Phone': phone,
            'currency': currency
        })

    return pd.DataFrame(data)


# Main Dashboard Content
col1, col2 = st.columns([7, 3])

with col1:
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">Transform Your Customer Data</h1>
        <p class="hero-subtitle">Extract and format contact information for marketing campaigns with our advanced processing engine</p>
    </div>
    """, unsafe_allow_html=True)

    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["Dashboard", "Process Data", "Data Explorer"])

    with tab1:
        # Quick stats
        st.markdown("""
        <div class="metric-container">
            <div class="metric-card">
                <div class="metric-value">14,382</div>
                <div class="metric-label">Total Records</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">9,827</div>
                <div class="metric-label">Valid Emails</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">8,549</div>
                <div class="metric-label">Valid Phones</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">12</div>
                <div class="metric-label">Campaigns</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Main charts
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.subheader("Market Distribution")
            market_data = {
                'Market': ['India', 'Bangladesh', 'USA', 'UK', 'Singapore', 'UAE', 'Others'],
                'Records': [4200, 2800, 2100, 1900, 1600, 1200, 582]
            }
            market_df = pd.DataFrame(market_data)
            fig = px.pie(market_df, values='Records', names='Market', hole=0.4,
                         color_discrete_sequence=px.colors.sequential.Blues_r)
            fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=300)
            st.plotly_chart(fig, use_container_width=True)

        with chart_col2:
            st.subheader("Processing Statistics")
            stats_data = {
                'Metric': ['Valid Emails', 'Invalid Emails', 'Valid Phones', 'Invalid Phones'],
                'Count': [9827, 4555, 8549, 5833]
            }
            stats_df = pd.DataFrame(stats_data)
            fig = px.bar(stats_df, x='Metric', y='Count',
                         color='Count',
                         color_continuous_scale='Blues')
            fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=300)
            st.plotly_chart(fig, use_container_width=True)

        # Recent activity
        st.subheader("Recent Activity")
        activity_data = {
            'Action': [
                'Campaign Data Export',
                'New Data Import',
                'Data Processing',
                'API Integration',
                'Email Validation'
            ],
            'Description': [
                'Exported 3,450 contacts for Email Campaign',
                'Imported 2,800 new contacts from CRM',
                'Processed 5,200 records for phone formatting',
                'Connected Mailchimp API',
                'Validated 7,800 email addresses'
            ],
            'Date': [
                '2025-04-21',
                '2025-04-20',
                '2025-04-19',
                '2025-04-18',
                '2025-04-17'
            ],
            'Status': [
                'Completed',
                'Completed',
                'Completed',
                'Active',
                'Completed'
            ]
        }
        activity_df = pd.DataFrame(activity_data)
        st.dataframe(activity_df, use_container_width=True, hide_index=True)

    with tab2:
        # Process Data Tab
        process_col1, process_col2 = st.columns([2, 1])

        with process_col1:
            st.subheader("Upload Data")
            uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx", "xls"])

            use_sample_data = st.checkbox("Use sample data instead")

            if use_sample_data:
                sample_size = st.slider("Number of sample records", 100, 5000, 1000)
                if st.button("Generate Sample Data", key="generate_sample"):
                    st.session_state['input_df'] = generate_sample_data(sample_size)
                    st.success(f"Generated {sample_size} sample records")

            if uploaded_file is not None:
                try:
                    if uploaded_file.name.endswith('.csv'):
                        input_df = pd.read_csv(uploaded_file)
                    else:
                        input_df = pd.read_excel(uploaded_file)
                    st.session_state['input_df'] = input_df
                    st.success(f"Successfully uploaded {len(input_df)} records")
                except Exception as e:
                    st.error(f"Error processing file: {e}")

            if 'input_df' in st.session_state:
                st.dataframe(st.session_state['input_df'].head(), use_container_width=True)

        with process_col2:
            st.subheader("Processing Options")

            st.markdown("**Select Markets**")
            markets = list(currency_mapping.keys())
            selected_markets = st.multiselect(
                "Markets",
                markets,
                default=["INR", "BDT", "USD"],
                format_func=lambda x: f"{x} - {currency_mapping[x]['name']}",
                label_visibility="collapsed"
            )

            st.markdown("**Options**")
            opt_col1, opt_col2 = st.columns(2)
            with opt_col1:
                remove_invalid = st.checkbox("Remove invalid emails", value=True)
                format_phones = st.checkbox("Format phone numbers", value=True)
            with opt_col2:
                deduplicate = st.checkbox("Remove duplicates", value=True)
                lowercase_emails = st.checkbox("Convert to lowercase", value=True)

            if st.button("Process Data", type="primary"):
                if 'input_df' not in st.session_state:
                    st.warning("Please upload data or generate sample data first")
                else:
                    with st.spinner("Processing data..."):
                        progress_bar = st.progress(0)
                        for i in range(0, 101, 5):
                            time.sleep(0.02)
                            progress_bar.progress(i)

                        filtered_df = st.session_state['input_df'].copy()

                        if selected_markets and 'currency' in filtered_df.columns:
                            filtered_df = filtered_df[filtered_df['currency'].isin(selected_markets)]

                        if lowercase_emails and 'Email' in filtered_df.columns:
                            filtered_df['Email'] = filtered_df['Email'].str.lower()

                        df1 = process_snippet1_data(filtered_df)
                        df2 = process_snippet2_data(filtered_df)
                        final_result_df = combine_results(df1, df2)

                        st.session_state['processed_df'] = final_result_df
                        st.session_state['processing_complete'] = True

                        st.success(f"Processing complete! {len(final_result_df)} records produced.")

    with tab3:
        # Data Explorer Tab
        if 'processing_complete' not in st.session_state or not st.session_state['processing_complete']:
            st.info("Process your data first to explore results")
        else:
            explore_col1, explore_col2 = st.columns([3, 2])

            with explore_col1:
                st.subheader("Processed Data")
                processed_df = st.session_state['processed_df']
                st.dataframe(processed_df, use_container_width=True)

                st.markdown("**Download Options**")
                download_col1, download_col2 = st.columns(2)

                with download_col1:
                    excel_link = get_table_download_link(processed_df, "processed_data.xlsx", "Download Excel")
                    st.markdown(excel_link, unsafe_allow_html=True)

                with download_col2:
                    csv = processed_df.to_csv(index=False)
                    b64_csv = base64.b64encode(csv.encode()).decode()
                    href_csv = f'<a href="data:file/csv;base64,{b64_csv}" download="processed_data.csv" class="secondary-button">Download CSV</a>'
                    st.markdown(href_csv, unsafe_allow_html=True)

            with explore_col2:
                st.subheader("Data Analysis")

                if not processed_df.empty and 'Email' in processed_df.columns:
                    processed_df_copy = processed_df.copy()
                    processed_df_copy['Domain'] = processed_df_copy['Email'].str.split('@').str[1]
                    domain_counts = processed_df_copy['Domain'].value_counts().reset_index()
                    domain_counts.columns = ['Domain', 'Count']

                    fig = px.bar(domain_counts.head(10), x='Domain', y='Count',
                                 color='Count', color_continuous_scale='Blues')
                    fig.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=250)
                    st.plotly_chart(fig, use_container_width=True)

                if not processed_df.empty and 'Phone' in processed_df.columns:
                    processed_df_copy = processed_df.copy()
                    processed_df_copy['Phone_Code'] = processed_df_copy['Phone'].str.split(' ').str[0]
                    phone_code_counts = processed_df_copy['Phone_Code'].value_counts().reset_index()
                    phone_code_counts.columns = ['Country Code', 'Count']

                    phone_code_counts['Country'] = phone_code_counts['Country Code'].map(
                        {code: info['name'] for code, info in COUNTRY_INFO.items()}
                    )
                    phone_code_counts['Country'] = phone_code_counts['Country'].fillna('Unknown')

                    fig = px.pie(phone_code_counts, values='Count', names='Country', hole=0.4)
                    fig.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=250)
                    st.plotly_chart(fig, use_container_width=True)

with col2:
    # AI Assistant Card
    st.subheader("AI Assistant")

    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Hello! I'm your DataSync Assistant. I can help you process customer data, analyze results, or answer questions about our features."}
        ]

    # Display chat history
    chat_html = ""
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            chat_html += f'<div class="user-message">{message["content"]}</div>'
        else:
            chat_html += f'<div class="bot-message">{message["content"]}</div>'

    st.markdown(f'<div class="chat-messages-box">{chat_html}</div>', unsafe_allow_html=True)

    # Chat input
    user_input = st.text_input("Ask me anything...", key="user_input")

    if st.button("Send", key="send_button"):
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})

            query = user_input.lower()
            if "india" in query:
                response = "I can help you process data for India! Indian phone numbers use country code +91 and typically have 10 digits."
            elif "bangladesh" in query:
                response = "For Bangladesh, we use country code +880 and format phone numbers to 8 digits."
            elif "email" in query:
                response = "Our system can extract and validate emails from your data. We support various email formats and domains."
            elif "phone" in query:
                response = "We format phone numbers according to country standards. Just specify which markets you want to process."
            elif "download" in query:
                response = "You can download your processed data in Excel or CSV format from the Data Explorer tab."
            elif "currency" in query:
                response = "We support multiple currencies including USD, INR, BDT, GBP, and others. Each currency is associated with its relevant country code."
            else:
                response = "I can help you with data processing, market selection, or explain our features. What specifically would you like to know about?"

            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()

    # Quick Actions Card
    st.subheader("Quick Actions")
    action_col1, action_col2 = st.columns(2)

    with action_col1:
        st.button("New Dataset", key="new_dataset")
        st.button("Export All", key="export_all")

    with action_col2:
        st.button("API Access", key="api_access")
        st.button("Run Report", key="run_report")

# Data Insights Section - Full Width
st.markdown("---")
st.subheader("Data Insights & Recommendations")
insights_col1, insights_col2, insights_col3 = st.columns(3)

with insights_col1:
    st.markdown("""
    #### Email Quality

    Based on your data, we've identified several optimization opportunities:

    * **Valid email rate:** 68.5%
    * **Deliverability score:** 92.3%
    * **Duplicate ratio:** 7.8%

    **Recommendation:** Consider implementing email verification before importing data.
    """)

with insights_col2:
    st.markdown("""
    #### Phone Number Coverage

    The phone number analysis shows:

    * **Formatted numbers:** 59.4%
    * **Missing country codes:** 21.7%
    * **Invalid formats:** 18.9%

    **Recommendation:** Use the phone reformatting feature to standardize all numbers.
    """)

with insights_col3:
    st.markdown("""
    #### Market Distribution

    Your data is concentrated in:

    * **India:** 29.2%
    * **Bangladesh:** 19.5%
    * **USA/Canada:** 14.6%

    **Recommendation:** Consider expanding coverage in Singapore and UAE markets.
    """)

# Footer
st.markdown("""
<div style="background-color: #1a1f2b; padding: 1rem; border-radius: 10px; margin-top: 1.5rem; color: white; text-align: center;">
    <div style="display: flex; justify-content: space-between; align-items: center; max-width: 600px; margin: 0 auto;">
        <div>DataSync Pro &copy; 2025</div>
        <div>Terms of Service | Privacy Policy | Help Center</div>
    </div>
</div>
""", unsafe_allow_html=True)
