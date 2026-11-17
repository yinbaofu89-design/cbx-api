import streamlit as st
import requests
import json
import base64

# Streamlit Page Config
st.set_page_config(
    page_title="CBX API Minimal Commander",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for clean UI
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

# --- SIDEBAR: GLOBAL TOKEN & CONFIG ---
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

# Initialize session state for execution box if not present
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
st.markdown('<div class="main-header">⚡ CBX API Minimal Commander</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">すべてのAPIカテゴリ・メソッドを網羅し、テンプレートから実行ボックスへ即時転送できるプロフェッショナルツール</div>', unsafe_allow_html=True)

# --- CATEGORY SELECTION COVERING ALL APIS ---
cat = st.selectbox(
    "📁 APIカテゴリを選択してすべての機能・メソッドにアクセス",
    [
        "🔑 Authentication (OAuth Tokens)",
        "🎯 Custom Detections (Search / CRUD / Bulk)",
        "💻 Device Query (Commands / Schedules)",
        "🚨 Alerts & Threats (Search / Notes / Workflow)",
        "⚙️ Jobs & Export (Event Export / Download)",
        "🔌 Live Response (Sessions / Files / Commands)",
        "🔔 Notifications (Rules / History)",
        "📜 Policy Management (Policies / Allow-Deny / Import-Export)",
        "🔓 Script Deobfuscation (Reveal)",
        "🌐 Threat Intel (TAXII 1.1 Discovery & Poll)",
        "🛡️ Vulnerability Assessment (Org & Device Summaries / CVEs)"
    ]
)

st.markdown("---")

# Template Generator covering all endpoints & methods
with st.container():
    st.subheader(f"📝 テンプレート設定: {cat}")
    
    t_method = "POST"
    t_endpoint = ""
    t_data = {}

    col_in1, col_in2 = st.columns([1, 1])

    with col_in1:
        if "Authentication" in cat:
            sub_op = st.selectbox("Operation", ["Get Bearer Token"])
            t_method = "POST"
            t_endpoint = "/common/v1/oauth2/tokens"
            t_data = {"grant_type": "client_credentials", "scope": "domain"}
            
        elif "Custom Detections" in cat:
            sub_op = st.selectbox("Operation", [
                "Search Custom Detections (_search)",
                "Create Custom Detection",
                "Get Custom Detection",
                "Update Custom Detection",
                "Delete Custom Detection",
                "Search Query Sub-resources (queries/_search)",
                "Create Query Sub-resource"
            ])
            if "Search Custom Detections" in sub_op:
                t_method = "POST"
                t_endpoint = "/detect-respond/detection/v1/custom-detections/_search"
                t_data = {"page": 1, "size": 10}
            elif "Create Custom Detection" in sub_op:
                t_method = "POST"
                t_endpoint = "/detect-respond/detection/v1/custom-detections"
                t_data = {"name": "Sample Detection", "description": "Description here", "enabled": True}
            elif "Get Custom Detection" in sub_op:
                t_method = "GET"
                det_id = st.text_input("Detection ID", value="det-123")
                t_endpoint = f"/detect-respond/detection/v1/custom-detections/{det_id}"
                t_data = {}
            elif "Update Custom Detection" in sub_op:
                t_method = "PUT"
                det_id = st.text_input("Detection ID", value="det-123")
                t_endpoint = f"/detect-respond/detection/v1/custom-detections/{det_id}"
                t_data = {"name": "Updated Name", "enabled": True}
            elif "Delete Custom Detection" in sub_op:
                t_method = "DELETE"
                det_id = st.text_input("Detection ID", value="det-123")
                t_endpoint = f"/detect-respond/detection/v1/custom-detections/{det_id}"
                t_data = {}
            elif "Search Query Sub-resources" in sub_op:
                t_method = "POST"
                t_endpoint = "/detect-respond/detection/v1/custom-detections/queries/_search"
                t_data = {"criteria": {"query": "cmd.exe"}}
            elif "Create Query Sub-resource" in sub_op:
                t_method = "POST"
                det_id = st.text_input("Detection ID", value="det-123")
                t_endpoint = f"/detect-respond/detection/v1/custom-detections/{det_id}/queries"
                t_data = {"query": "process_name: calc.exe", "severity": 5}

        elif "Device Query" in cat:
            sub_op = st.selectbox("Operation", [
                "Trigger Device Query (POST /commands)",
                "List Commands (GET /commands)",
                "Get Command By Id",
                "Cancel Command",
                "List Schedules",
                "Create Schedule"
            ])
            if "Trigger Device Query" in sub_op:
                t_method = "POST"
                t_endpoint = "/detect-respond/device-query/v2/commands"
                cmd_type = st.selectbox("Command Type", ["forensic", "artifact"])
                scope = st.selectbox("Scope", ["all", "device_ids"])
                q = st.text_area("Query", value="SELECT * FROM processes;")
                t_data = {"command_type": cmd_type, "scope": scope, "query": q, "device_ids": ["dev-001"]}
            elif "List Commands" in sub_op:
                t_method = "GET"
                t_endpoint = "/detect-respond/device-query/v2/commands"
                t_data = {}
            elif "Get Command By Id" in sub_op:
                t_method = "GET"
                cid = st.text_input("Command ID", value="cmd-123")
                t_endpoint = f"/detect-respond/device-query/v2/commands/{cid}"
                t_data = {}
            elif "Cancel Command" in sub_op:
                t_method = "PUT"
                cid = st.text_input("Command ID", value="cmd-123")
                t_endpoint = f"/detect-respond/device-query/v2/commands/{cid}/cancel"
                t_data = {}
            elif "List Schedules" in sub_op:
                t_method = "GET"
                t_endpoint = "/detect-respond/device-query/v2/schedules"
                t_data = {}
            elif "Create Schedule" in sub_op:
                t_method = "POST"
                t_endpoint = "/detect-respond/device-query/v2/schedules"
                t_data = {"name": "Daily Query", "query": "SELECT * FROM services;", "command_type": "forensic"}

        elif "Alerts & Threats" in cat:
            sub_op = st.selectbox("Operation", [
                "Find Ungrouped Alerts (_search)",
                "Get Alert By ID",
                "Export Alerts (_export)",
                "Find Grouped Alerts (_search)",
                "Update Alerts Workflow"
            ])
            if "Find Ungrouped Alerts" in sub_op:
                t_method = "POST"
                t_endpoint = "/detect-respond/alerts/v8/alerts/_search"
                t_data = {"criteria": {}, "rows": 10, "start": 0}
            elif "Get Alert By ID" in sub_op:
                t_method = "GET"
                aid = st.text_input("Alert ID", value="alt-123")
                t_endpoint = f"/detect-respond/alerts/v8/alerts/{aid}"
                t_data = {}
            elif "Export Alerts" in sub_op:
                t_method = "POST"
                t_endpoint = "/detect-respond/alerts/v8/alerts/_export"
                t_data = {"criteria": {}}
            elif "Find Grouped Alerts" in sub_op:
                t_method = "POST"
                t_endpoint = "/detect-respond/alerts/v8/grouped_alerts/_search"
                t_data = {"group_by": "threat_id", "rows": 10}
            elif "Update Alerts Workflow" in sub_op:
                t_method = "POST"
                t_endpoint = "/detect-respond/alerts/v8/alerts/workflow"
                t_data = {"status": "RESOLVED", "determination": "TRUE_POSITIVE"}

        elif "Jobs & Export" in cat:
            sub_op = st.selectbox("Operation", [
                "Start Event Export",
                "Get Job Details",
                "Download Job Output File"
            ])
            if "Start Event Export" in sub_op:
                t_method = "POST"
                t_endpoint = "/detect-respond/jobs/v4/event_export"
                t_data = {"query": "process_name: powershell.exe", "time_range": "1h"}
            elif "Get Job Details" in sub_op:
                t_method = "GET"
                jid = st.text_input("Job ID", value="job-123")
                t_endpoint = f"/detect-respond/jobs/v4/jobs/{jid}"
                t_data = {}
            elif "Download Job Output" in sub_op:
                t_method = "GET"
                jid = st.text_input("Job ID", value="job-123")
                t_endpoint = f"/detect-respond/jobs/v4/jobs/{jid}/download"
                t_data = {}

        elif "Live Response" in cat:
            sub_op = st.selectbox("Operation", [
                "Get All Sessions",
                "Create Session",
                "Close Session",
                "Queue Command"
            ])
            if "Get All Sessions" in sub_op:
                t_method = "GET"
                t_endpoint = "/detect-respond/live-response/v7/sessions"
                t_data = {}
            elif "Create Session" in sub_op:
                t_method = "POST"
                t_endpoint = "/detect-respond/live-response/v7/sessions"
                t_data = {"device_id": "device-001"}
            elif "Close Session" in sub_op:
                t_method = "DELETE"
                sid = st.text_input("Session ID", value="sess-123")
                t_endpoint = f"/detect-respond/live-response/v7/sessions/{sid}"
                t_data = {}
            elif "Queue Command" in sub_op:
                t_method = "POST"
                sid = st.text_input("Session ID", value="sess-123")
                t_endpoint = f"/detect-respond/live-response/v7/sessions/{sid}/commands"
                t_data = {"command": "processes"}

        elif "Notifications" in cat:
            sub_op = st.selectbox("Operation", ["Fetch Notification Rules", "Create Notification Rule", "Search History"])
            if "Fetch Notification Rules" in sub_op:
                t_method = "GET"
                t_endpoint = "/detect-respond/notifications/v2/rules"
                t_data = {}
            elif "Create Notification Rule" in sub_op:
                t_method = "POST"
                t_endpoint = "/detect-respond/notifications/v2/rules"
                t_data = {"name": "High Severity Alert Rule", "enabled": True}
            elif "Search History" in sub_op:
                t_method = "POST"
                t_endpoint = "/detect-respond/notifications/v2/history/_search"
                t_data = {}

        elif "Policy Management" in cat:
            sub_op = st.selectbox("Operation", ["List Policies", "Create Policy", "Export All Policies"])
            if "List Policies" in sub_op:
                t_method = "GET"
                t_endpoint = "/common/policy-management/v2/policies"
                t_data = {}
            elif "Create Policy" in sub_op:
                t_method = "POST"
                t_endpoint = "/common/policy-management/v2/policies"
                t_data = {"name": "Firewall Policy 1", "type": "Firewall"}
            elif "Export All Policies" in sub_op:
                t_method = "POST"
                t_endpoint = "/common/policy-management/v2/policies/export/all"
                t_data = {}

        elif "Script Deobfuscation" in cat:
            sub_op = st.selectbox("Operation", ["Deobfuscate Script"])
            t_method = "POST"
            t_endpoint = "/detect-respond/script-deobfuscation/v3/reveal"
            t_data = {"script": "powershell.exe -e aQBm..."}

        elif "Threat Intel" in cat:
            sub_op = st.selectbox("Operation", ["TAXII Discovery", "List Collections", "TAXII Poll"])
            if "TAXII Discovery" in sub_op:
                t_method = "POST"
                t_endpoint = "/common/threat-intel/v1/taxii11/discovery"
                t_data = {}
            elif "List Collections" in sub_op:
                t_method = "POST"
                t_endpoint = "/common/threat-intel/v1/taxii11/collection-management"
                t_data = {}
            elif "TAXII Poll" in sub_op:
                t_method = "POST"
                t_endpoint = "/common/threat-intel/v1/taxii11/poll"
                t_data = {"collection_name": "threat-alerts"}

        elif "Vulnerability Assessment" in cat:
            sub_op = st.selectbox("Operation", [
                "Get Org Vulnerability Summary",
                "Search Vulnerable Devices",
                "Search Organization Vulnerabilities",
                "Get Vulnerability Details"
            ])
            if "Get Org Vulnerability Summary" in sub_op:
                t_method = "GET"
                t_endpoint = "/endpoint-security/vulnerability/assessment/v3/vulnerabilities/summary"
                t_data = {}
            elif "Search Vulnerable Devices" in sub_op:
                t_method = "POST"
                t_endpoint = "/endpoint-security/vulnerability/assessment/v3/devices/vulnerabilities/summary/_search"
                t_data = {"rows": 10, "start": 0}
            elif "Search Organization Vulnerabilities" in sub_op:
                t_method = "POST"
                t_endpoint = "/endpoint-security/vulnerability/assessment/v3/devices/vulnerabilities/_search"
                t_data = {"rows": 10, "start": 0}
            elif "Get Vulnerability Details" in sub_op:
                t_method = "GET"
                cve = st.text_input("CVE ID", value="CVE-2023-1234")
                t_endpoint = f"/endpoint-security/vulnerability/assessment/v3/vulnerabilities/{cve}"
                t_data = {}

        # Automatically inject customer_id and domain_id if available & POST/PUT/PATCH
        if t_method in ["POST", "PUT", "PATCH"] and isinstance(t_data, dict):
            if c_id and "customer_id" not in t_data: t_data["customer_id"] = c_id
            if d_id and "domain_id" not in t_data: t_data["domain_id"] = d_id

    with col_in2:
        st.markdown("**生成されるプレビュー (Rawデータ / URL):**")
        preview_text = f"Endpoint: {t_endpoint}\nMethod: {t_method}\nData:\n{json.dumps(t_data, indent=2)}"
        st.code(preview_text, language="json")
        
        if st.button("📥 このコマンドとデータを下の実行ボックスに移す", use_container_width=True, type="primary"):
            st.session_state["exec_method"] = t_method
            st.session_state["exec_endpoint"] = t_endpoint
            st.session_state["exec_payload"] = json.dumps(t_data, indent=2)
            st.success("実行ボックスに転送しました！下へスクロールしてください。")

st.markdown("---")

# --- ALWAYS VISIBLE EXECUTION BOX (SIDE-BY-SIDE LAYOUT) ---
st.markdown("## 🚀 共通実行ボックス (Execution Box)")
st.markdown("どのカテゴリ・どのメソッドを選択しても、ここにURLやリクエストデータが保持され、横並びで自由に編集・実行できます。")

with st.container():
    st.markdown('<div class="box-container">', unsafe_allow_html=True)
    
    ex_col1, ex_col2 = st.columns([1, 3])
    with ex_col1:
        methods_list = ["GET", "POST", "PUT", "DELETE", "PATCH"]
        curr_m = st.session_state["exec_method"]
        m_index = methods_list.index(curr_m) if curr_m in methods_list else 0
        method = st.selectbox("Method", methods_list, index=m_index)
    with ex_col2:
        endpoint = st.text_input("Endpoint Path / URL", value=st.session_state["exec_endpoint"])

    exec_col_left, exec_col_right = st.columns([1, 1])

    with exec_col_left:
        st.markdown("#### 🔗 URL / Endpoint")
        full_url_preview = f"{server_url.rstrip('/')}{endpoint}"
        st.code(full_url_preview, language="text")
        
        st.markdown("#### 🔑 Request Headers")
        headers_preview = {
            "Authorization": f"Bearer {api_token}" if not api_token.startswith("Basic ") else api_token,
            "content-type": "application/json"
        }
        st.json(headers_preview)

    with exec_col_right:
        st.markdown("#### 📦 Request Data (JSON Raw)")
        raw_data_input = st.text_area("JSON Payload", value=st.session_state["exec_payload"], height=160)

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
                st.markdown("### 📥 実行結果 (Response & cURL)")
                
                if 200 <= resp.status_code < 300:
                    st.success(f"Status Code: {resp.status_code} OK")
                else:
                    st.error(f"Status Code: {resp.status_code} Error")

                res_tab1, res_tab2, res_tab3 = st.tabs(["Response Body", "Response Headers", "Actual cURL"])
                
                with res_tab1:
                    try:
                        st.json(resp.json())
                    except Exception:
                        st.text(resp.text)
                        
                with res_tab2:
                    st.json(dict(resp.headers))
                    
                with res_tab3:
                    curl_gen = [f"curl --request {method} '{full_url_preview}'"]
                    for hk, hv in headers_preview.items():
                        curl_gen.append(f"  --header '{hk}: {hv}'")
                    if payload_to_send:
                        curl_gen.append(f"  --data '{json.dumps(payload_to_send)}'")
                    st.code(" \\\n".join(curl_gen), language="bash")

            except Exception as ex:
                st.error(f"リクエスト送信失敗: {str(ex)}")

    st.markdown('</div>', unsafe_allow_html=True)
