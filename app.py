import streamlit as st
from agents import process_message
from database import initialize, recent_logs, recent_tickets

initialize()
st.set_page_config(page_title='Banking AI Support', page_icon='🏦', layout='wide')
st.title('🏦 Banking Customer Support — Multi-Agent System')
st.caption('Phase 1: working rule-based prototype. LLM integration and evaluation come next.')

chat_tab, tickets_tab, logs_tab = st.tabs(['💬 Customer Support', '🎫 Tickets', '📋 Agent Logs'])
with chat_tab:
    customer_name = st.text_input('Customer name', value='Aisha')
    message = st.text_area('Enter a message', placeholder='My debit card replacement still has not arrived.')
    if st.button('Send to agents', type='primary'):
        if not message.strip():
            st.warning('Please enter a message.')
        else:
            try:
                result = process_message(customer_name, message.strip())
                st.success(result['response'])
                st.write('**Classification:**', result['classification'])
                st.write('**Routed to:**', result['agent'])
                if result['ticket_number']:
                    st.write('**Ticket number:**', result['ticket_number'])
            except Exception:
                st.error('We could not process this message. Please try again.')
    st.markdown('**Try these examples:**')
    st.code('Thanks for resolving my net banking login issue.\nMy debit card replacement still has not arrived.\nCan you check ticket 123456?')

with tickets_tab:
    st.subheader('Support tickets')
    tickets = recent_tickets()
    if tickets:
        st.dataframe(tickets, use_container_width=True, hide_index=True)
    else:
        st.info('No tickets yet. Submit negative feedback to create one.')

with logs_tab:
    st.subheader('Agent interaction history')
    logs = recent_logs()
    if logs:
        st.dataframe(logs, use_container_width=True, hide_index=True)
    else:
        st.info('No interactions logged yet.')

st.caption('Demonstration only. Do not enter account numbers, OTPs, PINs, or real customer data.')
