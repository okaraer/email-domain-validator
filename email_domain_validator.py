"""
Email Domain Validator (MX Checker)
----------------------------------
Reads an Excel file containing email addresses, extracts domains, and checks whether
each domain has an MX (mail exchanger) record. Writes results back to a new Excel file.

Output column:
- domain_active: 1 if MX exists, otherwise 0

Notes:
- This validates domain-level email infrastructure, NOT mailbox deliverability.
"""

from __future__ import annotations

import argparse
from typing import Dict, Optional

import pandas as pd
import dns.resolver


def extract_domain(email: str) -> Optional[str]:
    """
    Extract the domain part from an email address.

    Returns None if the email is missing '@' or is empty.
    """
    if not isinstance(email, str):
        return None
    email = email.strip()
    if "@" not in email or not email:
        return None
    return email.split("@", 1)[1].lower().strip()


def mx_exists(domain: str, resolver: dns.resolver.Resolver, cache: Dict[str, int]) -> int:
    """
    Check whether a domain has an MX record.

    Uses an in-memory cache to avoid repeating DNS queries for the same domain.
    Returns:
        1 -> MX record exists
        0 -> no MX record / query failed
    """
    if domain in cache:
        return cache[domain]

    try:
        resolver.resolve(domain, "MX")
        cache[domain] = 1
    except Exception:
        cache[domain] = 0

    return cache[domain]


def run(
    input_file: str,
    output_file: str,
    email_column: str = "email",
    output_column: str = "domain_active",
    timeout: float = 2.0,
    lifetime: float = 3.0,
    progress_every: int = 50,
) -> None:
    """
    Process the Excel file and write results to output_file.
    """
    print(f"Loading Excel: {input_file}", flush=True)
    df = pd.read_excel(input_file)

    if email_column not in df.columns:
        raise ValueError(
            f"Column '{email_column}' was not found. Available columns: {list(df.columns)}"
        )

    resolver = dns.resolver.Resolver()
    resolver.timeout = timeout
    resolver.lifetime = lifetime

    emails = df[email_column].astype(str).str.strip()
    domains = emails.apply(extract_domain)

    unique_domains = sorted({d for d in domains if d and d != "nan"})
    print(f"Rows: {len(df)} | Unique domains: {len(unique_domains)}", flush=True)

    cache: Dict[str, int] = {}

    for i, d in enumerate(unique_domains, start=1):
        mx_exists(d, resolver, cache)
        if i % progress_every == 0 or i == len(unique_domains):
            print(f"Checked domains: {i}/{len(unique_domains)}", flush=True)

    df[output_column] = domains.map(lambda d: cache.get(d, 0))

    print(f"Writing output: {output_file}", flush=True)
    df.to_excel(output_file, index=False)
    print("Done ✅", flush=True)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate email domains via MX record lookup.")
    parser.add_argument("--input", default="sample_emails.xlsx", help="Input Excel file path")
    parser.add_argument("--output", default="result.xlsx", help="Output Excel file path")
    parser.add_argument("--email-column", default="email", help="Column name containing emails")
    parser.add_argument("--output-column", default="domain_active", help="Output column name")
    parser.add_argument("--timeout", type=float, default=2.0, help="DNS query timeout (seconds)")
    parser.add_argument("--lifetime", type=float, default=3.0, help="DNS total lifetime (seconds)")
    return parser


if __name__ == "__main__":
    parser = build_arg_parser()
    args = parser.parse_args()

    run(
        input_file=args.input,
        output_file=args.output,
        email_column=args.email_column,
        output_column=args.output_column,
        timeout=args.timeout,
        lifetime=args.lifetime,
    )
