import streamlit as st
import requests
import json
import base64

# Streamlit Page Config
st.set_page_config(
    page_title="CBX API Professional Console",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #64748B;
        margin-bottom: 2rem;
    }
    .help-box {
        background-color: #EFF6FF;
        border-left: 4px solid #3B82F6;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        font-size: 0.9rem;
        color: #1E3A8A;
    }
</style>
""", unsafe_allow_html=True)

# Default Authorization Token
DEFAULT_TOKEN = "TzJJRC5Xdm0xTDlUQVJ3T1pXVHpFQkJqVzB3LmY2RzhyOXhIU1Zpc3dHTUhDZF9mTVEuNWttZXFwcWw1NGFmM3JxdjZrazRiZ2gyYzA6MWU5OWhvMGNnbDdiYzBia2xuaGViaTZuZGg4dmR1dmcyaTBy"

# Helper function to extract customer_id and domain_id from JWT Token automatically
def extract_jwt_claims(token_str):
    """Bearer JWTトークンから customer_id と domain_id を自動解析・抽出する関数"""
    if not token_str:
        return None, None
    clean_token = token_str.replace("Bearer ", "").strip()
    parts = clean_token.split(".")
    if len(parts) == 3:
        try:
            # Base64パディング補正
            payload_b64 = parts[1]
            payload_b64 += "=" * ((4 - len(payload_b64) % 4) % 4)
            decoded_bytes = base64.b64decode(payload_b64)
            payload_json = json.loads(decoded_bytes.decode("utf-8"))
            
            c_id = payload_json.get("customer_id")
            d_id = payload_json.get("domain_id")
            return c_id, d_id
        except Exception:
            pass
    return None, None

# Sidebar Configuration
st.sidebar.title("🛡️ CBX Control Panel")
st.sidebar.markdown("---")
st.sidebar.subheader("🔑 Authentication & Server Settings")

api_token = st.sidebar.text_input(
    "OAuth Basic Token / Bearer Token",
    value=DEFAULT_TOKEN,
    type="password",
    help="OAuth 認証トークンを設定します。Bearer トークンの場合、含まれる customer_id / domain_id は自動抽出されます。"
)

server_url = st.sidebar.selectbox(
    "Server Base URL",
    ["https://api.us.security.com"],
    help="CBX APIのベースURLを選択します。"
)

# JWTの自動解析処理
extracted_c_id, extracted_d_id = extract_jwt_claims(api_token)

st.sidebar.markdown("---")
st.sidebar.subheader("🏢 Auto-Detected Context")
if extracted_c_id or extracted_d_id:
    st.sidebar.success(f"**Customer ID:** `{extracted_c_id}`\n\n**Domain ID:** `{extracted_d_id}`")
else:
    st.sidebar.warning("⚠️ Bearer Token 未設定（Basic認証値または未設定の状態）")

st.sidebar.markdown("---")
st.sidebar.info("""
💡 **自動補正機能**
Bearer トークンが設定されている場合、トークンから `customer_id` と `domain_id` を自動抽出し、APIリクエストのペイロード（Data）へ自動適用します。
""")

st.session_state["cbx_token"] = api_token if api_token else DEFAULT_TOKEN

# API Request Dispatcher
def make_api_request(method, endpoint, headers=None, data=None, json_payload=None, params=None):
    full_url = f"{server_url.rstrip('/')}{endpoint}"
    
    # Headers Setup
    req_headers = {}
    if headers:
        req_headers.update(headers)
    
    if "authorization" not in [k.lower() for k in req_headers.keys()]:
        token_val = st.session_state["cbx_token"]
        if token_val.startswith("Bearer ") or token_val.startswith("Basic "):
            req_headers["Authorization"] = token_val
        else:
            req_headers["Authorization"] = f"Bearer {token_val}"

    # Auto-inject customer_id & domain_id into request data/json_payload from Token
    c_id, d_id = extract_jwt_claims(st.session_state["cbx_token"])

    if json_payload is not None and isinstance(json_payload, dict):
        if c_id and "customer_id" not in json_payload:
            json_payload["customer_id"] = c_id
        if d_id and "domain_id" not in json_payload:
            json_payload["domain_id"] = d_id
    elif method.upper() in ["POST", "PUT", "PATCH"]:
        if data is not None and isinstance(data, dict):
            if c_id and "customer_id" not in data:
                data["customer_id"] = c_id
            if d_id and "domain_id" not in data:
                data["domain_id"] = d_id
        elif json_payload is None and data is None:
            new_payload = {}
            if c_id:
                new_payload["customer_id"] = c_id
            if d_id:
                new_payload["domain_id"] = d_id
            if new_payload:
                json_payload = new_payload
                if "content-type" not in [k.lower() for k in req_headers.keys()]:
                    req_headers["content-type"] = "application/json"

    # Request Code Generation (cURL / Python)
    st.markdown("### 📤 API Request Visualization")
    req_tab1, req_tab2, req_tab3 = st.tabs(["cURL Command", "HTTP Details", "Python Code Snippet"])
    
    # Build cURL
    curl_parts = [f"curl --request {method.upper()} '{full_url}'"]
    for k, v in req_headers.items():
        curl_parts.append(f"  --header '{k}: {v}'")
    if params:
        param_str = "&".join([f"{k}={v}" for k, v in params.items() if v])
        if param_str:
            curl_parts[0] += f"?{param_str}"
    if json_payload:
        curl_parts.append(f"  --data '{json.dumps(json_payload, indent=2)}'")
    elif data:
        if isinstance(data, dict):
            for k, v in data.items():
                curl_parts.append(f"  --data '{k}={v}'")
        else:
            curl_parts.append(f"  --data '{data}'")
            
    curl_cmd = " \\\n".join(curl_parts)

    with req_tab1:
        st.code(curl_cmd, language="bash")
        
    with req_tab2:
        st.markdown(f"**Method:** `{method.upper()}`")
        st.markdown(f"**URL:** `{full_url}`")
        st.markdown("**Headers:**")
        st.json(req_headers)
        if params:
            st.markdown("**URL Parameters:**")
            st.json(params)
        if json_payload:
            st.markdown("**JSON Body:**")
            st.json(json_payload)
        elif data:
            st.markdown("**Form / Raw Data:**")
            st.code(str(data))

    with req_tab3:
        py_code = f"import requests\n\nurl = \"{full_url}\"\nheaders = {json.dumps(req_headers, indent=4)}\n"
        if json_payload:
            py_code += f"json_data = {json.dumps(json_payload, indent=4)}\n"
            py_code += f"response = requests.{method.lower()}(url, headers=headers, json=json_data)\n"
        elif data:
            py_code += f"data = {json.dumps(data, indent=4) if isinstance(data, dict) else str(data)}\n"
            py_code += f"response = requests.{method.lower()}(url, headers=headers, data=data)\n"
        else:
            py_code += f"response = requests.{method.lower()}(url, headers=headers)\n"
        py_code += "print(response.status_code)\nprint(response.json())"
        st.code(py_code, language="python")

    # Execution & Response Display
    st.markdown("### 📥 API Response")
    with st.spinner("Executing Request..."):
        try:
            resp = requests.request(
                method=method,
                url=full_url,
                headers=req_headers,
                params=params,
                data=data,
                json=json_payload,
                timeout=30
            )
            
            if 200 <= resp.status_code < 300:
                st.success(f"Status Code: {resp.status_code} OK")
            elif resp.status_code == 429:
                st.warning(f"Status Code: {resp.status_code} Too Many Requests (Rate Limit Exceeded)")
            else:
                st.error(f"Status Code: {resp.status_code} Error")

            resp_tab1, resp_tab2 = st.tabs(["Response Body", "Response Headers"])
            with resp_tab1:
                try:
                    st.json(resp.json())
                except Exception:
                    st.text(resp.text)
            with resp_tab2:
                st.json(dict(resp.headers))

        except Exception as e:
            st.error(f"HTTP Request Execution Failed: {str(e)}")

# Header Section
st.markdown('<div class="main-header">🛡️ CBX Security API Professional Workbench</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Symantec / Broadcom CBX APIのテスト・検証・運用を統合管理するプロフェッショナルWebツール</div>', unsafe_allow_html=True)

# Main Navigation
category = st.radio(
    "📁 API Categories",
    [
        "🔑 Authentication (OAuth 2.0)",
        "🎯 Custom Detections",
        "💻 Device Query",
        "⚙️ Jobs & Export",
        "🔌 Live Response",
        "🔔 Notifications",
        "📜 Policy Management",
        "🔓 Script Deobfuscation",
        "🌐 Threat Intel (TAXII 1.1)"
    ],
    horizontal=True
)

st.markdown("---")

# Category 1: Authentication
if category == "🔑 Authentication (OAuth 2.0)":
    st.header("🔑 Authentication APIs")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Get Bearer Token (`POST /common/v1/oauth2/tokens`)")
        st.markdown("OAuth Client Credentials (Basic Auth Token) を使って1時間有効な Bearer Token を発行します。")
        grant_type = st.text_input("Grant Type", value="client_credentials", key="auth_grant")
        scope = st.text_input("Scope", value="domain", key="auth_scope")
        
        if st.button("🚀 Tokenを発行する", use_container_width=True):
            make_api_request(
                method="POST",
                endpoint="/common/v1/oauth2/tokens",
                headers={
                    "accept": "application/json",
                    "content-type": "application/x-www-form-urlencoded"
                },
                data={
                    "grant_type": grant_type,
                    "scope": scope
                }
            )

    with col2:
        st.markdown("""
        <div class="help-box">
        <h4>📌 認証機能の使い方・ヘルプ</h4>
        <ul>
            <li><b>基本認証:</b> OAuth Client Credentials をサイドバーに設定します。</li>
            <li><b>自動判定:</b> 発行された Bearer トークンをサイドバーにセットすると、トークン内の <code>customer_id</code> / <code>domain_id</code> が自動認識されます。</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

