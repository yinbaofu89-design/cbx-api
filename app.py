import streamlit as st
import requests
import json
import base64

st.set_page_config(
    page_title="CBX API Master Commander",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header { font-size: 1.8rem; font-weight: 700; color: #1E293B; margin-bottom: 0.2rem; }
    .sub-header { font-size: 0.9rem; color: #64748B; margin-bottom: 1.5rem; }
    .box-container { background-color: #F8FAFC; padding: 1rem; border-radius: 8px; border: 1px solid #E2E8F0; }
</style>
""", unsafe_allow_html=True)

DEFAULT_TOKEN = "TzJJRC5Xdm0xTDlUQVJ3T1pXVHpFQkJqVzB3LmY2RzhyOXhIU1Zpc3dHTUhDZF9mTVEuNWttZXFwcWw1NGFmM3JxdjZrazRiZ2gyYzA6MWU5OWhvMGNnbDdiYzBia2xuaGViaTZuZGg4dmR1dmcyaTBy"

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

st.sidebar.title("⚡ CBX Control Panel")
st.sidebar.markdown("---")

api_token = st.sidebar.text_input(
    "OAuth Bearer / Basic Token",
    value=DEFAULT_TOKEN,
    type="password"
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
    st.session_state["exec_payload"] = json.dumps({}, indent=2)

st.markdown('<div class="main-header">⚡ CBX API Master Commander</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">すべてのAPI・全エンドポイント対応。テンプレートから実行ボックスへのデータ転送機能付き。</div>', unsafe_allow_html=True)

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

        # NOTE: Automatic customer_id and domain_id injection has been removed per request.

    with col_in2:
        st.markdown("**生成されるプレビュー (URL / データ):**")
        preview_text = f"Endpoint: {t_endpoint}
Method: {t_method}
Data:
{json.dumps(t_data, indent=2)}"
        st.code(preview_text, language="json")
        
        if st.button("📥 実行ボックスにこの設定を転送する", use_container_width=True, type="primary"):
            st.session_state["exec_method"] = t_method
            st.session_state["exec_endpoint"] = t_endpoint
            st.session_state["exec_payload"] = json.dumps(t_data, indent=2)
            st.rerun()

st.markdown("---")

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
        py_code = f"import requests
import json

url = "{full_url_preview}"
headers = {json.dumps(headers_preview, indent=4)}
"
        if method in ["POST", "PUT", "PATCH"] and raw_data_input.strip():
            py_code += f"payload = {raw_data_input.strip()}
response = requests.{method.lower()}(url, headers=headers, json=payload)
"
        else:
            py_code += f"response = requests.{method.lower()}(url, headers=headers)
"
        py_code += "print(response.status_code)
print(response.json())"
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
