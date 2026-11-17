import streamlit as st
import streamlit.components.v1 as components
import requests
import json
import base64
import re
import time
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

def jwt_exp(token_str):
    """JWT の exp（UNIX 秒）を返す。解析できなければ None"""
    try:
        p = (token_str or "").replace("Bearer ", "").strip().split(".")[1]
        p += "=" * ((4 - len(p) % 4) % 4)
        return int(json.loads(base64.urlsafe_b64decode(p).decode("utf-8")).get("exp"))
    except Exception:
        return None

def fetch_token(base_url, basic_b64, data=None, accept="application/json"):
    """POST /common/v1/oauth2/tokens（Method 2）。戻り値: (token, 期限UNIX秒, status, body)"""
    r = requests.post(f"{base_url.rstrip('/')}/common/v1/oauth2/tokens",
                      headers={"accept": accept or "application/json",
                               "authorization": f"Basic {basic_b64}",
                               "content-type": "application/x-www-form-urlencoded"},
                      data=data or {"grant_type": "client_credentials", "scope": "domain"}, timeout=30)
    try:
        body = r.json()
    except ValueError:
        body = {"raw": r.text}
    tok = body.get("access_token") if isinstance(body, dict) else None
    exp = None
    if r.ok and tok:
        exp = jwt_exp(tok)
        try:
            exp = exp or int(time.time() + int(body.get("expires_in", 3600)))
        except Exception:
            exp = int(time.time() + 3600)
    return (tok if r.ok else None), exp, r.status_code, body

AUTO_REFRESH_MARGIN = 300  # 残り 5 分を切ったら自動更新

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