# Category 2: Custom Detections
elif category == "🎯 Custom Detections":
    st.header("🎯 Custom Detections")
    tab_act1, tab_act2, tab_act3 = st.tabs(["Search Custom Detections", "Create Custom Detection", "Search Queries"])
    
    with tab_act1:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("Search Custom Detections")
            page_num = st.number_input("Page Number", value=1, min_value=1)
            page_size = st.number_input("Page Size", value=10, min_value=1, max_value=100)
            
            if st.button("検索実行", key="btn_cd_search", use_container_width=True):
                make_api_request(
                    method="POST",
                    endpoint="/detect-respond/detection/v1/custom-detections/_search",
                    headers={"content-type": "application/json"},
                    json_payload={"page": page_num, "size": page_size}
                )
        with col2:
            st.markdown("""
            <div class="help-box">
            <h4>📌 使い方・ヘルプ: Custom Detection Search</h4>
            <p>組織独自の脅威検知ルール（カスタムデテクション）の一覧を取得します。</p>
            </div>
            """, unsafe_allow_html=True)

    with tab_act2:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("Create Custom Detection")
            cd_name = st.text_input("Detection Name", value="Suspicious Execution Detection")
            cd_desc = st.text_area("Description", value="Detects unusual process execution patterns.")
            cd_alert = st.checkbox("Enable Alerts", value=True)
            
            if st.button("作成実行", key="btn_cd_create", use_container_width=True):
                make_api_request(
                    method="POST",
                    endpoint="/detect-respond/detection/v1/custom-detections",
                    headers={"content-type": "application/json"},
                    json_payload={"name": cd_name, "description": cd_desc, "enabled": cd_alert}
                )
        with col2:
            st.markdown("""
            <div class="help-box">
            <h4>📌 使い方・ヘルプ: Create Custom Detection</h4>
            <p>新しいカスタム検知ルールを作成します。</p>
            </div>
            """, unsafe_allow_html=True)

    with tab_act3:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("Search Query Sub-resources")
            q_search = st.text_input("Search Keyword", value="cmd.exe")
            if st.button("クエリ検索実行", key="btn_q_search", use_container_width=True):
                make_api_request(
                    method="POST",
                    endpoint="/detect-respond/detection/v1/custom-detections/queries/_search",
                    headers={"content-type": "application/json"},
                    json_payload={"query": q_search}
                )
        with col2:
            st.markdown("""
            <div class="help-box">
            <h4>📌 使い方・ヘルプ: Search Queries</h4>
            <p>検知クエリ文字列をグループ横断で検索します。</p>
            </div>
            """, unsafe_allow_html=True)

