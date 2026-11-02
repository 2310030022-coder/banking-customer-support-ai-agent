"""Baseline rule-based agents. Replace classifier and responses with LLM calls in phase 2."""
import re
import secrets
import sqlite3

from database import create_ticket, get_ticket, record_interaction

POSITIVE_WORDS = ('thank', 'thanks', 'grateful', 'appreciate', 'excellent', 'great service', 'helpful')
NEGATIVE_WORDS = ('not arrived', "hasn't arrived", 'failed', 'bad', 'disappointed',
                  'problem', 'issue', 'complaint', 'wrong', 'missing', 'not working',
                  'delayed', 'still waiting', 'poor', 'not received', 'unhappy', 'refund')


def classify(message):
    """Return Positive Feedback, Negative Feedback, or Query."""
    m = message.lower().strip()
    if re.search(r'\b\d{6}\b', m) and any(w in m for w in ('status', 'ticket', 'update', 'check', 'track')):
        return 'Query'
    if any(w in m for w in POSITIVE_WORDS) and not any(w in m for w in ('not resolved', 'not helpful', 'no thanks')):
        return 'Positive Feedback'
    if any(w in m for w in NEGATIVE_WORDS):
        return 'Negative Feedback'
    return 'Query'


def extract_ticket_number(message):
    match = re.search(r'\b\d{6}\b', message)
    return match.group(0) if match else None


def feedback_handler(customer_name, message, category):
    if category == 'Positive Feedback':
        return f'Thank you for your kind words, {customer_name}! We are delighted to assist you.', None
    # Generate collision-resistant *unique* six-digit IDs; retry on database conflict.
    for _ in range(100):
        ticket_number = str(secrets.randbelow(900000) + 100000)
        try:
            create_ticket(ticket_number, customer_name, message)
            return (f'We apologize for the inconvenience, {customer_name}. '
                    f'A new ticket #{ticket_number} has been created. Our support team will follow up.'), ticket_number
        except sqlite3.IntegrityError:
            continue
    raise RuntimeError('Unable to create a unique ticket. Please try again.')


def query_handler(message):
    ticket_number = extract_ticket_number(message)
    if ticket_number is None:
        return 'Please share your 6-digit support ticket number so I can check its status.', None
    ticket = get_ticket(ticket_number)
    if ticket is None:
        return f'I could not find ticket #{ticket_number}. Please check the number and try again.', ticket_number
    return f'Your ticket #{ticket_number} is currently marked as: {ticket["status"]}.', ticket_number


def process_message(customer_name, message):
    name = customer_name.strip() or 'Customer'
    category = classify(message)
    if category in ('Positive Feedback', 'Negative Feedback'):
        agent = 'Feedback Handler Agent'
        response, ticket_number = feedback_handler(name, message, category)
    else:
        agent = 'Query Handler Agent'
        response, ticket_number = query_handler(message)
    record_interaction(name, message, category, agent, response, ticket_number)
    return {'classification': category, 'agent': agent, 'response': response, 'ticket_number': ticket_number}