# --- API仕様（添付ドキュメント cbx_*.md から生成。汎用テストページで使用） ---
API_SPECS = {'💽 Devices': {'doc': 'cbx_devices.md',
               'permissions': ['Device and Device Group Management -> View'],
               'endpoints': [{'method': 'GET',
                              'path': '/agent-management/devices/v2/devices',
                              'summary': 'デバイス一覧を取得します。',
                              'operation_id': 'listDevices',
                              'sku': '',
                              'desc': '管理対象デバイスの一覧をページ単位で返します。任意でフィルタリングおよび並べ替えが可能です。Read Devices '
                                      '権限が必要です。この権限を持たない呼び出し元には 403 Forbidden レスポンスが返されます。',
                              'path_params': [],
                              'query_params': [{'name': 'page',
                                                'type': 'integer',
                                                'required': False,
                                                'default': '1',
                                                'desc': '取得するページ番号（1 始まり）。【注意】このフィールドが指定されていない場合は、最初のページが返されます。',
                                                'sample': ''},
                                               {'name': 'page_size',
                                                'type': 'integer',
                                                'required': False,
                                                'default': '100',
                                                'desc': '1 ページあたりのデバイス数。【注意】デフォルトでは 100 台のデバイスが返されます。最大ページサイズは 1000 '
                                                        'で、include_details=true を指定した場合は 500 です。page_size > 500 かつ '
                                                        'include_details=true のリクエストは…',
                                                'sample': ''},
                                               {'name': 'include_details',
                                                'type': 'boolean',
                                                'required': False,
                                                'default': '',
                                                'desc': 'レスポンスに製品および機能の詳細を含めるかどうかを示すフラグ。指定可能な値: true/false。【注意】このフラグが '
                                                        'true の場合、1 リクエストあたりでサポートされる最大レコード数は 500 です。',
                                                'sample': ''},
                                               {'name': 'include_path',
                                                'type': 'boolean',
                                                'required': False,
                                                'default': '',
                                                'desc': 'レスポンスにデバイスグループのフルパスを含めるかどうかを示すフラグ。指定可能な値: true/false。',
                                                'sample': ''},
                                               {'name': 'order_by',
                                                'type': 'string',
                                                'required': False,
                                                'default': '',
                                                'desc': 'レスポンス内のデバイスの並べ替えに使用するフィールド名。並べ替え方向を指定する場合は、続けてスペースと "asc" または '
                                                        '"desc" を付加します。省略した場合、並べ替え順序はデフォルトで昇順になります。指定できるフィールドは 1 つ…',
                                                'sample': ''},
                                               {'name': 'antimalware_content_version',
                                                'type': 'array',
                                                'required': False,
                                                'default': '',
                                                'desc': 'デバイスにインストールされているマルウェア対策コンテンツのバージョン。このパラメーターに複数の値を指定した場合は OR '
                                                        'で結合され、指定した値のいずれかを満たすデバイスが一致します。各値は…',
                                                'sample': ''},
                                               {'name': 'capabilities_enabled',
                                                'type': 'array',
                                                'required': False,
                                                'default': '',
                                                'desc': 'このデバイスで有効になっている機能。内部の機能定数でフィルタリングします（参考として表示しているマーケティング名は変更される可能性があります）: '
                                                        'ENDPOINT_PROTECTION (Endpoint Security)、WEB_SECURITY (Web '
                                                        'Securi…',
                                                'sample': ''},
                                               {'name': 'cloud_platform',
                                                'type': 'array',
                                                'required': False,
                                                'default': '',
                                                'desc': 'クラウドプラットフォーム。サポートされる値: '
                                                        'AWS、GCP、AZURE、NONE。このパラメーターに複数の値を指定した場合は OR '
                                                        'で結合され、指定した値のいずれかを満たすデバイスが一致します。各値は…',
                                                'sample': ''},
                                               {'name': 'connection_status',
                                                'type': 'string',
                                                'required': False,
                                                'default': '',
                                                'desc': 'デバイスにインストールされているエージェントの接続状態。Online は、デバイスが過去 48 '
                                                        '時間以内にバックエンドと通信したことを意味します。それ以外の場合、デバイスは Offline となります。注: '
                                                        'connection_status…',
                                                'sample': ''},
                                               {'name': 'data_security_version',
                                                'type': 'array',
                                                'required': False,
                                                'default': '',
                                                'desc': 'デバイスにインストールされている Data Security のバージョン。このパラメーターに複数の値を指定した場合は '
                                                        'OR で結合され、指定した値のいずれかを満たすデバイスが一致します。各値は…',
                                                'sample': ''},
                                               {'name': 'device_group',
                                                'type': 'array',
                                                'required': False,
                                                'default': '',
                                                'desc': '親デバイスグループの id。レスポンスの parent_device_group_id '
                                                        'フィールドに対応します。このパラメーターに複数の値を指定した場合は OR で結合され、指定した値のいずれかを…',
                                                'sample': ''},
                                               {'name': 'device_id',
                                                'type': 'string',
                                                'required': False,
                                                'default': '',
                                                'desc': 'デバイスの一意識別子。【注意】order_by が指定されていない場合、レスポンス内のデバイスは device_id '
                                                        'で並べ替えられます。',
                                                'sample': ''},
                                               {'name': 'device_name',
                                                'type': 'array',
                                                'required': False,
                                                'default': '',
                                                'desc': 'デバイスの名前。このパラメーターに複数の値を指定した場合は OR '
                                                        'で結合され、指定した値のいずれかを満たすデバイスが一致します。各値はフィールドに対して部分一致（部分文字列一致）を行い…',
                                                'sample': ''},
                                               {'name': 'device_os',
                                                'type': 'array',
                                                'required': False,
                                                'default': '',
                                                'desc': 'デバイスの OS 名。レスポンスの os.device_os '
                                                        'フィールドに対応します。このパラメーターに複数の値を指定した場合は OR '
                                                        'で結合され、指定した値のいずれかを満たすデバイスが…',
                                                'sample': ''},
                                               {'name': 'device_type',
                                                'type': 'array',
                                                'required': False,
                                                'default': '',
                                                'desc': 'デバイスの OS タイプ。内部的にはデバイスの os.type '
                                                        '値に対してサフィックスで照合されます。WORKSTATION は _WORKSTATION で終わる任意の os.type '
                                                        'に、SERVER は _SERVER で終わる任意の os.type に一致します。…',
                                                'sample': ''},
                                               {'name': 'disabled_expiration_time',
                                                'type': 'string',
                                                'required': False,
                                                'default': '',
                                                'desc': 'disabled_expiration_time '
                                                        'がこの値以降であるデバイス（つまり、トラブルシューティング期間の終了が指定時刻以降であるデバイス）を返します。トラブルシューティング期間が終了する時刻…',
                                                'sample': ''},
                                               {'name': 'domain',
                                                'type': 'array',
                                                'required': False,
                                                'default': '',
                                                'desc': 'このデバイスが接続しているドメイン。このパラメーターに複数の値を指定した場合は OR '
                                                        'で結合され、指定した値のいずれかを満たすデバイスが一致します。各値は部分…',
                                                'sample': ''},
                                               {'name': 'endpoint_security_version',
                                                'type': 'array',
                                                'required': False,
                                                'default': '',
                                                'desc': 'デバイスにインストールされている Endpoint Protection '
                                                        'のバージョン。このパラメーターに複数の値を指定した場合は OR '
                                                        'で結合され、指定した値のいずれかを満たすデバイスが一致します。各値は…',
                                                'sample': ''},
                                               {'name': 'enrollment_date',
                                                'type': 'integer',
                                                'required': False,
                                                'default': '',
                                                'desc': '現在までの指定日数以内に登録されたデバイスが返されます。注: このフィールドは enrollment_date '
                                                        'という名前で、デバイスのレスポンスでは日付を表しますが、このクエリーパラメーターが想定するのは…',
                                                'sample': ''},
                                               {'name': 'esa_version',
                                                'type': 'array',
                                                'required': False,
                                                'default': '',
                                                'desc': 'デバイスにインストールされている Endpoint Security Agent '
                                                        'のバージョン。このパラメーターに複数の値を指定した場合は OR '
                                                        'で結合され、指定した値のいずれかを満たすデバイスが一致します。各値は…',
                                                'sample': ''},
                                               {'name': 'form_factor',
                                                'type': 'string',
                                                'required': False,
                                                'default': '',
                                                'desc': 'デバイスのフォームファクター。注: レスポンスの form_factor フィールドは、ここで使用する '
                                                        'PHYSICAL/VIRTUAL '
                                                        'の大文字表記ではなく、同じ値を先頭のみ大文字（Physical/Virtual）で返します。',
                                                'sample': ''},
                                               {'name': 'host',
                                                'type': 'array',
                                                'required': False,
                                                'default': '',
                                                'desc': 'デバイスのホスト名。このパラメーターに複数の値を指定した場合は OR '
                                                        'で結合され、指定した値のいずれかを満たすデバイスが一致します。各値はフィールドに対して部分一致（部分文字列一致）を行い…',
                                                'sample': ''},
                                               {'name': 'instance_id',
                                                'type': 'array',
                                                'required': False,
                                                'default': '',
                                                'desc': 'デバイスのインスタンス ID。レスポンスの instance_id フィールド（および同一の '
                                                        'device_identifiers.instance_id）に対応します。このパラメーターに複数の値を指定した場合は '
                                                        'OR で結合され、デバイスは…',
                                                'sample': ''},
                                               {'name': 'ipv4_address',
                                                'type': 'array',
                                                'required': False,
                                                'default': '',
                                                'desc': 'デバイスの IPv4 アドレス。このパラメーターに複数の値を指定した場合は OR '
                                                        'で結合され、指定した値のいずれかを満たすデバイスが一致します。各値は部分一致（部分文字列一致）を行い…',
                                                'sample': ''},
                                               {'name': 'last_updated',
                                                'type': 'string',
                                                'required': False,
                                                'default': '',
                                                'desc': 'last_updated '
                                                        'タイムスタンプがこの値以降であるデバイス（つまり、指定時刻以降に更新されたデバイス）を返します。レスポンスの '
                                                        'products[0].last_updated に対応します。',
                                                'sample': ''},
                                               {'name': 'mac_address',
                                                'type': 'array',
                                                'required': False,
                                                'default': '',
                                                'desc': 'デバイスの MAC アドレス。レスポンスの adapters[].addr '
                                                        'フィールドに対応します。このパラメーターに複数の値を指定した場合は OR で結合され、指定した値のいずれかを満たす…',
                                                'sample': ''},
                                               {'name': 'mdm_id',
                                                'type': 'array',
                                                'required': False,
                                                'default': '',
                                                'desc': 'デバイスの MDM ID。注: '
                                                        'デバイスのレスポンススキーマにはこの値を読み戻すための対応フィールドがありません。フィルタリングはサポートされていますが、返されたデバイスレコード上で現在の値を確認することはできま…',
                                                'sample': ''},
                                               {'name': 'os_version',
                                                'type': 'string',
                                                'required': False,
                                                'default': '',
                                                'desc': 'デバイスの OS バージョン。レスポンスの os.os_version '
                                                        'フィールドに対応します。各値は完全一致ではなく、フィールドに対する部分一致（部分文字列一致）を行います。例: "10.0" '
                                                        'は "10.0.19044" に一致します。',
                                                'sample': ''},
                                               {'name': 'permission',
                                                'type': 'array',
                                                'required': False,
                                                'default': '',
                                                'desc': 'Cloud SWG の接続状態。サポートされる値: '
                                                        'ALLOWED（接続を許可）、BLOCKED（ポリシーなどにより接続を完全にブロック）、DISABLED（管理者が…まで接続を一時的に無効化）…',
                                                'sample': ''},
                                               {'name': 'security_status',
                                                'type': 'array',
                                                'required': False,
                                                'default': '',
                                                'desc': 'デバイスのセキュリティステータス。各値（NOT_COMPUTED、UNENROLLED、UNKNOWN '
                                                        'を含む）の意味は次のページに記載されています: '
                                                        'https://techdocs.broadcom.com/us/en/symantec-security-software/symantec-cbx/cbx/ind…',
                                                'sample': ''},
                                               {'name': 'status_reason',
                                                'type': 'array',
                                                'required': False,
                                                'default': '',
                                                'desc': 'エンドポイントエージェントが報告するデバイスステータスの理由コード。値は数値文字列（例: '
                                                        '"132"、"613"）で、固定の列挙型ではありません。コードのセットはエージェントのバージョンおよびインストールされている製品によって異なり…',
                                                'sample': ''},
                                               {'name': 'user',
                                                'type': 'array',
                                                'required': False,
                                                'default': '',
                                                'desc': '最後にログオンしたユーザー名。レスポンスの os.user '
                                                        'フィールドに対応します。このパラメーターに複数の値を指定した場合は OR で結合され、指定した値のいずれかを…',
                                                'sample': ''},
                                               {'name': 'web_security_version',
                                                'type': 'array',
                                                'required': False,
                                                'default': '',
                                                'desc': 'デバイスにインストールされている Web Security のバージョン。このパラメーターに複数の値を指定した場合は OR '
                                                        'で結合され、指定した値のいずれかを満たすデバイスが一致します。各値は部分…',
                                                'sample': ''}],
                              'body': None,
                              'body_schema': []},
                             {'method': 'DELETE',
                              'path': '/agent-management/devices/v2/devices',
                              'summary': '管理対象デバイスの一括削除',
                              'operation_id': 'deleteDevices',
                              'sku': '',
                              'desc': '識別子を指定して管理対象デバイスを一括削除します。device_uids リクエストフィールドに device_id の値（GET /devices '
                                      'で返されるもの）を指定します。デバイスごとの結果が返され、一部のみ成功する場合があります。Manage Devices '
                                      '権限が必要です。この権限を持たない呼び出し元には 403 Forbidden レスポンスが返されます。',
                              'path_params': [],
                              'query_params': [],
                              'body': {'device_uids': ['J1GpYTXlQmaD9c70WQIURA', 'doKfbw70SaKXvaR2PIxfLA']},
                              'body_schema': ['`device_uids` `array[string]` *(必須)* — 削除するデバイスの一意識別子のリスト。各値は GET '
                                              '/devices および GET /devices/{device_id} で返される device_id フィールドに対応します。']},
                             {'method': 'GET',
                              'path': '/agent-management/devices/v2/devices/{device_id}',
                              'summary': 'デバイスの詳細を取得します。',
                              'operation_id': 'getDeviceDetails',
                              'sku': '',
                              'desc': '指定したデバイスの OS、ハードウェア、ネットワークアダプター、インストール済みセキュリティ製品を含む完全な詳細を返します。Read Devices '
                                      '権限が必要です。この権限を持たない呼び出し元には 403 Forbidden レスポンスが返されます。',
                              'path_params': [{'name': 'device_id',
                                               'required': True,
                                               'desc': '詳細を取得するデバイスを指定します。GET /devices または事前の GET /devices/{device_id} '
                                                       '呼び出しで返される device_id フィールドに対応します。',
                                               'sample': 'ZROiMffzSAGb_2WT1c-75Q'}],
                              'query_params': [],
                              'body': None,
                              'body_schema': []},
                             {'method': 'GET',
                              'path': '/agent-management/devices/v2/devices/enums',
                              'summary': 'CBX の列挙値の詳細およびデバイス固有の詳細を取得するための API エンドポイント。',
                              'operation_id': 'getDeviceEnums',
                              'sku': '',
                              'desc': '機能名、セキュリティステータス値、理由コードなど、CBX デバイスフィールドの列挙値の詳細を返します。Read Devices '
                                      '権限が必要です。この権限を持たない呼び出し元には 403 Forbidden レスポンスが返されます。',
                              'path_params': [],
                              'query_params': [],
                              'body': None,
                              'body_schema': []}]},
 '🗂️ Device Groups': {'doc': 'cbx_device_groups.md',
                      'permissions': ['Device and Device Group Management -> View',
                                      'Device and Device Group Management -> Delete'],
                      'endpoints': [{'method': 'GET',
                                     'path': '/agent-management/device-groups/v2/groups',
                                     'summary': 'デバイスグループの一覧を取得します。',
                                     'operation_id': 'listDeviceGroups',
                                     'sku': '',
                                     'desc': 'すべてのデバイスグループの一覧をページ単位で返します。Read Device Groups 権限（API Credentials '
                                             'ページ上の表記では Agent Management > Device and Device Group Management > '
                                             'Read）が必要です。この権限を持たない呼び出し元には 403 Forbidden レスポンスが返されます。',
                                     'path_params': [],
                                     'query_params': [{'name': 'page',
                                                       'type': 'integer',
                                                       'required': False,
                                                       'default': '1',
                                                       'desc': '1 始まりのページ番号。',
                                                       'sample': ''},
                                                      {'name': 'page_size',
                                                       'type': 'integer',
                                                       'required': False,
                                                       'default': '1000',
                                                       'desc': '1 ページあたりのレコード数。1 リクエストあたりでサポートされる最大レコード数は 1000 です。',
                                                       'sample': ''},
                                                      {'name': 'root_only',
                                                       'type': 'boolean',
                                                       'required': False,
                                                       'default': 'false',
                                                       'desc': 'ルートデバイスグループのみを返すためのフィルター。',
                                                       'sample': ''},
                                                      {'name': 'order_by',
                                                       'type': 'string',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': '返されるデバイスグループの並べ替え順序。サポートされるのは name '
                                                               'フィールドのみで、昇順（"name"）または降順（"name '
                                                               'desc"）を指定できます。並べ替えでは大文字と小文字は区別されません。',
                                                       'sample': ''},
                                                      {'name': 'name',
                                                       'type': 'string',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'デバイスグループ名でグループをフィルタリングします（部分一致）。',
                                                       'sample': ''}],
                                     'body': None,
                                     'body_schema': []},
                                    {'method': 'POST',
                                     'path': '/agent-management/device-groups/v2/groups/{group_id}',
                                     'summary': '子デバイスグループを作成します。',
                                     'operation_id': 'createDeviceGroup',
                                     'sku': '',
                                     'desc': '指定した親グループの下に新しい子デバイスグループを作成します。Manage Device Groups 権限（API Credentials '
                                             'ページ上の表記では Agent Management > Device and Device Group Management > '
                                             'Manage）が必要です。この権限を持たない呼び出し元には 403 Forbidden レスポンスが返されます。',
                                     'path_params': [{'name': 'group_id',
                                                      'required': True,
                                                      'desc': '親デバイスグループの ID。',
                                                      'sample': '4Zh6VRUJQQauw_-AzxjtHw'}],
                                     'query_params': [],
                                     'body': {'name': 'Linux Servers - US East',
                                              'description': 'Group for all Linux servers located in the US East data '
                                                             'center'},
                                     'body_schema': ['`name` `string` *(必須)* — 新しいデバイスグループの名前。',
                                                     '`description` `string` — デバイスグループの説明']},
                                    {'method': 'GET',
                                     'path': '/agent-management/device-groups/v2/groups/{group_id}',
                                     'summary': 'デバイスグループを取得します。',
                                     'operation_id': 'getDeviceGroup',
                                     'sku': '',
                                     'desc': '指定した ID のデバイスグループを返します。Read Device Groups 権限（API Credentials ページ上の表記では '
                                             'Agent Management > Device and Device Group Management > '
                                             'Read）が必要です。この権限を持たない呼び出し元には 403 Forbidden レスポンスが返されます。',
                                     'path_params': [{'name': 'group_id',
                                                      'required': True,
                                                      'desc': 'デバイスグループの ID。',
                                                      'sample': '4Zh6VRUJQQauw_-AzxjtHw'}],
                                     'query_params': [],
                                     'body': None,
                                     'body_schema': []},
                                    {'method': 'PUT',
                                     'path': '/agent-management/device-groups/v2/groups/{group_id}',
                                     'summary': 'デバイスグループを更新します。',
                                     'operation_id': 'updateDeviceGroup',
                                     'sku': '',
                                     'desc': '指定したデバイスグループの名前または説明を更新します。リクエストボディで省略したフィールドは変更されず、指定したフィールドのみが更新されます。Manage '
                                             'Device Groups 権限（API Credentials ページ上の表記では Agent Management > Device and '
                                             'Device Group Management > Manage）が必要です。この権限を持たない呼び出し元には 403 Forbidden '
                                             'レスポンスが返されます。',
                                     'path_params': [{'name': 'group_id',
                                                      'required': True,
                                                      'desc': '更新するデバイスグループの ID。',
                                                      'sample': '4Zh6VRUJQQauw_-AzxjtHw'}],
                                     'query_params': [],
                                     'body': {'name': 'Linux Servers - US West',
                                              'description': 'Group for all Linux servers located in the US West data '
                                                             'center'},
                                     'body_schema': ['`name` `string` — デバイスグループに割り当てる新しい名前',
                                                     '`description` `string` — デバイスグループに割り当てる新しい説明']},
                                    {'method': 'DELETE',
                                     'path': '/agent-management/device-groups/v2/groups/{group_id}',
                                     'summary': 'デバイスグループを削除します。',
                                     'operation_id': 'deleteDeviceGroup',
                                     'sku': '',
                                     'desc': '指定したデバイスグループを削除します。削除できるのは空のグループ（関連付けられたデバイスがないグループ）のみです。グループにデバイスが含まれている場合は、先にそれらを削除または移動してください。recursive '
                                             'が true の場合、グループとネストされたすべての子グループが削除されます。この場合、すべての子グループも空である必要があります。Manage '
                                             'Device Groups 権限（API Credentials ページ上の表記では Agent Management > Device and '
                                             'Device Group Management > Manage）が必要です。この権限を持たない呼び出し元には 403 Forbidden '
                                             'レスポンスが返されます。',
                                     'path_params': [{'name': 'group_id',
                                                      'required': True,
                                                      'desc': '削除するデバイスグループの ID。',
                                                      'sample': '4Zh6VRUJQQauw_-AzxjtHw'}],
                                     'query_params': [{'name': 'recursive',
                                                       'type': 'boolean',
                                                       'required': False,
                                                       'default': 'false',
                                                       'desc': 'true '
                                                               'の場合、グループとネストされたすべての子グループを削除します。すべての子グループも空（関連付けられたデバイスがない状態）である必要があります。false '
                                                               'の場合、指定したグループのみが削除され、そのグループ自体が空である必要があります。',
                                                       'sample': ''}],
                                     'body': None,
                                     'body_schema': []},
                                    {'method': 'GET',
                                     'path': '/agent-management/device-groups/v2/groups/{group_id}/devices',
                                     'summary': 'デバイスグループのメンバーであるデバイスの一覧を取得します。',
                                     'operation_id': 'listGroupDevices',
                                     'sku': '',
                                     'desc': '指定したデバイスグループに属するデバイスの一覧をページ単位で返します。サポートされていないクエリーパラメーターやパラメーター値は無視されます。Read '
                                             'Device Groups 権限（API Credentials ページ上の表記では Agent Management > Device and '
                                             'Device Group Management > Read）が必要です。この権限を持たない呼び出し元には 403 Forbidden '
                                             'レスポンスが返されます。各エントリは概要（device_id と device_name）のみです。デバイスの完全な詳細を取得するには GET '
                                             '/agent-management/devices を使用してください。',
                                     'path_params': [{'name': 'group_id',
                                                      'required': True,
                                                      'desc': 'デバイスを取得する対象のデバイスグループの ID。',
                                                      'sample': '4Zh6VRUJQQauw_-AzxjtHw'}],
                                     'query_params': [{'name': 'page',
                                                       'type': 'integer',
                                                       'required': False,
                                                       'default': '1',
                                                       'desc': 'デバイス結果の 1 始まりのページ番号。',
                                                       'sample': ''},
                                                      {'name': 'page_size',
                                                       'type': 'integer',
                                                       'required': False,
                                                       'default': '1000',
                                                       'desc': '1 ページあたりのデバイスレコード数。1 リクエストあたりでサポートされる最大レコード数は 1000 です。',
                                                       'sample': ''},
                                                      {'name': 'device_id',
                                                       'type': 'string',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'デバイスの一意識別子。',
                                                       'sample': ''},
                                                      {'name': 'antimalware_content_version',
                                                       'type': 'array',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'デバイスにインストールされているマルウェア対策コンテンツのバージョン。',
                                                       'sample': ''},
                                                      {'name': 'endpoint_security_version',
                                                       'type': 'array',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'デバイスにインストールされている Endpoint Security のバージョン。',
                                                       'sample': ''},
                                                      {'name': 'web_security_version',
                                                       'type': 'array',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'デバイスにインストールされている Web Security のバージョン。',
                                                       'sample': ''},
                                                      {'name': 'data_security_version',
                                                       'type': 'array',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'デバイスにインストールされている Data Security のバージョン。',
                                                       'sample': ''},
                                                      {'name': 'esa_version',
                                                       'type': 'array',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'デバイスにインストールされている Endpoint Security Agent のバージョン。',
                                                       'sample': ''},
                                                      {'name': 'connection_status',
                                                       'type': 'string',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'デバイスにインストールされているエージェントの接続状態。Online は、デバイスが過去 48 '
                                                               '時間以内にバックエンドと通信したことを意味します。それ以外の場合、デバイスは Offline となります。',
                                                       'sample': ''},
                                                      {'name': 'security_status',
                                                       'type': 'array',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'デバイスのセキュリティステータス。各値（NOT_COMPUTED、UNENROLLED、UNKNOWN '
                                                               'を含む）の意味は次のページに記載されています: '
                                                               'https://techdocs.broadcom.com/us/en/symantec-security-software/symantec-cbx/cbx/ind…',
                                                       'sample': ''},
                                                      {'name': 'device_os',
                                                       'type': 'array',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'デバイスの OS 名。',
                                                       'sample': ''},
                                                      {'name': 'os_version',
                                                       'type': 'string',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'デバイスの OS バージョン（部分一致／前方一致）。例: "10.0" は "10.0.19044" '
                                                               'に一致します。',
                                                       'sample': ''},
                                                      {'name': 'device_type',
                                                       'type': 'array',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'デバイスの OS タイプ。列挙値: WORKSTATION = ユーザーワークステーション、SERVER = '
                                                               'サーバーインフラストラクチャ。',
                                                       'sample': ''},
                                                      {'name': 'form_factor',
                                                       'type': 'string',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'デバイスのフォームファクター。',
                                                       'sample': ''},
                                                      {'name': 'device_name',
                                                       'type': 'array',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'デバイスの名前。',
                                                       'sample': ''},
                                                      {'name': 'status_reason',
                                                       'type': 'array',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'エンドポイントエージェントが報告するデバイスステータスの理由コード。値は数値文字列（例: '
                                                               '"132"、"613"）で、固定の列挙型ではありません。コードのセットはエージェントのバージョンおよびインストールされている製品によって異なり…',
                                                       'sample': ''},
                                                      {'name': 'ipv4_address',
                                                       'type': 'array',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'デバイスの IPv4 アドレス。',
                                                       'sample': ''},
                                                      {'name': 'mac_address',
                                                       'type': 'array',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'デバイスの MAC アドレス。',
                                                       'sample': ''},
                                                      {'name': 'capabilities_enabled',
                                                       'type': 'array',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'このデバイスで有効になっている機能。サポートされる値: '
                                                               'ENDPOINT_PROTECTION、WEB_SECURITY、DATA_SECURITY。',
                                                       'sample': ''},
                                                      {'name': 'cloud_platform',
                                                       'type': 'array',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'クラウドプラットフォーム。サポートされる値: AWS、GCP、AZURE、NONE。',
                                                       'sample': ''},
                                                      {'name': 'enrollment_date',
                                                       'type': 'integer',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': '現在までの指定日数以内に登録されたデバイスが返されます。注: このフィールドは '
                                                               'enrollment_date '
                                                               'という名前で、デバイスのレスポンスでは日付を表しますが、このクエリーパラメーターが想定するのは…',
                                                       'sample': ''},
                                                      {'name': 'permission',
                                                       'type': 'array',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'Cloud SWG の接続状態。サポートされる値: ALLOWED、BLOCKED、DISABLED。',
                                                       'sample': ''},
                                                      {'name': 'instance_id',
                                                       'type': 'array',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'デバイスのインスタンス ID。',
                                                       'sample': ''},
                                                      {'name': 'domain',
                                                       'type': 'array',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'このデバイスが接続しているドメイン。',
                                                       'sample': ''},
                                                      {'name': 'host',
                                                       'type': 'array',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'デバイスのホスト名。',
                                                       'sample': ''},
                                                      {'name': 'user',
                                                       'type': 'array',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': '最後にログオンしたユーザー名。',
                                                       'sample': ''},
                                                      {'name': 'mdm_id',
                                                       'type': 'array',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'デバイスの MDM ID。',
                                                       'sample': ''}],
                                     'body': None,
                                     'body_schema': []},
                                    {'method': 'PUT',
                                     'path': '/agent-management/device-groups/v2/groups/{group_id}/devices',
                                     'summary': '複数のデバイスをあるデバイスグループから別のデバイスグループへ移動します。',
                                     'operation_id': 'moveDevicesToGroup',
                                     'sku': '',
                                     'desc': '複数のデバイスを現在のグループから指定したターゲットグループへ移動します。200 '
                                             'レスポンスはすべてのデバイスが移動されたことを保証するものではありません。個々の結果については各項目の `status` '
                                             'フィールドを確認してください。Manage Device Groups 権限（API Credentials ページ上の表記では Agent '
                                             'Management > Device and Device Group Management > '
                                             'Manage）が必要です。この権限を持たない呼び出し元には 403 Forbidden レスポンスが返されます。',
                                     'path_params': [{'name': 'group_id',
                                                      'required': True,
                                                      'desc': 'ターゲットデバイスグループの ID。',
                                                      'sample': '4Zh6VRUJQQauw_-AzxjtHw'}],
                                     'query_params': [],
                                     'body': {'device_uids': ['0ODNRjz5THGP0-SAXsTR_w']},
                                     'body_schema': ['`device_uids` `array[string]` *(必須)* — 移動するデバイスの一意識別子のリスト。各値は '
                                                     'GET /groups/{group_id}/devices が返す device_id フィールドに対応します。']},
                                    {'method': 'GET',
                                     'path': '/agent-management/device-groups/v2/groups/{group_id}/groups',
                                     'summary': 'デバイスグループのメンバーであるデバイスグループの一覧を取得します。',
                                     'operation_id': 'listChildDeviceGroups',
                                     'sku': '',
                                     'desc': '直下の子グループのみを返します。Read Device Groups 権限（API Credentials ページ上の表記では Agent '
                                             'Management > Device and Device Group Management > '
                                             'Read）が必要です。この権限を持たない呼び出し元には 403 Forbidden レスポンスが返されます。',
                                     'path_params': [{'name': 'group_id',
                                                      'required': True,
                                                      'desc': '子グループを返す対象のデバイスグループの ID。',
                                                      'sample': 'Rr_WEJixSMKN19kOilTf-g'}],
                                     'query_params': [{'name': 'page',
                                                       'type': 'integer',
                                                       'required': False,
                                                       'default': '1',
                                                       'desc': '子グループ結果のページ番号（1 始まり）。',
                                                       'sample': ''},
                                                      {'name': 'page_size',
                                                       'type': 'integer',
                                                       'required': False,
                                                       'default': '1000',
                                                       'desc': '1 ページあたりの子グループレコード数。1 回のリクエストでサポートされる最大レコード数は 1000 です。',
                                                       'sample': ''},
                                                      {'name': 'order_by',
                                                       'type': 'string',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': '返される子デバイスグループの並び順。name '
                                                               'フィールドのみサポートされ、昇順（"name"）または降順（"name '
                                                               'desc"）を指定できます。並べ替えでは大文字と小文字は区別されません。',
                                                       'sample': ''},
                                                      {'name': 'name',
                                                       'type': 'string',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': '名前で子グループをフィルタリングします（部分一致）。',
                                                       'sample': ''}],
                                     'body': None,
                                     'body_schema': []},
                                    {'method': 'PUT',
                                     'path': '/agent-management/device-groups/v2/groups/{group_id}/groups',
                                     'summary': 'デバイスグループを別のデバイスグループへ移動します。',
                                     'operation_id': 'moveGroupToGroup',
                                     'sku': '',
                                     'desc': '指定したデバイスグループを、そのすべての子を含めてターゲットデバイスグループへ移動します。グループを自身の子孫へ移動することは許可されておらず、400 '
                                             'エラーになります。Manage Device Groups 権限（API Credentials ページ上の表記では Agent '
                                             'Management > Device and Device Group Management > '
                                             'Manage）が必要です。この権限を持たない呼び出し元には 403 Forbidden レスポンスが返されます。',
                                     'path_params': [{'name': 'group_id',
                                                      'required': True,
                                                      'desc': '移動先となる親デバイスグループの ID。移動対象のデバイスグループ（ソースグループ）は、リクエストボディの '
                                                              'id フィールドで別途指定します。',
                                                      'sample': '4Zh6VRUJQQauw_-AzxjtHw'}],
                                     'query_params': [],
                                     'body': {'id': '7tiwNJWKSJmE4OYRzwHwsw'},
                                     'body_schema': ['`id` `string` *(必須)* — 移動するデバイスグループ（ソースグループ）の一意識別子。パスパラメーター '
                                                     'group_id は、移動先の親グループを指定します。']}]},
 '🕹️ Device Commands': {'doc': 'cbx_device_commands.md',
                        'permissions': ['Device Commands -> Quarantine Device / Unquarantine Device',
                                        'Device Commands -> Scan Device',
                                        'Device Commands -> Restart Device',
                                        'Device Commands -> Run LiveUpdate'],
                        'endpoints': [{'method': 'POST',
                                       'path': '/agent-management/device-commands/v2/commands/allow',
                                       'summary': 'この API を使用すると、管理対象デバイスの隔離を解除できます。',
                                       'operation_id': 'unquarantineDevice',
                                       'sku': '',
                                       'desc': '指定した管理対象デバイスの隔離を解除し、ネットワークアクセスを復元するコマンドを開始します。この非同期操作は、正常に開始されると 202 '
                                               'Accepted レスポンスを返します。GET '
                                               '/agent-management/device-commands/v2/commands/{command_id} '
                                               'をポーリングし、返された command_state_ref を使用してコマンド実行のステータスを監視できます。',
                                       'path_params': [],
                                       'query_params': [],
                                       'body': {'device_ids': ['550e8400-e29b-41d4-a716-446655440000',
                                                               '732a3921-1191-447a-85b1-124b81093012']},
                                       'body_schema': ['`device_ids` `array[string]` *(必須)* — コマンドを送信するデバイス ID のリスト。最小 '
                                                       '1 件、最大 1000 件。']},
                                      {'method': 'POST',
                                       'path': '/agent-management/device-commands/v2/commands/contain',
                                       'summary': 'この API を使用すると、管理対象デバイスを隔離できます。',
                                       'operation_id': 'quarantineDevice',
                                       'sku': '',
                                       'desc': '指定した管理対象デバイスを隔離するコマンドを開始し、ネットワークアクセスを制限して脅威の拡散を防ぎます。この非同期操作は、正常に開始されると '
                                               '202 Accepted レスポンスを返します。GET '
                                               '/agent-management/device-commands/v2/commands/{command_id} '
                                               'をポーリングし、返された command_state_ref を使用してコマンド実行のステータスを監視できます。',
                                       'path_params': [],
                                       'query_params': [],
                                       'body': {'device_ids': ['550e8400-e29b-41d4-a716-446655440000',
                                                               '732a3921-1191-447a-85b1-124b81093012'],
                                                'org_unit_ids': ['org-12345', 'org-67890'],
                                                'payload': {'quarantine_host_group_name': 'isolated-hosts'},
                                                'is_recursive': False},
                                       'body_schema': ['`device_ids` `array[string]` — コマンドを送信するデバイス ID のリスト。最小 1 件、最大 '
                                                       '1000 件。',
                                                       '`org_unit_ids` `array[string]` — コマンドを送信する組織単位 ID のリスト。最小 1 '
                                                       '件、最大 1000 件。',
                                                       '`payload` `object` *(必須)* — 隔離コマンドの詳細を含むペイロード',
                                                       '`is_recursive` `boolean` — コマンドをサブユニットにも再帰的に適用するかどうか']},
                                      {'method': 'POST',
                                       'path': '/agent-management/device-commands/v2/commands/files/contain',
                                       'summary': 'この API を使用すると、管理対象デバイス上のファイルを隔離できます。',
                                       'operation_id': 'quarantineFile',
                                       'sku': '',
                                       'desc': '管理対象デバイス上の特定のファイルを隔離するコマンドを開始し、その実行とアクセスを防止します。この非同期操作は、正常に開始されると 202 '
                                               'Accepted レスポンスを返します。GET '
                                               '/agent-management/device-commands/v2/commands/{command_id} '
                                               'をポーリングし、返された command_state_ref を使用してコマンド実行のステータスを監視できます。',
                                       'path_params': [],
                                       'query_params': [],
                                       'body': {'device_ids': ['123e4567-e89b-12d3-a456-426614174000',
                                                               '987e6543-e21b-34d3-b456-426614174011'],
                                                'hashes': ['e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
                                                           '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92']},
                                       'body_schema': ['`device_ids` `array[string]` *(必須)* — コマンドを送信するデバイス ID のリスト。最小 '
                                                       '1 件、最大 1000 件。',
                                                       '`hashes` `array[string]` *(必須)* — '
                                                       'デバイス上で隔離するファイルハッシュのリスト。SHA-256 ハッシュ文字列を受け付けます。最小 1 件、最大 100 '
                                                       '件。']},
                                      {'method': 'POST',
                                       'path': '/agent-management/device-commands/v2/commands/restart',
                                       'summary': 'この API を使用すると、管理対象デバイスを再起動できます。',
                                       'operation_id': 'restartDevice',
                                       'sku': '',
                                       'desc': '指定した管理対象デバイスを再起動します。コマンドを受信するには、デバイスが現在オンラインである必要があります。この非同期操作は、正常に開始されると '
                                               '202 Accepted レスポンスを返します。GET '
                                               '/agent-management/device-commands/v2/commands/{command_id} '
                                               'をポーリングして返された command_state_ref を使用するか、Devices API（GET '
                                               '/agent-management/devices/{device_id}）でデバイスのステータスを監視してオンライン状態への復帰を確認することで、コマンド実行のステータスを監視できます。',
                                       'path_params': [],
                                       'query_params': [],
                                       'body': {'device_ids': ['123e4567-e89b-12d3-a456-426614174000',
                                                               '987e6543-e21b-34d3-b456-426614174011'],
                                                'payload': {'prompt_type': 'prompt',
                                                            'schedule_type': 'later',
                                                            'reason_type': 'remediation',
                                                            'message': 'Restarting device for remediation'}},
                                       'body_schema': ['`device_ids` `array[string]` *(必須)* — コマンドを送信するデバイス ID のリスト。最小 '
                                                       '1 件、最大 1000 件。',
                                                       '`payload` `object` *(必須)* — 再起動コマンドの詳細を含むペイロード']},
                                      {'method': 'POST',
                                       'path': '/agent-management/device-commands/v2/commands/scans/quick',
                                       'summary': 'この API を使用すると、管理対象デバイスでクイックスキャンを開始できます。',
                                       'operation_id': 'initiateDeviceScanQuick',
                                       'sku': '',
                                       'desc': '指定した管理対象デバイスでクイックスキャンを開始し、アクティブな脅威やマルウェアを検出します。この非同期操作は、正常に開始されると 202 '
                                               'Accepted レスポンスを返します。GET '
                                               '/agent-management/device-commands/v2/commands/{command_id} '
                                               'をポーリングし、返された command_state_ref を使用してコマンド実行のステータスを監視できます。',
                                       'path_params': [],
                                       'query_params': [],
                                       'body': {'device_ids': ['550e8400-e29b-41d4-a716-446655440000',
                                                               '732a3921-1191-447a-85b1-124b81093012'],
                                                'org_unit_ids': ['org-12345', 'org-67890'],
                                                'is_recursive': False},
                                       'body_schema': ['`device_ids` `array[string]` — コマンドを送信するデバイス ID のリスト。最小 1 件、最大 '
                                                       '1000 件。',
                                                       '`org_unit_ids` `array[string]` — コマンドを送信する組織単位 ID のリスト。最小 1 '
                                                       '件、最大 1000 件。',
                                                       '`is_recursive` `boolean` — コマンドをサブユニットにも再帰的に適用するかどうか']},
                                      {'method': 'POST',
                                       'path': '/agent-management/device-commands/v2/commands/scans/full',
                                       'summary': 'この API を使用すると、管理対象デバイスでフルスキャンを開始できます。',
                                       'operation_id': 'initiateDeviceScanFull',
                                       'sku': '',
                                       'desc': '指定した管理対象デバイスでフルスキャンを開始し、詳細なシステム分析と脅威検出を実行します。この非同期操作は、正常に開始されると 202 '
                                               'Accepted レスポンスを返します。GET '
                                               '/agent-management/device-commands/v2/commands/{command_id} '
                                               'をポーリングし、返された command_state_ref を使用してコマンド実行のステータスを監視できます。',
                                       'path_params': [],
                                       'query_params': [],
                                       'body': {'device_ids': ['550e8400-e29b-41d4-a716-446655440000',
                                                               '732a3921-1191-447a-85b1-124b81093012'],
                                                'org_unit_ids': ['org-12345', 'org-67890'],
                                                'is_recursive': False},
                                       'body_schema': ['`device_ids` `array[string]` — コマンドを送信するデバイス ID のリスト。最小 1 件、最大 '
                                                       '1000 件。',
                                                       '`org_unit_ids` `array[string]` — コマンドを送信する組織単位 ID のリスト。最小 1 '
                                                       '件、最大 1000 件。',
                                                       '`is_recursive` `boolean` — コマンドをサブユニットにも再帰的に適用するかどうか']},
                                      {'method': 'POST',
                                       'path': '/agent-management/device-commands/v2/commands/scans/custom',
                                       'summary': 'この API を使用すると、管理対象デバイスでカスタムスキャンを開始できます。',
                                       'operation_id': 'initiateDeviceScanCustom',
                                       'sku': '',
                                       'desc': 'カスタムスキャンパラメーターに基づき、指定した管理対象デバイスでカスタムスキャンを開始します。この非同期操作は、正常に開始されると 202 '
                                               'Accepted レスポンスを返します。GET '
                                               '/agent-management/device-commands/v2/commands/{command_id} '
                                               'をポーリングし、返された command_state_ref を使用してコマンド実行のステータスを監視できます。',
                                       'path_params': [],
                                       'query_params': [],
                                       'body': {'device_ids': ['550e8400-e29b-41d4-a716-446655440000',
                                                               '732a3921-1191-447a-85b1-124b81093012'],
                                                'org_unit_ids': ['org-12345', 'org-67890'],
                                                'is_recursive': False},
                                       'body_schema': ['`device_ids` `array[string]` — コマンドを送信するデバイス ID のリスト。最小 1 件、最大 '
                                                       '1000 件。',
                                                       '`org_unit_ids` `array[string]` — コマンドを送信する組織単位 ID のリスト。最小 1 '
                                                       '件、最大 1000 件。',
                                                       '`is_recursive` `boolean` — コマンドをサブユニットにも再帰的に適用するかどうか']},
                                      {'method': 'POST',
                                       'path': '/agent-management/device-commands/v2/commands/update-content',
                                       'summary': 'この API を使用すると、管理対象デバイスのセキュリティ定義とコンテンツを更新できます。',
                                       'operation_id': 'updateDeviceContent',
                                       'sku': '',
                                       'desc': '指定した管理対象デバイスのセキュリティ定義、ポリシー、シグネチャコンテンツを更新するコマンドを開始し、最新の保護状態を確保します。この非同期操作は、正常に開始されると '
                                               '202 Accepted レスポンスを返します。GET '
                                               '/agent-management/device-commands/v2/commands/{command_id} '
                                               'をポーリングし、返された command_state_ref を使用してコマンド実行のステータスを監視できます。',
                                       'path_params': [],
                                       'query_params': [],
                                       'body': {'device_ids': ['550e8400-e29b-41d4-a716-446655440000',
                                                               '732a3921-1191-447a-85b1-124b81093012'],
                                                'org_unit_ids': ['org-12345', 'org-67890'],
                                                'is_recursive': False},
                                       'body_schema': ['`device_ids` `array[string]` — コマンドを送信するデバイス ID のリスト。最小 1 件、最大 '
                                                       '1000 件。',
                                                       '`org_unit_ids` `array[string]` — コマンドを送信する組織単位 ID のリスト。最小 1 '
                                                       '件、最大 1000 件。',
                                                       '`is_recursive` `boolean` — コマンドをサブユニットにも再帰的に適用するかどうか']},
                                      {'method': 'GET',
                                       'path': '/agent-management/device-commands/v2/commands',
                                       'summary': 'この API を使用すると、すべてのコマンドの一覧を取得できます。',
                                       'operation_id': 'listDeviceCommands',
                                       'sku': '',
                                       'desc': 'オプションのクエリパラメーターでフィルタリングされた、すべてのデバイスコマンドのページ分割された一覧を取得します。',
                                       'path_params': [],
                                       'query_params': [{'name': 'page_size',
                                                         'type': 'integer',
                                                         'required': False,
                                                         'default': '100',
                                                         'desc': '1 回のリクエストで取得するレコード数。1 回のリクエストでサポートされる最大レコード数は 1000 '
                                                                 'です。',
                                                         'sample': ''},
                                                        {'name': 'page',
                                                         'type': 'integer',
                                                         'required': False,
                                                         'default': '1',
                                                         'desc': 'このフィールドが指定されていない場合は、最初のページが返されます。',
                                                         'sample': ''},
                                                        {'name': 'correlation_id',
                                                         'type': 'array',
                                                         'required': False,
                                                         'default': '',
                                                         'desc': '検索対象のコマンドに関連付けられた相関 ID。複数の相関 ID をカンマ区切りのリストで指定できます。',
                                                         'sample': ''},
                                                        {'name': 'device_id',
                                                         'type': 'array',
                                                         'required': False,
                                                         'default': '',
                                                         'desc': '検索対象の一意のデバイス識別子（UUID）。これは POST コマンドのボディで使用される UUID '
                                                                 '形式の device_ids に対応します。複数のデバイス ID をカンマ区切りのリストで指定できます。',
                                                         'sample': ''},
                                                        {'name': 'created',
                                                         'type': 'string',
                                                         'required': False,
                                                         'default': '',
                                                         'desc': 'ISO 8601 形式の作成日。先頭に > または < '
                                                                 'を付ける必要があります。範囲を定義するために、単一の文字列値内で複数の範囲式をカンマ区切りのリストとして指定できます。例: '
                                                                 '>2026-0…',
                                                         'sample': ''},
                                                        {'name': 'modified',
                                                         'type': 'string',
                                                         'required': False,
                                                         'default': '',
                                                         'desc': 'ISO 8601 形式の更新日。先頭に > または < '
                                                                 'を付ける必要があります。範囲を定義するために、単一の文字列値内で複数の範囲式をカンマ区切りのリストとして指定できます。例: '
                                                                 '>2026-…',
                                                         'sample': ''},
                                                        {'name': 'command_name',
                                                         'type': 'string',
                                                         'required': False,
                                                         'default': '',
                                                         'desc': '検索対象のコマンド名。有効な値: - FDR: Flight Data Recorder コマンド。- '
                                                                 'RESTART: 管理対象デバイスを再起動します。- QUARANTINE_DEVICE: '
                                                                 '指定したデバイスを隔離します。- UNQUARANTINE_DEVI…',
                                                         'sample': ''},
                                                        {'name': 'state',
                                                         'type': 'array',
                                                         'required': False,
                                                         'default': '',
                                                         'desc': '検索対象のコマンド実行状態。複数の状態をカンマ区切りのリストで指定できます。有効な値: - '
                                                                 'PENDING: コマンドはキューに入っていますが、まだ開始されていません。- IN_PROGRESS: '
                                                                 'コマンドは…',
                                                         'sample': ''}],
                                       'body': None,
                                       'body_schema': []},
                                      {'method': 'GET',
                                       'path': '/agent-management/device-commands/v2/commands/{command_id}',
                                       'summary': 'この API を使用すると、コマンドの詳細を取得できます。',
                                       'operation_id': 'getDeviceCommandDetails',
                                       'sku': '',
                                       'desc': '特定のデバイスコマンドの詳細情報と実行ステータスを取得します。',
                                       'path_params': [{'name': 'command_id',
                                                        'required': True,
                                                        'desc': '返すコマンド詳細の一意識別子。サーバーは、コマンドを発行する POST エンドポイントが返す UUID '
                                                                '形式の `command_state_ref`、または…が返す不透明な文字列 `id` '
                                                                'のいずれかを受け付けます…',
                                                        'sample': '-CCS-CMD-TD6TBi8mTiWO_4TiLZy91w'}],
                                       'query_params': [],
                                       'body': None,
                                       'body_schema': []}]},
 '📊 Reporting': {'doc': 'cbx_reporting.md',
                 'permissions': ['Reports -> View Endpoint Security', 'Reports -> Manage Endpoint Security'],
                 'endpoints': [{'method': 'GET',
                                'path': '/common/reporting/v1/report-templates',
                                'summary': 'この API を使用すると、レポートテンプレートの一覧を取得できます。',
                                'operation_id': 'listReportTemplates',
                                'sku': '',
                                'desc': 'レポートテンプレートの一覧を、その構成、フィルター、スケジュール情報とともに取得します。必要な権限: '
                                        'ses_view_reports。この権限を持たない呼び出し元には 403 Forbidden レスポンスが返されます。',
                                'path_params': [],
                                'query_params': [{'name': 'page',
                                                  'type': 'integer',
                                                  'required': False,
                                                  'default': '1',
                                                  'desc': '取得するページ番号（1 始まり）。',
                                                  'sample': ''},
                                                 {'name': 'page_size',
                                                  'type': 'integer',
                                                  'required': False,
                                                  'default': '25',
                                                  'desc': '1 ページあたりのレコード数。',
                                                  'sample': ''},
                                                 {'name': 'report_type_id',
                                                  'type': 'string',
                                                  'required': False,
                                                  'default': '',
                                                  'desc': 'レポートタイプでフィルタリングします',
                                                  'sample': ''},
                                                 {'name': 'report_format',
                                                  'type': 'string',
                                                  'required': False,
                                                  'default': '',
                                                  'desc': 'レポート形式でフィルタリングします。有効な値: `PDF`（Portable Document '
                                                          'Format）、`CSV`（カンマ区切り値）、`HTML`（HyperText Markup '
                                                          'Language）、`EMAIL`（ダウンロード…ではなくメール本文として送信…',
                                                  'sample': ''}],
                                'body': None,
                                'body_schema': []},
                               {'method': 'POST',
                                'path': '/common/reporting/v1/report-templates',
                                'summary': 'この API を使用すると、新しいレポートテンプレートを作成できます。',
                                'operation_id': 'createReportTemplate',
                                'sku': '',
                                'desc': '指定された構成で新しいレポートテンプレートを作成します。必要な権限: ses_manage_reports。この権限を持たない呼び出し元には 403 '
                                        'Forbidden レスポンスが返されます。',
                                'path_params': [],
                                'query_params': [],
                                'body': {'name': 'Default Weekly Report',
                                         'report_type_id': 'saep-weekly-report',
                                         'report_format': 'PDF',
                                         'schedule': {'schedule_type': 'WEEKLY',
                                                      'days_of_week': ['MONDAY', 'WEDNESDAY', 'FRIDAY'],
                                                      'repeat_frequency': 1},
                                         'report_recipients': [{'email': 'john.doe@broadcom.com',
                                                                'email_notification': True,
                                                                'email_as_attachment': False}],
                                         'schedule_at': '2026-12-01T10:00:00.000Z'},
                                'body_schema': ['`name` `string` *(必須)* — レポートテンプレートの名前',
                                                '`report_type_id` `string` *(必須)* — このテンプレートのレポートタイプの識別子',
                                                '`report_format` `string` *(必須)* — レポートを生成する形式。有効な値: `PDF`（Portable '
                                                'Document Format）、`CSV`（カンマ区切り値）、`HTML`（HyperText Markup Language）…',
                                                '`schedule` `any` *(必須)* — レポートを生成する頻度の構成',
                                                '`schedule_at` `string` — ISO 8601 UTC '
                                                '形式のスケジュール基準日時。`schedule.schedule_type` が '
                                                '`DAILY`、`WEEKLY`、`MONTHLY`、`QUARTERLY` '
                                                'の場合は必須です。`ONCE_A_DAY`、`VARIABLE`、…の場合は省略するか `null` を設定…',
                                                '`report_recipients` `array[object]` — '
                                                'レポート受信者の設定構成。受信者なしでテンプレートを作成する場合は、省略するか null を送信します。',
                                                '`report_filters` `object` — report_type_id が fw-comprehensive-report '
                                                'または ips-comprehensive-report '
                                                'の場合にのみリクエストボディに含めることができます。その他のレポートタイプで含めると 400 が返されます。省略…']},
                               {'method': 'GET',
                                'path': '/common/reporting/v1/reports',
                                'summary': 'この API を使用すると、生成済みレポートの一覧を取得できます。',
                                'operation_id': 'listReports',
                                'sku': '',
                                'desc': '生成済みのすべてのレポートの一覧を、ステータス、作成日、完了日とともに取得します。一覧レスポンスにはダウンロードリンクは含まれません。このエンドポイントが返す結果では、`include_download_link` '
                                        'パラメーターに関係なく `download_link` は常に `null` '
                                        'です。使用可能なダウンロードリンクを取得するには、`include_download_link=true` を指定して ID '
                                        'で個別のレポートを取得してください。ページネーション、およびレポートタイプとテンプレート ID によるフィルタリングをサポートします。必要な権限: '
                                        'ses_view_reports。この権限を持たない呼び出し元には 403 Forbidden レスポンスが返されます。',
                                'path_params': [],
                                'query_params': [{'name': 'page',
                                                  'type': 'integer',
                                                  'required': False,
                                                  'default': '1',
                                                  'desc': '取得するページ番号（1 始まり）。',
                                                  'sample': ''},
                                                 {'name': 'page_size',
                                                  'type': 'integer',
                                                  'required': False,
                                                  'default': '25',
                                                  'desc': '1 ページあたりのレコード数。',
                                                  'sample': ''},
                                                 {'name': 'report_type_id',
                                                  'type': 'string',
                                                  'required': False,
                                                  'default': '',
                                                  'desc': 'レポートタイプでフィルタリングします',
                                                  'sample': ''},
                                                 {'name': 'template_id',
                                                  'type': 'string',
                                                  'required': False,
                                                  'default': '',
                                                  'desc': 'レポートテンプレート ID でフィルタリングし、特定のテンプレートを使用して生成されたすべてのレポートを取得します。',
                                                  'sample': ''},
                                                 {'name': 'name',
                                                  'type': 'array',
                                                  'required': False,
                                                  'default': '',
                                                  'desc': 'レポートテンプレート名でフィルタリングします。複数の名前を検索する場合は、複数の値を指定します。',
                                                  'sample': ''},
                                                 {'name': 'format',
                                                  'type': 'string',
                                                  'required': False,
                                                  'default': '',
                                                  'desc': 'レポート形式でフィルタリングします。有効な値: `PDF`（Portable Document '
                                                          'Format）、`CSV`（カンマ区切り値）、`HTML`（HyperText Markup '
                                                          'Language）、`EMAIL`（ダウンロード…ではなくメール本文として送信…',
                                                  'sample': ''},
                                                 {'name': 'status',
                                                  'type': 'string',
                                                  'required': False,
                                                  'default': '',
                                                  'desc': 'レポートのステータスでフィルタリングします。指定可能な値: IN_PROGRESS, COMPLETED, '
                                                          'FAILED',
                                                  'sample': ''},
                                                 {'name': 'created_at',
                                                  'type': 'string',
                                                  'required': False,
                                                  'default': '',
                                                  'desc': '作成日でフィルタリングします。各トークンには > (以降) または < (以前) '
                                                          'をプレフィックスとして付け、日時は単一引用符で囲んだ ISO 8601 UTC '
                                                          '形式で指定する必要があります。範囲を指定する場合は、カンマ区切りで 2 つのトークンを指定します。例:…',
                                                  'sample': ''},
                                                 {'name': 'generation_mode',
                                                  'type': 'string',
                                                  'required': False,
                                                  'default': '',
                                                  'desc': '生成モードでフィルタリングします。指定可能な値: ad-hoc, scheduled',
                                                  'sample': ''},
                                                 {'name': 'language',
                                                  'type': 'string',
                                                  'required': False,
                                                  'default': '',
                                                  'desc': '言語/ロケール設定でフィルタリングします (例: 英語の場合は en)。',
                                                  'sample': ''}],
                                'body': None,
                                'body_schema': []},
                               {'method': 'POST',
                                'path': '/common/reporting/v1/report-templates/{template_id}/generate',
                                'summary': '既存のレポートテンプレートを ID で指定してレポートを生成する API です。',
                                'operation_id': 'generateReportByTemplateId',
                                'sku': '',
                                'desc': '既存のレポートテンプレートの設定を使用してレポートを生成します。テンプレート ID のみを必要とする簡易エンドポイントです。必要な権限: '
                                        'ses_manage_reports。この権限を持たない呼び出し元には 403 Forbidden レスポンスが返されます。',
                                'path_params': [{'name': 'template_id',
                                                 'required': True,
                                                 'desc': '生成に使用するレポートテンプレートの UUID。',
                                                 'sample': '3114e32c-bcb1-4bd7-b403-b73d7f297b40'}],
                                'query_params': [],
                                'body': None,
                                'body_schema': []},
                               {'method': 'GET',
                                'path': '/common/reporting/v1/reports/{report_id}',
                                'summary': '生成されたレポートのステータスとダウンロードリンクを取得する API です。',
                                'operation_id': 'getReportStatus',
                                'sku': '',
                                'desc': 'レポート生成ジョブのステータスとメタデータ (作成日、完了日、および任意のダウンロードリンクを含む) '
                                        'を取得します。include_download_link=true '
                                        'が指定され、かつレポートが完了している場合、レスポンスにダウンロードリンクが含まれます。必要な権限: '
                                        'ses_view_reports。この権限を持たない呼び出し元には 403 Forbidden レスポンスが返されます。',
                                'path_params': [{'name': 'report_id',
                                                 'required': True,
                                                 'desc': 'レポート生成ジョブの UUID。',
                                                 'sample': '7d16d3cd-6460-48bb-b2ff-3668afafd940'}],
                                'query_params': [{'name': 'include_download_link',
                                                  'type': 'boolean',
                                                  'required': False,
                                                  'default': 'false',
                                                  'desc': 'true '
                                                          'に設定すると、レポートの完了時にレスポンスにダウンロードリンクが含まれます。ダウンロードリンクは完了したレポートでのみ利用できます。',
                                                  'sample': ''}],
                                'body': None,
                                'body_schema': []},
                               {'method': 'GET',
                                'path': '/common/reporting/v1/report-templates/{template_id}',
                                'summary': '特定のレポートテンプレートを ID で取得する API です。',
                                'operation_id': 'getReportTemplate',
                                'sku': '',
                                'desc': '単一のレポートテンプレートを、その設定、フィルター、およびスケジュール情報とともに取得します。必要な権限: '
                                        'ses_view_reports。この権限を持たない呼び出し元には 403 Forbidden レスポンスが返されます。',
                                'path_params': [{'name': 'template_id',
                                                 'required': True,
                                                 'desc': '取得するレポートテンプレートの UUID。',
                                                 'sample': '3114e32c-bcb1-4bd7-b403-b73d7f297b40'}],
                                'query_params': [],
                                'body': None,
                                'body_schema': []},
                               {'method': 'PUT',
                                'path': '/common/reporting/v1/report-templates/{template_id}',
                                'summary': 'レポートテンプレートの設定を更新する API です。',
                                'operation_id': 'updateReportTemplate',
                                'sku': '',
                                'desc': '既存のレポートテンプレートの更新可能なフィールド (名前、スケジュール、レポート形式、レポート受信者設定) を置き換えます。PUT '
                                        'であるため、リクエストボディにはこれらのフィールドの完全な表現を含める必要があります。ボディで省略された更新可能なフィールドは、変更されずに保持されるのではなくリセットされます。このセット以外のフィールド '
                                        '(例: template_id, report_type_id) '
                                        'は読み取り専用であり、このエンドポイントでは変更できません。リクエストボディに他のフィールドが指定された場合、リクエストは 400 Bad Input '
                                        'エラーで失敗する可能性があります。テンプレート ID は URI パスに含める必要があります。必要な権限: '
                                        'ses_manage_reports。この権限を持たない呼び出し元…',
                                'path_params': [{'name': 'template_id',
                                                 'required': True,
                                                 'desc': '更新するレポートテンプレートの UUID。',
                                                 'sample': '3114e32c-bcb1-4bd7-b403-b73d7f297b40'}],
                                'query_params': [],
                                'body': {'name': 'Updated Weekly Report',
                                         'report_format': 'PDF',
                                         'schedule': {'schedule_type': 'WEEKLY',
                                                      'days_of_week': ['MONDAY', 'WEDNESDAY', 'FRIDAY'],
                                                      'repeat_frequency': 1},
                                         'schedule_at': '2026-12-01T10:00:00.000Z'},
                                'body_schema': ['`name` `string` *(必須)* — レポートテンプレートの名前',
                                                '`report_format` `string` *(必須)* — レポートを生成する形式。有効な値: `PDF`（Portable '
                                                'Document Format）、`CSV`（カンマ区切り値）、`HTML`（HyperText Markup Language）…',
                                                '`schedule` `any` *(必須)* — レポートを生成する頻度の構成',
                                                '`report_recipients` `array[object]` — レポート受信者の設定',
                                                '`schedule_at` `string` — ISO 8601 UTC 形式のスケジュール基準日時。schedule_type が '
                                                'DAILY, WEEKLY, MONTHLY, または QUARTERLY の場合は必須です。NONE, VARIABLE, '
                                                'TWO_PER_QUARTER, または ONCE_A_DAY の場合は省略するか null を設定します。',
                                                '`report_filters` `object` — レポートフィルターの設定。テンプレートの `report_type_id` が '
                                                '`fw-comprehensive-report` または `ips-comprehensive-report` '
                                                'の場合にのみ適用されます。`null` を送信すると、既存の…']},
                               {'method': 'DELETE',
                                'path': '/common/reporting/v1/report-templates/{template_id}',
                                'summary': 'レポートテンプレートを ID で指定して削除する API です。',
                                'operation_id': 'deleteReportTemplate',
                                'sku': '',
                                'desc': '指定された ID のレポートテンプレートを削除します。必要な権限: ses_manage_reports。この権限を持たない呼び出し元には 403 '
                                        'Forbidden レスポンスが返されます。',
                                'path_params': [{'name': 'template_id',
                                                 'required': True,
                                                 'desc': '削除するレポートテンプレートの UUID。',
                                                 'sample': '3114e32c-bcb1-4bd7-b403-b73d7f297b40'}],
                                'query_params': [],
                                'body': None,
                                'body_schema': []},
                               {'method': 'GET',
                                'path': '/common/reporting/v1/report-templates/{template_id}/reports',
                                'summary': '特定のレポートテンプレートを使用して生成されたレポートを取得する API です。',
                                'operation_id': 'listReportsByTemplateId',
                                'sku': '',
                                'desc': 'URL で指定されたレポートテンプレート ID を使用して生成されたレポートを一覧表示します。ページネーションに対応しています。必要な権限: '
                                        'ses_view_reports。この権限を持たない呼び出し元には 403 Forbidden レスポンスが返されます。',
                                'path_params': [{'name': 'template_id',
                                                 'required': True,
                                                 'desc': 'レポートテンプレートの UUID。',
                                                 'sample': '9c3ff049-9f7a-4b4f-8958-add0d3328884'}],
                                'query_params': [{'name': 'page',
                                                  'type': 'integer',
                                                  'required': False,
                                                  'default': '1',
                                                  'desc': '取得するページ番号（1 始まり）。',
                                                  'sample': ''},
                                                 {'name': 'page_size',
                                                  'type': 'integer',
                                                  'required': False,
                                                  'default': '25',
                                                  'desc': '1 ページあたりのレコード数。',
                                                  'sample': ''}],
                                'body': None,
                                'body_schema': []}]},
 '📤 Data Forwarder': {'doc': 'cbx_data_forwarder.md',
                      'permissions': ['Data Forwarder -> View', 'Data Forwarder -> Manage'],
                      'endpoints': [{'method': 'GET',
                                     'path': '/common/data-forwarders/v3/configs',
                                     'summary': '設定済みのすべてのフォワーダーの取得',
                                     'operation_id': 'listConfigs',
                                     'sku': '',
                                     'desc': '認証済みトークンに関連付けられた環境のすべてのフォワーダー設定を返します。無効化されたフォワーダーも含まれます。配列の順序は保証されません。Data '
                                             'Forwarder の `READ` 権限が必要です。',
                                     'path_params': [],
                                     'query_params': [],
                                     'body': None,
                                     'body_schema': []},
                                    {'method': 'POST',
                                     'path': '/common/data-forwarders/v3/configs',
                                     'summary': '新しいフォワーダー設定の作成',
                                     'operation_id': 'createConfig',
                                     'sku': '',
                                     'desc': '新しいフォワーダーを作成します。API '
                                             'は、指定された設定を使用してフォワーダーが指定のストレージに書き込めるかどうかを確認するための呼び出しを行います。指定されたバケットまたはコンテナーの '
                                             '`healthcheck` というサブフォルダーに、`healthcheck.json` '
                                             'というテストメッセージの書き込みを試行します。バケットの設定に誤りがある場合 (例: 権限やプリンシパル ARN '
                                             'の誤りなど)、または設定が正しくない場合 (例: バケットプレフィックスがポリシーで指定されたパスと一致しない)、API '
                                             'は何が誤っているか、およびその修正方法に関する情報を含む `400` エラーを返します。Data Forwarder…',
                                     'path_params': [],
                                     'query_params': [],
                                     'body': {'name': 'Alert Forwarder',
                                              'enabled': True,
                                              'type': 'alert',
                                              'version_constraint': '3.0.*',
                                              'destination_config': {'destination': 'aws_s3',
                                                                     's3_bucket_name': 'demo-bucket',
                                                                     's3_prefix': 'demo-alert'}},
                                     'body_schema': ['`name` `string` *(必須)* — 新しいフォワーダーに割り当てる表示名。',
                                                     '`enabled` `boolean` — フォワーダーを有効な状態で作成するかどうか。',
                                                     '`type` `string` *(必須)* — '
                                                     '転送するデータストリームの種類。種類ごとにデータストリームと利用可能な機能が決まります: - `alert`: Web '
                                                     'Traffic、Behavior などのすべてのアラートを含みます…',
                                                     '`version_constraint` `string` — '
                                                     '転送するデータのバージョンを制御するセマンティックバージョンパターン。省略時のデフォルト: alert=2.0.0, '
                                                     'event=2.0.0, forensicquery=2.0.0。メジャーバージョンは…である必要があります…',
                                                     '`destination_config` `oneOf` *(必須)* — '
                                                     '転送先固有のストレージ設定。必須および指定可能なフィールドは `destination` '
                                                     'の値によって異なります。別の種類に属するフィールドを指定すると…']},
                                    {'method': 'GET',
                                     'path': '/common/data-forwarders/v3/configs/{id}',
                                     'summary': '特定のフォワーダー設定の取得',
                                     'operation_id': 'getConfigById',
                                     'sku': '',
                                     'desc': '指定された ID のフォワーダー設定を返します。設定は認証済みトークンの環境に属している必要があり、そうでない場合は `404 Not '
                                             'Found` が返されます。Data Forwarder の `READ` 権限が必要です。',
                                     'path_params': [{'name': 'id',
                                                      'required': True,
                                                      'desc': 'フォワーダー設定の一意の識別子。',
                                                      'sample': '011b9d03-b12d-11ec-af42-ae26c44461dc'}],
                                     'query_params': [],
                                     'body': None,
                                     'body_schema': []},
                                    {'method': 'PUT',
                                     'path': '/common/data-forwarders/v3/configs/{id}',
                                     'summary': 'フォワーダー設定の更新',
                                     'operation_id': 'updateConfig',
                                     'sku': '',
                                     'desc': '既存のフォワーダー設定を置き換えます (完全な PUT — すべてのフィールドが必須)。`type` (例: `event`, `alert`) '
                                             'と `destination` (例: `aws_s3`, `azure_blob_storage`) '
                                             'は作成後に変更できません。現在の値をそのまま指定しないと、リクエストは `400` で拒否されます。その他のフィールド '
                                             '(バケット名、プレフィックス、ストレージアカウント、コンテナーを含む) は自由に変更できます。既存のフォワーダーを編集する場合、API '
                                             'は指定された設定を使用してフォワーダーが指定の転送先に書き込めるかどうかを確認するための追加の呼び出しを行います。テストメッセージの書き込みを試行します…',
                                     'path_params': [{'name': 'id',
                                                      'required': True,
                                                      'desc': 'フォワーダー設定の一意の識別子。',
                                                      'sample': '011b9d03-b12d-11ec-af42-ae26c44461dc'}],
                                     'query_params': [],
                                     'body': {'name': 'DevRelTest',
                                              'enabled': False,
                                              'type': 'event',
                                              'version_constraint': '2.0.0',
                                              'destination_config': {'destination': 'aws_s3',
                                                                     's3_bucket_name': 'DevRelTestBucket',
                                                                     's3_prefix': 'test'}},
                                     'body_schema': ['`name` `string` *(必須)* — フォワーダーの更新後の名前。',
                                                     '`enabled` `boolean` *(必須)* — フォワーダーを有効にするかどうか。',
                                                     '`type` `string` *(必須)* — '
                                                     '転送するデータストリームの種類。種類ごとにデータストリームと利用可能な機能が決まります: - `alert`: Web '
                                                     'Traffic、Behavior などのすべてのアラートを含みます…',
                                                     '`version_constraint` `string` *(必須)* — '
                                                     '転送するデータのバージョンを制御する、更新後のセマンティックバージョンパターン。有効な形式: `N.N.N`, `N.N.*`, '
                                                     '`N.*.*`。',
                                                     '`destination_config` `oneOf` *(必須)* — '
                                                     '転送先固有のストレージ設定。必須および指定可能なフィールドは `destination` '
                                                     'の値によって異なります。別の種類に属するフィールドを指定すると…']},
                                    {'method': 'DELETE',
                                     'path': '/common/data-forwarders/v3/configs/{id}',
                                     'summary': 'フォワーダー設定の削除',
                                     'operation_id': 'deleteConfig',
                                     'sku': '',
                                     'desc': 'フォワーダー設定を ID で指定して完全に削除します。関連付けられたすべてのフィルターも設定とともに自動的に削除されます。データ転送は削除後約 '
                                             '1～2 分以内に停止します。削除は元に戻せません。削除イベントは監査ログに記録されます。',
                                     'path_params': [{'name': 'id',
                                                      'required': True,
                                                      'desc': 'フォワーダー設定の一意の識別子。',
                                                      'sample': '011b9d03-b12d-11ec-af42-ae26c44461dc'}],
                                     'query_params': [],
                                     'body': None,
                                     'body_schema': []},
                                    {'method': 'POST',
                                     'path': '/common/data-forwarders/v3/validate-filter',
                                     'summary': 'フィルターの検証',
                                     'operation_id': 'validateFilter',
                                     'sku': '',
                                     'desc': 'フィルターが互換性のあるクエリ構文、フィールド名、および値を使用しているかどうかを検証します。このエンドポイントはフィルターを作成または保存せず、有効性の確認のみを行います。フィルターは '
                                             '`event` タイプのフォワーダーにのみ適用されます。フィルターの作成時または更新時にクエリが受け入れられるようにするには、対象の設定と同じ '
                                             '`version_constraint` '
                                             'の値を指定してください。設定で使用されているバージョンとは異なるバージョンに対して検証した場合、フィルターの作成時または更新時にクエリが通ることは保証されません。Data '
                                             'Forwarder の `MANAGE` 権限が必要です。',
                                     'path_params': [],
                                     'query_params': [],
                                     'body': {'name': 'Example Filter',
                                              'action': 'INCLUDE',
                                              'enabled': True,
                                              'query': 'device_os:WINDOWS AND alert_id:*',
                                              'version_constraint': '2.0.0'},
                                     'body_schema': ['`name` `string` *(必須)* — 検証対象のフィルターの名前。',
                                                     '`enabled` `boolean` — フィルターを有効にするかどうか。',
                                                     '`action` `string` *(必須)* — 検証するアクション。一致したイベントを転送する場合は '
                                                     '`INCLUDE`、破棄する場合は `EXCLUDE` を指定します。(enum: `INCLUDE`, `EXCLUDE`)',
                                                     '`query` `string` *(必須)* — 指定されたスキーマバージョンに対して検証するクエリ。',
                                                     '`version_constraint` `string` — '
                                                     'フィルターの検証に使用するスキーマバージョン。指定しない場合、API はサポートされている最も低いスキーマバージョン '
                                                     '(2.0.0) に対して検証します。有効な形式: `N.N.N`, `N.N.*`…']},
                                    {'method': 'GET',
                                     'path': '/common/data-forwarders/v3/configs/{id}/health-check',
                                     'summary': 'フォワーダー設定のヘルスチェックの実行',
                                     'operation_id': 'getHealthCheckByConfigId',
                                     'sku': '',
                                     'desc': 'フォワーダーのヘルスチェックを実行し、既存の設定を使用してフォワーダーが指定の S3 バケット、GCS バケット、または Azure '
                                             'コンテナーに書き込めるかどうかを判定します。ヘルスチェックにより、バケットの設定に誤りがあるか (例: 権限やプリンシパル ARN '
                                             'の誤りなど)、設定が正しくないか (例: '
                                             'バケットプレフィックスがポリシーで指定されたパスと一致しない)、またはフォワーダーが想定どおりに動作しているかを確認できます。成功した場合、ヘルスチェックはバケットの '
                                             '`healthcheck` というサブフォルダー (または Azure コンテナー) に `healthcheck.json` '
                                             'というテストメッセージの書き込みを試行し…',
                                     'path_params': [{'name': 'id',
                                                      'required': True,
                                                      'desc': 'フォワーダー設定の一意の識別子。',
                                                      'sample': '011b9d03-b12d-11ec-af42-ae26c44461dc'}],
                                     'query_params': [],
                                     'body': None,
                                     'body_schema': []},
                                    {'method': 'GET',
                                     'path': '/common/data-forwarders/v3/configs/{id}/filters',
                                     'summary': '設定のすべてのフィルターの取得',
                                     'operation_id': 'listFiltersByConfig',
                                     'sku': '',
                                     'desc': '指定されたフォワーダー設定のすべてのフィルターを返します。1 つの設定でサポートされるフィルターは最大 25 個です。フィルターは '
                                             '`event` タイプのフォワーダーにのみ適用されます。`alert` または `forensicquery` '
                                             'の設定に対してこのエンドポイントを呼び出すと、空の配列が返されます。',
                                     'path_params': [{'name': 'id',
                                                      'required': True,
                                                      'desc': 'フォワーダー設定の一意の識別子。',
                                                      'sample': '011b9d03-b12d-11ec-af42-ae26c44461dc'}],
                                     'query_params': [],
                                     'body': None,
                                     'body_schema': []},
                                    {'method': 'POST',
                                     'path': '/common/data-forwarders/v3/configs/{id}/filters',
                                     'summary': '設定のフィルターの作成',
                                     'operation_id': 'createFilter',
                                     'sku': '',
                                     'desc': '指定された設定に対して、データを転送対象に含めるか除外するかを指定するフィルターを作成します。同じ設定 ID に対する複数のフィルターには論理 '
                                             'OR が適用され、分離された複雑な条件をサポートします。例えば、2 つの包含フィルターと 2 つの除外フィルターは '
                                             '`(IncludeFilter1 OR IncludeFilter2) AND NOT (ExcludeFilter1 OR '
                                             'ExcludeFilter2)` として適用されます。複数のフィルターを一度に作成する場合は、`bulk` または '
                                             '`bulk-overwrite` エンドポイントを参照してください。フィルターは `event` タイプのフォワーダーにのみ適用されます。1 '
                                             'つの設定でサポートされるフィルターは最大 25 個です。上限にすでに達している場合にフィルターを作成しようとすると…',
                                     'path_params': [{'name': 'id',
                                                      'required': True,
                                                      'desc': 'フォワーダー設定の一意の識別子。',
                                                      'sample': '011b9d03-b12d-11ec-af42-ae26c44461dc'}],
                                     'query_params': [],
                                     'body': {'name': 'Example Filter',
                                              'action': 'INCLUDE',
                                              'enabled': True,
                                              'query': 'device_os:WINDOWS AND alert_id:*'},
                                     'body_schema': ['`name` `string` *(必須)* — 新しいフィルターに割り当てる表示名。',
                                                     '`enabled` `boolean` — 作成時にフィルターを有効にするかどうか。デフォルトは `true` です。',
                                                     '`action` `string` *(必須)* — 一致したイベントを転送する (`INCLUDE`) か破棄する '
                                                     '(`EXCLUDE`) かを決定します。(enum: `INCLUDE`, `EXCLUDE`)',
                                                     '`query` `string` *(必須)* — 受信データと照合するクエリ。Data Forwarder '
                                                     'は個々のイベント単位でフィルタリングを行うため、クエリに異なるイベントタイプのフィールドを含めることはできません。']},
                                    {'method': 'POST',
                                     'path': '/common/data-forwarders/v3/configs/{id}/filters/bulk',
                                     'summary': '設定のフィルターの一括作成または更新',
                                     'operation_id': 'bulkCreateOrUpdateFilters',
                                     'sku': '',
                                     'desc': '指定された設定に対して複数のフィルターを作成または更新します。`id` フィールドの有無によって作成と更新が区別されます。`id` '
                                             'を含む項目は更新、`id` を含まない項目は作成として扱われます。同じ設定 ID に対する複数のフィルターには論理 OR '
                                             'が適用され、分離された複雑な条件をサポートします: `(IncludeFilter1 OR IncludeFilter2) AND NOT '
                                             '(ExcludeFilter1 OR '
                                             'ExcludeFilter2)`。バックエンドの制約により、アトミック性を確保するため、一括リクエストは合計最大 25 '
                                             '項目に制限されます。フィルターは `event` タイプのフォワーダーにのみ適用されます。フィルタークエリは検証され…',
                                     'path_params': [{'name': 'id',
                                                      'required': True,
                                                      'desc': 'フォワーダー設定の一意の識別子。',
                                                      'sample': '011b9d03-b12d-11ec-af42-ae26c44461dc'}],
                                     'query_params': [],
                                     'body': [{'action': 'INCLUDE',
                                               'enabled': True,
                                               'name': 'Example Filter',
                                               'query': 'device_os:LINUX AND alert_id:*',
                                               'id': 'f13e6723-7779-4fdc-a26e-5a95e66be891'},
                                              {'action': 'EXCLUDE',
                                               'enabled': True,
                                               'name': 'Example EXCLUDE Filter',
                                               'query': 'device_os:MAC'}],
                                     'body_schema': ['`[ ]` `array[any]`']},
                                    {'method': 'POST',
                                     'path': '/common/data-forwarders/v3/configs/{id}/filters/bulk-overwrite',
                                     'summary': '設定のすべてのフィルターの一括置換',
                                     'operation_id': 'bulkReplaceFilters',
                                     'sku': '',
                                     'desc': '指定された設定の既存のフィルターをすべて、指定されたセットで置き換えます。リクエストボディに含まれていない既存のフィルターは削除されます。バックエンドの制約により、アトミック性を確保するため、一括リクエストは合計最大 '
                                             '25 項目に制限されます。フィルターは `event` タイプのフォワーダーにのみ適用されます。フィルタークエリは書き込み時に対象の設定自身の '
                                             '`version_constraint` に対して検証されます。フィルター自体には `version_constraint` '
                                             'フィールドはありません。送信前にクエリを事前検証するには、…と同じ `version_constraint` の値を指定して `POST '
                                             '/validate-filter` を呼び出します…',
                                     'path_params': [{'name': 'id',
                                                      'required': True,
                                                      'desc': 'フォワーダー設定の一意の識別子。',
                                                      'sample': '011b9d03-b12d-11ec-af42-ae26c44461dc'}],
                                     'query_params': [],
                                     'body': [{'name': 'Block Malicious Processes',
                                               'action': 'EXCLUDE',
                                               'query': 'process_reputation:1_KNOWN_BAD',
                                               'enabled': True},
                                              {'name': 'Windows Events Only',
                                               'action': 'INCLUDE',
                                               'query': 'device_os:WINDOWS',
                                               'enabled': True}],
                                     'body_schema': ['`[ ]` `array[any]`']},
                                    {'method': 'GET',
                                     'path': '/common/data-forwarders/v3/configs/{id}/filters/{filterId}',
                                     'summary': '特定のフィルターの ID による取得',
                                     'operation_id': 'getFilterById',
                                     'sku': '',
                                     'desc': '指定されたフォワーダー設定について、指定された ID のフィルターを返します。設定またはフィルターのいずれかが見つからない場合は `404` '
                                             'を返します。',
                                     'path_params': [{'name': 'id',
                                                      'required': True,
                                                      'desc': 'フォワーダー設定の一意の識別子。',
                                                      'sample': '011b9d03-b12d-11ec-af42-ae26c44461dc'},
                                                     {'name': 'filterId',
                                                      'required': True,
                                                      'desc': 'フィルターの一意の識別子。',
                                                      'sample': 'f13e6723-7779-4fdc-a26e-5a95e66be891'}],
                                     'query_params': [],
                                     'body': None,
                                     'body_schema': []},
                                    {'method': 'PUT',
                                     'path': '/common/data-forwarders/v3/configs/{id}/filters/{filterId}',
                                     'summary': 'フィルターの更新',
                                     'operation_id': 'updateFilter',
                                     'sku': '',
                                     'desc': '既存のフィルターを置き換えます (完全な PUT — `id` 以外のすべてのフィールドが必須)。更新対象のフィルターは `filterId` '
                                             'パスパラメーターで識別されます。リクエストボディに `id` フィールドが含まれていても無視されます。`create_time` と '
                                             '`update_time` は常にバックエンドで管理され、ボディに含まれていても通知なしに無視されます。フィルターは `event` '
                                             'タイプのフォワーダーにのみ適用されます。更新後のクエリは対象の設定自身の `version_constraint` '
                                             'に対して検証されます。フィルター自体には `version_constraint` '
                                             'フィールドはありません。更新前にクエリを事前検証するには、`POST /validate-filter` を…とともに呼び出します…',
                                     'path_params': [{'name': 'id',
                                                      'required': True,
                                                      'desc': 'フォワーダー設定の一意の識別子。',
                                                      'sample': '011b9d03-b12d-11ec-af42-ae26c44461dc'},
                                                     {'name': 'filterId',
                                                      'required': True,
                                                      'desc': 'フィルターの一意の識別子。',
                                                      'sample': 'f13e6723-7779-4fdc-a26e-5a95e66be891'}],
                                     'query_params': [],
                                     'body': {'id': 'f13e6723-7779-4fdc-a26e-5a95e66be891',
                                              'name': 'Example Filter - Edited',
                                              'action': 'INCLUDE',
                                              'enabled': True,
                                              'query': 'device_os:WINDOWS AND alert_id:* AND '
                                                       'process_reputation:1_KNOWN_BAD'},
                                     'body_schema': ['`id` `string` — フィルターの UUID。任意指定です。サーバーは `filterId` '
                                                     'パスパラメーターを使用してフィルターを識別し、この値を通知なしに上書きします。',
                                                     '`name` `string` *(必須)* — フィルターの更新後の表示名。',
                                                     '`enabled` `boolean` *(必須)* — 更新後にフィルターを有効にするかどうか。',
                                                     '`action` `string` *(必須)* — 一致したイベントをフィルターで含めるか除外するか。(enum: '
                                                     '`INCLUDE`, `EXCLUDE`)',
                                                     '`query` `string` *(必須)* — 受信データと照合する更新後のクエリ。']},
                                    {'method': 'DELETE',
                                     'path': '/common/data-forwarders/v3/configs/{id}/filters/{filterId}',
                                     'summary': 'フィルターの削除',
                                     'operation_id': 'deleteFilter',
                                     'sku': '',
                                     'desc': '指定されたフォワーダー設定からフィルターを完全に削除します。フィルターは `event` タイプのフォワーダーにのみ適用されます。Data '
                                             'Forwarder の `MANAGE` 権限が必要です。',
                                     'path_params': [{'name': 'id',
                                                      'required': True,
                                                      'desc': 'フォワーダー設定の一意の識別子。',
                                                      'sample': '011b9d03-b12d-11ec-af42-ae26c44461dc'},
                                                     {'name': 'filterId',
                                                      'required': True,
                                                      'desc': 'フィルターの一意の識別子。',
                                                      'sample': 'f13e6723-7779-4fdc-a26e-5a95e66be891'}],
                                     'query_params': [],
                                     'body': None,
                                     'body_schema': []},
                                    {'method': 'GET',
                                     'path': '/common/data-forwarders/v3/schemas/events',
                                     'summary': 'フィルタ可能なイベントスキーマの取得',
                                     'operation_id': 'getFilterableSchema',
                                     'sku': '',
                                     'desc': 'エンドポイントイベントのフィルタ可能なフィールド、その型、および利用可能な enum 値を記述した JSON '
                                             'スキーマドキュメントを返します。`version_constraint` を指定した場合、API '
                                             'はそのスキーマバージョンで利用可能なすべてのフィルタ可能フィールドを返します。指定しない場合は、サポートされている最も低いスキーマバージョン（2.0.0）のフィルタ可能フィールドを返します。このエンドポイントは公開されており、認証トークンは不要です。',
                                     'path_params': [],
                                     'query_params': [{'name': 'version_constraint',
                                                       'type': 'string',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'フィルタ可能フィールドを取得するスキーマバージョン（例: '
                                                               '`2.0.0`、`2.1.0`、`2.2.0`）。指定しない場合は、サポートされている最も低いスキーマバージョンが使用されます。有効な形式: '
                                                               '`N.N.N`、`N.N.*`、`N.*.*`。',
                                                       'sample': ''}],
                                     'body': None,
                                     'body_schema': []},
                                    {'method': 'GET',
                                     'path': '/common/data-forwarders/v3/versions',
                                     'summary': '利用可能なフォワーダーバージョンの取得',
                                     'operation_id': 'getAvailableVersions',
                                     'sku': '',
                                     'desc': '利用可能なすべての GA '
                                             'フォワーダースキーマバージョンを返します（任意でタイプによる絞り込みが可能）。バージョンは昇順で返されます。リリース済みのバージョンのみが含まれ、非推奨のバージョンは除外されます。新しい設定の '
                                             '`version_constraint` を選択するには、該当するタイプの配列内で最新のバージョンを選んでください。Data Forwarder '
                                             'の `READ` 権限が必要です。',
                                     'path_params': [],
                                     'query_params': [{'name': 'type',
                                                       'type': 'string',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': '絞り込みに使用するフォワーダーのタイプ。省略した場合は、すべてのタイプのバージョンが返されます。',
                                                       'sample': ''}],
                                     'body': None,
                                     'body_schema': []}]},
 '🧭 TI: TAXII 2.1': {'doc': 'cbx_taxii21.md',
                     'permissions': ['Threat Intel -> Read'],
                     'endpoints': [{'method': 'GET',
                                    'path': '/common/threat-intel/v1/taxii2',
                                    'summary': 'TAXII サーバーディスカバリー',
                                    'operation_id': 'getTAXII21Discovery',
                                    'sku': '',
                                    'desc': 'TAXII サーバーのタイトル、説明、および API ルート URL の一覧を返します。**必要な権限:** '
                                            '`ses_threat_intel_api_access` OAuth2 スコープ（または HTTP Basic '
                                            '認証）。トークンにこのスコープがない呼び出し元には 403 Forbidden レスポンスが返されます。**cURL の例:** `curl -u '
                                            '<client_id>:<client_secret> -H "Content-Type: '
                                            'application/taxii+json;version=2.1" '
                                            'https://api.us.security.com/common/threat-intel/v1/taxii2`',
                                    'path_params': [],
                                    'query_params': [],
                                    'body': None,
                                    'body_schema': []},
                                   {'method': 'GET',
                                    'path': '/common/threat-intel/v1/taxii2/feeds/collections',
                                    'summary': 'コレクション一覧の取得',
                                    'operation_id': 'listTAXII21Collections',
                                    'sku': '',
                                    'desc': '利用可能なすべての TAXII 2.1 '
                                            'データコレクション（脅威インテリジェンスフィード）の一覧を返します。すべてのコレクションは読み取り専用です。このエンドポイントはコレクションの完全な一覧を単一のレスポンスで返し、ページネーションはサポートされていません。コレクションのセットは現在 '
                                            '3 つ（`threat-alert`、`malicious-uri`、`malicious-file`）に固定されています。**必要な権限:** '
                                            '`ses_threat_intel_api_access` OAuth2 スコープ（または HTTP Basic '
                                            '認証）。トークンにこのスコープがない呼び出し元には 403 Forbidden レスポンスが返されます。**Python の例:** '
                                            '`import requests; response = '
                                            'requests.get("https://api.us.security.com/common/threat-intel/v…',
                                    'path_params': [],
                                    'query_params': [],
                                    'body': None,
                                    'body_schema': []},
                                   {'method': 'GET',
                                    'path': '/common/threat-intel/v1/taxii2/feeds/collections/{collection_id}/objects',
                                    'summary': 'コレクションオブジェクトの取得（STIX 2.1 Bundle）',
                                    'operation_id': 'getTAXII21Objects',
                                    'sku': '',
                                    'desc': 'コレクションの STIX 2.1 バンドルを返します。**ページサイズ:** 各レスポンスに含まれる STIX オブジェクトは最大 **2000 '
                                            '件** です。この上限はサーバー側で強制される固定値であり、`limit` クエリパラメータは存在しません。クライアントが送信した `limit` '
                                            'の値は通知なく無視されます。**一括取り込みループ:** 1. 最初のリクエストは `added_after` '
                                            'のみを指定して送信します（`next` は省略）。2. レスポンスに `more: true` が含まれる場合は、レスポンス本文の `next` '
                                            'の値を `next` に設定して次のリクエストを送信します。3. レスポンスで `more: false` になるか、`next` '
                                            'が存在しない/null になるまで繰り返します。これが最終ページであることを示します。**`next` のセマンティクス:** `next`…',
                                    'path_params': [{'name': 'collection_id',
                                                     'required': True,
                                                     'desc': 'オブジェクトを取得するコレクションの名前。有効な値: `threat-alert`（IoC '
                                                             'バンドルレポート、週あたり約 1 件の新規レポート）、`malicious-uri`（高信頼度の悪意ある '
                                                             'URL/ドメインインジケーター、約数千件/…',
                                                     'sample': 'threat-alert'}],
                                    'query_params': [{'name': 'added_after',
                                                      'type': 'string',
                                                      'required': False,
                                                      'default': '',
                                                      'desc': 'このタイムスタンプ以降に追加されたオブジェクトのみを返します（マイクロ秒精度の ISO 8601、例: '
                                                              '`2026-01-01T00:00:00.0000000Z`）。省略した場合、サーバーは…の時点から過去 30 '
                                                              '日間のローリング期間を適用します…',
                                                      'sample': ''},
                                                     {'name': 'next',
                                                      'type': 'string',
                                                      'required': False,
                                                      'default': '',
                                                      'desc': '一括取り込みループ用のページネーションカーソル。最初のリクエストでは省略します。後続のリクエストでは、前のレスポンスの '
                                                              '`next` の値を設定します。これは 1 始まりのレコードオフセットで、200 ずつ増加…',
                                                      'sample': ''}],
                                    'body': None,
                                    'body_schema': []}]},
 '🔗 TI: Data Related': {'doc': 'cbx_ti_data_related.md',
                        'permissions': ['Threat Intel -> Read'],
                        'endpoints': [{'method': 'GET',
                                       'path': '/common/threat-intel/v1/related/file/{file_sha256}',
                                       'summary': '指定したファイルに関連するファイルまたはネットワーク情報を提供する API です。',
                                       'operation_id': 'listFileRelated',
                                       'sku': '',
                                       'desc': '指定したファイルの SHA-256 '
                                               'に関連するファイルおよびネットワークのインジケーターを返します。関連するネットワークインジケーターおよび関連ファイルの SHA-256 '
                                               '値の配列が含まれ、それぞれ関連タイプ（例: byThreatActor、byProcessChain）ごとにグループ化されます。必要な権限: '
                                               'ses_threat_intel_api_access。この権限を持たない呼び出し元には 403 Forbidden '
                                               'レスポンスが返されます。',
                                       'path_params': [{'name': 'file_sha256',
                                                        'required': True,
                                                        'desc': '検索対象ファイルの SHA-256 ハッシュ',
                                                        'sample': 'eec3f761f7eabe9ed569f39e896be24c9bbb8861b15dbde1b3d539505cd9dd8d'}],
                                       'query_params': [{'name': 'page',
                                                         'type': 'integer',
                                                         'required': False,
                                                         'default': '1',
                                                         'desc': 'related 配列のページネーションに使用するページ番号（1 始まり、デフォルト: 1）',
                                                         'sample': ''},
                                                        {'name': 'page_size',
                                                         'type': 'integer',
                                                         'required': False,
                                                         'default': '50',
                                                         'desc': '1 ページあたりに返す関連グループの数（デフォルト: 50、最大: 200）',
                                                         'sample': ''}],
                                       'body': None,
                                       'body_schema': []},
                                      {'method': 'GET',
                                       'path': '/common/threat-intel/v1/related/network/{network}',
                                       'summary': '指定したネットワークドメインまたは IP アドレスに関連するファイルまたはネットワーク情報を提供する API です。',
                                       'operation_id': 'listNetworkRelated',
                                       'sku': '',
                                       'desc': '指定したネットワークドメインまたは IP アドレスに関連するファイルおよびネットワークのインジケーターを返します。関連する IOC '
                                               '値は関連タイプ（例: byThreatActor、bySignature）ごとにグループ化されます。必要な権限: '
                                               'ses_threat_intel_api_access。この権限を持たない呼び出し元には 403 Forbidden '
                                               'レスポンスが返されます。',
                                       'path_params': [{'name': 'network',
                                                        'required': True,
                                                        'desc': '検索対象のネットワークインジケーター。受け付ける形式: FQDN（例: '
                                                                'example.com、sub.example.com）、完全な '
                                                                'URL（スキームは任意。ドメインが抽出され、パスは無視されます）、またはパブリック IPv4/IPv6 '
                                                                'アドレス。IPv6 は…',
                                                        'sample': '145.249.105.165'}],
                                       'query_params': [{'name': 'page',
                                                         'type': 'integer',
                                                         'required': False,
                                                         'default': '1',
                                                         'desc': 'related 配列のページネーションに使用するページ番号（1 始まり、デフォルト: 1）',
                                                         'sample': ''},
                                                        {'name': 'page_size',
                                                         'type': 'integer',
                                                         'required': False,
                                                         'default': '50',
                                                         'desc': '1 ページあたりに返す関連グループの数（デフォルト: 50、最大: 200）',
                                                         'sample': ''}],
                                       'body': None,
                                       'body_schema': []}]},
 '💡 TI: Insight': {'doc': 'cbx_ti_insight.md',
                   'permissions': ['Threat Intel -> Read'],
                   'endpoints': [{'method': 'GET',
                                  'path': '/common/threat-intel/v1/insight/file/{file_sha256}',
                                  'summary': '指定したファイルの sha256 に対するファイルインサイトのエンリッチメントを返す API です。',
                                  'operation_id': 'getFileInsight',
                                  'sku': '',
                                  'desc': '指定したファイルの SHA-256 '
                                          'ハッシュに対する脅威インテリジェンスのエンリッチメントを返します。レピュテーション、信頼度スコア、普及度帯、標的となった組織、関連する脅威アクター、およびリンクされた参照情報が含まれます。必要な権限: '
                                          'ses_threat_intel_api_access。この権限を持たない呼び出し元には 403 Forbidden レスポンスが返されます。',
                                  'path_params': [{'name': 'file_sha256',
                                                   'required': True,
                                                   'desc': '検索対象ファイルの SHA-256 ハッシュ',
                                                   'sample': 'f6afa84b0847414220bb15517b8b5e2c505b64b53efbba73b753379c66ac5017'}],
                                  'query_params': [],
                                  'body': None,
                                  'body_schema': []},
                                 {'method': 'GET',
                                  'path': '/common/threat-intel/v1/insight/network',
                                  'summary': '指定した URL、ドメイン、または IP に対するネットワークエンリッチメントを返す API です。',
                                  'operation_id': 'getNetworkInsight',
                                  'sku': '',
                                  'desc': '指定した URL、ドメイン、または IP '
                                          'アドレスに対する脅威インテリジェンスのエンリッチメントを返します。レピュテーション、信頼度スコア、普及度、カテゴリ分類、脅威リスクレベル、標的となった組織、および関連する脅威アクターが含まれます。必要な権限: '
                                          'ses_threat_intel_api_access。この権限を持たない呼び出し元には 403 Forbidden レスポンスが返されます。',
                                  'path_params': [],
                                  'query_params': [{'name': 'network',
                                                    'type': 'string',
                                                    'required': True,
                                                    'default': '',
                                                    'desc': "検索対象の完全な URL、ドメイン名、または IP アドレス。【注意】完全な URL には '/' "
                                                            '文字が含まれ、パスセグメントとして渡すとリクエストのルーティングが壊れてしまうため、この値はパスセグメントではなくクエリパラメータとして渡されます…',
                                                    'sample': '115.55.57.208'}],
                                  'body': None,
                                  'body_schema': []},
                                 {'method': 'GET',
                                  'path': '/common/threat-intel/v1/insight/network/{network}',
                                  'summary': '【パス形式】指定した URL、ドメイン、または IP のネットワークエンリッチメントを返します（実環境で確認された形式）。',
                                  'operation_id': 'getNetworkInsight (path)',
                                  'sku': '',
                                  'desc': 'md ではクエリパラメータ形式（?network=）ですが、実環境では "Path must be /api/cbx-threat-intel/{api}/{ioc_type}/{ioc_value}" '
                                          'となり 400 が返るため、IOC をパスに含める形式を追加しています。値は URL エンコードせずに送信します（\'/\' を含む URL も可）。',
                                  'path_params': [{'name': 'network', 'type': 'string', 'required': True,
                                                   'desc': '検索対象の URL、ドメイン名、または IP アドレス（URL エンコード不要）',
                                                   'sample': '145.249.105.165'}],
                                  'query_params': [],
                                  'body': None,
                                  'body_schema': []},
                                 {'method': 'GET',
                                  'path': '/common/threat-intel/v1/insight/network/history',
                                  'summary': '指定した URL、ドメイン、または IP のカテゴリ分類およびリスクレベルの履歴を返す API です。',
                                  'operation_id': 'listNetworkInsightHistory',
                                  'sku': '',
                                  'desc': '指定した URL、ドメイン、または IP について、Web '
                                          'コンテンツのカテゴリ分類の変更および脅威リスクレベルの更新の履歴を返します。このエンドポイントはページネーションされません。カテゴリ分類と脅威リスクレベルの両配列の完全な履歴が単一のレスポンスで返されます。両配列は独立したイベントストリームを表すため、長さが異なる場合があります。必要な権限: '
                                          'ses_threat_intel_api_access。この権限を持たない呼び出し元には 403 Forbidden レスポンスが返されます。',
                                  'path_params': [],
                                  'query_params': [{'name': 'network',
                                                    'type': 'string',
                                                    'required': True,
                                                    'default': '',
                                                    'desc': "検索対象の完全な URL、ドメイン名、または IP アドレス。【注意】完全な URL には '/' "
                                                            '文字が含まれ、パスセグメントとして渡すとリクエストのルーティングが壊れてしまうため、この値はパスセグメントではなくクエリパラメータとして渡されます…',
                                                    'sample': 'google.com'}],
                                  'body': None,
                                  'body_schema': []}]},
 '🧬 TI: Process Chain': {'doc': 'cbx_ti_process_chain.md',
                         'permissions': ['Threat Intel -> Read'],
                         'endpoints': [{'method': 'GET',
                                        'path': '/common/threat-intel/v1/process-chain/file/{file_sha256}',
                                        'summary': '指定したファイルの sha256 に対する上位 K 件のプロセス系統エンリッチメントを返す API です。',
                                        'operation_id': 'listFileProcessChain',
                                        'sku': '',
                                        'desc': '指定したファイルの SHA-256 に対する上位 K '
                                                '件のプロセス系統（親子プロセスチェーン）エンリッチメントを返し、そのファイルが通常どのように実行され、どの親プロセスと関連しているかを示します。必要な権限: '
                                                'ses_threat_intel_api_access。この権限を持たない呼び出し元には 403 Forbidden '
                                                'レスポンスが返されます。すべての結果を取得するには、レスポンス本文の `total_pages` を確認し、`page` が '
                                                '`total_pages` に等しくなるまで、呼び出しごとに `page` を 1 ずつ増やしてリクエストを繰り返します。各ページでは最大 '
                                                '`page_size` 件（デフォルト 10、最大 100）のエントリが返されます。',
                                        'path_params': [{'name': 'file_sha256',
                                                         'required': True,
                                                         'desc': '検索対象ファイルの SHA-256 ハッシュ',
                                                         'sample': 'eec3f761f7eabe9ed569f39e896be24c9bbb8861b15dbde1b3d539505cd9dd8d'}],
                                        'query_params': [{'name': 'page_size',
                                                          'type': 'integer',
                                                          'required': False,
                                                          'default': '10',
                                                          'desc': '1 回のリクエストで返す上位 K '
                                                                  '件のプロセスチェーンエントリの数。【注意】このフィールドが存在しない場合、最大 10 '
                                                                  '件のエントリが返されます。1 回のリクエストでサポートされる最大エントリ数は 100…',
                                                          'sample': ''},
                                                         {'name': 'page',
                                                          'type': 'integer',
                                                          'required': False,
                                                          'default': '1',
                                                          'desc': '取得するページ番号（1 '
                                                                  '始まり）。【注意】このフィールドが指定されていない場合は、最初のページが返されます。',
                                                          'sample': ''}],
                                        'body': None,
                                        'body_schema': []}]},
 '🛡️ TI: Protected': {'doc': 'cbx_ti_protected.md',
                      'permissions': ['Threat Intel -> Read'],
                      'endpoints': [{'method': 'GET',
                                     'path': '/common/threat-intel/v1/protection/file/{file_sha256}',
                                     'summary': '指定したファイルがいずれかの Symantec テクノロジーによってブロックされたかどうかの情報を返す API です。',
                                     'operation_id': 'getFileProtection',
                                     'sku': '',
                                     'desc': '指定したファイル（SHA-256 で識別）がいずれかの Symantec '
                                             'セキュリティテクノロジーによってブロックされたかどうかの情報を返します。テクノロジー名、最初にブロックした定義セットのバージョン、および関連する脅威名が含まれます。必要な権限: '
                                             'ses_threat_intel_api_access。この権限を持たない呼び出し元には 403 Forbidden レスポンスが返されます。',
                                     'path_params': [{'name': 'file_sha256',
                                                      'required': True,
                                                      'desc': '検索対象ファイルの SHA-256 ハッシュ',
                                                      'sample': '9f660524a026bce8d83f9f701ac5aac3f645cd3d03ddd356c8217e424b52a7af'}],
                                     'query_params': [],
                                     'body': None,
                                     'body_schema': []},
                                    {'method': 'GET',
                                     'path': '/common/threat-intel/v1/protection/network/{network}',
                                     'summary': '指定したドメインがいずれかの Symantec テクノロジーによってブロックされたかどうかの情報を返す API です。',
                                     'operation_id': 'getNetworkProtection',
                                     'sku': '',
                                     'desc': '指定したネットワークドメインがいずれかの Symantec '
                                             'セキュリティテクノロジーによってブロックされたかどうかの情報を返します。テクノロジー名、最初にブロックした定義セットのバージョン、および関連する脅威名が含まれます。必要な権限: '
                                             'ses_threat_intel_api_access。この権限を持たない呼び出し元には 403 Forbidden レスポンスが返されます。',
                                     'path_params': [{'name': 'network',
                                                      'required': True,
                                                      'desc': '検索対象のドメイン名',
                                                      'sample': 'paste.ee'}],
                                     'query_params': [],
                                     'body': None,
                                     'body_schema': []},
                                    {'method': 'GET',
                                     'path': '/common/threat-intel/v1/protection/cve/{cve}',
                                     'summary': '指定した CVE がいずれかの Symantec テクノロジーによってブロックされたかどうかの情報を返す API です。',
                                     'operation_id': 'getCveProtection',
                                     'sku': '',
                                     'desc': '指定した CVE 脆弱性がいずれかの Symantec '
                                             'セキュリティテクノロジーによってブロックされたかどうかの情報を返します。テクノロジー名、最初にブロックした定義セットのバージョン、および関連する脅威名が含まれます。必要な権限: '
                                             'ses_threat_intel_api_access。この権限を持たない呼び出し元には 403 Forbidden レスポンスが返されます。',
                                     'path_params': [{'name': 'cve',
                                                      'required': True,
                                                      'desc': 'CVE 識別子（例: CVE-2017-0038）',
                                                      'sample': 'CVE-2017-0038'}],
                                     'query_params': [],
                                     'body': None,
                                     'body_schema': []}]}}

