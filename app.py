import streamlit as st
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
        g_path = g_path.replace("{" + p["name"] + "}", quote(val.strip(), safe=""))

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
    st.components.v1.html(f"""
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
