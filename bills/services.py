"""
KLISS API integration.
Base URL: https://www.kslegislature.gov/li/api/v10/rev-1/
"""
import requests

KLISS_BASE = "https://www.kslegislature.gov/li/api/v10/rev-1"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; KSBillTracker/1.0)"}


def fetch_bill_list():
    """Return raw list of bill dicts from the KLISS API."""
    url = f"{KLISS_BASE}/bill_status/"
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    return response.json()


def fetch_bill_detail(bill_number):
    """Return raw detail dict for a single bill."""
    url = f"{KLISS_BASE}/bill_status/{bill_number}/"
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    return response.json()
