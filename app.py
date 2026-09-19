import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Page Configuration
st.set_page_config(
    page_title="Mental Health Dashboard",
    page_icon="🧠",
    layout="wide"
)


# Load custom CSS
with open("style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )
# Load Dataset
df = pd.read_csv("survey(1).csv")

# Dashboard Title
st.title("🧠 Mental Health in Tech Dashboard")

st.write(
    "Exploring workplace mental health and treatment-seeking patterns"
)

# Sidebar Filters
st.sidebar.header("🎛️ Dashboard Filters")

# Country Filter
country_options = ["All"] + sorted(
    df["Country"].dropna().unique().tolist()
)

selected_country = st.sidebar.selectbox(
    "Country",
    country_options
)

# Gender Filter
gender_options = ["All"] + sorted(
    df["Gender"].dropna().unique().tolist()
)

selected_gender = st.sidebar.selectbox(
    "Gender",
    gender_options
)

# Treatment Filter
treatment_options = ["All"] + sorted(
    df["treatment"].dropna().unique().tolist()
)

selected_treatment = st.sidebar.selectbox(
    "Treatment Sought",
    treatment_options
)

# Apply Filters
filtered_df = df.copy()

if selected_country != "All":
    filtered_df = filtered_df[
        filtered_df["Country"] == selected_country
    ]

if selected_gender != "All":
    filtered_df = filtered_df[
        filtered_df["Gender"] == selected_gender
    ]

if selected_treatment != "All":
    filtered_df = filtered_df[
        filtered_df["treatment"] == selected_treatment
    ]

    
# -----------------------------------
# Empty Data Check
# -----------------------------------

if filtered_df.empty:
    st.warning(
        "⚠️ No data available for the selected filters. "
        "Please choose different filter options."
    )
    st.info("Try selecting 'All' for Country, Gender, or Treatment.")
    st.stop()

# Dataset Overview
st.subheader("📊 Dataset Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Respondents", len(df))

with col2:
    st.metric("Total Columns", len(df.columns))

with col3:
    st.metric(
        "Missing Values",
        int(df.isnull().sum().sum())
    )

# Filtered Dataset Summary
st.subheader("🔍 Filtered Dataset Summary")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Filtered Respondents",
        len(filtered_df)
    )

with col2:
    st.metric(
        "Filtered Missing Values",
        int(filtered_df.isnull().sum().sum())
    )



# -----------------------------------
# Professional KPI Cards
# -----------------------------------

total_filtered = len(filtered_df)

treatment_yes = (
    filtered_df["treatment"]
    .astype(str)
    .str.lower()
    .eq("yes")
    .sum()
)

treatment_no = (
    filtered_df["treatment"]
    .astype(str)
    .str.lower()
    .eq("no")
    .sum()
)

treatment_rate = (
    (treatment_yes / total_filtered) * 100
    if total_filtered > 0 else 0
)

st.subheader("📈 Treatment Statistics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("✅ Sought Treatment", treatment_yes)

with col2:
    st.metric("❌ Did Not Seek Treatment", treatment_no)

with col3:
    st.metric("📊 Treatment Rate", f"{treatment_rate:.1f}%")
# Display Filtered Data
st.subheader("📋 Dataset Preview")

st.dataframe(
    filtered_df.head(),
    use_container_width=True
)



# -----------------------------------
# Clean Gender Column
# -----------------------------------

filtered_df = filtered_df.copy()

def clean_gender(gender):
    gender = str(gender).strip().lower()

    if gender in ["male", "m", "man", "cis male", "cis man"]:
        return "Male"
    elif gender in ["female", "f", "woman", "cis female", "cis woman"]:
        return "Female"
    else:
        return "Other"

filtered_df["Gender_Cleaned"] = filtered_df["Gender"].apply(clean_gender)

# -----------------------------------
# Chart 1 & Chart 2
# -----------------------------------

col1, col2 = st.columns(2)

# -----------------------------------
# Chart 1: Treatment Distribution
# -----------------------------------

with col1:
    st.subheader("📊 Treatment Sought Distribution")

    treatment_counts = filtered_df["treatment"].value_counts()

    fig, ax = plt.subplots(figsize=(7, 4))
    treatment_counts.plot(kind="bar", ax=ax)

    ax.set_title("Mental Health Treatment Sought")
    ax.set_xlabel("Treatment Sought")
    ax.set_ylabel("Number of Respondents")
    plt.xticks(rotation=0)
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)