# Category 3: Device Query
elif category == "💻 Device Query":
    st.header("💻 Device Query")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Trigger Device Query (`POST /commands`)")
        query_type = st.selectbox("Query Type", ["forensic", "artifact"])
        query_cmd = st.text_area("Query / Command", value="SELECT * FROM processes WHERE name = 'powershell.exe';")
        device_ids = st.text_input("Target Device IDs (カンマ区切り)", value="dev-001,dev-002")
        
        if st.button("クエリコマンド実行", key="btn_dq_trigger", use_container_width=True):
            dev_list = [d.strip() for d in device_ids.split(",") if d.strip()]
            make_api_request(
                method="POST",
                endpoint="/detect-respond/device-query/v2/commands",
                headers={"content-type": "application/json"},
                json_payload={
                    "type": query_type,
                    "query": query_cmd,
                    "device_ids": dev_list
                }
            )

    with col2:
        st.markdown("""
        <div class="help-box">
        <h4>📌 使い方・ヘルプ: Device Query</h4>
        <p>エンドポイントに対してリアルタイムにフォレンジック調査クエリを送信します。</p>
        </div>
        """, unsafe_allow_html=True)

# Category 4: Jobs & Export
elif category == "⚙️ Jobs & Export":
    st.header("⚙️ Jobs & Export")
    tab_j1, tab_j2 = st.tabs(["Start Event Export", "Get Job Status & Download"])
    
    with tab_j1:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("Start Event Export Job")
            search_query = st.text_input("Threat Hunter Query", value="process_name: powershell.exe")
            time_range = st.selectbox("Time Range", ["1h", "24h", "7d", "30d"])
            
            if st.button("エクスポートジョブ開始", key="btn_job_start", use_container_width=True):
                make_api_request(
                    method="POST",
                    endpoint="/detect-respond/jobs/v4/event_export",
                    headers={"content-type": "application/json"},
                    json_payload={"query": search_query, "time_range": time_range}
                )
        with col2:
            st.markdown("""
            <div class="help-box">
            <h4>📌 使い方・ヘルプ: Start Event Export</h4>
            <p>大量のイベントデータをバックグラウンド抽出するジョブを発行します。</p>
            </div>
            """, unsafe_allow_html=True)

    with tab_j2:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("Get Job Details / Download")
            job_id = st.text_input("Job ID", value="job-12345678")
            action = st.radio("Action", ["Check Status", "Get Download URL"])
            
            if st.button("実行", key="btn_job_check", use_container_width=True):
                if action == "Check Status":
                    make_api_request(
                        method="GET",
                        endpoint=f"/detect-respond/jobs/v4/jobs/{job_id}"
                    )
                else:
                    make_api_request(
                        method="GET",
                        endpoint=f"/detect-respond/jobs/v4/jobs/{job_id}/download"
                    )
        with col2:
            st.markdown("""
            <div class="help-box">
            <h4>📌 使い方・ヘルプ: Job Status & Download</h4>
            <p>ジョブの完了確認とファイルダウンロードURLの取得を行います。</p>
            </div>
            """, unsafe_allow_html=True)

