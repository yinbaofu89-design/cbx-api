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
st.markdown('<div class="sub-header">すべてのAPIカテゴリ（脆弱性評価を含む）に対応し、テンプレートから実行ボックスへ即時転送できるシンプルツール</div>', unsafe_allow_html=True)

# --- CATEGORY TABS FOR INPUT GENERATION ---
cat = st.selectbox(
    "📁 APIカテゴリを選択してテンプレート項目を表示",
    [
        "🎯 Custom Detections (Search)",
        "💻 Device Query (Trigger)",
        "⚙️ Jobs (Event Export)",
        "🔌 Live Response (Create Session)",
        "🔔 Notifications (Rules)",
        "📜 Policy Management (List)",
        "🔓 Script Deobfuscation (Reveal)",
        "🌐 Threat Intel (TAXII Discovery)",
        "🛡️ Vulnerability Assessment (Org Summary)"
    ]
)

st.markdown("---")

# Template Generator based on Selection
with st.container():
    st.subheader(f"📝 テンプレート設定: {cat}")
    
    t_method = "POST"
    t_endpoint = ""
    t_data = {}

    col_in1, col_in2 = st.columns([1, 1])

    with col_in1:
        if "Custom Detections" in cat:
            t_endpoint = "/detect-respond/detection/v1/custom-detections/_search"
            page = st.number_input("Page", value=1, min_value=1)
            size = st.number_input("Size", value=10, min_value=1)
            t_data = {"page": page, "size": size}
        elif "Device Query" in cat:
            t_endpoint = "/detect-respond/device-query/v2/commands"
            cmd_type = st.selectbox("Command Type", ["forensic", "artifact"])
            scope = st.selectbox("Scope", ["all", "device_ids"])
            query_str = st.text_area("Query", value="SELECT * FROM processes WHERE name = 'powershell.exe';")
            t_data = {"command_type": cmd_type, "scope": scope, "query": query_str}
        elif "Jobs" in cat:
            t_endpoint = "/detect-respond/jobs/v4/event_export"
            q = st.text_input("Threat Hunter Query", value="process_name: powershell.exe")
            time_range = st.selectbox("Time Range", ["1h", "24h", "7d"])
            t_data = {"query": q, "time_range": time_range}
        elif "Live Response" in cat:
            t_endpoint = "/detect-respond/live-response/v7/sessions"
            dev_id = st.text_input("Device ID", value="device-001")
            t_data = {"device_id": dev_id}
        elif "Notifications" in cat:
            t_method = "GET"
            t_endpoint = "/detect-respond/notifications/v2/rules"
            t_data = {}
        elif "Policy Management" in cat:
            t_method = "GET"
            t_endpoint = "/common/policy-management/v2/policies"
            t_data = {}
        elif "Script Deobfuscation" in cat:
            t_endpoint = "/detect-respond/script-deobfuscation/v3/reveal"
            script = st.text_area("Script / Base64", value="powershell.exe -e aQBm...")
            t_data = {"script": script}
        elif "Threat Intel" in cat:
            t_endpoint = "/common/threat-intel/v1/taxii11/discovery"
            t_data = {}
        elif "Vulnerability Assessment" in cat:
            t_method = "GET"
            t_endpoint = "/endpoint-security/vulnerability/assessment/v3/vulnerabilities/summary"
            t_data = {}

        # Automatically inject customer_id and domain_id if available & POST/PUT
        if t_method in ["POST", "PUT", "PATCH"] and isinstance(t_data, dict):
            if c_id: t_data["customer_id"] = c_id
            if d_id: t_data["domain_id"] = d_id

    with col_in2:
        st.markdown("**生成されるプレビュー (Rawデータ / URL):**")
        st.code(f"Endpoint: {t_endpoint}
Method: {t_method}
Data:
{json.dumps(t_data, indent=2)}", language="json")
        
        if st.button("📥 このコマンドとデータを下の実行ボックスに移す", use_container_width=True, type="primary"):
            st.session_state["exec_method"] = t_method
            st.session_state["exec_endpoint"] = t_endpoint
            st.session_state["exec_payload"] = json.dumps(t_data, indent=2)
            st.success("実行ボックスに転送しました！下へスクロールしてください。")

st.markdown("---")

# --- ALWAYS VISIBLE EXECUTION BOX (SIDE-BY-SIDE LAYOUT) ---
st.markdown("## 🚀 共通実行ボックス (Execution Box)")
st.markdown("どのカテゴリを選択しても、常にここにURLやリクエストデータが保持され、横並びで自由に編集・実行できます。")

with st.container():
    st.markdown('<div class="box-container">', unsafe_allow_html=True)
    
    ex_col1, ex_col2 = st.columns([1, 3])
    with ex_col1:
        method = st.selectbox("Method", ["GET", "POST", "PUT", "DELETE", "PATCH"], index=["GET", "POST", "PUT", "DELETE", "PATCH"].index(st.session_state["exec_method"]))
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
                    st.code(" \
".join(curl_gen), language="bash")

            except Exception as ex:
                st.error(f"リクエスト送信失敗: {str(ex)}")

    st.markdown('</div>', unsafe_allow_html=True)
