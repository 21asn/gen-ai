import pandas as pd

def check_db_user_settings(service_name, timeframe=None):
    df = pd.read_csv("data/db_user_settings.csv")
    findings = []
    non_compliant_users = []

    for _, row in df.iterrows():
        issues = []

        if row["has_admin_access"] and row["role"] != "admin":
            issues.append("Non-admin user with admin access")

        # Handle NaN and convert safely
        expiry = row.get("password_expiry_days")
        if pd.isna(expiry) or float(expiry) > 90:
            issues.append("Password expiry not enforced")

        idle_timeout = row.get("idle_timeout")
        if pd.notna(idle_timeout) and float(idle_timeout) < 300:
            issues.append("Low idle timeout")

        if row.get("allowed_hosts") == "%":
            issues.append("Wildcard host allowed")

        if issues:
            non_compliant_users.append(row["db_user"])
            findings.append(f"User {row['db_user']} issues: {', '.join(issues)}")

    return {
        "findings": findings,
        "non_compliant_users": non_compliant_users
    }