# Category 5: Live Response
elif category == "🔌 Live Response":
    st.header("🔌 Live Response")
    tab_lr1, tab_lr2 = st.tabs(["Session Management", "Command Execution"])
    
    with tab_lr1:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("Create Live Response Session")
            target_device = st.text_input("Device ID", value="device-998877")
            
            if st.button("セッション接続開始", key="btn_lr_sess", use_container_width=True):
                make_api_request(
                    method="POST",
                    endpoint="/detect-respond/live-response/v7/sessions",
                    headers={"content-type": "application/json"},
                    json_payload={"device_id": target_device}
                )
        with col2:
            st.markdown("""
            <div class="help-box">
            <h4>📌 使い方・ヘルプ: Live Response Session</h4>
            <p>リモート端末と対話型リアルタイムセッションを確立します。</p>
            </div>
            """, unsafe_allow_html=True)

    with tab_lr2:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("Queue Live Response Command")
            sess_id = st.text_input("Session ID", value="sess-001")
            lr_cmd = st.text_input("Command (e.g. exec, dir, processes)", value="processes")
            
            if st.button("コマンド送信", key="btn_lr_cmd", use_container_width=True):
                make_api_request(
                    method="POST",
                    endpoint=f"/detect-respond/live-response/v7/sessions/{sess_id}/commands",
                    headers={"content-type": "application/json"},
                    json_payload={"command": lr_cmd}
                )
        with col2:
            st.markdown("""
            <div class="help-box">
            <h4>📌 使い方・ヘルプ: Live Response Command</h4>
            <p>セッションに対して管理者コマンドを実行します。</p>
            </div>
            """, unsafe_allow_html=True)

