
import streamlit as st

from agents import process_message
from database import initialize, recent_logs, recent_tickets

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Nexus Bank AI | Smart Support",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

initialize()

# ---------------- MODERN UI STYLING ----------------

st.markdown("""
<style>
.stApp {
    background: linear-gradient(
        135deg, #09142c 0%, #152650 55%, #231b50 100%
    );
    color: #f5f7ff;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #101d43, #211b55);
    border-right: 1px solid #34477d;
}

[data-testid="stSidebar"] * {
    color: #eef2ff;
}

.block-container {
    padding-top: 1.7rem;
    max-width: 1400px;
}

h1, h2, h3, p, label {
    color: #f4f6ff;
}

.hero {
    background: linear-gradient(
        110deg, #2545c1, #7040cf, #a82f9f
    );
    padding: 34px;
    border-radius: 22px;
    margin-bottom: 25px;
    box-shadow: 0 12px 35px #02091955;
}

.hero h1 {
    font-size: 38px;
    color: white;
    margin: 0 0 10px 0;
}

.hero p {
    color: #eeeaff;
    font-size: 16px;
    margin: 0;
}

.metric-card {
    background: linear-gradient(145deg, #263969, #1c2a50);
    border: 1px solid #43578d;
    padding: 23px;
    border-radius: 16px;
    margin-bottom: 16px;
}

.metric-card .value {
    font-size: 31px;
    font-weight: 800;
    color: #a9bcff;
}

.metric-card .label {
    font-size: 14px;
    color: #d5defb;
    margin-top: 5px;
}

.section-heading {
    font-size: 22px;
    font-weight: 750;
    margin: 20px 0;
    color: #ffffff;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
}

.stTabs [data-baseweb="tab"] {
    background: #223560;
    border-radius: 12px;
    padding: 10px 18px;
    color: #e1e9ff;
}

.stTabs [aria-selected="true"] {
    background: #7253dc !important;
    color: white !important;
}

.stButton button[kind="primary"],
.stFormSubmitButton button[kind="primary"] {
    background: linear-gradient(90deg, #4268ef, #9851e6);
    border: none;
    border-radius: 12px;
    color: white;
    font-weight: 700;
    padding: 12px 25px;
}

.stButton button[kind="primary"]:hover,
.stFormSubmitButton button[kind="primary"]:hover {
    background: linear-gradient(90deg, #3459dd, #7841cd);
}

[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    background: #202e53;
    color: #ffffff;
    border: 1px solid #4e6093;
    border-radius: 11px;
}

[data-testid="stAlert"] {
    border-radius: 14px;
}

[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
}

.footer {
    text-align: center;
    color: #aab9d9;
    padding: 22px;
    margin-top: 30px;
    border-top: 1px solid #3d4e7b;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.markdown("## 🏦 NEXUS BANK AI")
    st.caption("Smart Banking Support Platform")

    st.divider()

    st.markdown("### 🤖 AI Agent Network")
    st.write("🧠 Classification Agent")
    st.write("💬 Feedback Handler Agent")
    st.write("🎫 Query Handler Agent")

    st.divider()

    st.markdown("### ⚙️ Technology")
    st.write("✨ Google Gemini")
    st.write("🐍 Python")
    st.write("📊 Streamlit")
    st.write("🗃️ SQLite")

    st.divider()
    st.info(
        "Demo environment only. "
        "Never enter real banking credentials, "
        "PINs, OTPs, or account numbers."
    )

# ---------------- HEADER ----------------

st.markdown("""
<div class="hero">
    <h1>🏦 Intelligent Banking Support</h1>
    <p>
        AI-powered customer assistance with smart
        classification, personalized replies,
        and real-time ticket tracking.
    </p>
    <p style="margin-top:14px;">
        ✨ Gemini AI &nbsp; | &nbsp;
        🤖 Multi-Agent Architecture &nbsp; | &nbsp;
        🔐 Secure Demo
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------- DASHBOARD METRICS ----------------

tickets = recent_tickets()
logs = recent_logs()

unresolved = sum(
    1 for ticket in tickets
    if ticket.get("status") == "Unresolved"
)

m1, m2, m3, m4 = st.columns(4)

metrics = [
    ("💬 Interactions", len(logs)),
    ("🎫 Support Tickets", len(tickets)),
    ("⏳ Unresolved", unresolved),
    ("🤖 AI Agents", 3),
]

for column, (label, value) in zip(
    [m1, m2, m3, m4], metrics
):
    with column:
        st.markdown(
            f'''
            <div class="metric-card">
                <div class="value">{value}</div>
                <div class="label">{label}</div>
            </div>
            ''',
            unsafe_allow_html=True,
        )

st.caption(
    "Statistics reflect recent database records "
    "loaded by the application."
)

# ---------------- MAIN TABS ----------------

chat_tab, tickets_tab, logs_tab, about_tab = st.tabs([
    "💬 AI Customer Support",
    "🎫 Support Tickets",
    "📊 Agent Logs",
    "ℹ️ About",
])

# ---------------- CUSTOMER SUPPORT ----------------

with chat_tab:

    st.markdown(
        '<div class="section-heading">'
        '💬 Talk to our AI Support Agents'
        '</div>',
        unsafe_allow_html=True,
    )

    st.write(
        "Describe your banking concern and "
        "our agents will classify and route it."
    )

    with st.form("support_form", clear_on_submit=False):

        customer_name = st.text_input(
            "👤 Customer Name",
            value="Aisha",
        )

        message = st.text_area(
            "✍️ Your Message",
            placeholder=(
                "Example: My debit card has not arrived "
                "and I need assistance."
            ),
            height=145,
        )

        submitted = st.form_submit_button(
            "🚀 Send to AI Agents",
            type="primary",
            use_container_width=True,
        )

    if submitted:

        if not message.strip():
            st.warning("Please enter a message.")

        else:
            with st.spinner("AI agents are processing..."):
                try:
                    result = process_message(
                        customer_name,
                        message.strip(),
                    )
                    st.session_state["last_result"] = result

                except Exception:
                    st.session_state.pop(
                        "last_result", None
                    )
                    st.error(
                        "We could not process your request. "
                        "Please try again."
                    )

    if "last_result" in st.session_state:

        result = st.session_state["last_result"]

        st.markdown("### ✨ Agent Response")
        st.success(result["response"])

        c1, c2 = st.columns(2)

        with c1:
            st.info(
                "📌 Classification: "
                + result["classification"]
            )

        with c2:
            st.info(
                "🤖 Handled By: "
                + result["agent"]
            )

        if result["ticket_number"]:
            st.warning(
                "🎫 Your Support Ticket Number: "
                + str(result["ticket_number"])
            )

    st.markdown("### 💡 Example Messages")

    examples = [
        "Thank you for resolving my banking issue!",
        "My replacement debit card has not arrived.",
        "What is the status of ticket 123456?",
    ]

    for example in examples:
        st.code(example, language=None)

# ---------------- SUPPORT TICKETS ----------------

with tickets_tab:

    st.markdown("### 🎫 Customer Support Tickets")
    st.caption("Recent tickets recorded in SQLite.")

    ticket_data = recent_tickets()

    if ticket_data:
        st.dataframe(
            ticket_data,
            width="stretch",
            hide_index=True,
        )
    else:
        st.info(
            "No support tickets yet. "
            "Submit negative feedback to create one."
        )

    if st.button("🔄 Refresh Tickets"):
        st.rerun()

# ---------------- AGENT LOGS ----------------

with logs_tab:

    st.markdown("### 📊 AI Agent Interaction History")
    st.caption(
        "Classification decisions, routing, "
        "and generated responses."
    )

    log_data = recent_logs()

    if log_data:
        st.dataframe(
            log_data,
            width="stretch",
            hide_index=True,
        )
    else:
        st.info("No agent interactions recorded yet.")

    if st.button("🔄 Refresh Logs"):
        st.rerun()

# ---------------- ABOUT ----------------

with about_tab:

    st.markdown("### 🚀 Banking AI Architecture")

    st.write(
        "This project demonstrates a multi-agent "
        "customer support system for digital banking."
    )

    st.markdown("""
    **Agent 1 — Classification Agent**

    Categorizes messages as Positive Feedback,
    Negative Feedback, or Query.

    **Agent 2 — Feedback Handler Agent**

    Generates personalized responses and creates
    support tickets for complaints.

    **Agent 3 — Query Handler Agent**

    Retrieves support-ticket information
    using the SQLite database.

    **Evaluation**

    Classification accuracy, agent routing,
    and response-quality assessment are evaluated
    using separate Python scripts.
    """)

    st.info(
        "This is an educational demonstration, "
        "not a production banking system."
    )

# ---------------- FOOTER ----------------

st.markdown("""
<div class="footer">
    🏦 Nexus Bank AI | Multi-Agent Customer Support Demo<br>
    Built using Python, Streamlit, Gemini AI and SQLite
</div>
""", unsafe_allow_html=True)