def render_generic_api(module_key):
    """API_SPECS（ドキュメントから生成）に基づく汎用テストフォーム。(method, endpoint, data) を返す"""
    spec = API_SPECS[module_key]
    eps = spec["endpoints"]
    labels = [f'{e["method"]} {e["path"]}' for e in eps]
    op = st.selectbox("Endpoint", labels, key=f"gen_ep_{module_key}")
    ep = eps[labels.index(op)]
    g_method, g_path = ep["method"], ep["path"]
    kp = f"gen_{module_key}_{g_method}_{g_path}"

    with st.expander(f"ℹ️ {ep['summary'] or ep['operation_id']}", expanded=False):
        if ep["operation_id"]:
            st.markdown(f"**Operation ID:** `{ep['operation_id']}`")
        if ep["sku"]:
            st.markdown(f"**SKU:** {ep['sku']}")
        if ep["desc"]:
            st.caption(ep["desc"])
        if spec["permissions"]:
            st.markdown("**必要な権限:** " + " / ".join(f"`{p}`" for p in spec["permissions"]))
        if ep["body_schema"]:
            st.markdown("**リクエストBody スキーマ:**")
            st.markdown("\n".join(f"- {line}" for line in ep["body_schema"]))
        st.caption(f"出典: {spec['doc']}")

    if g_method == "DELETE" or any(w in g_path for w in ["/contain", "/restart", "bulk-overwrite"]):
        st.warning("⚠️ このAPIは環境に変更を加えます（削除・隔離・再起動・上書きなど）。対象IDを確認してから実行してください。")

    # Path parameters
    for p in ep["path_params"]:
        val = st.text_input(f"{p['name']} (path)", value=p["sample"], key=f"{kp}_pp_{p['name']}", help=p["desc"])
        g_path = g_path.replace("{" + p["name"] + "}", net_path(val) if p["name"] == "network" else quote(val.strip(), safe=""))

    # Query parameters
    qps = ep["query_params"]
    params = {}
    if qps:
        has_array = any(q["type"] == "array" for q in qps)
        array_mode = "repeat"
        if has_array:
            comma_default = any(("comma-separated" in q["desc"] or "カンマ区切り" in q["desc"]) for q in qps if q["type"] == "array")
            array_mode = st.radio("配列パラメータの送信形式",
                                  ["repeat", "comma"], index=1 if comma_default else 0, horizontal=True,
                                  format_func=lambda x: "繰り返し (a=1&a=2)" if x == "repeat" else "カンマ区切り (a=1,2)",
                                  key=f"{kp}_arrmode")
        main_q = [q for q in qps if q["required"] or q["default"] or q["sample"]]
        opt_q = [q for q in qps if q not in main_q]

        def q_input(q):
            label = f"{q['name']} ({q['type']}{', 必須' if q['required'] else ''})"
            init = q["sample"] or q["default"]
            if q["type"] == "array":
                label += " ※カンマ区切りで複数"
            v = st.text_input(label, value=init, key=f"{kp}_qp_{q['name']}", help=q["desc"])
            v = v.strip()
            if not v:
                return
            if q["type"] == "array":
                items = csv_list(v)
                params[q["name"]] = items if array_mode == "repeat" else ",".join(items)
            else:
                params[q["name"]] = v

        for q in main_q:
            q_input(q)
        if opt_q:
            with st.expander(f"オプションのクエリパラメータ（{len(opt_q)}件, 空欄は送信しません）"):
                for q in opt_q:
                    q_input(q)
    if params:
        g_path = f"{g_path}?{urlencode(params, doseq=True)}"

    # Request body
    g_data = {}
    if ep["body"] is not None:
        body_txt = st.text_area("Request Body (JSON) ※ドキュメントのサンプル。編集可",
                                value=json.dumps(ep["body"], indent=2, ensure_ascii=False),
                                height=220, key=f"{kp}_body")
        if body_txt.strip():
            try:
                g_data = json.loads(body_txt)
            except Exception as e:
                st.error(f"Request Body のJSONが不正です: {e}")
                g_data = {}
    return g_method, g_path, g_data


