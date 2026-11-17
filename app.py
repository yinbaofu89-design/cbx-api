import streamlit as st
import requests
import json
import base64

# Streamlit Page Config
st.set_page_config(
    page_title="CBX API Master Commander",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header { font-size: 1.8rem; font-weight: 700; color: #1E293B; margin-bottom: 0.2rem; }
    .sub-header { font-size: 0.9rem; color: #64748B; margin-bottom: 1.5rem; }
    .box-container { background-color: #F8FAFC; padding: 1rem; border-radius: 8px; border: 1px solid #E2E8F0; }
</style>
""", unsafe_allow_html=True)

# Default Token
DEFAULT_TOKEN = "eyJraWQiOiJGenFEamZXNlRYaTUzNVN4QnFoMTIzIiwidHlwIjoiSldUIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJ1cm46YnJvYWRjb206c2Fhczpkb21haW46ZjZHOHI5eEhTVmlzd0dNSENkX2ZNUTpjbGllbnQ6TzJJRC5Xdm0xTDlUQVJ3T1pXVHpFQkJqVzB3LmY2RzhyOXhIU1Zpc3dHTUhDZF9mTVEuNWttZXFwcWw1NGFmM3JxdjZrazRiZ2gyYzAiLCJ2ZXIiOjIsImlzcyI6Imh0dHBzOi8vYXBpLnNlY3VyaXR5LmNvbSIsInVyaSI6Ii9vYXV0aDIvY2xpZW50cy9PMklELld2bTFMOVRBUndPWldUekVCQmpXMHcuZjZHOHI5eEhTVmlzd0dNSENkX2ZNUS41a21lcXBxbDU0YWYzcnF2NmtrNGJnaDJjMCIsImNsaWVudF9pZCI6Ik8ySUQuV3ZtMUw5VEFSd09aV1R6RUJCalcwdy5mNkc4cjl4SFNWaXN3R01IQ2RfZk1RLjVrbWVxcHFsNTRhZjNycXY2a2s0YmdoMmMwIiwiZG9tYWluX2lkIjoiZjZHOHI5eEhTVmlzd0dNSENkX2ZNUSIsInNjb3BlIjoiZG9tYWluIG9hdXRoIiwidHR5IjoiYWNjZXNzIiwicHJpdnMiOiJlZHJfZ2V0X2ZpbGUgY2J4X2Rvd25sb2FkX2ZpbGUgd3NzX3ZpZXdfcG9saWN5X2xpc3RzIGFlcF9ydW5fcXVhcmFudGluZSBzZXNfdXBkYXRlX3NoYXJlZF9lbmRwb2ludCBzZXNfdmlld19zaGFyZWRfZW5kcG9pbnQgZWRyX2RlbGV0ZV9maWxlIGVkcl9kZWxldGVfZW5kcG9pbnRzZWFyY2ggY2JjX2xyX2V4ZWN1dGVfcHJvY2VzcyBjYnhfdmlld192dWxuZXJhYmlsaXR5X2RhdGEgY3BfbWFuYWdlX2VuZHBvaW50X3BvbGljeSBjYmNfdmlld19scSBjYmNfdmlld19kYXRhX2ZvcndhcmRlcnMgY2J4X3N1Ym1pdF9zYW5kYm94IGNiY192aWV3X25vdGlmaWNhdGlvbnMgY2J4X21hbmFnZV92dWxuZXJhYmlsaXR5X2RhdGEgY2JjX3ZpZXdfd2F0Y2hsaXN0cyBjYmNfdmlld19hbGVydHMgY2JjX3VzZV9sciBlZHJfZ2V0ZmlsZV9ub2NyZWQgYWVwX3J1bl9saXZldXBkYXRlIGFlcF9tYW5hZ2VfY29tbWFuZHMgY2JjX21uZ19hbGVydHNfbm90ZXNfdGFncyBjYnhfdmlld19kZXZpY2Vfc2VhcmNoIGNiY19tbmdfbm90aWZpY2F0aW9ucyBjYmNfcGVyZm9ybV9kZW9iZnVzY2F0aW9uIGNiY19yZXF1ZXN0X3VwZGF0ZWRfdnVsbl9kYXRhIGNiY19tbmdfd2F0Y2hsaXN0cyBzZXNfdmlld19hbGxfZmlsZXMgY3BfbWFuYWdlX2dsb2JhbF9wb2xpY3kgY2JjX2Nsb3NlX2FsZXJ0cyBjYmNfbW5nX2RhdGFfZm9yd2FyZGVycyB3c3NfbWFuYWdlX3BvbGljeV9saXN0cyBjYmNfbWFuYWdlX2FsZXJ0cyBzZXNfbWFuYWdlX3NoYXJlZF9lbmRwb2ludCBjYmNfbHJfdmlldyBlZHJfdHJpZ2dlcl9lbmRwb2ludHNlYXJjaCBzZXNfdmlld19yZXBvcnRzIHZpZXdfZXZlbnRzIGVkcl9yc2hlbGxfaW52ZXMgc2VzX3RocmVhdF9pbnRlbF9hcGlfYWNjZXNzIGNiY192aWV3X2V4cG9ydF92dWxuX2RhdGEgc2VzX21hbmFnZV9yZXBvcnRzIGNiY19jb25kdWN0X3Byb2Nlc3NfYW5hbHlzaXMgY3Bfdmlld19nbG9iYWxfcG9saWN5IGFlcF9yZW1vdGVfbG9nX2NvbGxlY3QgYWVwX3J1bl9yZWJvb3QgYWVwX3J1bl9zY2FuIHRkYWRfdHJpZ2dlcl9mb3JlbnNpY3MgY2JjX2xyX2R1bXBfbWVtb3J5IGNwX3ZpZXdfeGRyX3BvbGljeSBjYmNfZXhwb3J0X2V2ZW50X2RhdGEgY3BfbWFuYWdlX3hkcl9wb2xpY3kgY2JjX2NvbmR1Y3RfaW52ZXN0aWdhdGlvbiBlZHJfdmlld19pbnZlc3RpZ2F0aW9uIGNwX3ZpZXdfZW5kcG9pbnRfcG9saWN5IGVkcl9jYW5jZWxfZW5kcG9pbnRzZWFyY2ggY2J4X2RlbGV0ZV9maWxlIGFlcF92aWV3X2NvbW1hbmRzIGNieF9tYW5hZ2VfZGV2aWNlX3NlYXJjaCIsImV4cCI6MTc5NDg5NTE1NCwiY3VzdG9tZXJfaWQiOiJXdm0xTDlUQVJ3T1pXVHpFQkJqVzB3IiwiaWF0IjoxNzk0ODkxNTU0LCJqdGkiOiJuNkh1bUMwdFRFSy1EUHdBTThReTJnIn0.UK25LPk6Fj04SB8n30KRg9vXFa8CwoN-hb0PAw-cNvy_NKgJMwMCXWXMDG0b-9dSMcO6-fDAACjklRz_tgvcoWP0zFGrLYkIv_16WVlEuNTx9efq1yLqPeA7X83i5zJD0YJSkrn1CQjuT2QSmWHgYkwq_F8mgiUz21cUAPTHA8R3_jvWuKtZnyNBwHBvjwuRqVfgFfLSQfzxpXfAxBzdC3n8HE8JqnqwS8-4P5llulpa3NRoaRW04DItstYEcJ-Vq4pRySQEjY-pW4NriIzMzWoGabsJfFU65zrMDPk6OmpuK2cOizyJHe8QtHez3Zqb07kAjHOgDArk0-67i_UQLQ"

def extract_jwt_claims(token_str):
    if not token_str:
        return None, None
    clean_token = token_str.replace("Bearer ", "").strip()
    parts = clean_token.split(".")
    if len(parts) == 3:
        try:
            payload_b64 = parts[1] + "=" * ((4 - len(parts[1]) % 4) % 4)
            payload_json = json.loads(base64.b64decode(payload_b64).decode("utf-8"))
            return payload_json.get("customer_id"), payload_json.get("domain_id")
        except Exception:
            pass
    return None, None

# --- SIDEBAR ---
st.sidebar.title("⚡ CBX Control Panel")
st.sidebar.markdown("---")

api_token = st.sidebar.text_input(
    "OAuth Bearer / Basic Token",
    value=DEFAULT_TOKEN,
    type="password",
    help="認証トークンを入力してください。JWTの場合、customer_idとdomain_idが自動抽出されます。"
)

server_url = st.sidebar.text_input(
    "Server Base URL",
    value="https://api.us.security.com"
)

c_id, d_id = extract_jwt_claims(api_token)
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Auto-detected Customer ID:** `{c_id or 'N/A'}`")
st.sidebar.markdown(f"**Auto-detected Domain ID:** `{d_id or 'N/A'}`")

st.session_state["cbx_token"] = api_token if api_token else DEFAULT_TOKEN
st.session_state["server_url"] = server_url

if "exec_method" not in st.session_state:
    st.session_state["exec_method"] = "POST"
if "exec_endpoint" not in st.session_state:
    st.session_state["exec_endpoint"] = "/detect-respond/detection/v1/custom-detections/_search"
if "exec_payload" not in st.session_state:
    st.session_state["exec_payload"] = json.dumps({
        "page": 1,
        "size": 10,
        "customer_id": c_id or "",
        "domain_id": d_id or ""
    }, indent=2)

# Header
st.markdown('<div class="main-header">⚡ CBX API Master Commander</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">すべてのMDファイルに記載された全API・全エンドポイントを完全網羅。入力欄から動的にリクエストデータ・Pythonコード・cURLを生成して実行できます。</div>', unsafe_allow_html=True)

# Category selection covering ALL 11 modules
module_choice = st.selectbox(
    "📁 APIモジュール（カテゴリ）を選択",
    [
        "🔑 Authentication (OAuth 2.0)",
        "🎯 Custom Detections",
        "💻 Device Query",
        "🚨 Alerts & Threats",
        "⚙️ Jobs & Export",
        "🔌 Live Response",
        "🔔 Notifications",
        "📜 Policy Management",
        "🔓 Script Deobfuscation",
        "🌐 Threat Intel (TAXII 1.1)",
        "🛡️ Vulnerability Assessment"
    ]
)

st.markdown("---")

# Comprehensive Endpoint & Form Generator
with st.container():
    st.subheader(f"📝 テンプレート & 入力フォーム: {module_choice}")
    
    t_method = "GET"
    t_endpoint = ""
    t_data = {}

    col_in1, col_in2 = st.columns([1, 1])

    with col_in1:
        if "Authentication" in module_choice:
            op = st.selectbox("Endpoint", ["POST /common/v1/oauth2/tokens"])
            t_method = "POST"
            t_endpoint = "/common/v1/oauth2/tokens"
            grant_type = st.text_input("grant_type", value="client_credentials")
            scope = st.text_input("scope", value="domain")
            t_data = {"grant_type": grant_type, "scope": scope}

        elif "Custom Detections" in module_choice:
            op = st.selectbox("Endpoint", [
                "POST /detect-respond/detection/v1/custom-detections/_search",
                "POST /detect-respond/detection/v1/custom-detections",
                "POST /detect-respond/detection/v1/custom-detections/_import",
                "GET /detect-respond/detection/v1/custom-detections/{detection_id}",
                "PUT /detect-respond/detection/v1/custom-detections/{detection_id}",
                "DELETE /detect-respond/detection/v1/custom-detections/{detection_id}",
                "POST /detect-respond/detection/v1/custom-detections/_bulk",
                "POST /detect-respond/detection/v1/custom-detections/queries/_search",
                "POST /detect-respond/detection/v1/custom-detections/{detection_id}/queries",
                "GET /detect-respond/detection/v1/custom-detections/{detection_id}/queries/{query_id}",
                "PUT /detect-respond/detection/v1/custom-detections/{detection_id}/queries/{query_id}",
                "DELETE /detect-respond/detection/v1/custom-detections/{detection_id}/queries/{query_id}",
                "POST /detect-respond/detection/v1/custom-detections/{detection_id}/queries/_bulk"
            ])
            t_method, t_endpoint = op.split(" ", 1)
            
            if "{detection_id}" in t_endpoint:
                det_id = st.text_input("detection_id", value="det-123")
                t_endpoint = t_endpoint.replace("{detection_id}", det_id)
            if "{query_id}" in t_endpoint:
                q_id = st.text_input("query_id", value="q-123")
                t_endpoint = t_endpoint.replace("{query_id}", q_id)

            if "_search" in t_endpoint:
                page = st.number_input("page", value=1, min_value=1)
                size = st.number_input("size", value=10, min_value=1)
                t_data = {"page": page, "size": size}
            elif t_method in ["POST", "PUT"]:
                name = st.text_input("name", value="Sample Detection")
                desc = st.text_input("description", value="Description")
                enabled = st.checkbox("enabled", value=True)
                t_data = {"name": name, "description": desc, "enabled": enabled}

        elif "Device Query" in module_choice:
            op = st.selectbox("Endpoint", [
                "GET /detect-respond/device-query/v2/commands",
                "POST /detect-respond/device-query/v2/commands",
                "GET /detect-respond/device-query/v2/commands/{commandId}",
                "DELETE /detect-respond/device-query/v2/commands/{commandId}",
                "PUT /detect-respond/device-query/v2/commands/{commandId}/cancel",
                "POST /detect-respond/device-query/v2/commands/{commandId}/results",
                "GET /detect-respond/device-query/v2/schedules",
                "POST /detect-respond/device-query/v2/schedules",
                "DELETE /detect-respond/device-query/v2/schedules",
                "GET /detect-respond/device-query/v2/schedules/{scheduleId}",
                "PUT /detect-respond/device-query/v2/schedules/{scheduleId}",
                "GET /detect-respond/device-query/v2/schedules/{scheduleId}/commands",
                "PUT /detect-respond/device-query/v2/schedules/{scheduleId}/stop"
            ])
            t_method, t_endpoint = op.split(" ", 1)
            
            if "{commandId}" in t_endpoint:
                cid = st.text_input("commandId", value="cmd-123")
                t_endpoint = t_endpoint.replace("{commandId}", cid)
            if "{scheduleId}" in t_endpoint:
                sid = st.text_input("scheduleId", value="sched-123")
                t_endpoint = t_endpoint.replace("{scheduleId}", sid)

            if t_method == "POST" and "commands" in t_endpoint and "results" not in t_endpoint:
                cmd_type = st.selectbox("command_type", ["forensic", "artifact"])
                scope = st.selectbox("scope", ["all", "device_ids"])
                query_str = st.text_area("query", value="SELECT * FROM processes;")
                dev_ids = st.text_input("device_ids (comma separated)", value="dev-001,dev-002")
                t_data = {
                    "command_type": cmd_type,
                    "scope": scope,
                    "query": query_str,
                    "device_ids": [d.strip() for d in dev_ids.split(",") if d.strip()]
                }
            elif t_method == "POST" and "schedules" in t_endpoint:
                s_name = st.text_input("Schedule Name", value="Daily Forensic")
                s_query = st.text_area("Schedule Query", value="SELECT * FROM services;")
                t_data = {"name": s_name, "query": s_query, "command_type": "forensic"}

        elif "Alerts & Threats" in module_choice:
            op = st.selectbox("Endpoint", [
                "POST /detect-respond/alerts/v8/alerts/_search",
                "POST /detect-respond/alerts/v8/alerts/_export",
                "POST /detect-respond/alerts/v8/alerts/_facet",
                "POST /detect-respond/alerts/v8/alerts/_histogram",
                "POST /detect-respond/alerts/v8/alerts/_validate",
                "GET /detect-respond/alerts/v8/alerts/search_suggestions",
                "GET /detect-respond/alerts/v8/alerts/{alert_id}",
                "GET /detect-respond/alerts/v8/alerts/{alert_id}/history",
                "GET /detect-respond/alerts/v8/alerts/{alert_id}/notes",
                "POST /detect-respond/alerts/v8/alerts/{alert_id}/notes",
                "PATCH /detect-respond/alerts/v8/alerts/{alert_id}/notes",
                "PUT /detect-respond/alerts/v8/alerts/{alert_id}/notes/{id}",
                "DELETE /detect-respond/alerts/v8/alerts/{alert_id}/notes/{id}",
                "POST /detect-respond/alerts/v8/grouped_alerts/_search",
                "POST /detect-respond/alerts/v8/grouped_alerts/_facet",
                "POST /detect-respond/alerts/v8/grouped_alerts/_histogram",
                "GET /detect-respond/alerts/v8/threats/{threat_id}/history",
                "GET /detect-respond/alerts/v8/threats/{threat_id}/notes",
                "POST /detect-respond/alerts/v8/threats/{threat_id}/notes",
                "DELETE /detect-respond/alerts/v8/threats/{threat_id}/notes/{id}",
                "GET /detect-respond/alerts/v8/threats/{threat_id}/tags",
                "POST /detect-respond/alerts/v8/threats/{threat_id}/tags",
                "DELETE /detect-respond/alerts/v8/threats/{threat_id}/tags/{tag}",
                "POST /detect-respond/alerts/v8/alerts/workflow",
                "POST /detect-respond/alerts/v8/alerts/threat/workflow/_criteria"
            ])
            t_method, t_endpoint = op.split(" ", 1)
            
            if "{alert_id}" in t_endpoint:
                aid = st.text_input("alert_id", value="alt-123")
                t_endpoint = t_endpoint.replace("{alert_id}", aid)
            if "{threat_id}" in t_endpoint:
                tid = st.text_input("threat_id", value="threat-123")
                t_endpoint = t_endpoint.replace("{threat_id}", tid)
            if "{id}" in t_endpoint:
                nid = st.text_input("id (note/tag id)", value="note-123")
                t_endpoint = t_endpoint.replace("{id}", nid)
            if "{tag}" in t_endpoint:
                tag = st.text_input("tag", value="malware")
                t_endpoint = t_endpoint.replace("{tag}", tag)

            if "_search" in t_endpoint or "_export" in t_endpoint or "_facet" in t_endpoint or "_histogram" in t_endpoint:
                rows = st.number_input("rows", value=10, min_value=1)
                start = st.number_input("start", value=0, min_value=0)
                t_data = {"criteria": {}, "rows": rows, "start": start}
            elif "workflow" in t_endpoint:
                status = st.selectbox("status", ["NEW", "IN_PROGRESS", "RESOLVED", "CLOSED"])
                determination = st.selectbox("determination", ["TRUE_POSITIVE", "FALSE_POSITIVE", "UNKNOWN"])
                t_data = {"status": status, "determination": determination}

        elif "Jobs & Export" in module_choice:
            op = st.selectbox("Endpoint", [
                "POST /detect-respond/jobs/v4/event_export",
                "GET /detect-respond/jobs/v4/jobs/{job_id}",
                "GET /detect-respond/jobs/v4/jobs/{job_id}/download"
            ])
            t_method, t_endpoint = op.split(" ", 1)
            if "{job_id}" in t_endpoint:
                jid = st.text_input("job_id", value="job-123")
                t_endpoint = t_endpoint.replace("{job_id}", jid)
            if t_method == "POST":
                q = st.text_input("query", value="process_name: powershell.exe")
                time_range = st.selectbox("time_range", ["1h", "24h", "7d", "30d"])
                t_data = {"query": q, "time_range": time_range}

        elif "Live Response" in module_choice:
            op = st.selectbox("Endpoint", [
                "GET /detect-respond/live-response/v7/sessions",
                "POST /detect-respond/live-response/v7/sessions",
                "GET /detect-respond/live-response/v7/sessions/{session_id}",
                "DELETE /detect-respond/live-response/v7/sessions/{session_id}",
                "GET /detect-respond/live-response/v7/sessions/{session_id}/files",
                "POST /detect-respond/live-response/v7/sessions/{session_id}/files",
                "GET /detect-respond/live-response/v7/sessions/{session_id}/files/{file_id}",
                "DELETE /detect-respond/live-response/v7/sessions/{session_id}/files/{file_id}",
                "GET /detect-respond/live-response/v7/sessions/{session_id}/files/{file_id}/content",
                "GET /detect-respond/live-response/v7/sessions/{session_id}/commands",
                "POST /detect-respond/live-response/v7/sessions/{session_id}/commands",
                "GET /detect-respond/live-response/v7/sessions/{session_id}/commands/{command_id}",
                "DELETE /detect-respond/live-response/v7/sessions/{session_id}/commands/{command_id}"
            ])
            t_method, t_endpoint = op.split(" ", 1)
            if "{session_id}" in t_endpoint:
                sid = st.text_input("session_id", value="sess-123")
                t_endpoint = t_endpoint.replace("{session_id}", sid)
            if "{file_id}" in t_endpoint:
                fid = st.text_input("file_id", value="file-123")
                t_endpoint = t_endpoint.replace("{file_id}", fid)
            if "{command_id}" in t_endpoint:
                cmid = st.text_input("command_id", value="cmd-123")
                t_endpoint = t_endpoint.replace("{command_id}", cmid)

            if t_method == "POST" and "sessions" in t_endpoint and "commands" not in t_endpoint and "files" not in t_endpoint:
                dev_id = st.text_input("device_id", value="device-001")
                t_data = {"device_id": dev_id}
            elif t_method == "POST" and "commands" in t_endpoint:
                lr_cmd = st.text_input("command", value="processes")
                t_data = {"command": lr_cmd}

        elif "Notifications" in module_choice:
            op = st.selectbox("Endpoint", [
                "GET /detect-respond/notifications/v2/rules",
                "POST /detect-respond/notifications/v2/rules",
                "PUT /detect-respond/notifications/v2/rules/{ruleId}",
                "DELETE /detect-respond/notifications/v2/rules/{ruleId}",
                "POST /detect-respond/notifications/v2/history/_search"
            ])
            t_method, t_endpoint = op.split(" ", 1)
            if "{ruleId}" in t_endpoint:
                rid = st.text_input("ruleId", value="rule-123")
                t_endpoint = t_endpoint.replace("{ruleId}", rid)
            if t_method in ["POST", "PUT"]:
                r_name = st.text_input("Rule Name", value="Alert Notification")
                enabled = st.checkbox("enabled", value=True)
                t_data = {"name": r_name, "enabled": enabled}

        elif "Policy Management" in module_choice:
            op = st.selectbox("Endpoint", [
                "GET /common/policy-management/v2/policies",
                "POST /common/policy-management/v2/policies",
                "PUT /common/policy-management/v2/policies",
                "DELETE /common/policy-management/v2/policies/{policy-id}",
                "POST /common/policy-management/v2/policies/copy",
                "GET /common/policy-management/v2/policies/{policy-id}/versions",
                "GET /common/policy-management/v2/policies/{policy-id}/versions/{policy-version}",
                "PATCH /common/policy-management/v2/policies/allow-list/{policy-id}/versions/{policy-version}",
                "PUT /common/policy-management/v2/policies/allow-list/{policy-id}/versions/{policy-version}",
                "PATCH /common/policy-management/v2/policies/deny-list/{policy-id}/versions/{policy-version}",
                "PUT /common/policy-management/v2/policies/deny-list/{policy-id}/versions/{policy-version}",
                "GET /common/policy-management/v2/policies/device-groups/{group-id}/policies",
                "POST /common/policy-management/v2/policies/{policy-id}/versions/{policy-version}/device-groups",
                "DELETE /common/policy-management/v2/policies/{policy-id}/versions/{policy-version}/device-groups",
                "POST /common/policy-management/v2/policies/export/all",
                "POST /common/policy-management/v2/policies/export/types",
                "POST /common/policy-management/v2/policies/export/names",
                "GET /common/policy-management/v2/policies/export/{export-id}/status",
                "POST /common/policy-management/v2/policies/import",
                "GET /common/policy-management/v2/policies/import/{import-id}/status",
                "GET /common/policy-management/v2/policies/target-rules",
                "POST /common/policy-management/v2/policies/target-rules/export/all",
                "POST /common/policy-management/v2/policies/target-rules/export/names",
                "GET /common/policy-management/v2/policies/target-rules/export/{export-id}/status",
                "POST /common/policy-management/v2/policies/target-rules/import",
                "GET /common/policy-management/v2/policies/target-rules/import/{import-id}/status"
            ])
            t_method, t_endpoint = op.split(" ", 1)
            if "{policy-id}" in t_endpoint:
                pid = st.text_input("policy-id", value="pol-123")
                t_endpoint = t_endpoint.replace("{policy-id}", pid)
            if "{policy-version}" in t_endpoint:
                pver = st.text_input("policy-version", value="1")
                t_endpoint = t_endpoint.replace("{policy-version}", pver)
            if "{group-id}" in t_endpoint:
                gid = st.text_input("group-id", value="group-123")
                t_endpoint = t_endpoint.replace("{group-id}", gid)
            if "{export-id}" in t_endpoint:
                eid = st.text_input("export-id", value="exp-123")
                t_endpoint = t_endpoint.replace("{export-id}", eid)
            if "{import-id}" in t_endpoint:
                iid = st.text_input("import-id", value="imp-123")
                t_endpoint = t_endpoint.replace("{import-id}", iid)

            if t_method in ["POST", "PUT"] and "export" not in t_endpoint and "import" not in t_endpoint and "copy" not in t_endpoint:
                p_name = st.text_input("Policy Name", value="Firewall Policy")
                p_type = st.text_input("Policy Type", value="Firewall")
                t_data = {"name": p_name, "type": p_type}

        elif "Script Deobfuscation" in module_choice:
            op = st.selectbox("Endpoint", ["POST /detect-respond/script-deobfuscation/v3/reveal"])
            t_method, t_endpoint = op.split(" ", 1)
            script_b64 = st.text_area("Script / Base64", value="powershell.exe -e aQBm...")
            t_data = {"script": script_b64}

        elif "Threat Intel" in module_choice:
            op = st.selectbox("Endpoint", [
                "POST /common/threat-intel/v1/taxii11/discovery",
                "POST /common/threat-intel/v1/taxii11/collection-management",
                "POST /common/threat-intel/v1/taxii11/poll"
            ])
            t_method, t_endpoint = op.split(" ", 1)
            if "poll" in t_endpoint:
                col_name = st.text_input("collection_name", value="threat-alerts")
                t_data = {"collection_name": col_name}

        elif "Vulnerability Assessment" in module_choice:
            op = st.selectbox("Endpoint", [
                "GET /endpoint-security/vulnerability/assessment/v3/vulnerabilities/summary",
                "POST /endpoint-security/vulnerability/assessment/v3/devices/vulnerabilities/summary/_search",
                "POST /endpoint-security/vulnerability/assessment/v3/devices/vulnerabilities/summary/_facets",
                "POST /endpoint-security/vulnerability/assessment/v3/devices/vulnerabilities/summary/export",
                "POST /endpoint-security/vulnerability/assessment/v3/devices/vulnerabilities/_search",
                "POST /endpoint-security/vulnerability/assessment/v3/devices/vulnerabilities/_facets",
                "POST /endpoint-security/vulnerability/assessment/v3/devices/vulnerabilities/export",
                "GET /endpoint-security/vulnerability/assessment/v3/vulnerabilities/{cve_id}",
                "GET /endpoint-security/vulnerability/assessment/v3/vulnerabilities/{cve_id}/summary",
                "POST /endpoint-security/vulnerability/assessment/v3/vulnerabilities/{cve_id}/devices",
                "POST /endpoint-security/vulnerability/assessment/v3/vulnerabilities/{cve_id}/software/_search",
                "POST /endpoint-security/vulnerability/assessment/v3/vulnerabilities/{cve_id}/actions",
                "GET /endpoint-security/vulnerability/assessment/v3/devices/{device_uid}/vulnerabilities/summary",
                "POST /endpoint-security/vulnerability/assessment/v3/devices/{device_uid}/vulnerabilities/_search",
                "POST /endpoint-security/vulnerability/assessment/v3/devices/{device_uid}/vulnerabilities/export",
                "POST /endpoint-security/vulnerability/assessment/v3/devices/{device_uid}/device-actions"
            ])
            t_method, t_endpoint = op.split(" ", 1)
            if "{cve_id}" in t_endpoint:
                cve = st.text_input("cve_id", value="CVE-2023-1234")
                t_endpoint = t_endpoint.replace("{cve_id}", cve)
            if "{device_uid}" in t_endpoint:
                duid = st.text_input("device_uid", value="dev-1234")
                t_endpoint = t_endpoint.replace("{device_uid}", duid)

            if "_search" in t_endpoint or "summary" in t_endpoint and t_method == "POST":
                rows = st.number_input("rows", value=10, min_value=1)
                start = st.number_input("start", value=0, min_value=0)
                t_data = {"rows": rows, "start": start}

        # Auto inject customer_id & domain_id if POST/PUT/PATCH
        if t_method in ["POST", "PUT", "PATCH"] and isinstance(t_data, dict):
            if c_id and "customer_id" not in t_data: t_data["customer_id"] = c_id
            if d_id and "domain_id" not in t_data: t_data["domain_id"] = d_id

    with col_in2:
        st.markdown("**生成されるプレビュー (URL / データ):**")
        preview_text = f"Endpoint: {t_endpoint}\nMethod: {t_method}\nData:\n{json.dumps(t_data, indent=2)}"
        st.code(preview_text, language="json")
        
        if st.button("📥 実行ボックスにこの設定を転送する", use_container_width=True, type="primary"):
            st.session_state["exec_method"] = t_method
            st.session_state["exec_endpoint"] = t_endpoint
            st.session_state["exec_payload"] = json.dumps(t_data, indent=2)
            st.success("実行ボックスへ転送しました！下へスクロールしてください。")

st.markdown("---")

# --- ALWAYS VISIBLE EXECUTION BOX (SIDE-BY-SIDE + PYTHON SNIPPET) ---
st.markdown("## 🚀 共通実行ボックス (Execution Box)")
st.markdown("URL、Method、Request Data（JSON）を横並びで確認・編集でき、**cURL** と **Pythonコード** の両方を確認しながら実行できます。")

with st.container():
    st.markdown('<div class="box-container">', unsafe_allow_html=True)
    
    ex_col1, ex_col2 = st.columns([1, 3])
    with ex_col1:
        methods_list = ["GET", "POST", "PUT", "DELETE", "PATCH"]
        curr_m = st.session_state["exec_method"]
        m_index = methods_list.index(curr_m) if curr_m in methods_list else 0
        method = st.selectbox("Method", methods_list, index=m_index, key="box_method")
    with ex_col2:
        endpoint = st.text_input("Endpoint Path / URL", value=st.session_state["exec_endpoint"], key="box_endpoint")

    full_url_preview = f"{server_url.rstrip('/')}{endpoint}"
    headers_preview = {
        "Authorization": f"Bearer {api_token}" if not api_token.startswith("Basic ") else api_token,
        "content-type": "application/json"
    }

    exec_col_left, exec_col_right = st.columns([1, 1])

    with exec_col_left:
        st.markdown("#### 🔗 リクエスト情報")
        st.markdown(f"**URL:** `{full_url_preview}`")
        st.markdown("**Headers:**")
        st.json(headers_preview)

    with exec_col_right:
        st.markdown("#### 📦 リクエストデータ (JSON Payload)")
        raw_data_input = st.text_area("JSON Raw Data", value=st.session_state["exec_payload"], height=160, key="box_payload_input")

    # Code Snippets generation tab
    st.markdown("#### 💻 リクエストコード生成 (cURL & Python)")
    snip_tab1, snip_tab2 = st.tabs(["cURL Command", "Python Code Snippet"])
    
    with snip_tab1:
        curl_parts = [f"curl --request {method} '{full_url_preview}'"]
        for hk, hv in headers_preview.items():
            curl_parts.append(f"  --header '{hk}: {hv}'")
        if method in ["POST", "PUT", "PATCH"] and raw_data_input.strip():
            curl_parts.append(f"  --data '{raw_data_input.strip()}'")
        st.code(" \
".join(curl_parts), language="bash")

    with snip_tab2:
        py_code = f"import requests\nimport json\n\nurl = \"{full_url_preview}\"\nheaders = {json.dumps(headers_preview, indent=4)}\n"
        if method in ["POST", "PUT", "PATCH"] and raw_data_input.strip():
            py_code += f"payload = {raw_data_input.strip()}\nresponse = requests.{method.lower()}(url, headers=headers, json=payload)\n"
        else:
            py_code += f"response = requests.{method.lower()}(url, headers=headers)\n"
        py_code += "print(response.status_code)\nprint(response.json())"
        st.code(py_code, language="python")

    if st.button("⚡ 今すぐリクエストを実行する", use_container_width=True, type="primary"):
        payload_to_send = None
        if method in ["POST", "PUT", "PATCH"] and raw_data_input.strip():
            try:
                payload_to_send = json.loads(raw_data_input)
            except Exception as e:
                st.error(f"JSONパースエラー: {str(e)}")

        with st.spinner("API実行中..."):
            try:
                resp = requests.request(
                    method=method,
                    url=full_url_preview,
                    headers=headers_preview,
                    json=payload_to_send if method in ["POST", "PUT", "PATCH"] else None,
                    timeout=30
                )

                st.markdown("---")
                st.markdown("### 📥 実行結果 (Response)")
                
                if 200 <= resp.status_code < 300:
                    st.success(f"Status Code: {resp.status_code} OK")
                else:
                    st.error(f"Status Code: {resp.status_code} Error")

                res_tab1, res_tab2 = st.tabs(["Response Body", "Response Headers"])
                with res_tab1:
                    try:
                        st.json(resp.json())
                    except Exception:
                        st.text(resp.text)
                with res_tab2:
                    st.json(dict(resp.headers))

            except Exception as ex:
                st.error(f"リクエスト送信失敗: {str(ex)}")

    st.markdown('</div>', unsafe_allow_html=True)
