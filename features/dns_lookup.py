import streamlit as st
import dns.resolver
from dns.exception import DNSException


def perform_dns_lookup(domain, record_type):
    """
    Perform a DNS lookup for the given domain and record type.

    Args:
        domain (str): The domain to query.
        record_type (str): The type of DNS record to fetch (A, MX, NS, TXT, etc.).

    Returns:
        dict: Results of the DNS lookup or an error message.
    """
    try:
        # Resolver instance for DNS queries
        resolver = dns.resolver.Resolver()

        # Query DNS records
        records = resolver.resolve(domain, record_type)
        results = []

        # Parse results based on record type
        for record in records:
            if record_type == "A":
                results.append(record.to_text())  # IP addresses
            elif record_type == "MX":
                results.append(f"{record.exchange} (Priority: {record.preference})")
            elif record_type in ["NS", "TXT", "CNAME"]:
                results.append(record.to_text())
            else:
                results.append(str(record))

        return {"results": results}

    except dns.resolver.NXDOMAIN:
        return {"error": "Domain does not exist. Please enter a valid domain."}
    except dns.resolver.NoAnswer:
        return {"error": f"No {record_type} records found for the domain."}
    except dns.resolver.Timeout:
        return {"error": "DNS query timed out. Please try again later."}
    except DNSException as e:
        return {"error": f"An error occurred while performing the DNS lookup: {e}"}