# Category 6: Notifications
elif category == "🔔 Notifications":
    st.header("🔔 Notifications")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Fetch Notification Rules")
        if st.button("通知ルール一覧取得", key="btn_notif_rules", use_container_width=True):
            make_api_request(
                method="GET",
                endpoint="/detect-respond/notifications/v2/rules"
            )
            
        st.markdown("---")
        st.subheader("Search Notification History")
        rule_id = st.text_input("Rule ID (optional)", value="")
        if st.button("通知履歴検索", key="btn_notif_hist", use_container_width=True):
            payload = {"rule_id": rule_id} if rule_id else {}
            make_api_request(
                method="POST",
                endpoint="/detect-respond/notifications/v2/history/_search",
                headers={"content-type": "application/json"},
                json_payload=payload
            )

    with col2:
        st.markdown("""
        <div class="help-box">
        <h4>📌 使い方・ヘルプ: Notifications</h4>
        <p>アラート通知ルール管理および履歴の監査を行います。</p>
        </div>
        """, unsafe_allow_html=True)

# Category 7: Policy Management
elif category == "📜 Policy Management":
    st.header("📜 Policy Management")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("List Policies")
        if st.button("ポリシー一覧取得", key="btn_pol_list", use_container_width=True):
            make_api_request(
                method="GET",
                endpoint="/common/policy-management/v2/policies"
            )
            
        st.markdown("---")
        st.subheader("Export All Policies")
        if st.button("全ポリシー エクスポート実行", key="btn_pol_export", use_container_width=True):
            make_api_request(
                method="POST",
                endpoint="/common/policy-management/v2/policies/export/all"
            )

    with col2:
        st.markdown("""
        <div class="help-box">
        <h4>📌 使い方・ヘルプ: Policy Management</h4>
        <p>セキュリティポリシーの参照・一括エクスポートを行えます。</p>
        </div>
        """, unsafe_allow_html=True)

# Category 8: Script Deobfuscation
elif category == "🔓 Script Deobfuscation":
    st.header("🔓 Script Deobfuscation (Reveal API)")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Deobfuscate PowerShell Script")
        obfuscated_code = st.text_area(
            "Obfuscated Script / Command",
            value="powershell.exe -e aQBmACgAJABQAFMAVgBlAHIAcwBpAG8AbgBUAGEAYgBsAGUAKQB7AHcAcgBpAHQAZQAtAGgAbwBzAHQAIgBIAGUAbABsAG8AIgB9AA=="
        )
        
        if st.button("難読化解除を実行", key="btn_deob", use_container_width=True):
            make_api_request(
                method="POST",
                endpoint="/detect-respond/script-deobfuscation/v3/reveal",
                headers={"content-type": "application/json"},
                json_payload={"script": obfuscated_code}
            )

    with col2:
        st.markdown("""
        <div class="help-box">
        <h4>📌 使い方・ヘルプ: Script Deobfuscation</h4>
        <p>難読化・Base64エンコードされたスクリプトをMLベースで解析・解除します。</p>
        </div>
        """, unsafe_allow_html=True)

# Category 9: Threat Intel (TAXII 1.1)
elif category == "🌐 Threat Intel (TAXII 1.1)":
    st.header("🌐 Threat Intel TAXII 1.1")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("TAXII Discovery Service")
        if st.button("TAXII Discovery 実行", key="btn_taxii_disc", use_container_width=True):
            make_api_request(
                method="POST",
                endpoint="/common/threat-intel/v1/taxii11/discovery"
            )
            
        st.markdown("---")
        st.subheader("List TAXII Collections")
        if st.button("コレクション一覧取得", key="btn_taxii_coll", use_container_width=True):
            make_api_request(
                method="POST",
                endpoint="/common/threat-intel/v1/taxii11/collection-management"
            )

    with col2:
        st.markdown("""
        <div class="help-box">
        <h4>📌 使い方・ヘルプ: Threat Intel (TAXII 1.1)</h4>
        <p>STIX 1.x XML形式で脅威インテリジェンスフィードを取得します。</p>
        </div>
        """, unsafe_allow_html=True)