# --- 既存モジュールのエンドポイント一覧（cbx_*.md の一覧から生成） ---
LEGACY_SPECS = {'Custom Detections': {'doc': 'cbx_custom_detection.md',
                       'endpoints': [('POST',
                                      '/detect-respond/detection/v1/custom-detections/queries/_search',
                                      'クエリサブリソースの検索'),
                                     ('POST',
                                      '/detect-respond/detection/v1/custom-detections/{detection_id}/queries',
                                      'クエリサブリソースの作成'),
                                     ('GET',
                                      '/detect-respond/detection/v1/custom-detections/{detection_id}/queries/{query_id}',
                                      'クエリサブリソースの取得'),
                                     ('PUT',
                                      '/detect-respond/detection/v1/custom-detections/{detection_id}/queries/{query_id}',
                                      'クエリサブリソースの更新'),
                                     ('DELETE',
                                      '/detect-respond/detection/v1/custom-detections/{detection_id}/queries/{query_id}',
                                      'クエリサブリソースの削除'),
                                     ('POST', '/detect-respond/detection/v1/custom-detections/_search', 'カスタム検出の検索'),
                                     ('POST', '/detect-respond/detection/v1/custom-detections', 'カスタム検出の作成'),
                                     ('POST',
                                      '/detect-respond/detection/v1/custom-detections/_import',
                                      'カスタム検出とそのクエリの一括インポート（作成または追加）'),
                                     ('GET',
                                      '/detect-respond/detection/v1/custom-detections/{detection_id}',
                                      'カスタム検出の取得'),
                                     ('PUT',
                                      '/detect-respond/detection/v1/custom-detections/{detection_id}',
                                      'カスタム検出の更新'),
                                     ('DELETE',
                                      '/detect-respond/detection/v1/custom-detections/{detection_id}',
                                      'カスタム検出の削除'),
                                     ('POST',
                                      '/detect-respond/detection/v1/custom-detections/_bulk',
                                      '検出に対する統合一括操作（DELETE または UPDATE）'),
                                     ('POST',
                                      '/detect-respond/detection/v1/custom-detections/{detection_id}/queries/_bulk',
                                      'クエリに対する統合一括操作（DELETE または MOVE）')]},
 'Device Query': {'doc': 'cbx_device_query.md',
                  'endpoints': [('GET', '/detect-respond/device-query/v2/commands', 'Device Query コマンドの一覧を取得します。'),
                                ('POST',
                                 '/detect-respond/device-query/v2/commands',
                                 'Device Query コマンド（Forensic または Artifact）を実行します。'),
                                ('GET',
                                 '/detect-respond/device-query/v2/commands/{commandId}',
                                 'ID を指定して Device Query コマンドの詳細を取得します。'),
                                ('DELETE',
                                 '/detect-respond/device-query/v2/commands/{commandId}',
                                 'ID を指定して Device Query コマンドを削除します。'),
                                ('PUT',
                                 '/detect-respond/device-query/v2/commands/{commandId}/cancel',
                                 '実行された Device Query コマンドをキャンセルします。'),
                                ('POST',
                                 '/detect-respond/device-query/v2/commands/{commandId}/results',
                                 'Device Query 結果の取得'),
                                ('GET',
                                 '/detect-respond/device-query/v2/schedules',
                                 'ページネーションとソートを指定して Device Query スケジュールの一覧を取得します。'),
                                ('POST', '/detect-respond/device-query/v2/schedules', '新しい Device Query スケジュールを作成します。'),
                                ('DELETE',
                                 '/detect-respond/device-query/v2/schedules',
                                 'Device Query スケジュールを削除します（一括）。'),
                                ('GET',
                                 '/detect-respond/device-query/v2/schedules/{scheduleId}',
                                 '特定の Device Query スケジュールの詳細を取得します。'),
                                ('PUT',
                                 '/detect-respond/device-query/v2/schedules/{scheduleId}',
                                 '既存の Device Query スケジュールを更新します。'),
                                ('GET',
                                 '/detect-respond/device-query/v2/schedules/{scheduleId}/commands',
                                 '指定したスケジュール ID の Device Query コマンドの一覧を、ページネーションとソートを指定して取得します。'),
                                ('PUT',
                                 '/detect-respond/device-query/v2/schedules/{scheduleId}/stop',
                                 '実行中の Device Query スケジュールを停止します。')]},
 'Alerts & Threats': {'doc': 'cbx_alerts.md',
                      'endpoints': [('GET', '/detect-respond/alerts/v8/threats/{threat_id}/notes', '脅威のノートの取得'),
                                    ('POST', '/detect-respond/alerts/v8/threats/{threat_id}/notes', '脅威レベルのノートの作成'),
                                    ('DELETE',
                                     '/detect-respond/alerts/v8/threats/{threat_id}/notes/{id}',
                                     '脅威レベルのノートの削除'),
                                    ('POST', '/detect-respond/alerts/v8/grouped_alerts/_facet', 'アラートのファセット - グループ化'),
                                    ('POST',
                                     '/detect-respond/alerts/v8/grouped_alerts/_histogram',
                                     'グラフやダッシュボード用に、時間バケットごとの脅威グループ数を取得します。'),
                                    ('POST',
                                     '/detect-respond/alerts/v8/grouped_alerts/_search',
                                     'クエリ、条件、および除外演算子を使用してアラートを検索します。アラートはリクエストで指定した group_by '
                                     'フィールドでグループ化されます。現在、グループ化に使用できるのは threat_id のみです。レスポンススキーマはグループ化フィールドによって異なります。'),
                                    ('GET',
                                     '/detect-respond/alerts/v8/threats/{threat_id}/history',
                                     '追加されたノートなど、脅威に対して実行されたアクションを取得します。'),
                                    ('POST',
                                     '/detect-respond/alerts/v8/alerts/workflow',
                                     'リクエストの検索条件に一致する既存のすべてのアラートを更新する非同期操作です。'),
                                    ('POST',
                                     '/detect-respond/alerts/v8/alerts/threat/workflow/_criteria',
                                     'ID を指定して脅威のワークフローを一括更新します（非同期操作）'),
                                    ('GET', '/detect-respond/alerts/v8/alerts/{alert_id}/notes', 'アラートのノートの取得'),
                                    ('POST', '/detect-respond/alerts/v8/alerts/{alert_id}/notes', 'アラートレベルのノートの作成'),
                                    ('PATCH',
                                     '/detect-respond/alerts/v8/alerts/{alert_id}/notes',
                                     '顧客ノートの read_history を更新する Patch ルート'),
                                    ('PUT',
                                     '/detect-respond/alerts/v8/alerts/{alert_id}/notes/{id}',
                                     'アラートレベルの顧客ノートの更新'),
                                    ('DELETE',
                                     '/detect-respond/alerts/v8/alerts/{alert_id}/notes/{id}',
                                     'アラートレベルのノートの削除'),
                                    ('GET',
                                     '/detect-respond/alerts/v8/threats/{threat_id}/tags',
                                     'threatId に基づいてタグ一覧を取得します。'),
                                    ('POST', '/detect-respond/alerts/v8/threats/{threat_id}/tags', '脅威 ID にタグを追加します。'),
                                    ('DELETE',
                                     '/detect-respond/alerts/v8/threats/{threat_id}/tags/{tag}',
                                     '指定した脅威 ID との関連付けを解除するため、タグを削除します。'),
                                    ('POST',
                                     '/detect-respond/alerts/v8/alerts/_export',
                                     'アラートを CSV 形式でエクスポートします。これは非同期リクエストであり、1 回のリクエストで最大 25,000 '
                                     '件のレコードをエクスポートできます。ここで定義されている Export Alerts エンドポイントを使用して、必要な検索条件を指定したジョブを作成し…'),
                                    ('POST', '/detect-respond/alerts/v8/alerts/_facet', 'アラートのファセット（グループ化なし）'),
                                    ('POST',
                                     '/detect-respond/alerts/v8/alerts/_histogram',
                                     'チャートやダッシュボード向けに、時間バケットごとのアラート件数を取得します。'),
                                    ('POST',
                                     '/detect-respond/alerts/v8/alerts/_search',
                                     'クエリ、条件、および除外演算子を使用してアラートを検索します。'),
                                    ('POST',
                                     '/detect-respond/alerts/v8/alerts/_validate',
                                     '検索が有効かどうかを検証し、無効な場合はエラーメッセージを返します。'),
                                    ('GET',
                                     '/detect-respond/alerts/v8/alerts/search_suggestions',
                                     '検索で使用するフィールドの推奨候補を取得します。'),
                                    ('GET', '/detect-respond/alerts/v8/alerts/{alert_id}', 'ID を指定してアラートの詳細を取得します。'),
                                    ('GET',
                                     '/detect-respond/alerts/v8/alerts/{alert_id}/history',
                                     '追加されたメモやワークフロー状態の変更など、アラートに対して実行されたアクションを取得します。history '
                                     'ルートには、アラートの現在の状態の詳細は含まれません。')]},
 'Jobs & Export': {'doc': 'cbx_jobs.md',
                   'endpoints': [('GET', '/detect-respond/jobs/v4/jobs/{job_id}/download', 'ジョブ出力のダウンロード'),
                                 ('GET', '/detect-respond/jobs/v4/jobs/{job_id}', '特定のジョブの詳細を取得します。'),
                                 ('POST', '/detect-respond/jobs/v4/event_export', 'イベントエクスポートジョブの開始')]},
 'Live Response': {'doc': 'cbx_live_response.md',
                   'endpoints': [('GET',
                                  '/detect-respond/live-response/v7/sessions',
                                  'すべての Live Response セッションを取得します。'),
                                 ('POST', '/detect-respond/live-response/v7/sessions', 'Live Response セッションの作成'),
                                 ('GET',
                                  '/detect-respond/live-response/v7/sessions/{session_id}',
                                  'Live Response セッションの取得'),
                                 ('DELETE',
                                  '/detect-respond/live-response/v7/sessions/{session_id}',
                                  'Live Response セッションのクローズ'),
                                 ('GET',
                                  '/detect-respond/live-response/v7/sessions/{session_id}/files',
                                  'セッションのすべてのファイルを取得します。'),
                                 ('POST',
                                  '/detect-respond/live-response/v7/sessions/{session_id}/files',
                                  'セッションへのファイルのアップロード'),
                                 ('GET',
                                  '/detect-respond/live-response/v7/sessions/{session_id}/files/{file_id}',
                                  'ID を指定してファイルオブジェクトを取得します。'),
                                 ('DELETE',
                                  '/detect-respond/live-response/v7/sessions/{session_id}/files/{file_id}',
                                  'セッションからのファイルの削除'),
                                 ('GET',
                                  '/detect-respond/live-response/v7/sessions/{session_id}/files/{file_id}/content',
                                  'ファイルコンテンツのダウンロード'),
                                 ('GET',
                                  '/detect-respond/live-response/v7/sessions/{session_id}/commands',
                                  'セッションのすべてのコマンドを取得します。'),
                                 ('POST',
                                  '/detect-respond/live-response/v7/sessions/{session_id}/commands',
                                  'Live Response コマンドをキューに追加します。'),
                                 ('GET',
                                  '/detect-respond/live-response/v7/sessions/{session_id}/commands/{command_id}',
                                  'ID を指定して Live Response コマンドを取得します。'),
                                 ('DELETE',
                                  '/detect-respond/live-response/v7/sessions/{session_id}/commands/{command_id}',
                                  'Live Response コマンドのキャンセル')]},
 'Notifications': {'doc': 'cbx_notifications.md',
                   'endpoints': [('GET', '/detect-respond/notifications/v2/rules', '通知ルールを取得します。'),
                                 ('POST', '/detect-respond/notifications/v2/rules', '通知ルールの作成'),
                                 ('PUT', '/detect-respond/notifications/v2/rules/{ruleId}', 'ID を指定してルールの詳細を更新します。'),
                                 ('DELETE', '/detect-respond/notifications/v2/rules/{ruleId}', 'ID を指定してルールを削除します。'),
                                 ('POST', '/detect-respond/notifications/v2/history/_search', '特定のルールの通知履歴を取得します。')]},
 'Policy Management': {'doc': 'cbx_policy_management.md',
                       'endpoints': [('POST',
                                      '/common/policy-management/v2/policies/copy',
                                      'この API を使用すると、ワークスペースのポリシーを別の環境にコピーできます。'),
                                     ('GET', '/common/policy-management/v2/policies', 'この API を使用すると、ポリシーの一覧を取得できます。'),
                                     ('PUT', '/common/policy-management/v2/policies', 'この API を使用すると、ポリシー設定を更新できます。'),
                                     ('POST', '/common/policy-management/v2/policies', 'この API を使用すると、ポリシーを作成できます。'),
                                     ('DELETE',
                                      '/common/policy-management/v2/policies/{policy-id}',
                                      'この API を使用すると、ポリシーを削除できます。'),
                                     ('GET',
                                      '/common/policy-management/v2/policies/{policy-id}/versions/{policy-version}',
                                      'この API を使用すると、ID とバージョンを指定してポリシーの詳細を取得できます。'),
                                     ('GET',
                                      '/common/policy-management/v2/policies/{policy-id}/versions',
                                      'この API を使用すると、ポリシーのバージョン一覧を取得できます。'),
                                     ('PATCH',
                                      '/common/policy-management/v2/policies/allow-list/{policy-id}/versions/{policy-version}',
                                      'この API を使用すると、許可リストポリシーを部分更新できます。'),
                                     ('PUT',
                                      '/common/policy-management/v2/policies/allow-list/{policy-id}/versions/{policy-version}',
                                      'この API を使用すると、許可リストポリシーを更新できます。'),
                                     ('PATCH',
                                      '/common/policy-management/v2/policies/deny-list/{policy-id}/versions/{policy-version}',
                                      'この API を使用すると、拒否リストポリシーを部分更新できます。'),
                                     ('PUT',
                                      '/common/policy-management/v2/policies/deny-list/{policy-id}/versions/{policy-version}',
                                      'この API を使用すると、拒否リストポリシーを更新できます。'),
                                     ('GET',
                                      '/common/policy-management/v2/policies/device-groups/{group-id}/policies',
                                      'この API を使用すると、デバイスグループに割り当てられたポリシーの一覧を取得できます。'),
                                     ('POST',
                                      '/common/policy-management/v2/policies/{policy-id}/versions/{policy-version}/device-groups',
                                      'この API を使用すると、デバイスグループにポリシーを適用できます。'),
                                     ('DELETE',
                                      '/common/policy-management/v2/policies/{policy-id}/versions/{policy-version}/device-groups',
                                      'この API を使用すると、デバイスグループからポリシーを削除できます。'),
                                     ('GET',
                                      '/common/policy-management/v2/policies/export/{export-id}/status',
                                      'この API を使用すると、ポリシーのエクスポート処理のステータスを確認できます。'),
                                     ('POST',
                                      '/common/policy-management/v2/policies/export/all',
                                      'この API を使用すると、すべてのポリシーをエクスポートできます。'),
                                     ('POST',
                                      '/common/policy-management/v2/policies/export/types',
                                      'この API を使用すると、ポリシータイプで絞り込んだポリシーをエクスポートできます。'),
                                     ('POST',
                                      '/common/policy-management/v2/policies/export/names',
                                      'この API を使用すると、ポリシー名で絞り込んだポリシーをエクスポートできます。'),
                                     ('POST',
                                      '/common/policy-management/v2/policies/import',
                                      'この API を使用すると、ファイルからポリシーをインポートできます。'),
                                     ('GET',
                                      '/common/policy-management/v2/policies/import/{import-id}/status',
                                      'この API を使用すると、ポリシーのインポート処理のステータスを確認できます。'),
                                     ('POST',
                                      '/common/policy-management/v2/policies/target-rules/export/all',
                                      'この API を使用すると、すべてのターゲットルールをエクスポートできます。'),
                                     ('POST',
                                      '/common/policy-management/v2/policies/target-rules/export/names',
                                      'この API を使用すると、名前を指定してターゲットルールをエクスポートできます。'),
                                     ('GET',
                                      '/common/policy-management/v2/policies/target-rules/export/{export-id}/status',
                                      'この API を使用すると、ターゲットルールのエクスポート処理のステータスを確認できます。'),
                                     ('POST',
                                      '/common/policy-management/v2/policies/target-rules/import',
                                      'この API を使用すると、ファイルからターゲットルールをインポートできます。'),
                                     ('GET',
                                      '/common/policy-management/v2/policies/target-rules/import/{import-id}/status',
                                      'この API を使用すると、ターゲットルールのインポート処理のステータスを確認できます。'),
                                     ('GET',
                                      '/common/policy-management/v2/policies/target-rules',
                                      'この API を使用すると、ターゲットルールの一覧を取得できます。')]},
 'Script Deobfuscation': {'doc': 'cbx_script_deob.md',
                          'endpoints': [('POST',
                                         '/detect-respond/script-deobfuscation/v3/reveal',
                                         '難読化された PowerShell スクリプトの難読化解除')]},
 'Threat Intel': {'doc': 'cbx_taxii11.md',
                  'endpoints': [('POST', '/common/threat-intel/v1/taxii11/discovery', 'TAXII Discovery'),
                                ('POST', '/common/threat-intel/v1/taxii11/collection-management', 'TAXII コレクション管理'),
                                ('POST', '/common/threat-intel/v1/taxii11/poll', 'TAXII Poll – STIX CTI フィードの取得')]},
 'Vulnerability Assessment': {'doc': 'cbx_vuln_assessment.md',
                              'endpoints': [('GET',
                                             '/endpoint-security/vulnerability/assessment/v3/vulnerabilities/summary',
                                             '組織の脆弱性サマリーのロールアップを取得します。'),
                                            ('POST',
                                             '/endpoint-security/vulnerability/assessment/v3/devices/vulnerabilities/summary/_search',
                                             '組織内の脆弱なデバイスの検索'),
                                            ('POST',
                                             '/endpoint-security/vulnerability/assessment/v3/devices/vulnerabilities/summary/_facets',
                                             '脆弱なデバイスのフィルターファセットを取得します。'),
                                            ('POST',
                                             '/endpoint-security/vulnerability/assessment/v3/devices/vulnerabilities/summary/export',
                                             '脆弱なデバイス一覧の CSV エクスポート'),
                                            ('POST',
                                             '/endpoint-security/vulnerability/assessment/v3/devices/vulnerabilities/_search',
                                             '組織全体の脆弱性の検索'),
                                            ('POST',
                                             '/endpoint-security/vulnerability/assessment/v3/devices/vulnerabilities/_facets',
                                             '脆弱性のフィルターファセットを取得します。'),
                                            ('POST',
                                             '/endpoint-security/vulnerability/assessment/v3/devices/vulnerabilities/export',
                                             '脆弱性一覧の CSV エクスポート'),
                                            ('GET',
                                             '/endpoint-security/vulnerability/assessment/v3/vulnerabilities/{cve_id}',
                                             '脆弱性の詳細を取得します。'),
                                            ('GET',
                                             '/endpoint-security/vulnerability/assessment/v3/vulnerabilities/{cve_id}/summary',
                                             'CVE フライアウトのサマリーを取得します。'),
                                            ('POST',
                                             '/endpoint-security/vulnerability/assessment/v3/vulnerabilities/{cve_id}/devices',
                                             '特定の CVE の影響を受けるデバイスの検索'),
                                            ('POST',
                                             '/endpoint-security/vulnerability/assessment/v3/vulnerabilities/{cve_id}/software/_search',
                                             '特定の CVE に対して脆弱なソフトウェア構成の一覧'),
                                            ('POST',
                                             '/endpoint-security/vulnerability/assessment/v3/vulnerabilities/{cve_id}/actions',
                                             '脆弱性に対するアクションの実行'),
                                            ('GET',
                                             '/endpoint-security/vulnerability/assessment/v3/devices/{device_uid}/vulnerabilities/summary',
                                             'デバイスの脆弱性サマリーを取得します。'),
                                            ('POST',
                                             '/endpoint-security/vulnerability/assessment/v3/devices/{device_uid}/vulnerabilities/_search',
                                             'デバイス上の脆弱性の検索'),
                                            ('POST',
                                             '/endpoint-security/vulnerability/assessment/v3/devices/{device_uid}/vulnerabilities/export',
                                             'デバイスの脆弱性一覧の CSV エクスポート'),
                                            ('POST',
                                             '/endpoint-security/vulnerability/assessment/v3/devices/{device_uid}/device-actions',
                                             'デバイスに対するアクションの実行')]}}