# -----------------------------------
# Chart 2: Gender vs Treatment
# -----------------------------------

with col2:
    st.subheader("👥 Gender vs Treatment")

    def clean_gender(gender):
        gender = str(gender).strip().lower()

        if gender in ["male", "m", "man", "cis male", "cis man"]:
            return "Male"
        elif gender in ["female", "f", "woman", "cis female", "cis woman"]:
            return "Female"
        else:
            return "Other"

    filtered_df["Gender_Cleaned"] = filtered_df["Gender"].apply(clean_gender)

    gender_treatment = pd.crosstab(
        filtered_df["Gender_Cleaned"],
        filtered_df["treatment"]
    )

    fig, ax = plt.subplots(figsize=(7, 4))
    gender_treatment.plot(kind="barh", ax=ax)

    ax.set_title("Gender-wise Treatment Seeking")
    ax.set_xlabel("Number of Respondents")
    ax.set_ylabel("Gender")
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)
# -----------------------------------
# Chart 3 & Chart 4
# -----------------------------------

col1, col2 = st.columns(2)

# -----------------------------------
# Chart 3: Family History vs Treatment
# -----------------------------------

with col1:
    st.subheader("🧬 Family History vs Treatment")

    family_treatment = pd.crosstab(
        filtered_df["family_history"],
        filtered_df["treatment"]
    )

    fig, ax = plt.subplots(figsize=(7, 4))
    family_treatment.plot(kind="bar", ax=ax)

    ax.set_title("Family History and Treatment Seeking")
    ax.set_xlabel("Family History")
    ax.set_ylabel("Number of Respondents")
    plt.xticks(rotation=0)
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)


# -----------------------------------
# Chart 4: Benefits vs Treatment
# -----------------------------------

with col2:
    st.subheader("🎁 Benefits vs Treatment")

    benefits_treatment = pd.crosstab(
        filtered_df["benefits"],
        filtered_df["treatment"]
    )

    fig, ax = plt.subplots(figsize=(7, 4))
    benefits_treatment.plot(kind="bar", ax=ax)

    ax.set_title("Workplace Benefits and Treatment Seeking")
    ax.set_xlabel("Benefits Available")
    ax.set_ylabel("Number of Respondents")
    plt.xticks(rotation=0)
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

# -----------------------------------
# Chart 5 & Chart 6
# -----------------------------------

col1, col2 = st.columns(2)

# -----------------------------------
# Chart 5: Work Interference vs Treatment
# -----------------------------------

with col1:
    st.subheader("💼 Work Interference vs Treatment")

    work_treatment = pd.crosstab(
        filtered_df["work_interfere"],
        filtered_df["treatment"]
    )

    fig, ax = plt.subplots(figsize=(7, 4))
    work_treatment.plot(kind="bar", ax=ax)

    ax.set_title("Work Interference and Treatment Seeking")
    ax.set_xlabel("Work Interference")
    ax.set_ylabel("Number of Respondents")
    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)


# -----------------------------------
# Chart 6: Company Size vs Treatment
# -----------------------------------

with col2:
    st.subheader("🏢 Company Size vs Treatment")

    company_treatment = pd.crosstab(
        filtered_df["no_employees"],
        filtered_df["treatment"]
    )

    fig, ax = plt.subplots(figsize=(7, 4))
    company_treatment.plot(kind="bar", ax=ax)

    ax.set_title("Company Size and Treatment Seeking")
    ax.set_xlabel("Number of Employees")
    ax.set_ylabel("Number of Respondents")
    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)



