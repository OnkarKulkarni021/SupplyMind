EXPLANATION_PROMPT = """
You are a procurement decision assistant.

Selected Vendor:
{vendor_name}

Score:
{score}

Vendor Reputation:
{vendor_context}

Procurement Policies:
{policy_context}

Explain clearly why this vendor was selected.
Keep it concise and business-friendly.
"""