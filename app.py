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

# Initialize execution state
if "exec_method" not in st.session_state:
    st.session_state["exec_method"] = "POST"
if "exec_endpoint" not in st.session_state:
    st.session_state["exec_endpoint"] = "/endpoint-security/vulnerability/assessment/v3/vulnerabilities/summary"
if "exec_payload" not in st.session_state:
    st.session_state["exec_payload"] = json.dumps({"customer_id": c_id or "", "domain_id": d_id or ""}, indent=2)

# Header
st.markdown('<div class="main-header">⚡ CBX API Master Commander</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">すべてのAPI・全エンドポイント対応。テンプレートから実行ボックスへのデータ転送機能付き。</div>', unsafe_allow_html=True)

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
    st.subheader(f"📝 テンプレート設定: {module_choice}")
    
    t_method = "GET"
    t_endpoint = ""
    t_data = {}

    col_in1, col_in2 = st.columns([1, 1])

    with col_in1:
        if "Authentication" in module_choice:
            op = st.selectbox("Endpoint", ["POST /common/v1/oauth2/tokens"])
            t_method, t_endpoint = op.split(" ", 1)
            grant_type = st.text_input("grant_type", value="client_credentials")
            scope = st.text_input("scope", value="domain")
            t_data = {"grant_type": grant_type, "scope": scope}

        elif "Custom Detections" in module_choice:
            op = st.selectbox("Endpoint", [
                "POST /detect-respond/detection/v1/custom-detections/_search",
                "POST /detect-respond/detection/v1/custom-detections",
                "GET /detect-respond/detection/v1/custom-detections/{detection_id}",
                "PUT /detect-respond/detection/v1/custom-detections/{detection_id}",
                "DELETE /detect-respond/detection/v1/custom-detections/{detection_id}",
                "POST /detect-respond/detection/v1/custom-detections/queries/_search"
            ])
            t_method, t_endpoint = op.split(" ", 1)
            if "{detection_id}" in t_endpoint:
                det_id = st.text_input("detection_id", value="det-123")
                t_endpoint = t_endpoint.replace("{detection_id}", det_id)

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
                "GET /detect-respond/device-query/v2/commands/{commandId}"
            ])
            t_method, t_endpoint = op.split(" ", 1)
            if "{commandId}" in t_endpoint:
                cid = st.text_input("commandId", value="cmd-123")
                t_endpoint = t_endpoint.replace("{commandId}", cid)

            if t_method == "POST" and "commands" in t_endpoint:
                cmd_type = st.selectbox("command_type", ["forensic", "artifact"])
                scope = st.selectbox("scope", ["all", "device_ids"])
                query_str = st.text_area("query", value="SELECT * FROM processes;")
                t_data = {"command_type": cmd_type, "scope": scope, "query": query_str}

        elif "Alerts & Threats" in module_choice:
            op = st.selectbox("Endpoint", [
                "POST /detect-respond/alerts/v8/alerts/_search",
                "GET /detect-respond/alerts/v8/alerts/{alert_id}",
                "POST /detect-respond/alerts/v8/alerts/workflow"
            ])
            t_method, t_endpoint = op.split(" ", 1)
            if "{alert_id}" in t_endpoint:
                aid = st.text_input("alert_id", value="alt-123")
                t_endpoint = t_endpoint.replace("{alert_id}", aid)
            if "_search" in t_endpoint:
                rows = st.number_input("rows", value=10, min_value=1)
                t_data = {"criteria": {}, "rows": rows}
            elif "workflow" in t_endpoint:
                status = st.selectbox("status", ["RESOLVED", "CLOSED"])
                t_data = {"status": status, "determination": "TRUE_POSITIVE"}

        elif "Jobs & Export" in module_choice:
            op = st.selectbox("Endpoint", [
                "POST /detect-respond/jobs/v4/event_export",
                "GET /detect-respond/jobs/v4/jobs/{job_id}"
            ])
            t_method, t_endpoint = op.split(" ", 1)
            if "{job_id}" in t_endpoint:
                jid = st.text_input("job_id", value="job-123")
                t_endpoint = t_endpoint.replace("{job_id}", jid)
            if t_method == "POST":
                q = st.text_input("query", value="process_name: powershell.exe")
                t_data = {"query": q, "time_range": "1h"}

        elif "Live Response" in module_choice:
            op = st.selectbox("Endpoint", [
                "GET /detect-respond/live-response/v7/sessions",
                "POST /detect-respond/live-response/v7/sessions"
            ])
            t_method, t_endpoint = op.split(" ", 1)
            if t_method == "POST":
                dev_id = st.text_input("device_id", value="device-001")
                t_data = {"device_id": dev_id}

        elif "Notifications" in module_choice:
            op = st.selectbox("Endpoint", [
                "GET /detect-respond/notifications/v2/rules",
                "POST /detect-respond/notifications/v2/rules"
            ])
            t_method, t_endpoint = op.split(" ", 1)
            if t_method == "POST":
                r_name = st.text_input("Rule Name", value="Alert Rule")
                t_data = {"name": r_name, "enabled": True}

        elif "Policy Management" in module_choice:
            op = st.selectbox("Endpoint", [
                "GET /common/policy-management/v2/policies",
                "POST /common/policy-management/v2/policies/export/all"
            ])
            t_method, t_endpoint = op.split(" ", 1)
            t_data = {}

        elif "Script Deobfuscation" in module_choice:
            op = st.selectbox("Endpoint", ["POST /detect-respond/script-deobfuscation/v3/reveal"])
            t_method, t_endpoint = op.split(" ", 1)
            script_b64 = st.text_area("Script / Base64", value="powershell.exe -e aQBm...")
            t_data = {"script": script_b64}

        elif "Threat Intel" in module_choice:
            op = st.selectbox("Endpoint", ["POST /common/threat-intel/v1/taxii11/discovery"])
            t_method, t_endpoint = op.split(" ", 1)
            t_data = {}

        elif "Vulnerability Assessment" in module_choice:
            op = st.selectbox("Endpoint", [
                "GET /endpoint-security/vulnerability/assessment/v3/vulnerabilities/summary",
                "POST /endpoint-security/vulnerability/assessment/v3/devices/vulnerabilities/_search"
            ])
            t_method, t_endpoint = op.split(" ", 1)
            if "_search" in t_endpoint:
                t_data = {"rows": 10, "start": 0}

        # Auto inject customer_id & domain_id if POST/PUT/PATCH
        if t_method in ["POST", "PUT", "PATCH"] and isinstance(t_data, dict):
            if c_id and "customer_id" not in t_data: t_data["customer_id"] = c_id
            if d_id and "domain_id" not in t_data: t_data["domain_id"] = d_id

    with col_in2:
        st.markdown("**生成されるプレビュー (URL / データ):**")
        preview_text = f"Endpoint: {t_endpoint}\nMethod: {t_method}\nData:\n{json.dumps(t_data, indent=2)}"
        st.code(preview_text, language="json")
        
        # 転送ボタンのクリック処理 (st.rerun() で確実に反映)
        if st.button("📥 実行ボックスにこの設定を転送する", use_container_width=True, type="primary"):
            st.session_state["exec_method"] = t_method
            st.session_state["exec_endpoint"] = t_endpoint
            st.session_state["exec_payload"] = json.dumps(t_data, indent=2)
            st.rerun()

st.markdown("---")

# --- ALWAYS VISIBLE EXECUTION BOX (NO KEYS TO AVOID STATE CONFLICTS) ---
st.markdown("## 🚀 共通実行ボックス (Execution Box)")
st.markdown("下部のボックスでURLやリクエストデータを直接編集し、**cURL** や **Pythonコード** を確認しながら実行できます。")

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
        raw_data_input = st.text_area("JSON Raw Data", value=st.session_state["exec_payload"], height=160)

    # Code Snippets generation tab
    st.markdown("#### 💻 リクエストコード生成 (cURL & Python)")
    snip_tab1, snip_tab2 = st.tabs(["cURL Command", "Python Code Snippet"])
    
    with snip_tab1:
        curl_parts = [f"curl --request {method} '{full_url_preview}'"]
        for hk, hv in headers_preview.items():
            curl_parts.append(f"  --header '{hk}: {hv}'")
        if method in ["POST", "PUT", "PATCH"] and raw_data_input.strip():
            curl_parts.append(f"  --data '{raw_data_input.strip()}'")
        st.code(" \\\n".join(curl_parts), language="bash")

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