# -----------------------------------
# Chart 7 & Chart 8
# -----------------------------------

col1, col2 = st.columns(2)

# -----------------------------------
# Chart 7: Remote Work vs Treatment
# -----------------------------------

with col1:
    st.subheader("🏠 Remote Work vs Treatment")

    remote_treatment = pd.crosstab(
        filtered_df["remote_work"],
        filtered_df["treatment"]
    )

    fig, ax = plt.subplots(figsize=(7, 4))
    remote_treatment.plot(kind="bar", ax=ax)

    ax.set_title("Remote Work and Treatment Seeking")
    ax.set_xlabel("Remote Work")
    ax.set_ylabel("Number of Respondents")
    plt.xticks(rotation=0)
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)


# -----------------------------------
# Chart 8: Tech Company vs Treatment
# -----------------------------------

with col2:
    st.subheader("💻 Tech Company vs Treatment")

    tech_treatment = pd.crosstab(
        filtered_df["tech_company"],
        filtered_df["treatment"]
    )

    fig, ax = plt.subplots(figsize=(7, 4))
    tech_treatment.plot(kind="bar", ax=ax)

    ax.set_title("Tech Company and Treatment Seeking")
    ax.set_xlabel("Tech Company")
    ax.set_ylabel("Number of Respondents")
    plt.xticks(rotation=0)
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

# -----------------------------------
# Chart 9 & Chart 10
# -----------------------------------

col1, col2 = st.columns(2)

# -----------------------------------
# Chart 9: Wellness Program vs Treatment
# -----------------------------------

with col1:
    st.subheader("🧘 Wellness Program vs Treatment")

    wellness_treatment = pd.crosstab(
        filtered_df["wellness_program"],
        filtered_df["treatment"]
    )

    fig, ax = plt.subplots(figsize=(7, 4))
    wellness_treatment.plot(kind="bar", ax=ax)

    ax.set_title("Wellness Program and Treatment Seeking")
    ax.set_xlabel("Wellness Program")
    ax.set_ylabel("Number of Respondents")
    plt.xticks(rotation=0)
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)


# -----------------------------------
# Chart 10: Care Options vs Treatment
# -----------------------------------

with col2:
    st.subheader("🏥 Care Options vs Treatment")

    care_treatment = pd.crosstab(
        filtered_df["care_options"],
        filtered_df["treatment"]
    )

    fig, ax = plt.subplots(figsize=(7, 4))
    care_treatment.plot(kind="bar", ax=ax)

    ax.set_title("Care Options and Treatment Seeking")
    ax.set_xlabel("Care Options Available")
    ax.set_ylabel("Number of Respondents")
    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

# -----------------------------------
# Download Filtered Dataset
# -----------------------------------

st.subheader("📥 Download Filtered Data")

csv_data = filtered_df.to_csv(index=False)

st.download_button(
    label="⬇️ Download Filtered Dataset",
    data=csv_data,
    file_name="filtered_mental_health_data.csv",
    mime="text/csv"
)


# -----------------------------------
# Dashboard Footer
# -----------------------------------

st.markdown("---")

st.markdown(
    """
    <div style="text-align: center; padding: 20px;">
        <h4 style="color: #1f3c88;">
            🧠 Mental Health in Tech Dashboard
        </h4>
        <p style="color: #6b7280;">
            Data Analysis & Visualization Project
        </p>
        <p style="color: #6b7280;">
            Built using Python, Pandas, Matplotlib & Streamlit
        </p>
        <p style="color: #9ca3af; font-size: 13px;">
            © 2026 | Mental Health Survey Analysis
        </p>
    </div>
    """,
    unsafe_allow_html=True
)