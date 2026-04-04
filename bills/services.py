"""
KLISS API integration.
Base URL: https://www.kslegislature.gov/li/api/v10/rev-1/
"""
import requests
from datetime import timedelta

from django.utils import timezone

from .models import Bill

KLISS_BASE = "https://www.kslegislature.gov/li/api/v10/rev-1"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; KSBillTracker/1.0)"}
CACHE_TTL = timedelta(hours=1)


# ---------------------------------------------------------------------------
# Raw HTTP helpers
# ---------------------------------------------------------------------------

def fetch_bill_list():
    """Return raw API response for all bills in current session."""
    url = f"{KLISS_BASE}/bill_status/"
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    return response.json()


def fetch_bill_detail(bill_number):
    """Return raw API response for a single bill."""
    url = f"{KLISS_BASE}/bill_status/{bill_number}/"
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    return response.json()


# ---------------------------------------------------------------------------
# Normalisation / upsert
# ---------------------------------------------------------------------------

def _extract_bills(data):
    """Pull the list of bill dicts out of whatever shape the API returns."""
    if isinstance(data, dict):
        return data.get("content", [])
    if isinstance(data, list):
        return data
    return []


def _parse_bill(raw):
    sponsors = raw.get("SPONSOR_NAMES", [])
    if isinstance(sponsors, list):
        sponsors = ", ".join(sponsors)
    return {
        "short_title": raw.get("SHORTTITLE", "") or "",
        "long_title": raw.get("LONGTITLE", "") or "",
        "status": raw.get("STATUS", "") or "",
        "sponsors": sponsors,
        "effective_date": raw.get("EFFECTIVEDATE") or "",
        "last_fetched": timezone.now(),
    }


def _upsert_bill(raw):
    bill_number = (raw.get("BILLNO") or "").strip()
    if not bill_number:
        return None
    bill, _ = Bill.objects.update_or_create(
        bill_number=bill_number,
        defaults=_parse_bill(raw),
    )
    return bill


# ---------------------------------------------------------------------------
# Public interface used by views
# ---------------------------------------------------------------------------

def get_bill_list(force_refresh=False):
    """
    Return a QuerySet of all Bills ordered by bill_number.
    Hits the API when:
      - no bills exist in the DB, or
      - any bill is older than CACHE_TTL, or
      - force_refresh is True.
    Falls back to cached DB data if the API is unavailable.
    """
    stale_cutoff = timezone.now() - CACHE_TTL
    needs_refresh = (
        force_refresh
        or not Bill.objects.exists()
        or Bill.objects.filter(last_fetched__lt=stale_cutoff).exists()
    )
    if needs_refresh:
        try:
            data = fetch_bill_list()
            for raw in _extract_bills(data):
                _upsert_bill(raw)
        except Exception:
            pass  # serve stale cache if API is down

    return Bill.objects.all().order_by("bill_number")


def get_bill(bill_number):
    """
    Return a single Bill instance.
    Hits the API when the bill is missing or stale.
    Returns None if the bill can't be found anywhere.
    """
    stale_cutoff = timezone.now() - CACHE_TTL
    try:
        bill = Bill.objects.get(bill_number=bill_number)
        if bill.last_fetched and bill.last_fetched > stale_cutoff:
            return bill
    except Bill.DoesNotExist:
        pass

    try:
        data = fetch_bill_detail(bill_number)
        raws = _extract_bills(data)
        if raws:
            return _upsert_bill(raws[0])
    except Exception:
        pass

    return Bill.objects.filter(bill_number=bill_number).first()
