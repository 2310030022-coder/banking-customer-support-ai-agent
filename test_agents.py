from agents import classify, extract_ticket_number


def test_positive():
    assert classify('Thanks for your help!') == 'Positive Feedback'


def test_negative():
    assert classify('My debit card has not arrived.') == 'Negative Feedback'


def test_query():
    assert classify('Check ticket 650932 status') == 'Query'


def test_extract():
    assert extract_ticket_number('Status for #650932?') == '650932'