def legacy_endpoint_select(key, hand_ops):
    """既存テンプレートのエンドポイント + mdに記載のある残りのエンドポイントを選択肢にする"""
    all_ops = list(hand_ops) + [f"{m} {p}" for m, p, _ in LEGACY_SPECS[key]["endpoints"] if f"{m} {p}" not in hand_ops]
    return st.selectbox("Endpoint", all_ops, key=f"legacy_ep_{key}")

def render_legacy_generic(key, op):
    """md にパス一覧しかないエンドポイント用の汎用フォーム（パスパラメータ / クエリ / Body を入力）"""
    spec = LEGACY_SPECS[key]
    g_method, g_path = op.split(" ", 1)
    summary = next((s for m, p, s in spec["endpoints"] if m == g_method and p == g_path), "")
    kp = f"lg_{key}_{g_method}_{g_path}"
    if summary:
        st.caption(f"ℹ️ {summary}（出典: {spec['doc']}）")
    st.caption("※ このエンドポイントのパラメータ詳細は md に記載がないため、パス以外（クエリ / Body）は手入力してください。")
    if g_method == "DELETE" or any(w in g_path for w in ["/cancel", "/stop", "/workflow", "/actions", "/device-actions"]):
        st.warning("⚠️ このAPIは環境に変更を加えます。対象IDを確認してから実行してください。")
    if g_method == "POST" and (g_path.endswith("/files") or g_path.endswith("/import")):
        st.warning("⚠️ ファイルアップロード系のAPIです。本ツールの JSON / フォーム送信では実行できない場合があります。")

    for name in re.findall(r"\{([^}]+)\}", g_path):
        val = st.text_input(f"{name} (path, 必須)", value="", key=f"{kp}_pp_{name}")
        if not val.strip():
            st.error(f"{name} を入力してください")
        g_path = g_path.replace("{" + name + "}", quote(val.strip(), safe="") or "{" + name + "}")

    qs = st.text_input("クエリ文字列（任意, 例: page=1&page_size=10）", value="", key=f"{kp}_qs")
    if qs.strip():
        g_path = f"{g_path}?{qs.strip().lstrip('?')}"

    g_data = {}
    if g_method in ["POST", "PUT", "PATCH", "DELETE"]:
        body_txt = st.text_area("Request Body (JSON)" + ("（DELETE は空なら送信しません）" if g_method == "DELETE" else ""),
                                value="{}" if g_method != "DELETE" else "", height=160, key=f"{kp}_body")
        if body_txt.strip():
            try:
                g_data = json.loads(body_txt)
            except Exception as e:
                st.error(f"Request Body のJSONが不正です: {e}")
    return g_method, g_path, g_data

def json_obj_input(label, key, default=""):
    """任意の JSON オブジェクト入力（空なら None）"""
    txt = st.text_area(label, value=default, height=80, key=key)
    if not txt.strip():
        return None
    try:
        v = json.loads(txt)
        if not isinstance(v, dict):
            st.error(f"{label}: JSON オブジェクト（{{...}}）で入力してください")
            return None
        return v
    except Exception as e:
        st.error(f"{label}: JSON が不正です: {e}")
        return None

TAXII11_NS = "http://taxii.mitre.org/messages/taxii_xml_binding-1.1"
TAXII11_HEADERS = {
    "X-TAXII-Content-Type": "urn:taxii.mitre.org:message:xml:1.1",
    "X-TAXII-Accept": "urn:taxii.mitre.org:message:xml:1.1",
    "X-TAXII-Protocol": "urn:taxii.mitre.org:protocol:https:1.0",
    "X-TAXII-Services": "urn:taxii.mitre.org:services:1.1",
    "Accept": "application/xml",
}

# =====================================================================
# 📊 ダッシュボード（管理クライアント / 脆弱性レポート / 攻撃フォロー）
#   - データ取得は Python 側（グローバル適用トークン / 401 時は自動更新に連動）
#   - 描画はブラウザ側（globe.gl / 3d-force-graph / ECharts を CDN から読み込み）
# =====================================================================
DASH_CLIENT = "📊 管理クライアント ダッシュボード"
DASH_VULN = "🧯 脆弱性レポート ダッシュボード"
DASH_ATTACK = "⚔️ 攻撃フォロー ダッシュボード"
DASHBOARD_NAMES = [DASH_CLIENT, DASH_VULN, DASH_ATTACK]

# 国コード → (緯度, 経度, 日本語名)
COUNTRY_GEO = {
    "jp": (36.2, 138.3, "日本"), "us": (39.8, -98.6, "米国"), "cn": (35.9, 104.2, "中国"), "kr": (36.5, 127.9, "韓国"),
    "tw": (23.7, 121.0, "台湾"), "hk": (22.3, 114.2, "香港"), "sg": (1.35, 103.8, "シンガポール"), "in": (21.0, 78.0, "インド"),
    "th": (15.9, 100.9, "タイ"), "vn": (14.1, 108.3, "ベトナム"), "my": (4.2, 102.0, "マレーシア"), "id": (-2.5, 118.0, "インドネシア"),
    "ph": (12.9, 121.8, "フィリピン"), "au": (-25.3, 133.8, "オーストラリア"), "nz": (-41.0, 174.0, "ニュージーランド"),
    "gb": (54.0, -2.0, "英国"), "ie": (53.4, -8.2, "アイルランド"), "fr": (46.6, 2.2, "フランス"), "de": (51.2, 10.4, "ドイツ"),
    "nl": (52.1, 5.3, "オランダ"), "be": (50.5, 4.5, "ベルギー"), "ch": (46.8, 8.2, "スイス"), "at": (47.5, 14.6, "オーストリア"),
    "it": (41.9, 12.6, "イタリア"), "es": (40.5, -3.7, "スペイン"), "pt": (39.4, -8.2, "ポルトガル"), "se": (60.1, 18.6, "スウェーデン"),
    "no": (60.5, 8.5, "ノルウェー"), "fi": (61.9, 25.7, "フィンランド"), "dk": (56.3, 9.5, "デンマーク"), "pl": (51.9, 19.1, "ポーランド"),
    "cz": (49.8, 15.5, "チェコ"), "ro": (45.9, 24.9, "ルーマニア"), "ua": (48.4, 31.2, "ウクライナ"), "ru": (61.5, 105.3, "ロシア"),
    "tr": (39.0, 35.2, "トルコ"), "il": (31.0, 34.9, "イスラエル"), "ae": (23.4, 53.8, "UAE"), "sa": (23.9, 45.1, "サウジアラビア"),
    "ir": (32.4, 53.7, "イラン"), "kp": (40.3, 127.5, "北朝鮮"), "eg": (26.8, 30.8, "エジプト"), "za": (-30.6, 22.9, "南アフリカ"),
    "ng": (9.1, 8.7, "ナイジェリア"), "ke": (-0.02, 37.9, "ケニア"), "br": (-14.2, -51.9, "ブラジル"), "ar": (-38.4, -63.6, "アルゼンチン"),
    "cl": (-35.7, -71.5, "チリ"), "mx": (23.6, -102.6, "メキシコ"), "ca": (56.1, -106.3, "カナダ"), "co": (4.6, -74.3, "コロンビア"),
    "pk": (30.4, 69.3, "パキスタン"), "bd": (23.7, 90.4, "バングラデシュ"),
}
# OS 言語コード → 国（en など複数国にまたがる言語は推定しない）
LANG_COUNTRY = {"ja": "jp", "ko": "kr", "zh": "cn", "de": "de", "fr": "fr", "it": "it", "es": "es", "pt": "br", "nl": "nl",
                "sv": "se", "fi": "fi", "da": "dk", "no": "no", "nb": "no", "pl": "pl", "cs": "cz", "ru": "ru", "tr": "tr",
                "th": "th", "vi": "vn", "id": "id", "ms": "my", "he": "il", "ar": "sa", "uk": "ua", "ro": "ro"}
# UTC オフセット（分, 東が正）→ 代表国
TZ_COUNTRY = {540: "jp", 480: "cn", 420: "th", 330: "in", 300: "pk", 240: "ae", 180: "ru", 120: "fi", 60: "de", 0: "gb",
              -180: "br", -240: "ca", -300: "us", -360: "us", -420: "us", -480: "us", 600: "au", 720: "nz", 570: "au", 345: "in"}

DASH_CSS = """
<style>
  body{margin:0;background:#050a18;color:#dbe7ff;font-family:'Segoe UI','Yu Gothic UI',sans-serif;}
  .wrap{padding:10px 12px;}
  .title{font-size:22px;font-weight:800;letter-spacing:.5px;background:linear-gradient(90deg,#4fd1ff,#a96bff);-webkit-background-clip:text;color:transparent;}
  .sub{font-size:12px;color:#8aa0c8;margin-bottom:8px;}
  .kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:8px 0 12px;}
  .kpi{background:linear-gradient(145deg,#0c1631,#0a1024);border:1px solid #1d2c55;border-radius:12px;padding:10px 12px;box-shadow:0 0 18px rgba(79,209,255,.08) inset;}
  .kpi .l{font-size:12px;color:#8aa0c8}.kpi .v{font-size:30px;font-weight:800;line-height:1.15}
  .card{background:#0a1226;border:1px solid #1b2a52;border-radius:12px;padding:8px 10px;}
  .card h4{margin:2px 0 6px;font-size:14px;color:#9fc3ff}
  .grid2{display:grid;grid-template-columns:1.6fr 1fr;gap:10px;}
  .grid3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;}
  table{width:100%;border-collapse:collapse;font-size:12px}
  th{color:#7f95c2;text-align:left;font-weight:600;border-bottom:1px solid #1b2a52;padding:4px}
  td{padding:4px;border-bottom:1px solid #111d3b}
  .flag{width:22px;height:15px;border-radius:2px;vertical-align:middle;margin-right:5px;box-shadow:0 0 3px #000}
  .bar{height:8px;border-radius:4px;background:#14234a;overflow:hidden}.bar>i{display:block;height:100%}
  .pill{display:inline-block;padding:1px 7px;border-radius:10px;font-size:11px;font-weight:700}
  .scroll{max-height:360px;overflow:auto}
  @keyframes pulse{0%{box-shadow:0 0 0 0 rgba(255,45,85,.7)}70%{box-shadow:0 0 0 14px rgba(255,45,85,0)}100%{box-shadow:0 0 0 0 rgba(255,45,85,0)}}
  @keyframes blink{50%{opacity:.35}}
  @keyframes scan{0%{background-position:-200% 0}100%{background-position:200% 0}}
  @keyframes ticker{0%{transform:translateX(100%)}100%{transform:translateX(-100%)}}
</style>
"""

def _flag_img(cc):
    return f'<img class="flag" src="https://flagcdn.com/w40/{cc}.png" onerror="this.style.display=\'none\'">' if cc else ""

def net_path(v):
    """ネットワーク IOC をパスに埋め込む（md: URL エンコードしない。'/' ':' はそのまま、空白等のみエンコード）"""
    return quote(str(v).strip(), safe=":/[]@!$&'()*+,;=-._~")

def dash_api(method, path, params=None, body=None):
    """ダッシュボード用 API 呼び出し（Bearer = グローバル適用トークン / 自動更新 ON なら 401 時に 1 回再取得）"""
    url = f"{server_url.rstrip('/')}{path}"
    def _do():
        h = {"Authorization": "Bearer " + (st.session_state.get("global_token") or api_token),
             "accept": "application/json", "content-type": "application/json"}
        return requests.request(method, url, headers=h, params=params, json=body if method != "GET" else None, timeout=30)
    r = _do()
    if r.status_code == 401 and st.session_state.get("auto_refresh") and refresh_global_token("ダッシュボードで 401 を受信"):
        r = _do()
    try:
        data = r.json()
    except ValueError:
        data = {"raw": r.text[:2000]}
    return r.status_code, data

def _find_records(obj):
    """レスポンス中の最大の「dict の配列」を返す（スキーマ差異に強くするため）"""
    best = []
    def walk(o):
        nonlocal best
        if isinstance(o, list):
            if o and all(isinstance(x, dict) for x in o) and len(o) > len(best):
                best = o
            for x in o:
                walk(x)
        elif isinstance(o, dict):
            for v in o.values():
                walk(v)
    walk(obj)
    return best

def _flat(d, prefix=""):
    out = {}
    if isinstance(d, dict):
        for k, v in d.items():
            key = f"{prefix}{k}".lower()
            if isinstance(v, dict):
                out.update(_flat(v, key + "."))
            else:
                out[key] = v
    return out

def _pick(rec, names, contains=None, numeric=False):
    f = _flat(rec)
    for n in names:
        for k, v in f.items():
            if k == n or k.endswith("." + n):
                if not numeric or isinstance(v, (int, float)):
                    return v
    if contains:
        for k, v in f.items():
            if all(c in k for c in contains) and (not numeric or isinstance(v, (int, float))):
                return v
    return None

SEV_ORDER = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "NONE"]

def _norm_sev(v):
    s = str(v or "").upper()
    for x in SEV_ORDER:
        if x in s:
            return x
    if s in ("INFO", "INFORMATIONAL", "UNKNOWN", ""):
        return "NONE"
    try:  # CVSS 数値
        f = float(s)
        return "CRITICAL" if f >= 9 else "HIGH" if f >= 7 else "MEDIUM" if f >= 4 else "LOW" if f > 0 else "NONE"
    except ValueError:
        return "NONE"

def _severity_counts(obj):
    """サマリーレスポンスから深刻度別件数を抽出（キー名 / 配列のどちらの形式にも対応）"""
    counts = {s: 0 for s in SEV_ORDER}
    found = False
    def walk(o):
        nonlocal found
        if isinstance(o, dict):
            sev_key = next((k for k in o if k.lower() in ("severity", "sev", "level", "name", "key")), None)
            cnt_key = next((k for k in o if k.lower() in ("count", "total", "value", "doc_count", "vulnerability_count")), None)
            if sev_key and cnt_key and isinstance(o[cnt_key], (int, float)) and _norm_sev(o[sev_key]) != "NONE":
                counts[_norm_sev(o[sev_key])] += int(o[cnt_key]); found = True
                return
            for k, v in o.items():
                kk = k.upper()
                if isinstance(v, (int, float)) and any(kk == s or kk.startswith(s + "_") or kk.endswith("_" + s) for s in SEV_ORDER[:4]):
                    counts[_norm_sev(kk)] += int(v); found = True
                else:
                    walk(v)
        elif isinstance(o, list):
            for x in o:
                walk(x)
    walk(obj)
    return counts if found else None

def _risk10(v):
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return round(f / 10.0, 1) if f > 10 else round(f, 1)

def _guess_country(dev, overrides, tz_sign):
    hay = " ".join(str(x) for x in [dev.get("device_name"), dev.get("parent_device_group_name"), dev.get("path"),
                                    " ".join(dev.get("dns_names") or [])]).lower()
    for pat, cc in overrides:
        if pat and pat in hay:
            return cc, "指定"
    for n in (dev.get("dns_names") or []) + [dev.get("host") or ""]:
        tld = str(n).rstrip(".").rsplit(".", 1)[-1].lower()
        if tld in COUNTRY_GEO and tld not in ("us",):
            return tld, "ドメイン"
    lang = str((dev.get("os") or {}).get("lang") or "").lower()[:2]
    if lang in LANG_COUNTRY:
        return LANG_COUNTRY[lang], "OS言語"
    tz = (dev.get("os") or {}).get("tz_offset")
    if isinstance(tz, (int, float)):
        cc = TZ_COUNTRY.get(int(tz) * tz_sign)
        if cc:
            return cc, "タイムゾーン"
    return None, "不明"

def _status_risk(dev):
    s = str(dev.get("security_status") or "").upper()
    base = {"COMPROMISED": 9.5, "AT_RISK": 7.0, "UNKNOWN": 4.0, "NOT_COMPUTED": 3.5, "INITIALIZING": 3.0, "UNENROLLED": 5.0, "SECURE": 1.0}.get(s, 3.0)
    if str(dev.get("connection_status") or "").upper() == "OFFLINE":
        base = min(10.0, base + 1.0)
    return base

# ---------------- デモデータ ----------------
def _demo_devices():
    import random
    rnd = random.Random(7)
    sites = [("jp", "Tokyo-HQ", 38), ("jp", "Osaka-Branch", 14), ("us", "US-SanJose", 12), ("sg", "APAC-Singapore", 9),
             ("de", "EU-Frankfurt", 8), ("cn", "CN-Shanghai", 6), ("in", "IN-Bangalore", 7), ("gb", "UK-London", 4), ("au", "AU-Sydney", 3)]
    types = ["WINDOWS_WORKSTATION"] * 6 + ["WINDOWS_SERVER"] * 2 + ["MAC_WORKSTATION", "LINUX_SERVER"]
    devs = []
    for cc, grp, n in sites:
        for i in range(n):
            st_ = rnd.choices(["SECURE", "AT_RISK", "COMPROMISED", "NOT_COMPUTED"], [70, 22, 3, 5])[0]
            t = rnd.choice(types)
            risk = round(min(10, max(0, rnd.gauss(4.5 if st_ == "SECURE" else 7.8, 1.8))), 1)
            devs.append({"device_id": f"demo{cc}{i:03d}", "device_name": f"{grp.split('-')[0].lower()}-{t.split('_')[0][:3].lower()}-{i:03d}",
                         "parent_device_group_name": grp, "security_status": st_,
                         "connection_status": rnd.choices(["ONLINE", "OFFLINE"], [85, 15])[0],
                         "os": {"type": t, "device_os": {"WINDOWS": "Windows", "MAC": "Mac OS X", "LINUX": "Linux"}[t.split("_")[0]]},
                         "_cc": cc, "_risk": risk, "_vulns": int(max(0, rnd.gauss(risk * 6, 8)))})
    return devs

def _demo_vulns():
    import random
    rnd = random.Random(11)
    soft = ["Google Chrome", "Microsoft Edge", "OpenSSL", "Apache Log4j", "Microsoft Office", "Adobe Acrobat Reader", "Zoom Client",
            "Java SE", "7-Zip", "Windows Kernel", "Mozilla Firefox", "Python", "Node.js", "VMware Tools", "Citrix Workspace"]
    out = []
    for i in range(48):
        cvss = round(min(10, max(2, rnd.gauss(6.8, 1.9))), 1)
        out.append({"cve_id": f"CVE-202{rnd.randint(3, 6)}-{rnd.randint(1000, 49999)}", "severity": _norm_sev(cvss),
                    "risk_score": round(min(10, cvss + rnd.uniform(-1, 1.2)), 1), "cvss": cvss,
                    "affected_devices": int(max(1, rnd.expovariate(1 / 12))), "software": rnd.choice(soft),
                    "exploited": rnd.random() < 0.18})
    out.sort(key=lambda x: (-x["risk_score"], -x["affected_devices"]))
    return out

def _demo_attack():
    f1 = "eec3f761f7eabe9ed569f39e896be24c9bbb8861b15dbde1b3d539505cd9dd8d"
    f2 = "f6afa84b0847414220bb15517b8b5e2c505b64b53efbba73b753379c66ac5017"
    return {
        "insights": [
            {"kind": "file", "id": f1, "reputation": "BAD", "reputation_confidence": 100, "first_seen": "2024-05-22", "last_seen": "2025-09-24",
             "prevalence": "LessThanFifty", "actors": ["Snakefly"], "target_orgs": {"top_countries": ["us", "in", "jp", "de"], "top_industries": ["Government", "Information Technology"]}},
            {"kind": "file", "id": f2, "reputation": "BAD", "reputation_confidence": 96, "first_seen": "2024-11-02", "last_seen": "2025-10-30",
             "prevalence": "Hundreds", "actors": ["Clop"], "target_orgs": {"top_countries": ["us", "gb", "jp", "au"], "top_industries": ["Manufacturing", "Retail"]}},
            {"kind": "network", "id": "145.249.105.165", "reputation": "BAD", "reputation_confidence": 98, "first_seen": "2023-03-14", "last_seen": "2025-11-01",
             "threat_risk_level": {"level": 9}, "actors": ["Snakefly"], "target_orgs": {"top_countries": ["us", "sg", "jp"], "top_industries": ["Financial Services"]}},
            {"kind": "network", "id": "nicolascoolman.eu", "reputation": "BAD", "reputation_confidence": 90, "first_seen": "2024-01-08", "last_seen": "2025-08-19",
             "threat_risk_level": {"level": 7}, "actors": ["Snakefly"], "target_orgs": {"top_countries": ["fr", "de", "jp"], "top_industries": ["Healthcare"]}},
            {"kind": "network", "id": "115.55.57.208", "reputation": "BAD", "reputation_confidence": 100, "first_seen": "2020-07-21", "last_seen": "2025-01-30",
             "threat_risk_level": {"level": 6}, "actors": ["Waterbug"], "target_orgs": {"top_countries": ["us", "kr"], "top_industries": ["Information Technology"]}},
        ],
        "related": [
            {"from": f1, "ioc_type": "network", "ioc_values": ["nicolascoolman.eu", "145.249.105.165"], "relation": "byThreatActor"},
            {"from": f1, "ioc_type": "file", "ioc_values": [f2], "relation": "bySignature"},
            {"from": "145.249.105.165", "ioc_type": "file", "ioc_values": [f1], "relation": "bySignature"},
            {"from": f2, "ioc_type": "network", "ioc_values": ["115.55.57.208"], "relation": "byNetworkTrait"},
            {"from": "115.55.57.208", "ioc_type": "file", "ioc_values": ["9b1c7e0d4a2f6e8b3c5d7a9e1f2b4c6d8e0a1b3c5d7e9f1a2b4c6d8e0f1a2b3c"], "relation": "byIncident"},
        ],
        "chains": [
            {"file": f1, "parent": {"file": "a732df0b1b4b4b8dbf5dc2c9286c212cb172d29ddfa88a2c5e5e9f84ec0d5380", "process_name": "winlogon.exe"},
             "child": {"file": f1, "process_name": "malware.exe"}},
            {"file": f1, "parent": {"file": "1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e", "process_name": "explorer.exe"},
             "child": {"file": "a732df0b1b4b4b8dbf5dc2c9286c212cb172d29ddfa88a2c5e5e9f84ec0d5380", "process_name": "powershell.exe"}},
            {"file": f2, "parent": {"file": "4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d", "process_name": "outlook.exe"},
             "child": {"file": f2, "process_name": "invoice_viewer.exe"}},
        ],
        "origins": {"145.249.105.165": "nl", "115.55.57.208": "cn", "nicolascoolman.eu": "ru"},
    }

def _dash_header(title, sub):
    st.markdown(f"### {title}")
    st.caption(sub)

def _dash_source(key):
    """データソース選択（ライブは認証済みのときのみ）"""
    authed = bool(st.session_state.get("global_token"))
    if authed:
        st.success("🔓 トークン認証済み（グローバル適用中）— ライブデータを取得できます。")
    else:
        st.warning("🔒 トークン未認証です。🔑 Authentication ページで『🌐 グローバル適用』を行うと、ライブデータを取得できます（それまではデモデータで表示）。")
    src = st.radio("データソース", ["ライブ（CBX API）", "デモデータ"], index=0 if authed else 1, horizontal=True, key=f"{key}_src")
    if src.startswith("ライブ") and not authed:
        st.error("トークン認証後に利用できます。デモデータで表示します。")
        return "demo"
    return "live" if src.startswith("ライブ") else "demo"

def _render_html(html, height):
    components.html(DASH_CSS + html, height=height, scrolling=True)

