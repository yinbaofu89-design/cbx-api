import streamlit as st
import requests
import json
import base64
from urllib.parse import urlencode, quote

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
DEFAULT_TOKEN = "eyJraWQiOiJGenFEamZXNlRYaTUzNVN4QnFoMTIzIiwidHlwIjoiSldUIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJ1cm46YnJvYWRjb206c2Fhczpkb21haW46ZjZHOHI5eEhTVmlzd0dNSENkX2ZNUTpjbGllbnQ6TzJJRC5Xdm0xTDlUQVJ3T1pXVHpFQkJqVzB3LmY2RzhyOXhIU1Zpc3dHTUhDZF9mTVEuNWttZXFwcWw1NGFmM3JxdjZrazRiZ2gyYzAiLCJ2ZXIiOjIsImlzcyI6Imh0dHBzOi8vYXBpLnNlY3VyaXR5LmNvbSIsInVyaSI6Ii9vYXV0aDIvY2xpZW50cy9PMklELld2bTFMOVRBUndPWldUekVCQmpXMHcuZjZHOHI5eEhTVmlzd0dNSENkX2ZNUS41a21lcXBxbDU0YWYzcnF2NmtrNGJnaDJjMCIsImNsaWVudF9pZCI6Ik8ySUQuV3ZtMUw5VEFSd09aV1R6RUJCalcwdy5mNkc4cjl4SFNWaXN3R01IQ2RfZk1RLjVrbWVxcHFsNTRhZjNycXY2a2s0YmdoMmMwIiwiZG9tYWluX2lkIjoiZjZHOHI5eEhTVmlzd0dNSENkX2ZNUSIsInNjb3BlIjoiZG9tYWluIG9hdXRoIiwidHR5IjoiYWNjZXNzIiwicHJpdnMiOiJlZHJfZ2V0X2ZpbGUgY2J4X2Rvd25sb2FkX2ZpbGUgd3NzX3ZpZXdfcG9saWN5X2xpc3RzIGFlcF9ydW5fcXVhcmFudGluZSBzZXNfdXBkYXRlX3NoYXJlZF9lbmRwb2ludCBzZXNfdmlld19zaGFyZWRfZW5kcG9pbnQgZWRyX2RlbGV0ZV9maWxlIGVkcl9kZWxldGVfZW5kcG9pbnRzZWFyY2ggY2JjX2xyX2V4ZWN1dGVfcHJvY2VzcyBjYnhfdmlld192dWxuZXJhYmlsaXR5X2RhdGEgY3BfbWFuYWdlX2VuZHBvaW50X3BvbGljeSBjYmNfdmlld19scSBjYmNfdmlld19kYXRhX2ZvcndhcmRlcnMgY2J4X3N1Ym1pdF9zYW5kYm94IGNiY192aWV3X25vdGlmaWNhdGlvbnMgY2J4X21hbmFnZV92dWxuZXJhYmlsaXR5X2RhdGEgY2JjX3ZpZXdfd2F0Y2hsaXN0cyBjYmNfdmlld19hbGVydHMgY2JjX3VzZV9sciBlZHJfZ2V0ZmlsZV9ub2NyZWQgYWVwX3J1bl9saXZldXBkYXRlIGFlcF9tYW5hZ2VfY29tbWFuZHMgY2JjX21uZ19hbGVydHNfbm90ZXNfdGFncyBjYnhfdmlld19kZXZpY2Vfc2VhcmNoIGNiY19tbmdfbm90aWZpY2F0aW9ucyBjYmNfcGVyZm9ybV9kZW9iZnVzY2F0aW9uIGNiY19yZXF1ZXN0X3VwZGF0ZWRfdnVsbl9kYXRhIGNiY19tbmdfd2F0Y2hsaXN0cyBzZXNfdmlld19hbGxfZmlsZXMgY3BfbWFuYWdlX2dsb2JhbF9wb2xpY3kgY2JjX2Nsb3NlX2FsZXJ0cyBjYmNfbW5nX2RhdGFfZm9yd2FyZGVycyB3c3NfbWFuYWdlX3BvbGljeV9saXN0cyBjYmNfbWFuYWdlX2FsZXJ0cyBzZXNfbWFuYWdlX3NoYXJlZF9lbmRwb2ludCBjYmNfbHJfdmlldyBlZHJfdHJpZ2dlcl9lbmRwb2ludHNlYXJjaCBzZXNfdmlld19yZXBvcnRzIHZpZXdfZXZlbnRzIGVkcl9yc2hlbGxfaW52ZXMgc2VzX3RocmVhdF9pbnRlbF9hcGlfYWNjZXNzIGNiY192aWV3X2V4cG9ydF92dWxuX2RhdGEgc2VzX21hbmFnZV9yZXBvcnRzIGNiY19jb25kdWN0X3Byb2Nlc3NfYW5hbHlzaXMgY3Bfdmlld19nbG9iYWxfcG9saWN5IGFlcF9yZW1vdGVfbG9nX2NvbGxlY3QgYWVwX3J1bl9yZWJvb3QgYWVwX3J1bl9zY2FuIHRkYWRfdHJpZ2dlcl9mb3JlbnNpY3MgY2JjX2xyX2R1bXBfbWVtb3J5IGNwX3ZpZXdfeGRyX3BvbGljeSBjYmNfZXhwb3J0X2V2ZW50X2RhdGEgY3BfbWFuYWdlX3hkcl9wb2xpY3kgY2JjX2NvbmR1Y3RfaW52ZXN0aWdhdGlvbiBlZHJfdmlld19pbnZlc3RpZ2F0aW9uIGNwX3ZpZXdfZW5kcG9pbnRfcG9saWN5IGVkcl9jYW5jZWxfZW5kcG9pbnRzZWFyY2ggY2J4X2RlbGV0ZV9maWxlIGFlcF92aWV3X2NvbW1hbmRzIGNieF9tYW5hZ2VfZGV2aWNlX3NlYXJjaCIsImV4cCI6MTc5NDg5NzcwNSwiY3VzdG9tZXJfaWQiOiJXdm0xTDlUQVJ3T1pXVHpFQkJqVzB3IiwiaWF0IjoxNzk0ODk0MTA1LCJqdGkiOiJiYUt2ZC1OVlNnR19RS3o1c2llbWd3In0.QUvcYhlkXNsbnReZVp4e20tGIqDu5DS7VshhW0VNKW_Kqasvu0E1EM7VSWwPgn1c_Rm_cqWR6JamNWGu3E-y6gjhBQ5WvhTxLZuAIV-u9mO2L0mhGSm1SAE4_nQPMWt9flPKn-pzdqIShh9vTTqXcTE_IWGHgMRMsl_Vw3XWEKwryLs_PWuIU7qZI2vqNkzvIG9Rk1nSNqJJBluhqAYph56h3okeJS4lGPW6rYlQwGbXzbVU5BqLVvE6FoJlDyv-3rGIrVpaX8hPlwpaQOOA5U1C_07j70MOSDIJaPMrz1MfYpztuX6I-fcueweiovIvKQ_9YlRKNYJ8UbO96mNW9A"

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