# ---------------- ① 管理クライアント ----------------
def render_dash_client():
    _dash_header("📊 管理クライアント ダッシュボード", "デバイス（資産）× リスクスコア × 拠点（国旗）を 3D 地球儀で可視化")
    src = _dash_source("dc")
    with st.expander("⚙️ 取得設定 / 拠点（国）の推定ルール", expanded=False):
        max_dev = st.number_input("最大取得デバイス数", min_value=100, max_value=10000, value=1000, step=100, key="dc_max")
        use_vuln = st.checkbox("脆弱性サマリー（デバイス別の最高リスクスコア・脆弱性数）を取得する", value=True, key="dc_vuln")
        vuln_body = st.text_area("POST .../devices/vulnerabilities/summary/_search の Body（JSON）", value="{}", height=70, key="dc_vbody")
        tz_sign = 1 if st.radio("os.tz_offset の符号", ["UTC+ が正（例: 日本 = 540）", "UTC+ が負（例: 日本 = -540）"], key="dc_tz").startswith("UTC+ が正") else -1
        ov_txt = st.text_area("拠点の指定（1行に『キーワード=国コード』。デバイス名 / グループ名 / パス / DNS に部分一致）",
                              value="tokyo=jp\nosaka=jp\njapan=jp", height=90, key="dc_ov")
        st.caption("国の推定順: ①上記の指定 → ②DNS 名の国別ドメイン（.jp 等）→ ③OS 言語 → ④タイムゾーン。API に位置情報がないため推定値です。")
        home_cc = st.text_input("自社拠点（未判定デバイスの表示先）国コード", value="jp", key="dc_home").strip().lower() or "jp"
    overrides = [tuple(x.strip().lower() for x in l.split("=", 1)) for l in ov_txt.splitlines() if "=" in l]

    if src == "live":
        if st.button("🔄 再取得", key="dc_fetch") or "dc_data" not in st.session_state:  # 開いた瞬間に自動取得
            devs, page, errs = [], 1, []
            with st.spinner("デバイス一覧を取得中..."):
                while len(devs) < max_dev:
                    code, data = dash_api("GET", "/agent-management/devices/v2/devices",
                                          params={"page": page, "page_size": min(1000, int(max_dev)), "include_path": "true"})
                    if code != 200:
                        errs.append(f"devices: Status {code} {str(data)[:200]}"); break
                    batch = data.get("devices") or []
                    devs += batch
                    if not batch or page >= int(data.get("total_pages") or 1):
                        break
                    page += 1
            vmap = {}
            if use_vuln:
                try:
                    vb = json.loads(vuln_body or "{}")
                except Exception as e:
                    vb = {}; errs.append(f"Body の JSON が不正です: {e}")
                with st.spinner("デバイス別の脆弱性サマリーを取得中..."):
                    code, vdata = dash_api("POST", "/endpoint-security/vulnerability/assessment/v3/devices/vulnerabilities/summary/_search", body=vb)
                if code == 200:
                    for r in _find_records(vdata):
                        did = _pick(r, ["device_uid", "device_id", "uid", "id"])
                        nm = _pick(r, ["device_name", "name", "host"])
                        rs = _pick(r, ["highest_risk_score", "max_risk_score", "risk_score"], contains=["risk"], numeric=True)
                        vc = _pick(r, ["vulnerability_count", "vuln_count", "total_vulnerabilities", "count"], contains=["vuln"], numeric=True)
                        for key in (did, nm):
                            if key:
                                vmap[str(key).lower()] = (rs, vc)
                else:
                    errs.append(f"vulnerability summary: Status {code} {str(vdata)[:200]}")
            st.session_state["dc_data"] = {"devs": devs, "vmap": vmap, "errs": errs, "at": time.strftime("%H:%M:%S")}
        cache = st.session_state.get("dc_data", {"devs": [], "vmap": {}, "errs": []})
        for e in cache.get("errs", []):
            st.error(e)
        devs = cache["devs"]
        rows = []
        for d in devs:
            v = cache["vmap"].get(str(d.get("device_id", "")).lower()) or cache["vmap"].get(str(d.get("device_name", "")).lower()) or (None, None)
            cc, how = _guess_country(d, overrides, tz_sign)
            r10 = _risk10(v[0])
            rows.append({"name": d.get("device_name") or d.get("host") or d.get("device_id"), "group": d.get("parent_device_group_name") or "",
                         "status": d.get("security_status") or "", "conn": d.get("connection_status") or "",
                         "ostype": ((d.get("os") or {}).get("type") or "UNKNOWN"), "os": (d.get("os") or {}).get("device_os") or "",
                         "cc": cc or home_cc, "cc_how": how if cc else "既定", "risk": r10 if r10 is not None else _status_risk(d),
                         "risk_src": "脆弱性" if r10 is not None else "状態から推定", "vulns": int(v[1]) if isinstance(v[1], (int, float)) else None})
        if cache.get("at"):
            st.caption(f"取得時刻: {cache['at']} / デバイス {len(rows)} 台")
    else:
        rows = [{"name": d["device_name"], "group": d["parent_device_group_name"], "status": d["security_status"], "conn": d["connection_status"],
                 "ostype": d["os"]["type"], "os": d["os"]["device_os"], "cc": d["_cc"], "cc_how": "デモ", "risk": d["_risk"],
                 "risk_src": "デモ", "vulns": d["_vulns"]} for d in _demo_devices()]

    if not rows:
        st.info("表示するデバイスがありません。")
        return

    # 集計
    by_cc = {}
    for r in rows:
        c = by_cc.setdefault(r["cc"], {"cc": r["cc"], "n": 0, "risk_sum": 0, "max": 0, "atrisk": 0, "online": 0})
        c["n"] += 1; c["risk_sum"] += r["risk"]; c["max"] = max(c["max"], r["risk"])
        c["atrisk"] += r["status"] in ("AT_RISK", "COMPROMISED"); c["online"] += r["conn"] == "ONLINE"
    countries = []
    for c in by_cc.values():
        g = COUNTRY_GEO.get(c["cc"], (0, 0, c["cc"].upper()))
        countries.append({**c, "avg": round(c["risk_sum"] / c["n"], 1), "lat": g[0], "lng": g[1], "label": g[2]})
    countries.sort(key=lambda x: -x["n"])
    status_cnt, os_cnt = {}, {}
    for r in rows:
        status_cnt[r["status"] or "UNKNOWN"] = status_cnt.get(r["status"] or "UNKNOWN", 0) + 1
        os_cnt[r["ostype"]] = os_cnt.get(r["ostype"], 0) + 1
    top = sorted(rows, key=lambda r: -r["risk"])[:40]
    n = len(rows)
    kpi = {"total": n, "online": sum(r["conn"] == "ONLINE" for r in rows),
           "atrisk": sum(r["status"] in ("AT_RISK", "COMPROMISED") for r in rows),
           "comp": sum(r["status"] == "COMPROMISED" for r in rows),
           "avg": round(sum(r["risk"] for r in rows) / n, 1), "high": sum(r["risk"] >= 7 for r in rows), "countries": len(countries)}

    def rc(v):
        return "#ff2d55" if v >= 9 else "#ff7a1a" if v >= 7 else "#ffd23f" if v >= 4 else "#2ee6a6"
    trs = "".join(
        f"<tr><td>{_flag_img(r['cc'])}{r['name']}</td><td>{r['group']}</td><td>{r['os']}</td>"
        f"<td><span class='pill' style='background:{'#3a0d18' if r['status'] in ('AT_RISK','COMPROMISED') else '#0d3a2b'};color:{'#ff6b8a' if r['status'] in ('AT_RISK','COMPROMISED') else '#5ff0b8'}'>{r['status']}</span></td>"
        f"<td>{'🟢' if r['conn']=='ONLINE' else '⚫'}</td>"
        f"<td style='min-width:110px'><b style='color:{rc(r['risk'])}'>{r['risk']:.1f}</b> <div class='bar'><i style='width:{r['risk']*10}%;background:{rc(r['risk'])}'></i></div></td>"
        f"<td>{'' if r['vulns'] is None else r['vulns']}</td></tr>" for r in top)
    crs = "".join(
        f"<tr><td>{_flag_img(c['cc'])}{c['label']}</td><td>{c['n']}</td><td style='color:{rc(c['avg'])}'><b>{c['avg']}</b></td>"
        f"<td style='color:{rc(c['max'])}'>{c['max']}</td><td>{c['atrisk']}</td></tr>" for c in countries)
    payload = json.dumps({"countries": countries, "status": status_cnt, "os": os_cnt}, ensure_ascii=False)
    html = """
<div class="wrap">
 <div class="title">GLOBAL ENDPOINT RISK MAP</div><div class="sub">拠点ごとの柱の高さ = デバイス数 / 色 = 平均リスクスコア（0–10）。ドラッグで回転・ホイールでズーム</div>
 <div class="kpis">
  <div class="kpi"><div class="l">管理デバイス</div><div class="v" style="color:#4fd1ff">__TOTAL__</div></div>
  <div class="kpi"><div class="l">オンライン</div><div class="v" style="color:#2ee6a6">__ONLINE__</div></div>
  <div class="kpi" style="__ATRISK_STYLE__"><div class="l">AT_RISK / COMPROMISED</div><div class="v" style="color:#ff6b8a">__ATRISK__ <span style="font-size:14px">(侵害 __COMP__)</span></div></div>
  <div class="kpi"><div class="l">高リスク（≥7.0）</div><div class="v" style="color:#ff7a1a">__HIGH__</div></div>
  <div class="kpi"><div class="l">平均リスクスコア</div><div class="v" style="color:__AVGC__">__AVG__</div></div>
  <div class="kpi"><div class="l">拠点（国）</div><div class="v" style="color:#a96bff">__CTRY__</div></div>
 </div>
 <div class="grid2">
  <div class="card"><h4>🌐 3D リスク地球儀</h4><div id="globe" style="height:470px"></div></div>
  <div class="card"><h4>🏳️ 拠点別リスク</h4><div class="scroll" style="max-height:470px"><table><tr><th>拠点</th><th>台数</th><th>平均</th><th>最大</th><th>要注意</th></tr>__CROWS__</table></div></div>
 </div>
 <div class="grid3" style="margin-top:10px">
  <div class="card"><h4>🛡️ セキュリティ状態</h4><div id="st" style="height:250px"></div></div>
  <div class="card"><h4>💻 OS タイプ</h4><div id="os" style="height:250px"></div></div>
  <div class="card"><h4>📶 リスク分布（3D）</h4><div id="r3" style="height:250px"></div></div>
 </div>
 <div class="card" style="margin-top:10px"><h4>🔥 高リスク デバイス TOP 40</h4><div class="scroll"><table>
  <tr><th>デバイス</th><th>グループ</th><th>OS</th><th>状態</th><th>接続</th><th>リスク</th><th>脆弱性数</th></tr>__TROWS__</table></div></div>
</div>
<script src="https://unpkg.com/globe.gl"></script>
<script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/echarts-gl@2/dist/echarts-gl.min.js"></script>
<script>
const D = __DATA__;
const rc = v => v>=9?'#ff2d55':v>=7?'#ff7a1a':v>=4?'#ffd23f':'#2ee6a6';
try {
  const maxN = Math.max(...D.countries.map(c=>c.n));
  const g = Globe()(document.getElementById('globe'))
    .globeImageUrl('https://unpkg.com/three-globe/example/img/earth-night.jpg')
    .bumpImageUrl('https://unpkg.com/three-globe/example/img/earth-topology.png')
    .backgroundImageUrl('https://unpkg.com/three-globe/example/img/night-sky.png')
    .width(document.getElementById('globe').clientWidth).height(470)
    .pointsData(D.countries).pointLat('lat').pointLng('lng')
    .pointAltitude(c => 0.05 + 0.45*c.n/maxN).pointRadius(1.2).pointColor(c => rc(c.avg))
    .pointLabel(c => `<div style="background:#0a1226ee;padding:6px 8px;border:1px solid #2b4a8a;border-radius:6px">
        <img src="https://flagcdn.com/w40/${c.cc}.png" style="width:24px;vertical-align:middle"> <b>${c.label}</b><br>
        デバイス ${c.n} 台 / 平均リスク <b style="color:${rc(c.avg)}">${c.avg}</b> / 最大 ${c.max}<br>要注意 ${c.atrisk} 台</div>`)
    .ringsData(D.countries.filter(c=>c.avg>=7||c.atrisk>0)).ringLat('lat').ringLng('lng')
    .ringColor(c => t => `rgba(255,45,85,${1-t})`).ringMaxRadius(6).ringPropagationSpeed(2.5).ringRepeatPeriod(1100)
    .htmlElementsData(D.countries).htmlLat('lat').htmlLng('lng').htmlAltitude(c => 0.06 + 0.45*c.n/maxN)
    .htmlElement(c => { const el=document.createElement('div');
        el.innerHTML=`<img src="https://flagcdn.com/w40/${c.cc}.png" style="width:20px;border-radius:2px;box-shadow:0 0 6px #000"><span style="color:#fff;font:700 11px Segoe UI;text-shadow:0 0 4px #000;margin-left:3px">${c.n}</span>`;
        el.style.pointerEvents='none'; return el; });
  g.controls().autoRotate = true; g.controls().autoRotateSpeed = 0.5;
  const home = D.countries[0]; g.pointOfView({lat: home.lat, lng: home.lng, altitude: 2.2}, 0);
} catch(e) { document.getElementById('globe').innerHTML = '<div style="padding:20px;color:#ff7a1a">3D 地球儀を読み込めませんでした（CDN へのアクセスを確認してください）</div>'; }
try {
  const pie = (id, obj, colors) => echarts.init(document.getElementById(id)).setOption({
    tooltip:{trigger:'item'}, legend:{bottom:0,textStyle:{color:'#9fb3d9',fontSize:10}},
    series:[{type:'pie',radius:['45%','72%'],center:['50%','44%'],itemStyle:{borderColor:'#050a18',borderWidth:2},
      label:{color:'#dbe7ff',formatter:'{b}\\n{c}'},data:Object.entries(obj).map(([k,v])=>({name:k,value:v,itemStyle:colors&&colors[k]?{color:colors[k]}:undefined}))}]});
  pie('st', D.status, {SECURE:'#2ee6a6',AT_RISK:'#ff7a1a',COMPROMISED:'#ff2d55',NOT_COMPUTED:'#6b7aa1',UNKNOWN:'#6b7aa1',INITIALIZING:'#4fd1ff',UNENROLLED:'#a96bff'});
  pie('os', D.os);
  const bins=[...Array(10).keys()]; const data=[];
  D.countries.forEach((c,ci)=>bins.forEach(b=>data.push([b,ci,0])));
  (__RISKS__).forEach(([cc,r])=>{const ci=D.countries.findIndex(c=>c.cc===cc);const b=Math.min(9,Math.floor(r));data[ci*10+b][2]++;});
  echarts.init(document.getElementById('r3')).setOption({
    tooltip:{}, visualMap:{show:false,min:0,max:Math.max(1,...data.map(d=>d[2])),inRange:{color:['#12306b','#4fd1ff','#ffd23f','#ff2d55']}},
    xAxis3D:{type:'category',name:'リスク',data:bins.map(b=>b+'-'+(b+1)),axisLabel:{color:'#9fb3d9',fontSize:9},nameTextStyle:{color:'#9fb3d9'}},
    yAxis3D:{type:'category',name:'拠点',data:D.countries.map(c=>c.cc.toUpperCase()),axisLabel:{color:'#9fb3d9',fontSize:9},nameTextStyle:{color:'#9fb3d9'}},
    zAxis3D:{type:'value',name:'台数',axisLabel:{color:'#9fb3d9'},nameTextStyle:{color:'#9fb3d9'}},
    grid3D:{boxWidth:120,boxDepth:70,viewControl:{autoRotate:true,autoRotateSpeed:6,distance:210},light:{main:{intensity:1.2,shadow:true},ambient:{intensity:.35}},axisLine:{lineStyle:{color:'#2b4a8a'}},splitLine:{lineStyle:{color:'#13224a'}}},
    series:[{type:'bar3D',data:data.filter(d=>d[2]>0),shading:'lambert',bevelSize:.3,label:{show:false}}]});
} catch(e) {}
</script>
"""
    risks = json.dumps([[r["cc"], r["risk"]] for r in rows])
    for k, v in {"__DATA__": payload, "__RISKS__": risks, "__TOTAL__": kpi["total"], "__ONLINE__": kpi["online"], "__ATRISK__": kpi["atrisk"],
                 "__COMP__": kpi["comp"], "__HIGH__": kpi["high"], "__AVG__": kpi["avg"], "__AVGC__": rc(kpi["avg"]), "__CTRY__": kpi["countries"],
                 "__ATRISK_STYLE__": "animation:pulse 1.6s infinite;border-color:#ff2d55" if kpi["comp"] else "",
                 "__CROWS__": crs, "__TROWS__": trs}.items():
        html = html.replace(k, str(v))
    _render_html(html, 1330)
    if src == "live":
        with st.expander("🧾 推定根拠（拠点 / リスクスコア）"):
            st.json([{k: r[k] for k in ("name", "cc", "cc_how", "risk", "risk_src")} for r in rows[:200]])

# ---------------- ② 脆弱性レポート ----------------
def render_dash_vuln():
    _dash_header("🧯 脆弱性レポート ダッシュボード", "深刻度に応じて警告表示（CRITICAL は点滅アラート）。CVE × 影響デバイス × リスクを 3D で可視化")
    src = _dash_source("dv")
    with st.expander("⚙️ 取得設定", expanded=False):
        cve_body = st.text_area("POST .../devices/vulnerabilities/_search の Body（JSON）", value="{}", height=70, key="dv_body")
        dev_body = st.text_area("POST .../devices/vulnerabilities/summary/_search の Body（JSON）", value="{}", height=70, key="dv_dbody")
        st.caption("cbx_vuln_assessment.md にレスポンス形式の記載がないため、レスポンスから件数・CVE・深刻度・リスクスコアを自動抽出します（『🧾 生レスポンス』で確認できます）。")
    raw = {}
    if src == "live":
        if st.button("🔄 再取得", key="dv_fetch") or "dv_data" not in st.session_state:  # 開いた瞬間に自動取得
            errs = []
            with st.spinner("脆弱性データを取得中..."):
                c1, summ = dash_api("GET", "/endpoint-security/vulnerability/assessment/v3/vulnerabilities/summary")
                try:
                    c2, cves = dash_api("POST", "/endpoint-security/vulnerability/assessment/v3/devices/vulnerabilities/_search", body=json.loads(cve_body or "{}"))
                except ValueError as e:
                    c2, cves = 0, {}; errs.append(f"Body の JSON が不正です: {e}")
                try:
                    c3, devv = dash_api("POST", "/endpoint-security/vulnerability/assessment/v3/devices/vulnerabilities/summary/_search", body=json.loads(dev_body or "{}"))
                except ValueError as e:
                    c3, devv = 0, {}; errs.append(f"Body の JSON が不正です: {e}")
            for nm, c, d in (("summary", c1, summ), ("vulnerabilities/_search", c2, cves), ("devices summary/_search", c3, devv)):
                if c != 200:
                    errs.append(f"{nm}: Status {c} {str(d)[:200]}")
            st.session_state["dv_data"] = {"summ": summ if c1 == 200 else {}, "cves": cves if c2 == 200 else {}, "devv": devv if c3 == 200 else {},
                                           "errs": errs, "at": time.strftime("%H:%M:%S")}
        cache = st.session_state.get("dv_data", {})
        for e in cache.get("errs", []):
            st.error(e)
        raw = cache
        vulns = []
        for r in _find_records(cache.get("cves", {})):
            cve = _pick(r, ["cve_id", "cve", "id", "name"])
            rs = _pick(r, ["risk_score", "highest_risk_score"], contains=["risk"], numeric=True)
            cv = _pick(r, ["cvss_score", "cvss", "base_score", "score"], contains=["cvss"], numeric=True)
            sev = _pick(r, ["severity", "severity_level", "cvss_severity"]) or cv or rs
            ad = _pick(r, ["affected_devices", "affected_device_count", "device_count", "devices_count", "asset_count"], contains=["device"], numeric=True)
            sw = _pick(r, ["software", "product", "software_name", "product_name", "vendor"])
            if isinstance(sw, (list, dict)):
                sw = json.dumps(sw, ensure_ascii=False)[:60]
            ex = _pick(r, ["exploited", "known_exploited", "is_exploited", "kev"], contains=["exploit"])
            vulns.append({"cve_id": str(cve or "?"), "severity": _norm_sev(sev), "risk_score": _risk10(rs) if rs is not None else (_risk10(cv) or 0),
                          "cvss": cv, "affected_devices": int(ad or 1), "software": str(sw or ""), "exploited": bool(ex)})
        sev_counts = _severity_counts(cache.get("summ", {}))
        assets = _pick(cache.get("summ", {}), ["monitored_assets", "monitored_asset_count", "asset_count", "total_assets", "assets"], contains=["asset"], numeric=True)
        dev_top = []
        for r in _find_records(cache.get("devv", {})):
            dev_top.append({"name": str(_pick(r, ["device_name", "name", "host", "device_uid", "device_id"]) or "?"),
                            "risk": _risk10(_pick(r, ["highest_risk_score", "risk_score"], contains=["risk"], numeric=True)) or 0,
                            "count": int(_pick(r, ["vulnerability_count", "vuln_count", "total"], contains=["vuln"], numeric=True) or 0)})
        if cache.get("at"):
            st.caption(f"取得時刻: {cache['at']}")
    else:
        vulns = _demo_vulns()
        sev_counts, assets = None, 112
        dev_top = [{"name": d["device_name"], "risk": d["_risk"], "count": d["_vulns"]} for d in sorted(_demo_devices(), key=lambda x: -x["_risk"])[:15]]
    if sev_counts is None:
        sev_counts = {s: 0 for s in SEV_ORDER}
        for v in vulns:
            sev_counts[v["severity"]] += 1
    vulns.sort(key=lambda v: (SEV_ORDER.index(v["severity"]), -v["risk_score"], -v["affected_devices"]))
    dev_top = sorted(dev_top, key=lambda d: (-d["risk"], -d["count"]))[:15]
    total = sum(sev_counts[s] for s in SEV_ORDER[:4])
    # エクスポージャースコア（0-100）: 深刻度で重み付け
    w = {"CRITICAL": 10, "HIGH": 5, "MEDIUM": 2, "LOW": 0.5}
    expo = min(100, round(sum(sev_counts[s] * w[s] for s in w) / max(1, (assets or max(total, 1))) * 10, 1)) if total else 0
    crit, high = sev_counts["CRITICAL"], sev_counts["HIGH"]
    if crit:
        banner = f"<div style='animation:blink 1s infinite,pulse 1.6s infinite;background:linear-gradient(90deg,#5a0012,#a3001f,#5a0012);border:2px solid #ff2d55;border-radius:12px;padding:12px 16px;font-size:20px;font-weight:900;color:#fff;text-align:center'>🚨 CRITICAL 脆弱性 {crit} 件を検出 — 直ちにパッチ適用 / 緩和策を実施してください</div>"
    elif high:
        banner = f"<div style='background:linear-gradient(90deg,#4a2300,#8a4400);border:2px solid #ff7a1a;border-radius:12px;padding:10px 16px;font-size:18px;font-weight:800;color:#fff;text-align:center;animation:pulse 2.2s infinite'>⚠️ HIGH 脆弱性 {high} 件 — 優先的に対応してください</div>"
    else:
        banner = "<div style='background:#0d3a2b;border:1px solid #2ee6a6;border-radius:12px;padding:10px 16px;font-size:16px;font-weight:700;color:#5ff0b8;text-align:center'>✅ CRITICAL / HIGH の脆弱性はありません</div>"
    sev_col = {"CRITICAL": "#ff2d55", "HIGH": "#ff7a1a", "MEDIUM": "#ffd23f", "LOW": "#4fd1ff", "NONE": "#6b7aa1"}
    kcards = "".join(
        f"<div class='kpi' style='border-color:{sev_col[s]};{'animation:pulse 1.4s infinite' if s == 'CRITICAL' and crit else ''}'>"
        f"<div class='l'>{s}</div><div class='v' style='color:{sev_col[s]}'>{sev_counts[s]}</div></div>" for s in SEV_ORDER[:4])
    vrows = "".join(
        f"<tr style='{'animation:blink 1.2s infinite' if v['severity']=='CRITICAL' and v['exploited'] else ''}'>"
        f"<td><b>{v['cve_id']}</b>{' 🔥' if v['exploited'] else ''}</td>"
        f"<td><span class='pill' style='background:{sev_col[v['severity']]}22;color:{sev_col[v['severity']]};border:1px solid {sev_col[v['severity']]}'>{v['severity']}</span></td>"
        f"<td style='min-width:110px'><b style='color:{sev_col[v['severity']]}'>{v['risk_score']}</b><div class='bar'><i style='width:{min(100, v['risk_score']*10)}%;background:{sev_col[v['severity']]}'></i></div></td>"
        f"<td>{v['affected_devices']}</td><td>{v['software']}</td></tr>" for v in vulns[:60])
    drows = "".join(
        f"<tr><td>{d['name']}</td><td style='color:{'#ff2d55' if d['risk']>=9 else '#ff7a1a' if d['risk']>=7 else '#ffd23f'}'><b>{d['risk']}</b></td><td>{d['count']}</td></tr>" for d in dev_top)
    ticker = " ｜ ".join(f"{'🔴' if v['severity']=='CRITICAL' else '🟠'} {v['cve_id']} ({v['software']}) risk {v['risk_score']} / {v['affected_devices']} 台"
                        for v in vulns if v["severity"] in ("CRITICAL", "HIGH"))[:3000] or "重大な脆弱性はありません"
    payload = json.dumps({"sev": sev_counts, "vulns": vulns[:80], "expo": expo, "col": sev_col}, ensure_ascii=False)
    html = """
<div class="wrap">
 <div class="title">VULNERABILITY THREAT BOARD</div><div class="sub">監視資産 __ASSETS__ / 脆弱性 合計 __TOTAL__ 件</div>
 __BANNER__
 <div style="overflow:hidden;white-space:nowrap;border:1px solid #3a1020;background:#12050b;border-radius:8px;margin-top:8px;padding:5px 0">
  <div style="display:inline-block;animation:ticker 40s linear infinite;color:#ff9fb3;font-weight:700;font-size:13px">__TICKER__</div></div>
 <div class="kpis">__KCARDS__</div>
 <div class="grid3">
  <div class="card"><h4>🎯 エクスポージャースコア</h4><div id="gauge" style="height:260px"></div></div>
  <div class="card"><h4>📊 深刻度の内訳</h4><div id="sev" style="height:260px"></div></div>
  <div class="card"><h4>💻 脆弱デバイス TOP 15</h4><div class="scroll" style="max-height:260px"><table><tr><th>デバイス</th><th>最高リスク</th><th>件数</th></tr>__DROWS__</table></div></div>
 </div>
 <div class="grid2" style="margin-top:10px">
  <div class="card"><h4>🧊 3D：CVE × 影響デバイス数 × リスクスコア</h4><div id="b3" style="height:430px"></div></div>
  <div class="card"><h4>🗺️ ソフトウェア別 リスクマップ</h4><div id="tm" style="height:430px"></div></div>
 </div>
 <div class="card" style="margin-top:10px"><h4>📋 優先対応 CVE（🔥 = 悪用確認）</h4><div class="scroll"><table>
  <tr><th>CVE</th><th>深刻度</th><th>リスク</th><th>影響デバイス</th><th>ソフトウェア</th></tr>__VROWS__</table></div></div>
</div>
<script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/echarts-gl@2/dist/echarts-gl.min.js"></script>
<script>
const D = __DATA__;
try {
 echarts.init(document.getElementById('gauge')).setOption({series:[{type:'gauge',min:0,max:100,progress:{show:true,width:16},
   axisLine:{lineStyle:{width:16,color:[[.3,'#2ee6a6'],[.6,'#ffd23f'],[.8,'#ff7a1a'],[1,'#ff2d55']]}},
   pointer:{itemStyle:{color:'#fff'}},axisLabel:{color:'#8aa0c8'},splitLine:{lineStyle:{color:'#fff'}},
   detail:{valueAnimation:true,color:'#fff',fontSize:34,fontWeight:800,offsetCenter:[0,'70%']},title:{color:'#8aa0c8',offsetCenter:[0,'95%']},
   data:[{value:D.expo,name:'Exposure'}]}]});
 const sevs=['CRITICAL','HIGH','MEDIUM','LOW'];
 echarts.init(document.getElementById('sev')).setOption({tooltip:{},
   xAxis:{type:'category',data:sevs,axisLabel:{color:'#9fb3d9'}},yAxis:{type:'value',axisLabel:{color:'#9fb3d9'},splitLine:{lineStyle:{color:'#13224a'}}},
   series:[{type:'bar',data:sevs.map(s=>({value:D.sev[s],itemStyle:{color:new echarts.graphic.LinearGradient(0,0,0,1,[{offset:0,color:D.col[s]},{offset:1,color:D.col[s]+'33'}]),borderRadius:[6,6,0,0]}})),
     label:{show:true,position:'top',color:'#fff',fontWeight:700},animationDuration:1500,animationEasing:'elasticOut'}]});
 const v=D.vulns.slice(0,40);
 echarts.init(document.getElementById('b3')).setOption({tooltip:{formatter:p=>`${v[p.value[3]].cve_id}<br>${v[p.value[3]].software}<br>risk ${v[p.value[3]].risk_score} / ${v[p.value[3]].affected_devices} 台`},
   visualMap:{show:false,dimension:2,min:0,max:10,inRange:{color:['#4fd1ff','#ffd23f','#ff7a1a','#ff2d55']}},
   xAxis3D:{type:'category',name:'CVE',data:v.map(x=>x.cve_id),axisLabel:{show:false},nameTextStyle:{color:'#9fb3d9'}},
   yAxis3D:{type:'category',name:'深刻度',data:sevs,axisLabel:{color:'#9fb3d9'},nameTextStyle:{color:'#9fb3d9'}},
   zAxis3D:{type:'value',name:'リスク',max:10,axisLabel:{color:'#9fb3d9'},nameTextStyle:{color:'#9fb3d9'}},
   grid3D:{boxWidth:200,boxDepth:60,viewControl:{autoRotate:true,autoRotateSpeed:5,distance:230,alpha:22},
     light:{main:{intensity:1.3,shadow:true},ambient:{intensity:.3}},axisLine:{lineStyle:{color:'#2b4a8a'}},splitLine:{lineStyle:{color:'#13224a'}}},
   series:[{type:'bar3D',shading:'lambert',bevelSize:.4,barSize:[3,6],
     data:v.map((x,i)=>({value:[i,Math.max(0,sevs.indexOf(x.severity)),x.risk_score,i]}))}]});
 const sw={}; D.vulns.forEach(x=>{const k=x.software||'(不明)';sw[k]=sw[k]||{name:k,value:0,risk:0};sw[k].value+=x.affected_devices;sw[k].risk=Math.max(sw[k].risk,x.risk_score);});
 echarts.init(document.getElementById('tm')).setOption({tooltip:{formatter:p=>`${p.name}<br>影響 ${p.value} 台 / 最高リスク ${p.data.risk}`},
   series:[{type:'treemap',roam:false,breadcrumb:{show:false},label:{color:'#fff',fontWeight:700},
     data:Object.values(sw).map(s=>({...s,itemStyle:{color:s.risk>=9?'#b0102f':s.risk>=7?'#c2570f':s.risk>=4?'#a88a12':'#1b6a8a',borderColor:'#050a18',borderWidth:2}}))}]});
} catch(e) {}
</script>
"""
    for k, v in {"__DATA__": payload, "__ASSETS__": assets if assets is not None else "—", "__TOTAL__": total, "__BANNER__": banner,
                 "__TICKER__": ticker, "__KCARDS__": kcards, "__DROWS__": drows or "<tr><td colspan=3>データなし</td></tr>",
                 "__VROWS__": vrows or "<tr><td colspan=5>データなし</td></tr>"}.items():
        html = html.replace(k, str(v))
    _render_html(html, 1500)
    if src == "live":
        with st.expander("🧾 生レスポンス（抽出結果の確認用）"):
            st.json({"summary": raw.get("summ"), "vulnerabilities_search": raw.get("cves"), "devices_summary_search": raw.get("devv")})

# ---------------- ③ 攻撃フォロー ----------------
def render_dash_attack():
    _dash_header("⚔️ 攻撃フォロー ダッシュボード",
                 "Threat Intel（Data Related / Insight / Process Chain）のファイル・ネットワーク情報から攻撃の広がりをアニメーション表示")
    src = _dash_source("da")
    c1, c2 = st.columns(2)
    with c1:
        files_txt = st.text_area("起点ファイル SHA-256（1行に1つ）", height=90, key="da_files",
                                 value="eec3f761f7eabe9ed569f39e896be24c9bbb8861b15dbde1b3d539505cd9dd8d\nf6afa84b0847414220bb15517b8b5e2c505b64b53efbba73b753379c66ac5017")
    with c2:
        nets_txt = st.text_area("起点ネットワーク（ドメイン / URL / グローバル IP、1行に1つ）", height=90, key="da_nets",
                                value="145.249.105.165\nnicolascoolman.eu\n115.55.57.208")
    with st.expander("⚙️ 取得設定", expanded=False):
        expand = st.checkbox("関連 IOC をもう 1 段階たどる（API 呼び出し回数が増えます）", value=False, key="da_expand")
        max_exp = st.number_input("追加でたどる IOC の上限", min_value=1, max_value=50, value=10, key="da_maxexp")
        chain_related = st.checkbox("関連 IOC として見つかったファイルの Process Chain も取得する", value=True, key="da_chainrel")
        max_chain_pages = st.number_input("Process Chain の最大取得ページ数（1 ページ 100 件）", min_value=1, max_value=20, value=5, key="da_chainpg")
        geo = st.checkbox("ネットワーク IOC の発信地を IP 位置情報で推定する（外部サービス ipwho.is に IP を送信します）", value=False, key="da_geo")
        home_cc = st.text_input("自社拠点 国コード", value="jp", key="da_home").strip().lower() or "jp"
    files = [x.strip().lower() for x in files_txt.splitlines() if x.strip()]
    nets = [x.strip() for x in nets_txt.splitlines() if x.strip()]

    if src == "live":
        if st.button("🔄 再解析", key="da_fetch") or "da_data" not in st.session_state:  # 開いた瞬間に自動取得
            data = {"insights": [], "related": [], "chains": [], "origins": {}, "errs": []}
            seen = set()
            chain_done = set()
            def fetch_chain(sha):
                """Process Chain を全ページ取得（total_pages まで page を進める / 1 ページ最大 100 件）"""
                if sha in chain_done:
                    return
                chain_done.add(sha)
                pg = 1
                while pg <= int(max_chain_pages):
                    c3_, ch = dash_api("GET", f"/common/threat-intel/v1/process-chain/file/{quote(sha, safe='')}",
                                       params={"page": pg, "page_size": 100})
                    if c3_ != 200:
                        if c3_ != 404:
                            data["errs"].append(f"process-chain {sha[:12]}…: Status {c3_} {str(ch)[:150]}")
                        break
                    for x in ch.get("chain") or []:
                        data["chains"].append({"file": sha, **x})
                    data.setdefault("chain_totals", {})[sha] = ch.get("total_results")
                    if pg >= int(ch.get("total_pages") or 1):
                        break
                    pg += 1
            def look(kind, ioc):
                if (kind, ioc) in seen:
                    return []
                seen.add((kind, ioc))
                if kind == "file":
                    c, ins = dash_api("GET", f"/common/threat-intel/v1/insight/file/{quote(ioc, safe='')}")
                    c2_, rel = dash_api("GET", f"/common/threat-intel/v1/related/file/{quote(ioc, safe='')}", params={"page_size": 50})
                    fetch_chain(ioc)
                else:
                    # 実環境はパス形式（/insight/network/{ioc}）のみ受け付ける（md はクエリ形式）。失敗時はクエリ形式で再試行
                    c, ins = dash_api("GET", f"/common/threat-intel/v1/insight/network/{net_path(ioc)}")
                    if c in (400, 404, 405):
                        c_q, ins_q = dash_api("GET", "/common/threat-intel/v1/insight/network", params={"network": ioc})
                        if c_q == 200:
                            c, ins = c_q, ins_q
                    c2_, rel = dash_api("GET", f"/common/threat-intel/v1/related/network/{net_path(ioc)}", params={"page_size": 50})
                if c == 200:
                    data["insights"].append({"kind": kind, "id": ioc, **{k: v for k, v in ins.items() if k not in ("file", "network")}})
                else:
                    data["errs"].append(f"insight {kind} {ioc[:24]}: Status {c} {str(ins)[:150]}")
                out = []
                if c2_ == 200:
                    for g in rel.get("related") or []:
                        data["related"].append({"from": ioc, **g})
                        out += [(g.get("ioc_type") or "file", v) for v in g.get("ioc_values") or []]
                else:
                    data["errs"].append(f"related {kind} {ioc[:24]}: Status {c2_} {str(rel)[:150]}")
                return out
            with st.spinner("Threat Intel を照会中..."):
                nxt = []
                for f in files:
                    nxt += look("file", f)
                for n_ in nets:
                    nxt += look("network", n_)
                if expand:
                    for kind, ioc in nxt[: int(max_exp)]:
                        look("file" if kind == "file" else "network", ioc)
                if chain_related:  # 関連 IOC として見つかったファイルの Process Chain も取得
                    for kind, ioc in nxt:
                        if kind == "file" and re.fullmatch(r"[0-9a-fA-F]{64}", ioc or ""):
                            fetch_chain(ioc.lower())
                if geo:
                    import socket
                    for kind, ioc in list(seen):
                        if kind != "network":
                            continue
                        host = re.sub(r"^[a-z]+://", "", ioc).split("/")[0].strip("[]")
                        try:
                            ip = host if re.match(r"^[0-9.]+$|:", host) else socket.gethostbyname(host)
                            g = requests.get(f"https://ipwho.is/{ip}", timeout=8).json()
                            if g.get("country_code"):
                                data["origins"][ioc] = g["country_code"].lower()
                        except Exception:
                            pass
            data["at"] = time.strftime("%H:%M:%S")
            st.session_state["da_data"] = data
        data = st.session_state["da_data"]
        for e in data.get("errs", []):
            st.error(e)
        if data.get("at"):
            st.caption(f"解析時刻: {data['at']}")
    else:
        data = _demo_attack()

    # ---- グラフ構築 ----
    nodes, links = {}, []
    def short(x):
        return x[:10] + "…" if len(x) > 20 else x
    def add(nid, ntype, label, **kw):
        if nid not in nodes:
            nodes[nid] = {"id": nid, "type": ntype, "label": label, "val": 3, **kw}
        else:
            nodes[nid].update({k: v for k, v in kw.items() if v is not None})
        return nid
    ins_by = {i["id"]: i for i in data["insights"]}
    for i in data["insights"]:
        lvl = (i.get("threat_risk_level") or {}).get("level")
        add(i["id"], i["kind"], short(i["id"]), rep=i.get("reputation"), conf=i.get("reputation_confidence"), lvl=lvl, seed=True)
        nodes[i["id"]]["val"] = 8
        for a in i.get("actors") or []:
            links.append({"source": add("actor:" + a, "actor", a), "target": i["id"], "rel": "攻撃者"})
            nodes["actor:" + a]["val"] = 10
        for cc in (i.get("target_orgs") or {}).get("top_countries") or []:
            links.append({"source": i["id"], "target": add("cc:" + cc.lower(), "country", COUNTRY_GEO.get(cc.lower(), (0, 0, cc.upper()))[2], cc=cc.lower()), "rel": "標的国"})
    for r in data["related"]:
        add(r["from"], "file" if len(r["from"]) == 64 and r["from"].isalnum() else "network", short(r["from"]))
        for v in r.get("ioc_values") or []:
            t = "file" if (r.get("ioc_type") == "file") else "network"
            links.append({"source": r["from"], "target": add(v, t, short(v)), "rel": r.get("relation", "")})
    for c in data["chains"]:
        p, ch = c.get("parent") or {}, c.get("child") or {}
        pid = add("proc:" + (p.get("file") or p.get("process_name", "")), "process", p.get("process_name", "?"))
        cid = add("proc:" + (ch.get("file") or ch.get("process_name", "")), "process", ch.get("process_name", "?"))
        links.append({"source": pid, "target": cid, "rel": "起動"})
        if ch.get("file") and ch["file"] in nodes:
            links.append({"source": cid, "target": ch["file"], "rel": "実体"})
    # 地球儀用
    arcs, rings = [], {}
    for i in data["insights"]:
        tcs = [c.lower() for c in (i.get("target_orgs") or {}).get("top_countries") or [] if c.lower() in COUNTRY_GEO]
        lvl = (i.get("threat_risk_level") or {}).get("level") or (9 if i.get("reputation") == "BAD" else 4)
        for cc in tcs:
            rings[cc] = max(rings.get(cc, 0), lvl)
        org = data.get("origins", {}).get(i["id"])
        if org in COUNTRY_GEO:
            srcs = [(org, "発信地 → 標的国")]
        else:
            srcs = []
        for (o, kind) in srcs:
            for cc in tcs + ([home_cc] if home_cc in COUNTRY_GEO else []):
                if cc != o:
                    arcs.append({"s": COUNTRY_GEO[o][:2], "e": COUNTRY_GEO[cc][:2], "lvl": lvl, "lab": f"{short(i['id'])}: {COUNTRY_GEO[o][2]} → {COUNTRY_GEO[cc][2]}"})
        if not srcs and len(tcs) > 1:  # 発信地不明: 同一脅威の標的国どうしを結ぶ（キャンペーンの広がり）
            for a, b in zip(tcs, tcs[1:]):
                arcs.append({"s": COUNTRY_GEO[a][:2], "e": COUNTRY_GEO[b][:2], "lvl": lvl, "lab": f"{short(i['id'])}: 標的範囲 {COUNTRY_GEO[a][2]} ↔ {COUNTRY_GEO[b][2]}"})
    ring_list = [{"lat": COUNTRY_GEO[c][0], "lng": COUNTRY_GEO[c][1], "lvl": l, "cc": c, "name": COUNTRY_GEO[c][2], "home": c == home_cc} for c, l in rings.items()]
    actors = sorted({a for i in data["insights"] for a in i.get("actors") or []})
    bad = sum(i.get("reputation") == "BAD" for i in data["insights"])
    maxlvl = max([(i.get("threat_risk_level") or {}).get("level") or 0 for i in data["insights"]] + [0])
    home_hit = home_cc in rings
    tl = [{"id": short(i["id"]), "kind": i["kind"], "s": i.get("first_seen"), "e": i.get("last_seen") or i.get("first_seen"), "rep": i.get("reputation")}
          for i in data["insights"] if i.get("first_seen")]
    # ---- Process Chain 集計 ----
    rep_by = {i["id"]: i.get("reputation") for i in data["insights"]}
    pc_pairs, pc_nodes, pc_parent_cnt, pc_child_cnt = {}, {}, {}, {}
    for c in data["chains"]:
        p, ch = c.get("parent") or {}, c.get("child") or {}
        pn, cn = p.get("process_name") or "?", ch.get("process_name") or "?"
        pk, ck = f"{pn}|{(p.get('file') or '')[:8]}", f"{cn}|{(ch.get('file') or '')[:8]}"
        for key, nm, fh in ((pk, pn, p.get("file")), (ck, cn, ch.get("file"))):
            pc_nodes.setdefault(key, {"name": key, "proc": nm, "sha": fh or "", "bad": rep_by.get(fh or "") == "BAD"})
        pc_pairs[(pk, ck)] = pc_pairs.get((pk, ck), 0) + 1
        pc_parent_cnt[pn] = pc_parent_cnt.get(pn, 0) + 1
        pc_child_cnt[cn] = pc_child_cnt.get(cn, 0) + 1
    # 循環（A→B→A）は Sankey で描けないため除外
    pc_links, _adj = [], {}
    for (a, b), v in pc_pairs.items():
        if a == b:
            continue
        # b から a へ到達できるなら追加すると循環になるので除外（Sankey は DAG のみ）
        stack, seen_ = [b], set()
        cyc = False
        while stack:
            x = stack.pop()
            if x == a:
                cyc = True; break
            if x in seen_:
                continue
            seen_.add(x); stack += _adj.get(x, [])
        if not cyc:
            _adj.setdefault(a, []).append(b)
            pc_links.append({"source": a, "target": b, "value": v})
    # 系統ツリー（ルート = 親を持たないプロセス）
    children = {}
    for (a, b) in pc_pairs:
        if a != b:
            children.setdefault(a, []).append(b)
    has_parent = {b for (a, b) in pc_pairs if a != b}
    def build_tree(k, depth=0, path=()):
        n = pc_nodes[k]
        node = {"name": n["proc"], "sha": n["sha"], "bad": n["bad"],
                "itemStyle": {"color": "#ff2d55" if n["bad"] else "#a96bff", "borderColor": "#fff"}}
        if depth < 8 and k not in path:
            kids = [build_tree(x, depth + 1, path + (k,)) for x in children.get(k, [])]
            if kids:
                node["children"] = kids
        return node
    roots = [k for k in pc_nodes if k not in has_parent] or list(pc_nodes)[:1]
    pc_tree = {"name": "Process Lineage", "itemStyle": {"color": "#4fd1ff"}, "children": [build_tree(r) for r in roots[:30]]}
    pc_rows = "".join(
        f"<tr><td>{short(c.get('file',''))}</td><td>⚙️ <b>{(c.get('parent') or {}).get('process_name','?')}</b><div style='font-size:10px;color:#7f95c2'>{(c.get('parent') or {}).get('file','')}</div></td>"
        f"<td style='color:#ff2d55;font-size:16px'>━▶</td>"
        f"<td><b style='color:{'#ff2d55' if rep_by.get((c.get('child') or {}).get('file','')) == 'BAD' else '#ff9fb3'}'>{(c.get('child') or {}).get('process_name','?')}</b>"
        f"<div style='font-size:10px;color:#7f95c2'>{(c.get('child') or {}).get('file','')}</div></td>"
        f"<td style='font-size:10px;color:#7f95c2'>{short((c.get('parent') or {}).get('parent_sha256') or '—')}</td></tr>" for c in data["chains"][:200])
    top_par = sorted(pc_parent_cnt.items(), key=lambda x: -x[1])[:10]
    top_chi = sorted(pc_child_cnt.items(), key=lambda x: -x[1])[:10]
    pc_sec = "" if not data["chains"] else f"""
 <div class="title" style="margin-top:14px;font-size:18px">⛓️ PROCESS CHAIN ANALYSIS</div>
 <div class="sub">GET /common/threat-intel/v1/process-chain/file/{{file_sha256}} — 親子プロセスの系統（赤 = BAD 判定のファイル）</div>
 <div class="kpis">
  <div class="kpi"><div class="l">親子ペア</div><div class="v" style="color:#a96bff">{len(data['chains'])}</div></div>
  <div class="kpi"><div class="l">ユニーク プロセス</div><div class="v" style="color:#4fd1ff">{len(pc_nodes)}</div></div>
  <div class="kpi"><div class="l">起点（親）プロセス</div><div class="v" style="color:#ffd23f">{len(roots)}</div></div>
  <div class="kpi"><div class="l">最多の親プロセス</div><div class="v" style="color:#ff7a1a;font-size:18px">{top_par[0][0] if top_par else '—'}<span style="font-size:13px"> ×{top_par[0][1] if top_par else 0}</span></div></div>
 </div>
 <div class="grid2">
  <div class="card"><h4>🌊 プロセス実行フロー（Sankey）</h4><div id="pcs" style="height:420px"></div></div>
  <div class="card"><h4>🌳 プロセス系統ツリー</h4><div id="pct" style="height:420px"></div></div>
 </div>
 <div class="grid3" style="margin-top:10px">
  <div class="card"><h4>👆 親プロセス TOP</h4><div id="pcp" style="height:240px"></div></div>
  <div class="card"><h4>👇 子プロセス TOP</h4><div id="pcc" style="height:240px"></div></div>
  <div class="card"><h4>⛓️ 実行チェーン（アニメーション）</h4><div class="scroll" style="max-height:240px">__CHAINS__</div></div>
 </div>
 <div class="card" style="margin-top:10px"><h4>📋 Process Chain 詳細</h4><div class="scroll"><table>
  <tr><th>照会ファイル</th><th>親プロセス（SHA-256）</th><th></th><th>子プロセス（SHA-256）</th><th>親の親</th></tr>{pc_rows}</table></div></div>"""
    chain_html = "".join(
        f"<div style='margin:6px 0;animation:pulse 2s infinite;border-radius:8px;padding:6px 8px;background:#120b24;border:1px solid #3d2470'>"
        f"⚙️ <b>{(c.get('parent') or {}).get('process_name','?')}</b> <span style='color:#ff2d55'>━━▶</span> "
        f"<b style='color:#ff6b8a'>{(c.get('child') or {}).get('process_name','?')}</b>"
        f"<div style='font-size:10px;color:#7f95c2'>{short(c.get('file',''))}</div></div>" for c in data["chains"][:20]) or "<div style='color:#7f95c2'>プロセスチェーンなし</div>"
    payload = json.dumps({"nodes": list(nodes.values()), "links": links, "arcs": arcs, "rings": ring_list, "tl": tl,
                          "ins": data["insights"],
                          "pc": {"nodes": list(pc_nodes.values()), "links": pc_links, "tree": pc_tree, "toppar": top_par, "topchi": top_chi},
                          "home": list(COUNTRY_GEO.get(home_cc, (36.2, 138.3, ""))[:2])}, ensure_ascii=False)
    flags = "".join(f"<span style='margin-right:10px'>{_flag_img(r['cc'])}{r['name']} <b style='color:#ff6b8a'>Lv{r['lvl']}</b></span>" for r in sorted(ring_list, key=lambda x: -x["lvl"]))
    html = """
<div class="wrap">
 <div class="title">ATTACK FLOW TRACKER</div><div class="sub">粒子の流れ = IOC 間の関連（攻撃者 → IOC → 関連ファイル / 通信先 → プロセス）。赤いリング = 標的国</div>
 __HOMEALERT__
 <div class="kpis">
  <div class="kpi"><div class="l">照会 IOC</div><div class="v" style="color:#4fd1ff">__NI__</div></div>
  <div class="kpi" style="__BADSTYLE__"><div class="l">悪性（BAD）</div><div class="v" style="color:#ff2d55">__BAD__</div></div>
  <div class="kpi"><div class="l">関連 IOC</div><div class="v" style="color:#a96bff">__NREL__</div></div>
  <div class="kpi"><div class="l">攻撃者グループ</div><div class="v" style="color:#ff7a1a;font-size:18px">__ACTORS__</div></div>
  <div class="kpi"><div class="l">最大 脅威レベル</div><div class="v" style="color:#ffd23f">__MAXLVL__<span style="font-size:14px">/10</span></div></div>
 </div>
 <div class="grid2">
  <div class="card"><h4>🕸️ 3D 攻撃関係グラフ</h4><div id="fg" style="height:480px"></div>
   <div style="font-size:11px;color:#8aa0c8">● <span style="color:#ff2d55">攻撃者</span> ● <span style="color:#ff7a1a">ファイル</span> ● <span style="color:#4fd1ff">ネットワーク</span> ● <span style="color:#a96bff">プロセス</span> ● <span style="color:#2ee6a6">標的国</span></div></div>
  <div class="card"><h4>🌍 攻撃の広がり</h4><div id="globe" style="height:480px"></div></div>
 </div>
 <div class="card" style="margin-top:8px;font-size:12px">🎯 標的国: __FLAGS__</div>
 <div class="grid2" style="margin-top:10px">
  <div class="card"><h4>⏱️ 観測タイムライン（first_seen → last_seen）</h4><div id="tl" style="height:300px"></div></div>
  <div class="card"><h4>🧬 攻撃者 / 標的業界</h4><div id="ind" style="height:300px"></div></div>
 </div>
 __PCSEC__
</div>
<script src="https://unpkg.com/3d-force-graph"></script>
<script src="https://unpkg.com/globe.gl"></script>
<script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
<script>
const D = __DATA__;
const col = {actor:'#ff2d55',file:'#ff7a1a',network:'#4fd1ff',process:'#a96bff',country:'#2ee6a6'};
try {
 const el = document.getElementById('fg');
 const G = ForceGraph3D()(el).width(el.clientWidth).height(480).backgroundColor('#050a18')
  .graphData({nodes:D.nodes, links:D.links})
  .nodeColor(n => n.rep==='BAD' && n.type!=='actor' ? '#ff4060' : col[n.type]).nodeVal('val').nodeOpacity(.95)
  .nodeLabel(n => `<div style="background:#0a1226ee;padding:5px 7px;border:1px solid #2b4a8a;border-radius:6px">
     ${n.type==='country'?`<img src="https://flagcdn.com/w40/${n.cc}.png" style="width:20px;vertical-align:middle"> `:''}<b>${n.label}</b><br>
     <span style="color:#8aa0c8">${n.type}</span>${n.rep?` / ${n.rep} (${n.conf??'-'})`:''}${n.lvl!=null?` / 脅威Lv ${n.lvl}`:''}<br><span style="font-size:10px">${n.id}</span></div>`)
  .linkColor(l => l.rel==='攻撃者'?'#ff2d55':l.rel==='標的国'?'#2ee6a6':'#4f6fb0').linkOpacity(.45).linkWidth(.6)
  .linkLabel(l => l.rel)
  .linkDirectionalParticles(l => l.rel==='攻撃者'||l.rel==='起動'?5:3)
  .linkDirectionalParticleWidth(2.2).linkDirectionalParticleSpeed(.008)
  .linkDirectionalParticleColor(l => l.rel==='標的国'?'#2ee6a6':'#ff3b5c');
 let ang=0; setInterval(()=>{ang+=Math.PI/900;G.cameraPosition({x:260*Math.sin(ang),z:260*Math.cos(ang)});},40);
} catch(e) { document.getElementById('fg').innerHTML='<div style="padding:20px;color:#ff7a1a">3D グラフを読み込めませんでした（CDN へのアクセスを確認してください）</div>'; }
try {
 const ge = document.getElementById('globe');
 const lc = l => l>=8?['#ff2d55','#ff9a3c']:l>=5?['#ff7a1a','#ffd23f']:['#4fd1ff','#a96bff'];
 const g = Globe()(ge).width(ge.clientWidth).height(480)
  .globeImageUrl('https://unpkg.com/three-globe/example/img/earth-dark.jpg')
  .backgroundImageUrl('https://unpkg.com/three-globe/example/img/night-sky.png')
  .atmosphereColor('#ff2d55').atmosphereAltitude(.18)
  .arcsData(D.arcs).arcStartLat(a=>a.s[0]).arcStartLng(a=>a.s[1]).arcEndLat(a=>a.e[0]).arcEndLng(a=>a.e[1])
  .arcColor(a=>lc(a.lvl)).arcStroke(.7).arcDashLength(.35).arcDashGap(.15).arcDashAnimateTime(a=>3200-200*a.lvl).arcLabel('lab').arcAltitudeAutoScale(.45)
  .ringsData(D.rings).ringLat('lat').ringLng('lng').ringColor(r=>t=>r.home?`rgba(255,215,0,${1-t})`:`rgba(255,45,85,${1-t})`)
  .ringMaxRadius(r=>3+r.lvl*.6).ringPropagationSpeed(3).ringRepeatPeriod(r=>1400-90*r.lvl)
  .htmlElementsData(D.rings).htmlLat('lat').htmlLng('lng').htmlElement(r=>{const d=document.createElement('div');
    d.innerHTML=`<img src="https://flagcdn.com/w40/${r.cc}.png" style="width:20px;border-radius:2px;box-shadow:0 0 8px ${r.home?'#ffd700':'#ff2d55'}">`;d.style.pointerEvents='none';return d;});
 g.controls().autoRotate=true; g.controls().autoRotateSpeed=.8; g.pointOfView({lat:D.home[0],lng:D.home[1],altitude:2.3},0);
} catch(e) { document.getElementById('globe').innerHTML='<div style="padding:20px;color:#ff7a1a">地球儀を読み込めませんでした</div>'; }
try {
 const t = D.tl; const cat = t.map(x=>x.id);
 echarts.init(document.getElementById('tl')).setOption({tooltip:{formatter:p=>`${t[p.dataIndex].id}<br>${t[p.dataIndex].s} → ${t[p.dataIndex].e}`},
  grid:{left:110,right:20,top:10,bottom:30},xAxis:{type:'time',axisLabel:{color:'#9fb3d9'},splitLine:{lineStyle:{color:'#13224a'}}},
  yAxis:{type:'category',data:cat,axisLabel:{color:'#dbe7ff',fontSize:10}},
  series:[{type:'custom',renderItem:(params,api)=>{const s=api.coord([api.value(1),api.value(0)]),e=api.coord([api.value(2),api.value(0)]);const h=api.size([0,1])[1]*.5;
    return {type:'rect',shape:{x:s[0],y:s[1]-h/2,width:Math.max(4,e[0]-s[0]),height:h},style:{fill:t[params.dataIndex].rep==='BAD'?'#ff2d55':'#4fd1ff',shadowBlur:12,shadowColor:'#ff2d55'}};},
   encode:{x:[1,2],y:0},data:t.map((x,i)=>[i,x.s,x.e]),animationDuration:2000}]});
} catch(e) {}
try {
 const ind={}; D.ins.forEach(i=>((i.target_orgs||{}).top_industries||[]).forEach(x=>ind[x]=(ind[x]||0)+1));
 const act={}; D.ins.forEach(i=>(i.actors||[]).forEach(x=>act[x]=(act[x]||0)+1));
 echarts.init(document.getElementById('ind')).setOption({tooltip:{},series:[
  {type:'pie',radius:['0%','38%'],center:['50%','50%'],label:{color:'#fff',fontSize:10},data:Object.entries(act).map(([k,v])=>({name:k,value:v,itemStyle:{color:'#ff2d55'}}))},
  {type:'pie',radius:['48%','72%'],center:['50%','50%'],roseType:'radius',label:{color:'#9fb3d9',fontSize:10},data:Object.entries(ind).map(([k,v])=>({name:k,value:v}))}]});
} catch(e) {}
try {
 if (D.pc.links.length) {
  echarts.init(document.getElementById('pcs')).setOption({tooltip:{trigger:'item',formatter:p=>p.dataType==='edge'?`${p.data.source.split('|')[0]} ▶ ${p.data.target.split('|')[0]} (${p.data.value})`:p.name.split('|')[0]},
   series:[{type:'sankey',emphasis:{focus:'adjacency'},nodeAlign:'left',layoutIterations:32,
    data:D.pc.nodes.map(n=>({name:n.name,itemStyle:{color:n.bad?'#ff2d55':'#a96bff',borderColor:'#fff'}})),links:D.pc.links,
    label:{color:'#dbe7ff',fontSize:11,formatter:p=>p.name.split('|')[0]},lineStyle:{color:'gradient',curveness:.5,opacity:.45},animationDuration:2500}]});
 }
 const tc=echarts.init(document.getElementById('pct'));
 tc.setOption({tooltip:{formatter:p=>`<b>${p.name}</b><br><span style="font-size:10px">${p.data.sha||''}</span>`},
  series:[{type:'tree',data:[D.pc.tree],orient:'LR',left:'8%',right:'22%',top:'5%',bottom:'5%',symbolSize:11,initialTreeDepth:-1,
   label:{color:'#dbe7ff',fontSize:11,position:'left'},leaves:{label:{position:'right',color:'#ff9fb3'}},
   lineStyle:{color:'#4f6fb0',width:1.5,curveness:.5},expandAndCollapse:true,animationDuration:1200}]});
 const bar=(id,arr,c)=>echarts.init(document.getElementById(id)).setOption({grid:{left:110,right:30,top:5,bottom:20},
   xAxis:{type:'value',axisLabel:{color:'#9fb3d9'},splitLine:{lineStyle:{color:'#13224a'}}},
   yAxis:{type:'category',inverse:true,data:arr.map(x=>x[0]),axisLabel:{color:'#dbe7ff',fontSize:10}},
   series:[{type:'bar',data:arr.map(x=>x[1]),itemStyle:{color:c,borderRadius:[0,6,6,0]},label:{show:true,position:'right',color:'#fff'},animationDuration:1800}]});
 bar('pcp',D.pc.toppar,'#ffd23f'); bar('pcc',D.pc.topchi,'#ff2d55');
} catch(e) {}
</script>
"""
    home_alert = (f"<div style='animation:pulse 1.5s infinite;background:#3a2a00;border:2px solid #ffd700;border-radius:10px;padding:8px 14px;font-weight:800;color:#ffe680;margin-bottom:6px'>"
                  f"⚠️ 自社拠点（{_flag_img(home_cc)}{COUNTRY_GEO.get(home_cc, (0, 0, home_cc.upper()))[2]}）が標的国に含まれています</div>") if home_hit else ""
    for k, v in {"__DATA__": payload, "__NI__": len(data["insights"]), "__BAD__": bad, "__NREL__": sum(len(r.get("ioc_values") or []) for r in data["related"]),
                 "__ACTORS__": ", ".join(actors) or "—", "__MAXLVL__": maxlvl, "__FLAGS__": flags or "—", "__PCSEC__": pc_sec, "__CHAINS__": chain_html,
                 "__HOMEALERT__": home_alert, "__BADSTYLE__": "animation:pulse 1.6s infinite;border-color:#ff2d55" if bad else ""}.items():
        html = html.replace(k, str(v))
    _render_html(html, 2350 if data["chains"] else 1250)
    if src == "live":
        with st.expander("🧾 取得データ（生）"):
            st.json({k: data.get(k) for k in ("insights", "related", "chains", "origins")})

DASHBOARD_PAGES = {DASH_CLIENT: render_dash_client, DASH_VULN: render_dash_vuln, DASH_ATTACK: render_dash_attack}

# --- SIDEBAR ---
st.sidebar.title("⚡ CBX Control Panel")
st.sidebar.markdown("---")

DEFAULT_CLIENT_ID = "O2ID.Wvm1L9TARwOZWTzEBBjW0w.f6G8r9xHSViswGMHCd_fMQ.5kmeqpql54af3rqv6kk4bgh2c0"
DEFAULT_CLIENT_SECRET = "1e99ho0cgl7bc0bklnhebi6ndh8vduvg2i0r"