def build_query(path, params):
    """None / 空文字のパラメータを除外してクエリ文字列を付与する"""
    clean = {k: v for k, v in params.items() if v not in (None, "")}
    return f"{path}?{urlencode(clean)}" if clean else path

def parse_devices(text):
    """'device_id,device_name' を1行1台で解析して devices 配列にする"""
    devices = []
    for line in text.splitlines():
        if not line.strip():
            continue
        parts = [x.strip() for x in line.split(",", 1)]
        devices.append({"device_id": parts[0], "device_name": parts[1] if len(parts) > 1 else ""})
    return devices

def csv_list(text):
    """カンマ区切り文字列をリストに変換する"""
    return [x.strip() for x in text.split(",") if x.strip()]

def time_range_input(key_prefix, default_window="-2w"):
    """time_range（window か start/end のどちらか一方）を生成する"""
    tr_mode = st.radio("time_range", ["window (相対)", "start / end (絶対)", "指定しない"], horizontal=True, key=f"{key_prefix}_tr_mode")
    if tr_mode.startswith("window"):
        return {"window": st.text_input("window (例: -2w, -24h)", value=default_window, key=f"{key_prefix}_tr_window")}
    if tr_mode.startswith("start"):
        tr = {}
        tr_start = st.text_input("start (ISO 8601, 含む)", value="2026-11-01T00:00:00Z", key=f"{key_prefix}_tr_start")
        tr_end = st.text_input("end (ISO 8601, 含む)", value="2026-11-17T00:00:00Z", key=f"{key_prefix}_tr_end")
        if tr_start:
            tr["start"] = tr_start
        if tr_end:
            tr["end"] = tr_end
        return tr
    return None