sb_client_id = st.sidebar.text_input("Client ID", value=DEFAULT_CLIENT_ID)
sb_client_secret = st.sidebar.text_input("Client Secret", value=DEFAULT_CLIENT_SECRET, type="password")
server_url = st.sidebar.text_input(
    "Server Base URL",
    value="https://api.us.security.com"
)

# Basic 認証値（client_id:client_secret の Base64）… トークン取得・TAXII 1.1 で使用
client_cred = (base64.b64encode(f"{sb_client_id.strip()}:{sb_client_secret.strip()}".encode("utf-8")).decode("ascii")
               if sb_client_id.strip() and sb_client_secret.strip() else "")

# 自動更新（チェック時: 残り 5 分未満 / 期限切れなら操作のたびに自動で取り直す + 401 時に 1 回だけ再取得して再送）
auto_refresh = st.sidebar.checkbox("🔄 トークンを自動更新する", value=True, key="auto_refresh",
                                   help="チェックすると、トークンの残りが 5 分を切った時点で次の操作時に自動で再取得し、全操作に適用します。"
                                        "API が 401 を返した場合も 1 回だけ再取得して再送します。")

def refresh_global_token(reason=""):
    """サイドバーの Client ID / Secret でトークンを再取得してグローバル適用。成功で True"""
    if not client_cred:
        st.session_state["auto_refresh_msg"] = ("error", "自動更新できません: Client ID / Client Secret が未入力です。")
        return False
    st.session_state["auto_refresh_last_try"] = time.time()
    try:
        _t, _e, _st, _b = fetch_token(server_url, client_cred)
    except Exception as e:
        st.session_state["auto_refresh_msg"] = ("error", f"自動更新に失敗しました: {e}")
        return False
    if _t:
        st.session_state["global_token"] = _t
        st.session_state["global_token_exp"] = _e
        st.session_state["pending_token"] = _t
        st.session_state["pending_token_exp"] = _e
        st.session_state["auto_refresh_msg"] = ("success", f"🔄 トークンを自動更新しました（{time.strftime('%H:%M:%S')}{' / ' + reason if reason else ''}）")
        return True
    st.session_state["auto_refresh_msg"] = ("error", f"自動更新に失敗しました（Status: {_st}）")
    return False

def current_token_exp():
    if st.session_state.get("global_token"):
        return st.session_state.get("global_token_exp") or jwt_exp(st.session_state["global_token"])
    return jwt_exp(DEFAULT_TOKEN)

if auto_refresh:
    _exp = current_token_exp()
    _need = (_exp is None and not st.session_state.get("global_token")) or (_exp is not None and _exp - time.time() < AUTO_REFRESH_MARGIN)
    # 失敗時に毎操作で連打しないよう、再試行は 60 秒に 1 回まで
    if _need and time.time() - st.session_state.get("auto_refresh_last_try", 0) > 60:
        refresh_global_token("期限が近いため")

# 以降すべての操作で使う Bearer トークン（認証ページの『グローバル適用』または自動更新で設定）
api_token = st.session_state.get("global_token") or DEFAULT_TOKEN

# --- トークン残り時間（大きい太字・1秒ごとに動的更新） ---
_exp_now = current_token_exp()
with st.sidebar:
    components.html(f"""
<div id="tk" style="font-family:'Segoe UI',sans-serif;text-align:center;padding:8px 4px;border-radius:10px;background:#f4f6fb;">
  <div style="font-size:13px;color:#555;">🔑 Token 残り時間</div>
  <div id="tk_t" style="font-size:38px;font-weight:800;line-height:1.2;">--:--</div>
  <div id="tk_s" style="font-size:12px;color:#555;"></div>
</div>
<script>
const exp = {json.dumps(_exp_now)};
const auto = {json.dumps(bool(auto_refresh))};
const margin = {AUTO_REFRESH_MARGIN};
function pad(n){{return String(n).padStart(2,'0');}}
function tick(){{
  const t = document.getElementById('tk_t'), s = document.getElementById('tk_s');
  if (exp === null) {{ t.textContent = '不明'; t.style.color = '#888'; s.textContent = '期限を判定できません'; return; }}
  let r = Math.floor(exp - Date.now()/1000);
  if (r <= 0) {{
    t.textContent = '期限切れ'; t.style.color = '#d62728';
    s.textContent = auto ? '次の操作時に自動更新します' : '🔑 Authentication で再取得してください';
    return;
  }}
  const h = Math.floor(r/3600), m = Math.floor((r%3600)/60), sec = r%60;
  t.textContent = (h > 0 ? h + ':' + pad(m) : pad(m)) + ':' + pad(sec);
  t.style.color = r < margin ? '#d62728' : (r < 900 ? '#ff7f0e' : '#2ca02c');
  s.textContent = r < margin ? (auto ? '残り5分未満：次の操作時に自動更新' : '残り5分未満：再取得してください')
                             : (auto ? '自動更新: ON' : '自動更新: OFF');
}}
tick(); setInterval(tick, 1000);
</script>
""", height=110)
_m = st.session_state.get("auto_refresh_msg")
if _m:
    (st.sidebar.success if _m[0] == "success" else st.sidebar.error)(_m[1])

c_id, d_id = extract_jwt_claims(api_token)
st.sidebar.markdown("---")
if st.session_state.get("global_token"):
    st.sidebar.success("🌐 取得したトークンをグローバル適用中")
else:
    st.sidebar.info("トークン未適用（既定トークンを使用中）。🔑 Authentication ページで『グローバル適用』を押してください。")
st.sidebar.markdown(f"**Auto-detected Customer ID:** `{c_id or 'N/A'}`")
st.sidebar.markdown(f"**Auto-detected Domain ID:** `{d_id or 'N/A'}`")

st.session_state["cbx_token"] = api_token
st.session_state["server_url"] = server_url

# Initialize execution state
if "exec_method" not in st.session_state:
    st.session_state["exec_method"] = "GET"  # 初期エンドポイント（vulnerabilities/summary）は GET（cbx_vuln_assessment.md）
if "exec_endpoint" not in st.session_state:
    st.session_state["exec_endpoint"] = "/endpoint-security/vulnerability/assessment/v3/vulnerabilities/summary"
if "exec_payload" not in st.session_state:
    st.session_state["exec_payload"] = json.dumps({}, indent=2)
if "exec_auth" not in st.session_state:
    st.session_state["exec_auth"] = "Bearer"
if "exec_ctype" not in st.session_state:
    st.session_state["exec_ctype"] = "application/json"
if "exec_extra_headers" not in st.session_state:
    st.session_state["exec_extra_headers"] = ""

# Header
st.markdown('<div class="main-header">⚡ CBX API Master Commander</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">すべてのAPI・全エンドポイント対応（File Inventory v2 / Events v4 / Devices / Device Groups / Device Commands / Reporting / Data Forwarder / Threat Intel 対応版）。テンプレートから実行ボックスへのデータ転送機能付き。</div>', unsafe_allow_html=True)

# Category selection covering File Inventory & other modules
module_choice = st.selectbox(
    "📁 APIモジュール（カテゴリ）を選択",
    [
        "🔑 Authentication (OAuth 2.0)",
        DASH_CLIENT,
        DASH_VULN,
        DASH_ATTACK,
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
    ] + list(API_SPECS.keys())
)

st.markdown("---")

# 📊 ダッシュボードページ（テンプレート / 実行ボックスは表示しない）
_prev_module = st.session_state.get("_last_module")
st.session_state["_last_module"] = module_choice
if module_choice in DASHBOARD_PAGES:
    if _prev_module != module_choice:  # ダッシュボードを開いた瞬間 → API から最新データを自動取得
        for _k in ("dc_data", "dv_data", "da_data"):
            st.session_state.pop(_k, None)
    DASHBOARD_PAGES[module_choice]()
    st.stop()

# Comprehensive Endpoint & Form Generator
with st.container():
    st.subheader(f"📝 テンプレート設定: {module_choice}")
    
    t_method = "GET"
    t_endpoint = ""
    t_data = {}
    t_auth = "Bearer"                 # Bearer / Basic
    t_ctype = "application/json"      # Content-Type
    t_headers = {}                    # 追加ヘッダー
    t_basic = ""                      # Basic 認証値（空ならサイドバーの Client Credentials を使用）

    col_in1, col_in2 = st.columns([1, 1])

    with col_in1:
        if "Authentication" in module_choice:
            op = st.selectbox("Endpoint", ["POST /common/v1/oauth2/tokens"])
            t_method, t_endpoint = op.split(" ", 1)
            st.caption("cbx_auth.md / Method 2: Get the Token in the API — Step 1 でコピーした OAuth Client Secret（Basic 文字列）を authorization ヘッダーに指定し、フォーム形式で送信します。")
            st.markdown(f"**送信先:** `{server_url.rstrip('/')}{t_endpoint}`（サイドバーの Server Base URL）")

            cred_mode = st.radio("認証情報の入力方法",
                                 ["Client ID + Client Secret（自動で Base64 化）", "Basic 文字列（Step 1 でコピーした値）"],
                                 index=0, key="auth_cred_mode")
            if cred_mode.startswith("Client ID"):
                basic_b64 = client_cred
                if basic_b64:
                    st.caption(f"サイドバーの Client ID / Client Secret を Base64 化して使用します（client_id = `{sb_client_id.strip()}`）。")
                else:
                    st.warning("サイドバーの Client ID と Client Secret を入力してください。")
            else:
                basic_in = st.text_input("authorization: Basic (base64_encoded_client_credential)",
                                         value="", type="password", key="auth_basic_str",
                                         help="コンソールでコピーした Basic 文字列（Base64）。先頭の『Basic 』は有っても無くても可。")
                basic_b64 = basic_in.strip()
                if basic_b64.lower().startswith("basic "):
                    basic_b64 = basic_b64[6:].strip()
                if basic_b64:
                    try:
                        _dec = base64.b64decode(basic_b64, validate=True).decode("utf-8")
                        if ":" not in _dec:
                            st.warning("Base64 のデコード結果に『:』がありません（client_id:client_secret 形式ではない可能性があります）。")
                        else:
                            st.caption(f"✔ デコード確認: client_id = `{_dec.split(':', 1)[0]}`")
                    except Exception:
                        st.warning("Base64 として解析できません。コピーした値を確認してください。")
                else:
                    st.warning("Basic 文字列が未入力です。")

            grant_type = st.text_input("grant_type (--data)", value="client_credentials", key="auth_grant_type")
            scope = st.text_input("scope (--data)", value="domain", key="auth_scope")
            accept_h = st.text_input("accept ヘッダー", value="application/json", key="auth_accept")
            t_data = {"grant_type": grant_type, "scope": scope}
            t_auth = "Basic"
            t_ctype = "application/x-www-form-urlencoded"
            t_headers = {"accept": accept_h} if accept_h.strip() else {}
            t_basic = basic_b64  # 実行ボックスの Basic 認証に使用

            def _request_token():
                """トークンを生成し、session_state['pending_token'] に保存"""
                try:
                    _tok, _exp, _status, _j = fetch_token(server_url, basic_b64, data=t_data, accept=accept_h)
                    _body = {k: (f"{v[:12]}…（非表示）" if k == "access_token" else v) for k, v in _j.items()} if isinstance(_j, dict) else _j
                    st.session_state["auth_last_result"] = {"status": _status, "ok": bool(_tok), "body": _body}
                    if _tok:
                        st.session_state["pending_token"] = _tok
                        st.session_state["pending_token_exp"] = _exp
                        return _tok
                except Exception as e:
                    st.session_state["auth_last_result"] = {"status": None, "ok": False, "body": {"error": str(e)}}
                return None

            b_col1, b_col2 = st.columns([1, 1])
            with b_col1:
                if st.button("🔑 トークンを生成", use_container_width=True, disabled=not basic_b64):
                    _request_token()
            with b_col2:
                if st.button("🌐 グローバル適用", use_container_width=True, type="primary", disabled=not basic_b64,
                             help="生成したトークンを以降すべての操作（実行ボックス・各API）の Bearer トークンとして使用します。未生成の場合は生成してから適用します。"):
                    _tok = st.session_state.get("pending_token") or _request_token()
                    if _tok:
                        st.session_state["global_token"] = _tok
                        st.session_state["global_token_exp"] = st.session_state.get("pending_token_exp") or jwt_exp(_tok)
                        st.session_state.pop("auto_refresh_msg", None)
                        st.session_state["exec_auth"] = "Bearer"
                        st.session_state["auth_applied_msg"] = True
                        st.rerun()

            _last = st.session_state.get("auth_last_result")
            if _last:
                if _last["ok"]:
                    st.success(f"Status {_last['status']}: トークンを生成しました。")
                else:
                    st.error(f"トークン生成に失敗しました（Status: {_last['status']}）")
                st.json(_last["body"])
            if st.session_state.get("global_token"):
                if st.session_state.get("pending_token") and st.session_state["pending_token"] != st.session_state["global_token"]:
                    st.info("新しく生成したトークンはまだ適用されていません。『🌐 グローバル適用』を押すと切り替わります。")
                if st.session_state.pop("auth_applied_msg", False):
                    st.success("🌐 トークンをグローバル適用しました。以降すべての操作でこのトークンを使用します。")
                else:
                    st.caption("🌐 現在、生成したトークンをグローバル適用中です。")

        elif module_choice in API_SPECS:
            # Devices / Device Groups / Device Commands / Reporting / Data Forwarder / Threat Intel 各API（汎用テストページ）
            t_method, t_endpoint, t_data = render_generic_api(module_choice)

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
                for _fk in ["criteria", "exclusions"]:
                    _fv = json_obj_input(f"{_fk}（任意, JSON 例: {{\"device_name\": [\"PC01\"]}}）", f"ev_search_{_fk}_{t_endpoint}")
                    if _fv:
                        t_data[_fk] = _fv
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
                for _fk in ["criteria", "exclusions"]:
                    _fv = json_obj_input(f"{_fk}（任意, JSON 例: {{\"device_name\": [\"PC01\"]}}）", f"ev_facet_{_fk}_{t_endpoint}")
                    if _fv:
                        t_data[_fk] = _fv
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
            _hand = [
                "POST /detect-respond/detection/v1/custom-detections/_search",
                "POST /detect-respond/detection/v1/custom-detections",
                "GET /detect-respond/detection/v1/custom-detections/{detection_id}",
                "PUT /detect-respond/detection/v1/custom-detections/{detection_id}",
                "DELETE /detect-respond/detection/v1/custom-detections/{detection_id}",
                "POST /detect-respond/detection/v1/custom-detections/queries/_search"
            ]
            op = legacy_endpoint_select("Custom Detections", _hand)
            t_method, t_endpoint = op.split(" ", 1)
            if op not in _hand:
                t_method, t_endpoint, t_data = render_legacy_generic("Custom Detections", op)
            else:
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
            _hand = [
                "GET /detect-respond/device-query/v2/commands",
                "POST /detect-respond/device-query/v2/commands",
                "GET /detect-respond/device-query/v2/commands/{commandId}"
            ]
            op = legacy_endpoint_select("Device Query", _hand)
            t_method, t_endpoint = op.split(" ", 1)
            if op not in _hand:
                t_method, t_endpoint, t_data = render_legacy_generic("Device Query", op)
            else:
                if "{commandId}" in t_endpoint:
                    cid = st.text_input("commandId", value="cmd-123")
                    t_endpoint = t_endpoint.replace("{commandId}", cid)

                if t_method == "POST" and "commands" in t_endpoint:
                    cmd_type = st.selectbox("command_type", ["forensic", "artifact"])
                    scope = st.selectbox("scope", ["all", "device_ids"])
                    query_str = st.text_area("query", value="SELECT * FROM processes;")
                    t_data = {"command_type": cmd_type, "scope": scope, "query": query_str}

        elif "Alerts & Threats" in module_choice:
            _hand = [
                "POST /detect-respond/alerts/v8/alerts/_search",
                "GET /detect-respond/alerts/v8/alerts/{alert_id}",
                "POST /detect-respond/alerts/v8/alerts/workflow"
            ]
            op = legacy_endpoint_select("Alerts & Threats", _hand)
            t_method, t_endpoint = op.split(" ", 1)
            if op not in _hand:
                t_method, t_endpoint, t_data = render_legacy_generic("Alerts & Threats", op)
            else:
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
            _hand = [
                "POST /detect-respond/jobs/v4/event_export",
                "GET /detect-respond/jobs/v4/jobs/{job_id}"
            ]
            op = legacy_endpoint_select("Jobs & Export", _hand)
            t_method, t_endpoint = op.split(" ", 1)
            if op not in _hand:
                t_method, t_endpoint, t_data = render_legacy_generic("Jobs & Export", op)
            else:
                if "{job_id}" in t_endpoint:
                    jid = st.text_input("job_id", value="job-123")
                    t_endpoint = t_endpoint.replace("{job_id}", jid)
                if t_method == "POST":
                    q = st.text_input("query", value="process_name: powershell.exe")
                    t_data = {"query": q, "time_range": "1h"}

        elif "Live Response" in module_choice:
            _hand = [
                "GET /detect-respond/live-response/v7/sessions",
                "POST /detect-respond/live-response/v7/sessions"
            ]
            op = legacy_endpoint_select("Live Response", _hand)
            t_method, t_endpoint = op.split(" ", 1)
            if op not in _hand:
                t_method, t_endpoint, t_data = render_legacy_generic("Live Response", op)
            else:
                if t_method == "POST":
                    dev_id = st.text_input("device_id", value="device-001")
                    t_data = {"device_id": dev_id}

        elif "Notifications" in module_choice:
            _hand = [
                "GET /detect-respond/notifications/v2/rules",
                "POST /detect-respond/notifications/v2/rules"
            ]
            op = legacy_endpoint_select("Notifications", _hand)
            t_method, t_endpoint = op.split(" ", 1)
            if op not in _hand:
                t_method, t_endpoint, t_data = render_legacy_generic("Notifications", op)
            else:
                if t_method == "POST":
                    r_name = st.text_input("Rule Name", value="Alert Rule")
                    t_data = {"name": r_name, "enabled": True}

        elif "Policy Management" in module_choice:
            _hand = [
                "GET /common/policy-management/v2/policies",
                "POST /common/policy-management/v2/policies/export/all"
            ]
            op = legacy_endpoint_select("Policy Management", _hand)
            t_method, t_endpoint = op.split(" ", 1)
            if op not in _hand:
                t_method, t_endpoint, t_data = render_legacy_generic("Policy Management", op)
            else:
                t_data = {}

        elif "Script Deobfuscation" in module_choice:
            _hand = ["POST /detect-respond/script-deobfuscation/v3/reveal"]
            op = legacy_endpoint_select("Script Deobfuscation", _hand)
            t_method, t_endpoint = op.split(" ", 1)
            if op not in _hand:
                t_method, t_endpoint, t_data = render_legacy_generic("Script Deobfuscation", op)
            else:
                script_b64 = st.text_area("Script / Base64", value="powershell.exe -e aQBm...")
                t_data = {"script": script_b64}

        elif "Threat Intel" in module_choice:
            # cbx_taxii11.md: Basic 認証 / STIX 1.x XML。メッセージは TAXII 1.1 標準の XML 形式
            op = st.selectbox("Endpoint", [
                "POST /common/threat-intel/v1/taxii11/discovery",
                "POST /common/threat-intel/v1/taxii11/collection-management",
                "POST /common/threat-intel/v1/taxii11/poll"
            ])
            t_method, t_endpoint = op.split(" ", 1)
            t_auth = "Basic"
            t_ctype = "application/xml"
            t_headers = dict(TAXII11_HEADERS)
            st.caption("認証: サイドバーの Client ID + Client Secret（client_id:client_secret の Base64）による Basic 認証を使用します。")
            st.caption("※ md には Body の定義がないため、TAXII 1.1 標準のメッセージ形式（XML）で生成しています。")
            msg_id = st.text_input("message_id", value="1")
            if t_endpoint.endswith("/discovery"):
                t_data = f'<taxii_11:Discovery_Request xmlns:taxii_11="{TAXII11_NS}" message_id="{msg_id}"/>'
            elif t_endpoint.endswith("/collection-management"):
                t_data = f'<taxii_11:Collection_Information_Request xmlns:taxii_11="{TAXII11_NS}" message_id="{msg_id}"/>'
            else:
                coll = st.selectbox("collection_name", ["threat-alerts", "malicious-uri", "malicious-file"])
                coll = st.text_input("collection_name（編集可）", value=coll)
                begin = st.text_input("Exclusive_Begin_Timestamp（任意, 例: 2026-11-01T00:00:00Z）", value="")
                end = st.text_input("Inclusive_End_Timestamp（任意）", value="")
                inner = ""
                if begin.strip():
                    inner += f"<taxii_11:Exclusive_Begin_Timestamp>{begin.strip()}</taxii_11:Exclusive_Begin_Timestamp>"
                if end.strip():
                    inner += f"<taxii_11:Inclusive_End_Timestamp>{end.strip()}</taxii_11:Inclusive_End_Timestamp>"
                inner += '<taxii_11:Poll_Parameters allow_asynch="false"><taxii_11:Response_Type>FULL</taxii_11:Response_Type></taxii_11:Poll_Parameters>'
                t_data = (f'<taxii_11:Poll_Request xmlns:taxii_11="{TAXII11_NS}" message_id="{msg_id}" collection_name="{coll}">'
                          f'{inner}</taxii_11:Poll_Request>')

        elif "Vulnerability Assessment" in module_choice:
            _hand = [
                "GET /endpoint-security/vulnerability/assessment/v3/vulnerabilities/summary",
                "POST /endpoint-security/vulnerability/assessment/v3/devices/vulnerabilities/_search"
            ]
            op = legacy_endpoint_select("Vulnerability Assessment", _hand)
            t_method, t_endpoint = op.split(" ", 1)
            if op not in _hand:
                t_method, t_endpoint, t_data = render_legacy_generic("Vulnerability Assessment", op)
            else:
                if "_search" in t_endpoint:
                    t_data = {"rows": 10, "start": 0}

    with col_in2:
        st.markdown("**生成されるプレビュー (URL / データ):**")
        _data_txt = t_data if isinstance(t_data, str) else json.dumps(t_data, indent=2, ensure_ascii=False)
        preview_text = f"""Endpoint: {t_endpoint}
Method: {t_method}
Auth: {t_auth} / Content-Type: {t_ctype}
Data:
{_data_txt}"""
        st.code(preview_text, language="json")
        
        if st.button("📥 実行ボックスにこの設定を転送する", use_container_width=True, type="primary"):
            st.session_state["exec_method"] = t_method
            st.session_state["exec_endpoint"] = t_endpoint
            st.session_state["exec_payload"] = _data_txt
            st.session_state["exec_auth"] = t_auth
            st.session_state["exec_ctype"] = t_ctype
            st.session_state["exec_extra_headers"] = json.dumps(t_headers, indent=2) if t_headers else ""
            st.session_state["exec_basic"] = t_basic
            st.rerun()

st.markdown("---")

# --- ALWAYS VISIBLE EXECUTION BOX ---
def _sends_body(m, raw):
    """POST/PUT/PATCH は従来どおり。DELETE は Body が空でない JSON のときだけ送信（Devices 一括削除など用）"""
    if not raw.strip():
        return False
    if m in ["POST", "PUT", "PATCH"]:
        return True
    if m == "DELETE":
        try:
            return bool(json.loads(raw))
        except Exception:
            return False
    return False

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

    # 認証方式 / Content-Type / 追加ヘッダー（テンプレートから自動設定。手動変更も可）
    ex_a1, ex_a2 = st.columns([1, 1])
    with ex_a1:
        auth_list = ["Bearer", "Basic", "なし"]
        curr_a = st.session_state["exec_auth"]
        auth_mode = st.selectbox("認証方式", auth_list, index=auth_list.index(curr_a) if curr_a in auth_list else 0,
                                 help="Bearer: グローバル適用したトークン / Basic: サイドバーの Client ID + Client Secret")
    with ex_a2:
        ctype_list = ["application/json", "application/x-www-form-urlencoded", "application/xml", "application/taxii+json;version=2.1"]
        curr_c = st.session_state["exec_ctype"]
        ctype = st.selectbox("Content-Type", ctype_list, index=ctype_list.index(curr_c) if curr_c in ctype_list else 0)
    extra_headers_txt = st.text_area("追加ヘッダー（任意, JSON）", value=st.session_state["exec_extra_headers"], height=90)

    full_url_preview = f"{server_url.rstrip('/')}{endpoint}"
    headers_preview = {}
    if auth_mode == "Bearer":
        _tok = api_token.strip()
        if _tok.startswith("Basic ") or _tok.startswith("Bearer "):
            headers_preview["Authorization"] = _tok
        else:
            headers_preview["Authorization"] = f"Bearer {_tok}"
    elif auth_mode == "Basic":
        _cred = (st.session_state.get("exec_basic") or client_cred).strip()
        if not _cred:
            st.warning("Basic 認証情報が未入力です（サイドバーの Client ID / Client Secret を入力してください）。")
        headers_preview["Authorization"] = _cred if _cred.startswith("Basic ") else f"Basic {_cred}"
    headers_preview["content-type"] = ctype
    if extra_headers_txt.strip():
        try:
            _extra = json.loads(extra_headers_txt)
            if isinstance(_extra, dict):
                headers_preview.update({str(k): str(v) for k, v in _extra.items()})
            else:
                st.error("追加ヘッダーは JSON オブジェクトで入力してください")
        except Exception as e:
            st.error(f"追加ヘッダーの JSON が不正です: {e}")

    show_secret = st.checkbox("認証情報を画面に表示する（cURL / Python コードにも反映）", value=False)

    def _masked(h):
        h2 = dict(h)
        if "Authorization" in h2 and not show_secret:
            scheme, _, val = h2["Authorization"].partition(" ")
            h2["Authorization"] = f"{scheme} {val[:8]}…（非表示）" if val else scheme
        return h2

    headers_display = _masked(headers_preview)
    is_form = ctype == "application/x-www-form-urlencoded"
    is_json = "json" in ctype

    def _build_body(raw):
        """Content-Type に応じて送信形式を決める: ('json', obj) / ('data', dict or bytes)"""
        if is_form:
            d = json.loads(raw)
            if not isinstance(d, dict):
                raise ValueError("フォーム送信は JSON オブジェクト（{\"key\": \"value\"}）で入力してください")
            return "data", {k: (v if isinstance(v, str) else json.dumps(v)) for k, v in d.items()}
        if is_json:
            return "json", json.loads(raw)
        return "data", raw.encode("utf-8")

    exec_col_left, exec_col_right = st.columns([1, 1])

    with exec_col_left:
        st.markdown("#### 🔗 リクエスト情報")
        st.markdown(f"**URL:** `{full_url_preview}`")
        st.markdown("**Headers:**")
        st.json(headers_display)

    with exec_col_right:
        st.markdown("#### 📦 リクエストデータ (JSON Payload)")
        raw_data_input = st.text_area("JSON Raw Data", value=st.session_state["exec_payload"], height=160,
                                      help="JSON。フォーム送信時も JSON オブジェクトで入力、XML 送信時は XML をそのまま入力")

    # Code Snippets generation tab
    st.markdown("#### 💻 リクエストコード生成 (cURL & Python)")
    snip_tab1, snip_tab2 = st.tabs(["cURL Command", "Python Code Snippet"])

    with snip_tab1:
        curl_parts = [f"curl --request {method} '{full_url_preview}'"]
        for hk, hv in headers_display.items():
            curl_parts.append(f"  --header '{hk}: {hv}'")
        if _sends_body(method, raw_data_input):
            if is_form:
                try:
                    for fk, fv in _build_body(raw_data_input)[1].items():
                        curl_parts.append(f"  --data-urlencode '{fk}={fv}'")
                except Exception:
                    curl_parts.append(f"  --data '{raw_data_input.strip()}'")
            else:
                curl_parts.append(f"  --data '{raw_data_input.strip()}'")
        st.code(" \\\n".join(curl_parts), language="bash")

    with snip_tab2:
        py_code = f"import requests\nimport json\n\nurl = \"{full_url_preview}\"\nheaders = {json.dumps(headers_display, indent=4, ensure_ascii=False)}\n"
        if _sends_body(method, raw_data_input):
            if is_form:
                try:
                    py_code += f"payload = {_build_body(raw_data_input)[1]!r}\n"
                except Exception:
                    py_code += f"payload = {raw_data_input.strip()!r}\n"
                py_code += f"response = requests.{method.lower()}(url, headers=headers, data=payload)\n"
            elif is_json:
                py_code += f"payload = json.loads({raw_data_input.strip()!r})\nresponse = requests.{method.lower()}(url, headers=headers, json=payload)\n"
            else:
                py_code += f"payload = {raw_data_input.strip()!r}\nresponse = requests.{method.lower()}(url, headers=headers, data=payload.encode(\"utf-8\"))\n"
        else:
            py_code += f"response = requests.{method.lower()}(url, headers=headers)\n"
        py_code += "print(response.status_code)\ntry:\n    print(response.json())\nexcept ValueError:\n    print(response.text)"
        st.code(py_code, language="python")

    if st.button("⚡ 今すぐリクエストを実行する", use_container_width=True, type="primary"):
        body_kind, body_val = None, None
        if _sends_body(method, raw_data_input):
            try:
                body_kind, body_val = _build_body(raw_data_input)
            except Exception as e:
                st.error(f"リクエストデータの解析エラー（送信を中止しました）: {str(e)}")
                st.stop()

        with st.spinner("API実行中..."):
            try:
                resp = requests.request(
                    method=method,
                    url=full_url_preview,
                    headers=headers_preview,
                    json=body_val if body_kind == "json" else None,
                    data=body_val if body_kind == "data" else None,
                    timeout=30
                )
                # 自動更新 ON + Bearer 認証で 401 → トークンを 1 回だけ再取得して再送
                if resp.status_code == 401 and auto_refresh and auth_mode == "Bearer" and "/oauth2/tokens" not in endpoint:
                    if refresh_global_token("401 を受信したため"):
                        api_token = st.session_state["global_token"]
                        headers_preview["Authorization"] = "Bearer " + api_token
                        st.info("🔄 401 を受信したため、トークンを自動更新して 1 回だけ再送しました。")
                        resp = requests.request(
                            method=method,
                            url=full_url_preview,
                            headers=headers_preview,
                            json=body_val if body_kind == "json" else None,
                            data=body_val if body_kind == "data" else None,
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
                        _rj = resp.json()
                        if isinstance(_rj, dict) and _rj.get("access_token") and "/oauth2/tokens" in endpoint and resp.ok:
                            st.session_state["pending_token"] = _rj["access_token"]
                            st.session_state["pending_token_exp"] = jwt_exp(_rj["access_token"]) or int(time.time() + int(_rj.get("expires_in", 3600)))
                            st.info("トークンを取得しました。🔑 Authentication ページの『🌐 グローバル適用』で以降すべての操作に適用できます。")
                        st.json(_rj)
                    except Exception:
                        st.text(resp.text)
                with res_tab2:
                    st.json(dict(resp.headers))

            except Exception as ex:
                st.error(f"リクエスト送信失敗: {str(ex)}")

    st.markdown('</div>', unsafe_allow_html=True)