# --- SIDEBAR ---
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

# Header
st.markdown('<div class="main-header">⚡ CBX API Master Commander</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">すべてのAPI・全エンドポイント対応（File Inventory v2 / Events v4 対応版）。テンプレートから実行ボックスへのデータ転送機能付き。</div>', unsafe_allow_html=True)

# Category selection covering File Inventory & other modules
module_choice = st.selectbox(
    "📁 APIモジュール（カテゴリ）を選択",
    [
        "🔑 Authentication (OAuth 2.0)",
        "📁 File Inventory",
        "🔍 Events",
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

        elif "File Inventory" in module_choice:
            op = st.selectbox("Endpoint", [
                "GET /detect-respond/file-inventory/v2/files",
                "GET /detect-respond/file-inventory/v2/files/hashes",
                "GET /detect-respond/file-inventory/v2/files/{file_hash}",
                "GET /detect-respond/file-inventory/v2/files/{file_hash}/devices",
                "GET /detect-respond/file-inventory/v2/files/{file_hash}/devices/{device_id}/paths",
                "POST /detect-respond/file-inventory/v2/files/{file_hash}/download",
                "POST /detect-respond/file-inventory/v2/files/{file_hash}/quarantine",
                "POST /detect-respond/file-inventory/v2/files/{file_hash}/unquarantine",
                "POST /detect-respond/file-inventory/v2/files/{file_hash}/delete"
            ])
            t_method, t_endpoint = op.split(" ", 1)

            if "{file_hash}" in t_endpoint:
                sha_val = st.text_input("file_hash (SHA-256, 64桁小文字hex)", value="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
                t_endpoint = t_endpoint.replace("{file_hash}", sha_val.strip().lower())
            if "{device_id}" in t_endpoint:
                dev_val = st.text_input("device_id", value="tLHktvhvReukGuFiNUFSzw")
                t_endpoint = t_endpoint.replace("{device_id}", quote(dev_val.strip(), safe=""))

            if t_endpoint.endswith("/files") or t_endpoint.endswith("/files/hashes"):
                # listFileInventory / listFileHashes: クエリパラメータ
                where = st.text_input('where (例: risk = "High" / file_name = "notepad.exe" / sandbox_status = "malware")', value='risk = "High"')
                order_by = st.text_input("order_by (例: file_name asc,risk desc)", value="")
                page = st.number_input("page", value=1, min_value=1, max_value=10000)
                page_size = st.number_input("page_size", value=100, min_value=1, max_value=100)
                t_endpoint = build_query(t_endpoint, {"where": where, "order_by": order_by, "page": page, "page_size": page_size})
            elif t_method == "GET" and (t_endpoint.endswith("/devices") or t_endpoint.endswith("/paths")):
                page = st.number_input("page", value=1, min_value=1, max_value=10000)
                page_size = st.number_input("page_size", value=100, min_value=1, max_value=100)
                t_endpoint = build_query(t_endpoint, {"page": page, "page_size": page_size})
            elif t_method == "GET":
                # getFileDetails
                include = st.selectbox("include", ["", "alerts", "incidents", "incidents_and_alerts"])
                t_endpoint = build_query(t_endpoint, {"include": include})
            elif t_endpoint.endswith("/download"):
                st.caption("200: ダウンロードURLを返却 / 202: デバイスから取得中（同じリクエストを再送してポーリング）")
                file_name = st.text_input("file_name (必須)", value="malware.exe")
                dl_dev_id = st.text_input("device_id", value="fkzEZpZU9VdvuQh6Eeo6ra")
                dl_dev_name = st.text_input("device_name", value="DESKTOP-WIN10")
                dl_password = st.text_input("password (ZIP保護, 任意)", value="", type="password")
                dl_path = st.text_input("file_path (任意, 空なら自動解決)", value="")
                t_data = {"file_name": file_name}
                if dl_dev_id:
                    t_data["device_id"] = dl_dev_id
                if dl_dev_name:
                    t_data["device_name"] = dl_dev_name
                if dl_password:
                    t_data["password"] = dl_password
                if dl_path:
                    t_data["file_path"] = dl_path
            else:
                # quarantine / unquarantine / delete
                if t_endpoint.endswith("/delete"):
                    st.warning("⚠️ delete は対象デバイス上のファイルを完全に削除します（元に戻せません）。")
                file_name = st.text_input("file_name (必須)", value="malware.exe")
                devices_text = st.text_area("devices (1行1台: device_id,device_name)", value="fkzEZpZU9VdvuQh6Eeo6ra,DESKTOP-WIN10")
                t_data = {"file_name": file_name, "devices": parse_devices(devices_text)}
                st.caption("状態確認: GET /agent-management/device-commands/v2/commands?correlation_id={reference_command_id}")

        elif "Events" in module_choice:
            op = st.selectbox("Endpoint", [
                "GET /detect-respond/event-search/v4/events/search-suggestions",
                "POST /detect-respond/event-search/v4/events/search-validation",
                "POST /detect-respond/event-search/v4/events/search-jobs",
                "GET /detect-respond/event-search/v4/events/search-jobs/{job_id}/results",
                "POST /detect-respond/event-search/v4/events/facet-jobs",
                "GET /detect-respond/event-search/v4/events/facet-jobs/{job_id}/results",
                "POST /detect-respond/event-search/v4/events/detail-jobs",
                "GET /detect-respond/event-search/v4/events/detail-jobs/{job_id}/results",
                "POST /detect-respond/event-search/v4/processes/summary-jobs",
                "GET /detect-respond/event-search/v4/processes/summary-jobs/{job_id}",
                "GET /detect-respond/event-search/v4/processes/summary-jobs/{job_id}/results",
                "POST /detect-respond/event-search/v4/processes/search-jobs",
                "GET /detect-respond/event-search/v4/processes/search-jobs/{job_id}/results",
                "POST /detect-respond/event-search/v4/processes/facet-jobs",
                "GET /detect-respond/event-search/v4/processes/facet-jobs/{job_id}/results"
            ])
            t_method, t_endpoint = op.split(" ", 1)

            if "{job_id}" in t_endpoint:
                job_val = st.text_input("job_id (ジョブ作成レスポンスの job_id)", value="a1b2c3d4-1234-5678-9abc-def012345678")
                t_endpoint = t_endpoint.replace("{job_id}", quote(job_val.strip(), safe=""))
                st.caption("status が COMPLETED になるまでポーリング（推奨: 500ms + 指数バックオフ / ジョブは7日で失効）")

            if t_endpoint.endswith("/search-suggestions"):
                suggest_q = st.text_input("suggest_q (必須)", value="process_")
                suggest_count = st.number_input("suggest_count", value=50, min_value=1)
                resource = st.selectbox("resource", ["event_search", "process_event_search"])
                t_endpoint = build_query(t_endpoint, {"suggest_q": suggest_q, "suggest_count": suggest_count, "resource": resource})

            elif t_endpoint.endswith("/search-validation"):
                query = st.text_area("query (必須)", value="process_name:chrome.exe AND event_type:netconn")
                resource = st.selectbox("resource", ["event_search", "process_event_search"])
                t_data = {"query": query, "resource": resource}

            elif t_method == "POST" and t_endpoint.endswith("/search-jobs"):
                is_process = "/processes/" in t_endpoint
                t_data = {}
                if is_process:
                    st.caption("SKU: CBX Essentials では非対応")
                    t_data["process_guid"] = st.text_input("process_guid (必須)", value="ABCD1234-0002b226-00000474-00000000-1d6a1c1f2a3b4c5")
                t_data["query"] = st.text_area("query (必須)", value="event_type:netconn" if is_process else "process_name:chrome.exe")
                fields = st.text_input("fields (カンマ区切り, * で全フィールド)",
                                       value="device_timestamp,event_type,netconn_remote_ipv4" if is_process else "backend_timestamp,device_name,process_name,event_type")
                if csv_list(fields):
                    t_data["fields"] = csv_list(fields)
                t_data["rows"] = st.number_input("rows", value=500, min_value=1, max_value=10000)
                tr = time_range_input("ev_search", "-1w" if is_process else "-2w")
                if tr:
                    t_data["time_range"] = tr
                order_by = st.text_input("order_by (クエリパラメータ, 例: device_timestamp desc)", value="")
                t_endpoint = build_query(t_endpoint, {"order_by": order_by})

            elif t_method == "POST" and t_endpoint.endswith("/facet-jobs"):
                is_process = "/processes/" in t_endpoint
                t_data = {}
                if is_process:
                    st.caption("SKU: CBX Essentials では非対応")
                    t_data["process_guid"] = st.text_input("process_guid (必須)", value="ABCD1234-0002b226-00000474-00000000-1d6a1c1f2a3b4c5")
                t_data["query"] = st.text_area("query (必須)", value="event_type:filemod" if is_process else "process_name:chrome.exe")
                term_fields = st.text_input("terms.fields (カンマ区切り)", value="event_type" if is_process else "event_type,device_name")
                term_rows = st.number_input("terms.rows", value=10, min_value=1, max_value=10000)
                t_data["terms"] = {"fields": csv_list(term_fields), "rows": term_rows}
                if st.checkbox("ranges を追加（ヒストグラム）", value=not is_process):
                    r_field = st.text_input("ranges.field", value="device_timestamp")
                    r_start = st.text_input("ranges.start（含む）", value="2026-11-03T00:00:00Z")
                    r_end = st.text_input("ranges.end（含まない）", value="2026-11-18T00:00:00Z")
                    r_bucket = st.text_input("ranges.bucket_size", value="+1DAY")
                    t_data["ranges"] = [{"field": r_field, "start": r_start, "end": r_end, "bucket_size": r_bucket}]
                tr = time_range_input("ev_facet", "-2w")
                if tr:
                    t_data["time_range"] = tr

            elif t_endpoint.endswith("/detail-jobs"):
                id_type = st.radio("対象 (どちらか一方)", ["event_id", "alert_id"], horizontal=True)
                id_val = st.text_input(id_type, value="8f0a1b2c3d4e5f60718293a4b5c6d7e8" if id_type == "event_id" else "alt-123")
                t_data = {id_type: id_val}

            elif t_endpoint.endswith("/summary-jobs"):
                st.caption("SKU: CBX Essentials では非対応")
                t_data = {"process_guid": st.text_input("process_guid (必須)", value="ABCD1234-0002b226-00000474-00000000-1d6a1c1f2a3b4c5")}
                parent_guid = st.text_input("parent_guid (任意)", value="")
                alert_id = st.text_input("alert_id (任意)", value="")
                if parent_guid:
                    t_data["parent_guid"] = parent_guid
                tr = time_range_input("ev_summary", "-1w")
                if tr:
                    t_data["time_range"] = tr
                if alert_id:
                    t_data["alert_id"] = alert_id

            elif "/summary-jobs/" in t_endpoint and t_endpoint.endswith("/results"):
                fmt = st.selectbox("format", ["summary", "tree"])
                t_endpoint = build_query(t_endpoint, {"format": fmt})

            elif "/search-jobs/" in t_endpoint:
                page = st.number_input("page", value=1, min_value=1)
                page_size = st.number_input("page_size", value=500, min_value=1)
                t_endpoint = build_query(t_endpoint, {"page": page, "page_size": page_size})

            elif "/facet-jobs/" in t_endpoint:
                limit = st.number_input("limit (フィールドごとのバケット数)", value=100, min_value=1)
                t_endpoint = build_query(t_endpoint, {"limit": limit})

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

    with col_in2:
        st.markdown("**生成されるプレビュー (URL / データ):**")
        preview_text = f"""Endpoint: {t_endpoint}
Method: {t_method}
Data:
{json.dumps(t_data, indent=2)}"""
        st.code(preview_text, language="json")
        
        if st.button("📥 実行ボックスにこの設定を転送する", use_container_width=True, type="primary"):
            st.session_state["exec_method"] = t_method
            st.session_state["exec_endpoint"] = t_endpoint
            st.session_state["exec_payload"] = json.dumps(t_data, indent=2)
            st.rerun()

st.markdown("---")

# --- ALWAYS VISIBLE EXECUTION BOX ---
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
