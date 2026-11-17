import streamlit as st
import requests
import json
import base64
import re
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

# --- API仕様（添付ドキュメント cbx_*.md から生成。汎用テストページで使用） ---
API_SPECS = {'💽 Devices': {'doc': 'cbx_devices.md',
               'permissions': ['Device and Device Group Management -> View'],
               'endpoints': [{'method': 'GET',
                              'path': '/agent-management/devices/v2/devices',
                              'summary': 'Retrieve the list of devices.',
                              'operation_id': 'listDevices',
                              'sku': '',
                              'desc': 'Returns a paginated list of managed devices with optional filtering and sorting. Requires the Read Devices permission. '
                                      'Callers without this permission will receive a 403 Forbidden response.',
                              'path_params': [],
                              'query_params': [{'name': 'page',
                                                'type': 'integer',
                                                'required': False,
                                                'default': '1',
                                                'desc': 'The page number to retrieve (1-indexed). [NOTE] When this field is not present, the first page is '
                                                        'returned.',
                                                'sample': ''},
                                               {'name': 'page_size',
                                                'type': 'integer',
                                                'required': False,
                                                'default': '100',
                                                'desc': 'Number of devices per page. [NOTE] By default, 100 devices are returned. Maximum page size is 1000, '
                                                        'or 500 if include_details=true is specified. Requests with page_size > 500 and include_details=true…',
                                                'sample': ''},
                                               {'name': 'include_details',
                                                'type': 'boolean',
                                                'required': False,
                                                'default': '',
                                                'desc': 'Flag to include product and feature details in response. Possible values: true/false. [NOTE] When '
                                                        'this flag is true, the maximum number of records supported per request is 500.',
                                                'sample': ''},
                                               {'name': 'include_path',
                                                'type': 'boolean',
                                                'required': False,
                                                'default': '',
                                                'desc': 'Flag to include device group full path in response. Possible values: true/false.',
                                                'sample': ''},
                                               {'name': 'order_by',
                                                'type': 'string',
                                                'required': False,
                                                'default': '',
                                                'desc': 'Name of the field used to sort devices in the response, optionally followed by a space and "asc" or '
                                                        '"desc" to set sort direction; if omitted, sort order defaults to ascending. Only one field can be sp…',
                                                'sample': ''},
                                               {'name': 'antimalware_content_version',
                                                'type': 'array',
                                                'required': False,
                                                'default': '',
                                                'desc': 'Version of antimalware content installed on the device. Multiple values supplied for this parameter '
                                                        'are combined with OR — a device matches if it satisfies any of the provided values. Each value perfo…',
                                                'sample': ''},
                                               {'name': 'capabilities_enabled',
                                                'type': 'array',
                                                'required': False,
                                                'default': '',
                                                'desc': 'Capabilities enabled on this device, filtered by internal capability constant (marketing name shown '
                                                        'for reference, subject to change): ENDPOINT_PROTECTION (Endpoint Security), WEB_SECURITY (Web Securi…',
                                                'sample': ''},
                                               {'name': 'cloud_platform',
                                                'type': 'array',
                                                'required': False,
                                                'default': '',
                                                'desc': 'Cloud platform. Supported values: AWS, GCP, AZURE, NONE. Multiple values supplied for this parameter '
                                                        'are combined with OR — a device matches if it satisfies any of the provided values. Each value perf…',
                                                'sample': ''},
                                               {'name': 'connection_status',
                                                'type': 'string',
                                                'required': False,
                                                'default': '',
                                                'desc': 'Connection status of the agent installed on the device. Online means the device has communicated with '
                                                        'the backend within the last 48 hours; otherwise the device is Offline. Note: the connection_status…',
                                                'sample': ''},
                                               {'name': 'data_security_version',
                                                'type': 'array',
                                                'required': False,
                                                'default': '',
                                                'desc': 'Version of Data Security installed on the device. Multiple values supplied for this parameter are '
                                                        'combined with OR — a device matches if it satisfies any of the provided values. Each value performs '
                                                        'a…',
                                                'sample': ''},
                                               {'name': 'device_group',
                                                'type': 'array',
                                                'required': False,
                                                'default': '',
                                                'desc': 'id of the parent device group. Corresponds to the parent_device_group_id field in the response. '
                                                        'Multiple values supplied for this parameter are combined with OR — a device matches if it satisfies '
                                                        'any…',
                                                'sample': ''},
                                               {'name': 'device_id',
                                                'type': 'string',
                                                'required': False,
                                                'default': '',
                                                'desc': 'Unique device identifier. [NOTE] If order_by is not specified, devices in the response are sorted by '
                                                        'device_id.',
                                                'sample': ''},
                                               {'name': 'device_name',
                                                'type': 'array',
                                                'required': False,
                                                'default': '',
                                                'desc': 'name of the device. Multiple values supplied for this parameter are combined with OR — a device '
                                                        'matches if it satisfies any of the provided values. Each value performs a partial/substring match '
                                                        'agains…',
                                                'sample': ''},
                                               {'name': 'device_os',
                                                'type': 'array',
                                                'required': False,
                                                'default': '',
                                                'desc': 'OS name of the device. Corresponds to the os.device_os field in the response. Multiple values '
                                                        'supplied for this parameter are combined with OR — a device matches if it satisfies any of the '
                                                        'provided va…',
                                                'sample': ''},
                                               {'name': 'device_type',
                                                'type': 'array',
                                                'required': False,
                                                'default': '',
                                                'desc': "OS type of the device, matched internally against the device's os.type value by suffix — WORKSTATION "
                                                        'matches any os.type ending in _WORKSTATION, SERVER matches any os.type ending in _SERVER. There is…',
                                                'sample': ''},
                                               {'name': 'disabled_expiration_time',
                                                'type': 'string',
                                                'required': False,
                                                'default': '',
                                                'desc': 'Returns devices whose disabled_expiration_time is on or after this value (i.e. devices whose '
                                                        'troubleshooting period expires at or later than the given time). Time when the troubleshooting period '
                                                        'will…',
                                                'sample': ''},
                                               {'name': 'domain',
                                                'type': 'array',
                                                'required': False,
                                                'default': '',
                                                'desc': 'The domain to which this device is connected. Multiple values supplied for this parameter are '
                                                        'combined with OR — a device matches if it satisfies any of the provided values. Each value performs a '
                                                        'part…',
                                                'sample': ''},
                                               {'name': 'endpoint_security_version',
                                                'type': 'array',
                                                'required': False,
                                                'default': '',
                                                'desc': 'Version of Endpoint Protection installed on the device. Multiple values supplied for this parameter '
                                                        'are combined with OR — a device matches if it satisfies any of the provided values. Each value perfo…',
                                                'sample': ''},
                                               {'name': 'enrollment_date',
                                                'type': 'integer',
                                                'required': False,
                                                'default': '',
                                                'desc': 'Devices enrolled within the specified number of days up to now will be returned. Note: although this '
                                                        'field is named enrollment_date and represents a date in device responses, this query parameter expe…',
                                                'sample': ''},
                                               {'name': 'esa_version',
                                                'type': 'array',
                                                'required': False,
                                                'default': '',
                                                'desc': 'Version of Endpoint Security Agent installed on the device. Multiple values supplied for this '
                                                        'parameter are combined with OR — a device matches if it satisfies any of the provided values. Each '
                                                        'value p…',
                                                'sample': ''},
                                               {'name': 'form_factor',
                                                'type': 'string',
                                                'required': False,
                                                'default': '',
                                                'desc': 'Device form factor. Note: the form_factor field in the response returns this same value in Title Case '
                                                        '(Physical/Virtual), not the PHYSICAL/VIRTUAL casing used here.',
                                                'sample': ''},
                                               {'name': 'host',
                                                'type': 'array',
                                                'required': False,
                                                'default': '',
                                                'desc': 'Device host name. Multiple values supplied for this parameter are combined with OR — a device matches '
                                                        'if it satisfies any of the provided values. Each value performs a partial/substring match against…',
                                                'sample': ''},
                                               {'name': 'instance_id',
                                                'type': 'array',
                                                'required': False,
                                                'default': '',
                                                'desc': 'Device instance ID. Corresponds to the instance_id field (and the identical '
                                                        'device_identifiers.instance_id) in the response. Multiple values supplied for this parameter are '
                                                        'combined with OR — a device…',
                                                'sample': ''},
                                               {'name': 'ipv4_address',
                                                'type': 'array',
                                                'required': False,
                                                'default': '',
                                                'desc': 'IPv4 address of a device. Multiple values supplied for this parameter are combined with OR — a device '
                                                        'matches if it satisfies any of the provided values. Each value performs a partial/substring match…',
                                                'sample': ''},
                                               {'name': 'last_updated',
                                                'type': 'string',
                                                'required': False,
                                                'default': '',
                                                'desc': 'Returns devices whose last_updated timestamp is on or after this value (i.e. devices updated at or '
                                                        'later than the given time). Corresponds to products[0].last_updated in the response.',
                                                'sample': ''},
                                               {'name': 'mac_address',
                                                'type': 'array',
                                                'required': False,
                                                'default': '',
                                                'desc': 'MAC address of a device. Corresponds to the adapters[].addr field in the response. Multiple values '
                                                        'supplied for this parameter are combined with OR — a device matches if it satisfies any of the '
                                                        'provid…',
                                                'sample': ''},
                                               {'name': 'mdm_id',
                                                'type': 'array',
                                                'required': False,
                                                'default': '',
                                                'desc': 'Device MDM ID. Note: there is no corresponding field in the device response schema to read this value '
                                                        'back — filtering is supported, but the current value cannot be inspected on a returned device reco…',
                                                'sample': ''},
                                               {'name': 'os_version',
                                                'type': 'string',
                                                'required': False,
                                                'default': '',
                                                'desc': 'OS version of the device. Corresponds to the os.os_version field in the response. Each value performs '
                                                        'a partial/substring match against the field, not an exact match, e.g. "10.0" matches "10.0.19044".',
                                                'sample': ''},
                                               {'name': 'permission',
                                                'type': 'array',
                                                'required': False,
                                                'default': '',
                                                'desc': 'Cloud SWG connectivity state. Supported values: ALLOWED (connectivity permitted); BLOCKED '
                                                        '(connectivity completely blocked, e.g. by policy); DISABLED (connectivity temporarily disabled until '
                                                        'an admin…',
                                                'sample': ''},
                                               {'name': 'security_status',
                                                'type': 'array',
                                                'required': False,
                                                'default': '',
                                                'desc': 'Device security status. The meaning of each value (including NOT_COMPUTED, UNENROLLED, and UNKNOWN) '
                                                        'is documented at https://techdocs.broadcom.com/us/en/symantec-security-software/symantec-cbx/cbx/ind…',
                                                'sample': ''},
                                               {'name': 'status_reason',
                                                'type': 'array',
                                                'required': False,
                                                'default': '',
                                                'desc': 'Device status reason codes reported by the endpoint agent. Values are numeric strings (e.g. "132", '
                                                        '"613") and are not a fixed enum — the set of codes depends on the agent version and installed '
                                                        'product…',
                                                'sample': ''},
                                               {'name': 'user',
                                                'type': 'array',
                                                'required': False,
                                                'default': '',
                                                'desc': 'Last logged-on user name. Corresponds to the os.user field in the response. Multiple values supplied '
                                                        'for this parameter are combined with OR — a device matches if it satisfies any of the provided valu…',
                                                'sample': ''},
                                               {'name': 'web_security_version',
                                                'type': 'array',
                                                'required': False,
                                                'default': '',
                                                'desc': 'Version of Web Security installed on the device. Multiple values supplied for this parameter are '
                                                        'combined with OR — a device matches if it satisfies any of the provided values. Each value performs a '
                                                        'p…',
                                                'sample': ''}],
                              'body': None,
                              'body_schema': []},
                             {'method': 'DELETE',
                              'path': '/agent-management/devices/v2/devices',
                              'summary': 'Bulk delete managed devices',
                              'operation_id': 'deleteDevices',
                              'sku': '',
                              'desc': 'Bulk delete managed devices by their identifiers. Supply device_id values (returned by GET /devices) in the device_uids '
                                      'request field. Returns per-device results; partial success is possible. Requires the Manage Devices permission. Callers '
                                      'without this permission will receive a 403 Forbidden response.',
                              'path_params': [],
                              'query_params': [],
                              'body': {'device_uids': ['J1GpYTXlQmaD9c70WQIURA', 'doKfbw70SaKXvaR2PIxfLA']},
                              'body_schema': ['`device_uids` `array[string]` *(required)* — List of unique device identifiers to delete. Each value '
                                              'corresponds to the device_id field returned by GET /devices and GET /devices/{device_id}.']},
                             {'method': 'GET',
                              'path': '/agent-management/devices/v2/devices/{device_id}',
                              'summary': 'Retrieve device details.',
                              'operation_id': 'getDeviceDetails',
                              'sku': '',
                              'desc': 'Returns full details for the specified device, including OS, hardware, network adapters, and installed security '
                                      'products. Requires the Read Devices permission. Callers without this permission will receive a 403 Forbidden response.',
                              'path_params': [{'name': 'device_id',
                                               'required': True,
                                               'desc': 'Defines which device to retrieve device details from. Corresponds to the device_id field returned by '
                                                       'GET /devices or a prior GET /devices/{device_id} call.',
                                               'sample': 'ZROiMffzSAGb_2WT1c-75Q'}],
                              'query_params': [],
                              'body': None,
                              'body_schema': []},
                             {'method': 'GET',
                              'path': '/agent-management/devices/v2/devices/enums',
                              'summary': 'API endpoints for retrieving CBX enumeration details and device specific details.',
                              'operation_id': 'getDeviceEnums',
                              'sku': '',
                              'desc': 'Returns enumeration details for CBX device fields, including feature names, security status values, and reason codes. '
                                      'Requires the Read Devices permission. Callers without this permission will receive a 403 Forbidden response.',
                              'path_params': [],
                              'query_params': [],
                              'body': None,
                              'body_schema': []}]},
 '🗂️ Device Groups': {'doc': 'cbx_device_groups.md',
                      'permissions': ['Device and Device Group Management -> View', 'Device and Device Group Management -> Delete'],
                      'endpoints': [{'method': 'GET',
                                     'path': '/agent-management/device-groups/v2/groups',
                                     'summary': 'Retrieve a list of your device groups.',
                                     'operation_id': 'listDeviceGroups',
                                     'sku': '',
                                     'desc': 'Returns a paginated list of all device groups. Requires the Read Device Groups permission (Agent Management > '
                                             'Device and Device Group Management > Read, as labelled on the API Credentials page). Callers without this '
                                             'permission will receive a 403 Forbidden response.',
                                     'path_params': [],
                                     'query_params': [{'name': 'page',
                                                       'type': 'integer',
                                                       'required': False,
                                                       'default': '1',
                                                       'desc': '1-based page number.',
                                                       'sample': ''},
                                                      {'name': 'page_size',
                                                       'type': 'integer',
                                                       'required': False,
                                                       'default': '1000',
                                                       'desc': 'The number of records per page. The maximum number of records supported per request is 1000.',
                                                       'sample': ''},
                                                      {'name': 'root_only',
                                                       'type': 'boolean',
                                                       'required': False,
                                                       'default': 'false',
                                                       'desc': 'Filter to return only root device groups.',
                                                       'sample': ''},
                                                      {'name': 'order_by',
                                                       'type': 'string',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'Sort order for the returned device groups. Only the name field is supported, in either '
                                                               'ascending ("name") or descending ("name desc") direction; sorting is case-insensitive.',
                                                       'sample': ''},
                                                      {'name': 'name',
                                                       'type': 'string',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'Filter groups by device group name (partial match).',
                                                       'sample': ''}],
                                     'body': None,
                                     'body_schema': []},
                                    {'method': 'POST',
                                     'path': '/agent-management/device-groups/v2/groups/{group_id}',
                                     'summary': 'Create a child device group.',
                                     'operation_id': 'createDeviceGroup',
                                     'sku': '',
                                     'desc': 'Creates a new child device group under the specified parent group. Requires the Manage Device Groups permission '
                                             '(Agent Management > Device and Device Group Management > Manage, as labelled on the API Credentials page). '
                                             'Callers without this permission will receive a 403 Forbidden response.',
                                     'path_params': [{'name': 'group_id',
                                                      'required': True,
                                                      'desc': 'ID of parent device group.',
                                                      'sample': '4Zh6VRUJQQauw_-AzxjtHw'}],
                                     'query_params': [],
                                     'body': {'name': 'Linux Servers - US East',
                                              'description': 'Group for all Linux servers located in the US East data center'},
                                     'body_schema': ['`name` `string` *(required)* — The name of the new device group.',
                                                     '`description` `string` — The description of the device group']},
                                    {'method': 'GET',
                                     'path': '/agent-management/device-groups/v2/groups/{group_id}',
                                     'summary': 'Retrieve a device group.',
                                     'operation_id': 'getDeviceGroup',
                                     'sku': '',
                                     'desc': 'Returns the specified device group by ID. Requires the Read Device Groups permission (Agent Management > Device '
                                             'and Device Group Management > Read, as labelled on the API Credentials page). Callers without this permission '
                                             'will receive a 403 Forbidden response.',
                                     'path_params': [{'name': 'group_id', 'required': True, 'desc': 'ID of device group.', 'sample': '4Zh6VRUJQQauw_-AzxjtHw'}],
                                     'query_params': [],
                                     'body': None,
                                     'body_schema': []},
                                    {'method': 'PUT',
                                     'path': '/agent-management/device-groups/v2/groups/{group_id}',
                                     'summary': 'Update a device group.',
                                     'operation_id': 'updateDeviceGroup',
                                     'sku': '',
                                     'desc': 'Updates the name or description of the specified device group. Fields omitted from the request body are left '
                                             'unchanged; only the fields provided are updated. Requires the Manage Device Groups permission (Agent Management '
                                             '> Device and Device Group Management > Manage, as labelled on the API Credentials page). Callers without this '
                                             'permission will receive a 403 Forbidden response.',
                                     'path_params': [{'name': 'group_id',
                                                      'required': True,
                                                      'desc': 'ID of the device group to update.',
                                                      'sample': '4Zh6VRUJQQauw_-AzxjtHw'}],
                                     'query_params': [],
                                     'body': {'name': 'Linux Servers - US West',
                                              'description': 'Group for all Linux servers located in the US West data center'},
                                     'body_schema': ['`name` `string` — The new name to assign to the device group',
                                                     '`description` `string` — The new description to assign to the device group']},
                                    {'method': 'DELETE',
                                     'path': '/agent-management/device-groups/v2/groups/{group_id}',
                                     'summary': 'Delete a device group.',
                                     'operation_id': 'deleteDeviceGroup',
                                     'sku': '',
                                     'desc': 'Deletes the specified device group. Only empty groups (with no associated devices) can be deleted. If the group '
                                             'contains devices, remove or move them first. When recursive is true, the group and all nested child groups are '
                                             'deleted; all child groups must also be empty. Requires the Manage Device Groups permission (Agent Management > '
                                             'Device and Device Group Management > Manage, as labelled on the API Credentials page). Callers without this '
                                             'permission will receive a 403 Forbidden response.',
                                     'path_params': [{'name': 'group_id',
                                                      'required': True,
                                                      'desc': 'ID of device group to be deleted.',
                                                      'sample': '4Zh6VRUJQQauw_-AzxjtHw'}],
                                     'query_params': [{'name': 'recursive',
                                                       'type': 'boolean',
                                                       'required': False,
                                                       'default': 'false',
                                                       'desc': 'If true, delete the group and all nested child groups; all child groups must also be empty (no '
                                                               'associated devices). If false, only the specified group is deleted and it must itself be '
                                                               'empty.',
                                                       'sample': ''}],
                                     'body': None,
                                     'body_schema': []},
                                    {'method': 'GET',
                                     'path': '/agent-management/device-groups/v2/groups/{group_id}/devices',
                                     'summary': 'Retrieve a list of devices that are members of a device group.',
                                     'operation_id': 'listGroupDevices',
                                     'sku': '',
                                     'desc': 'Returns a paginated list of devices belonging to the specified device group. Unsupported query parameters or '
                                             'unsupported parameter values will be ignored. Requires the Read Device Groups permission (Agent Management > '
                                             'Device and Device Group Management > Read, as labelled on the API Credentials page). Callers without this '
                                             'permission will receive a 403 Forbidden response. Each entry is a summary only (device_id and device_name); use '
                                             'GET /agent-management/devices to retrieve full device detail.',
                                     'path_params': [{'name': 'group_id',
                                                      'required': True,
                                                      'desc': 'ID of the device group for which to retrieve devices.',
                                                      'sample': '4Zh6VRUJQQauw_-AzxjtHw'}],
                                     'query_params': [{'name': 'page',
                                                       'type': 'integer',
                                                       'required': False,
                                                       'default': '1',
                                                       'desc': '1-based page number for device results.',
                                                       'sample': ''},
                                                      {'name': 'page_size',
                                                       'type': 'integer',
                                                       'required': False,
                                                       'default': '1000',
                                                       'desc': 'Number of device records per page. The maximum number of records supported per request is '
                                                               '1000.',
                                                       'sample': ''},
                                                      {'name': 'device_id',
                                                       'type': 'string',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'Unique device identifier.',
                                                       'sample': ''},
                                                      {'name': 'antimalware_content_version',
                                                       'type': 'array',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'Version of antimalware content installed on the device.',
                                                       'sample': ''},
                                                      {'name': 'endpoint_security_version',
                                                       'type': 'array',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'Version of Endpoint Security installed on the device.',
                                                       'sample': ''},
                                                      {'name': 'web_security_version',
                                                       'type': 'array',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'Version of Web Security installed on the device.',
                                                       'sample': ''},
                                                      {'name': 'data_security_version',
                                                       'type': 'array',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'Version of Data Security installed on the device.',
                                                       'sample': ''},
                                                      {'name': 'esa_version',
                                                       'type': 'array',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'Version of Endpoint Security Agent installed on the device.',
                                                       'sample': ''},
                                                      {'name': 'connection_status',
                                                       'type': 'string',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'Connection status of the agent installed on the device. Online means the device has '
                                                               'communicated with the backend within the last 48 hours; otherwise the device is Offline.',
                                                       'sample': ''},
                                                      {'name': 'security_status',
                                                       'type': 'array',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'Device security status. The meaning of each value (including NOT_COMPUTED, UNENROLLED, and '
                                                               'UNKNOWN) is documented at '
                                                               'https://techdocs.broadcom.com/us/en/symantec-security-software/symantec-cbx/cbx/ind…',
                                                       'sample': ''},
                                                      {'name': 'device_os',
                                                       'type': 'array',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'OS name of the device.',
                                                       'sample': ''},
                                                      {'name': 'os_version',
                                                       'type': 'string',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'OS version of the device (partial/prefix match), e.g. "10.0" matches "10.0.19044".',
                                                       'sample': ''},
                                                      {'name': 'device_type',
                                                       'type': 'array',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'OS type of the device. Enum values: WORKSTATION = User workstation; SERVER = Server '
                                                               'infrastructure.',
                                                       'sample': ''},
                                                      {'name': 'form_factor',
                                                       'type': 'string',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'Device form factor.',
                                                       'sample': ''},
                                                      {'name': 'device_name',
                                                       'type': 'array',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'Name of the device.',
                                                       'sample': ''},
                                                      {'name': 'status_reason',
                                                       'type': 'array',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'Device status reason codes reported by the endpoint agent. Values are numeric strings (e.g. '
                                                               '"132", "613") and are not a fixed enum — the set of codes depends on the agent version and '
                                                               'installed product…',
                                                       'sample': ''},
                                                      {'name': 'ipv4_address',
                                                       'type': 'array',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'IPv4 address of a device.',
                                                       'sample': ''},
                                                      {'name': 'mac_address',
                                                       'type': 'array',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'MAC address of a device.',
                                                       'sample': ''},
                                                      {'name': 'capabilities_enabled',
                                                       'type': 'array',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'Capabilities enabled on this device. Supported values: ENDPOINT_PROTECTION, WEB_SECURITY, '
                                                               'DATA_SECURITY.',
                                                       'sample': ''},
                                                      {'name': 'cloud_platform',
                                                       'type': 'array',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'Cloud platform. Supported values: AWS, GCP, AZURE, NONE.',
                                                       'sample': ''},
                                                      {'name': 'enrollment_date',
                                                       'type': 'integer',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'Devices enrolled within the specified number of days up to now will be returned. Note: '
                                                               'although this field is named enrollment_date and represents a date in device responses, this '
                                                               'query parameter expe…',
                                                       'sample': ''},
                                                      {'name': 'permission',
                                                       'type': 'array',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'Cloud SWG connectivity state. Supported values: ALLOWED, BLOCKED, DISABLED.',
                                                       'sample': ''},
                                                      {'name': 'instance_id',
                                                       'type': 'array',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'Device instance ID.',
                                                       'sample': ''},
                                                      {'name': 'domain',
                                                       'type': 'array',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'The domain to which this device is connected.',
                                                       'sample': ''},
                                                      {'name': 'host',
                                                       'type': 'array',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'Device host name.',
                                                       'sample': ''},
                                                      {'name': 'user',
                                                       'type': 'array',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'Last logged-on user name.',
                                                       'sample': ''},
                                                      {'name': 'mdm_id',
                                                       'type': 'array',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'Device MDM ID.',
                                                       'sample': ''}],
                                     'body': None,
                                     'body_schema': []},
                                    {'method': 'PUT',
                                     'path': '/agent-management/device-groups/v2/groups/{group_id}/devices',
                                     'summary': 'Transfer multiple devices from one device group to another device group.',
                                     'operation_id': 'moveDevicesToGroup',
                                     'sku': '',
                                     'desc': 'Transfers multiple devices from their current group to the specified target group. A 200 response does not '
                                             "guarantee all devices were moved; inspect each item's `status` field for individual results. Requires the Manage "
                                             'Device Groups permission (Agent Management > Device and Device Group Management > Manage, as labelled on the API '
                                             'Credentials page). Callers without this permission will receive a 403 Forbidden response.',
                                     'path_params': [{'name': 'group_id',
                                                      'required': True,
                                                      'desc': 'ID of the target device group.',
                                                      'sample': '4Zh6VRUJQQauw_-AzxjtHw'}],
                                     'query_params': [],
                                     'body': {'device_uids': ['0ODNRjz5THGP0-SAXsTR_w']},
                                     'body_schema': ['`device_uids` `array[string]` *(required)* — List of device unique identifiers to move. Each value '
                                                     'corresponds to the device_id field returned by GET /groups/{group_id}/devices.']},
                                    {'method': 'GET',
                                     'path': '/agent-management/device-groups/v2/groups/{group_id}/groups',
                                     'summary': 'Retrieve a list of device groups that are members of a device group.',
                                     'operation_id': 'listChildDeviceGroups',
                                     'sku': '',
                                     'desc': 'Returns direct child groups only. Requires the Read Device Groups permission (Agent Management > Device and '
                                             'Device Group Management > Read, as labelled on the API Credentials page). Callers without this permission will '
                                             'receive a 403 Forbidden response.',
                                     'path_params': [{'name': 'group_id',
                                                      'required': True,
                                                      'desc': 'The ID of the device group for which to return child groups.',
                                                      'sample': 'Rr_WEJixSMKN19kOilTf-g'}],
                                     'query_params': [{'name': 'page',
                                                       'type': 'integer',
                                                       'required': False,
                                                       'default': '1',
                                                       'desc': '1-based page number for child group results.',
                                                       'sample': ''},
                                                      {'name': 'page_size',
                                                       'type': 'integer',
                                                       'required': False,
                                                       'default': '1000',
                                                       'desc': 'Number of child group records per page. The maximum number of records supported per request is '
                                                               '1000.',
                                                       'sample': ''},
                                                      {'name': 'order_by',
                                                       'type': 'string',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'Sort order for the returned child device groups. Only the name field is supported, in either '
                                                               'ascending ("name") or descending ("name desc") direction; sorting is case-insensitive.',
                                                       'sample': ''},
                                                      {'name': 'name',
                                                       'type': 'string',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'Filter child groups by name (partial match).',
                                                       'sample': ''}],
                                     'body': None,
                                     'body_schema': []},
                                    {'method': 'PUT',
                                     'path': '/agent-management/device-groups/v2/groups/{group_id}/groups',
                                     'summary': 'Move a device group into another device group.',
                                     'operation_id': 'moveGroupToGroup',
                                     'sku': '',
                                     'desc': 'Moves the specified device group, including all of its children, into the target device group. Moving a group '
                                             'into one of its own descendants is not permitted and results in a 400 error. Requires the Manage Device Groups '
                                             'permission (Agent Management > Device and Device Group Management > Manage, as labelled on the API Credentials '
                                             'page). Callers without this permission will receive a 403 Forbidden response.',
                                     'path_params': [{'name': 'group_id',
                                                      'required': True,
                                                      'desc': 'ID of the destination parent device group to move into. The device group being moved (the '
                                                              "source group) is identified separately in the request body's id field.",
                                                      'sample': '4Zh6VRUJQQauw_-AzxjtHw'}],
                                     'query_params': [],
                                     'body': {'id': '7tiwNJWKSJmE4OYRzwHwsw'},
                                     'body_schema': ['`id` `string` *(required)* — The unique identifier of the device group to move (the source group). The '
                                                     'path parameter group_id identifies the destination parent group it will be moved into.']}]},
 '🕹️ Device Commands': {'doc': 'cbx_device_commands.md',
                        'permissions': ['Device Commands -> Quarantine Device / Unquarantine Device',
                                        'Device Commands -> Scan Device',
                                        'Device Commands -> Restart Device',
                                        'Device Commands -> Run LiveUpdate'],
                        'endpoints': [{'method': 'POST',
                                       'path': '/agent-management/device-commands/v2/commands/allow',
                                       'summary': 'This API lets you unquarantine managed devices.',
                                       'operation_id': 'unquarantineDevice',
                                       'sku': '',
                                       'desc': 'Initiates a command to unquarantine and restore network access for the specified managed devices. This '
                                               'asynchronous operation returns a 202 Accepted response upon successful initiation. The status of the command '
                                               'execution can be monitored by polling GET /agent-management/device-commands/v2/commands/{command_id} using the '
                                               'returned command_state_ref.',
                                       'path_params': [],
                                       'query_params': [],
                                       'body': {'device_ids': ['550e8400-e29b-41d4-a716-446655440000', '732a3921-1191-447a-85b1-124b81093012']},
                                       'body_schema': ['`device_ids` `array[string]` *(required)* — The list of device ids to send the command. Minimum 1 and '
                                                       'maximum 1000 items.']},
                                      {'method': 'POST',
                                       'path': '/agent-management/device-commands/v2/commands/contain',
                                       'summary': 'This API lets you quarantine managed devices.',
                                       'operation_id': 'quarantineDevice',
                                       'sku': '',
                                       'desc': 'Initiates a command to quarantine the specified managed devices, restricting their network access to prevent '
                                               'threat spread. This asynchronous operation returns a 202 Accepted response upon successful initiation. The '
                                               'status of the command execution can be monitored by polling GET '
                                               '/agent-management/device-commands/v2/commands/{command_id} using the returned command_state_ref.',
                                       'path_params': [],
                                       'query_params': [],
                                       'body': {'device_ids': ['550e8400-e29b-41d4-a716-446655440000', '732a3921-1191-447a-85b1-124b81093012'],
                                                'org_unit_ids': ['org-12345', 'org-67890'],
                                                'payload': {'quarantine_host_group_name': 'isolated-hosts'},
                                                'is_recursive': False},
                                       'body_schema': ['`device_ids` `array[string]` — The list of device ids to send the command. Minimum 1 and maximum 1000 '
                                                       'items.',
                                                       '`org_unit_ids` `array[string]` — The list of org unit ids to send the command. Minimum 1 and maximum '
                                                       '1000 items.',
                                                       '`payload` `object` *(required)* — The payload containing details for the quarantine command',
                                                       '`is_recursive` `boolean` — Whether to recursively apply the command to sub-units']},
                                      {'method': 'POST',
                                       'path': '/agent-management/device-commands/v2/commands/files/contain',
                                       'summary': 'This API lets you quarantine files on managed devices.',
                                       'operation_id': 'quarantineFile',
                                       'sku': '',
                                       'desc': 'Initiates a command to quarantine a specific file on a managed device, preventing its execution and access. '
                                               'This asynchronous operation returns a 202 Accepted response upon successful initiation. The status of the '
                                               'command execution can be monitored by polling GET /agent-management/device-commands/v2/commands/{command_id} '
                                               'using the returned command_state_ref.',
                                       'path_params': [],
                                       'query_params': [],
                                       'body': {'device_ids': ['123e4567-e89b-12d3-a456-426614174000', '987e6543-e21b-34d3-b456-426614174011'],
                                                'hashes': ['e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
                                                           '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92']},
                                       'body_schema': ['`device_ids` `array[string]` *(required)* — The list of device ids to send the command. Minimum 1 and '
                                                       'maximum 1000 items.',
                                                       '`hashes` `array[string]` *(required)* — The list of file hashes to quarantine on devices. Accepts '
                                                       'SHA-256 hash strings. Minimum 1 and maximum 100 items.']},
                                      {'method': 'POST',
                                       'path': '/agent-management/device-commands/v2/commands/restart',
                                       'summary': 'This API lets you reboot managed devices.',
                                       'operation_id': 'restartDevice',
                                       'sku': '',
                                       'desc': 'Restarts the specified managed devices. The devices must be currently online to receive the command. This '
                                               'asynchronous operation returns a 202 Accepted response upon successful initiation. The status of the command '
                                               'execution can be monitored by polling GET /agent-management/device-commands/v2/commands/{command_id} using the '
                                               'returned command_state_ref, or by monitoring the device status via the Devices API (GET '
                                               '/agent-management/devices/{device_id}) to observe the transition back to an online state.',
                                       'path_params': [],
                                       'query_params': [],
                                       'body': {'device_ids': ['123e4567-e89b-12d3-a456-426614174000', '987e6543-e21b-34d3-b456-426614174011'],
                                                'payload': {'prompt_type': 'prompt',
                                                            'schedule_type': 'later',
                                                            'reason_type': 'remediation',
                                                            'message': 'Restarting device for remediation'}},
                                       'body_schema': ['`device_ids` `array[string]` *(required)* — The list of device ids to send the command. Minimum 1 and '
                                                       'maximum 1000 items.',
                                                       '`payload` `object` *(required)* — The payload containing details for the restart command']},
                                      {'method': 'POST',
                                       'path': '/agent-management/device-commands/v2/commands/scans/quick',
                                       'summary': 'This API lets you initiate a quick scan on managed devices.',
                                       'operation_id': 'initiateDeviceScanQuick',
                                       'sku': '',
                                       'desc': 'Initiates a quick scan on the specified managed devices to detect active threats and malware. This '
                                               'asynchronous operation returns a 202 Accepted response upon successful initiation. The status of the command '
                                               'execution can be monitored by polling GET /agent-management/device-commands/v2/commands/{command_id} using the '
                                               'returned command_state_ref.',
                                       'path_params': [],
                                       'query_params': [],
                                       'body': {'device_ids': ['550e8400-e29b-41d4-a716-446655440000', '732a3921-1191-447a-85b1-124b81093012'],
                                                'org_unit_ids': ['org-12345', 'org-67890'],
                                                'is_recursive': False},
                                       'body_schema': ['`device_ids` `array[string]` — The list of device ids to send the command. Minimum 1 and maximum 1000 '
                                                       'items.',
                                                       '`org_unit_ids` `array[string]` — The list of org unit ids to send the command. Minimum 1 and maximum '
                                                       '1000 items.',
                                                       '`is_recursive` `boolean` — Whether to recursively apply the command to sub-units']},
                                      {'method': 'POST',
                                       'path': '/agent-management/device-commands/v2/commands/scans/full',
                                       'summary': 'This API lets you initiate a full scan on managed devices.',
                                       'operation_id': 'initiateDeviceScanFull',
                                       'sku': '',
                                       'desc': 'Initiates a full scan on the specified managed devices to perform a deep system analysis and threat detection. '
                                               'This asynchronous operation returns a 202 Accepted response upon successful initiation. The status of the '
                                               'command execution can be monitored by polling GET /agent-management/device-commands/v2/commands/{command_id} '
                                               'using the returned command_state_ref.',
                                       'path_params': [],
                                       'query_params': [],
                                       'body': {'device_ids': ['550e8400-e29b-41d4-a716-446655440000', '732a3921-1191-447a-85b1-124b81093012'],
                                                'org_unit_ids': ['org-12345', 'org-67890'],
                                                'is_recursive': False},
                                       'body_schema': ['`device_ids` `array[string]` — The list of device ids to send the command. Minimum 1 and maximum 1000 '
                                                       'items.',
                                                       '`org_unit_ids` `array[string]` — The list of org unit ids to send the command. Minimum 1 and maximum '
                                                       '1000 items.',
                                                       '`is_recursive` `boolean` — Whether to recursively apply the command to sub-units']},
                                      {'method': 'POST',
                                       'path': '/agent-management/device-commands/v2/commands/scans/custom',
                                       'summary': 'This API lets you initiate a custom scan on managed devices.',
                                       'operation_id': 'initiateDeviceScanCustom',
                                       'sku': '',
                                       'desc': 'Initiates a custom scan on the specified managed devices based on custom scan parameters. This asynchronous '
                                               'operation returns a 202 Accepted response upon successful initiation. The status of the command execution can '
                                               'be monitored by polling GET /agent-management/device-commands/v2/commands/{command_id} using the returned '
                                               'command_state_ref.',
                                       'path_params': [],
                                       'query_params': [],
                                       'body': {'device_ids': ['550e8400-e29b-41d4-a716-446655440000', '732a3921-1191-447a-85b1-124b81093012'],
                                                'org_unit_ids': ['org-12345', 'org-67890'],
                                                'is_recursive': False},
                                       'body_schema': ['`device_ids` `array[string]` — The list of device ids to send the command. Minimum 1 and maximum 1000 '
                                                       'items.',
                                                       '`org_unit_ids` `array[string]` — The list of org unit ids to send the command. Minimum 1 and maximum '
                                                       '1000 items.',
                                                       '`is_recursive` `boolean` — Whether to recursively apply the command to sub-units']},
                                      {'method': 'POST',
                                       'path': '/agent-management/device-commands/v2/commands/update-content',
                                       'summary': 'This API lets you update security definitions and content of managed devices.',
                                       'operation_id': 'updateDeviceContent',
                                       'sku': '',
                                       'desc': 'Initiates a command to update the security definitions, policies, and signature content on the specified '
                                               'managed devices to ensure they have the latest protection. This asynchronous operation returns a 202 Accepted '
                                               'response upon successful initiation. The status of the command execution can be monitored by polling GET '
                                               '/agent-management/device-commands/v2/commands/{command_id} using the returned command_state_ref.',
                                       'path_params': [],
                                       'query_params': [],
                                       'body': {'device_ids': ['550e8400-e29b-41d4-a716-446655440000', '732a3921-1191-447a-85b1-124b81093012'],
                                                'org_unit_ids': ['org-12345', 'org-67890'],
                                                'is_recursive': False},
                                       'body_schema': ['`device_ids` `array[string]` — The list of device ids to send the command. Minimum 1 and maximum 1000 '
                                                       'items.',
                                                       '`org_unit_ids` `array[string]` — The list of org unit ids to send the command. Minimum 1 and maximum '
                                                       '1000 items.',
                                                       '`is_recursive` `boolean` — Whether to recursively apply the command to sub-units']},
                                      {'method': 'GET',
                                       'path': '/agent-management/device-commands/v2/commands',
                                       'summary': 'This API lets you retrieve a list of all commands.',
                                       'operation_id': 'listDeviceCommands',
                                       'sku': '',
                                       'desc': 'Retrieves a paginated list of all device commands filtered by optional query parameters.',
                                       'path_params': [],
                                       'query_params': [{'name': 'page_size',
                                                         'type': 'integer',
                                                         'required': False,
                                                         'default': '100',
                                                         'desc': 'The number of records fetched in a given request. The maximum number of records supported '
                                                                 'per request is 1000.',
                                                         'sample': ''},
                                                        {'name': 'page',
                                                         'type': 'integer',
                                                         'required': False,
                                                         'default': '1',
                                                         'desc': 'When this field is not present, it returns the first page.',
                                                         'sample': ''},
                                                        {'name': 'correlation_id',
                                                         'type': 'array',
                                                         'required': False,
                                                         'default': '',
                                                         'desc': 'The correlation ID associated with the command to search for. Multiple correlation IDs can '
                                                                 'be provided as a comma-separated list.',
                                                         'sample': ''},
                                                        {'name': 'device_id',
                                                         'type': 'array',
                                                         'required': False,
                                                         'default': '',
                                                         'desc': 'The unique device identifier (UUID) to search for. This corresponds to the UUID-formatted '
                                                                 'device_ids used in the POST command bodies. Multiple device IDs can be provided as a '
                                                                 'comma-separated list.',
                                                         'sample': ''},
                                                        {'name': 'created',
                                                         'type': 'string',
                                                         'required': False,
                                                         'default': '',
                                                         'desc': 'The created date in ISO 8601 format. Must be prepended with a > or <. Multiple range '
                                                                 'expressions can be provided as a comma-separated list within a single string value to define '
                                                                 'a range, e.g., >2026-0…',
                                                         'sample': ''},
                                                        {'name': 'modified',
                                                         'type': 'string',
                                                         'required': False,
                                                         'default': '',
                                                         'desc': 'The modified date in ISO 8601 format. Must be prepended with a > or <. Multiple range '
                                                                 'expressions can be provided as a comma-separated list within a single string value to define '
                                                                 'a range, e.g., >2026-…',
                                                         'sample': ''},
                                                        {'name': 'command_name',
                                                         'type': 'string',
                                                         'required': False,
                                                         'default': '',
                                                         'desc': 'The command name to search for. Valid values are: - FDR: Flight Data Recorder command. - '
                                                                 'RESTART: Reboot the managed devices. - QUARANTINE_DEVICE: Quarantine the specified devices. '
                                                                 '- UNQUARANTINE_DEVI…',
                                                         'sample': ''},
                                                        {'name': 'state',
                                                         'type': 'array',
                                                         'required': False,
                                                         'default': '',
                                                         'desc': 'The command execution state to search for. Multiple states can be provided as a '
                                                                 'comma-separated list. Valid values are: - PENDING: The command is queued but has not yet '
                                                                 'started. - IN_PROGRESS: The com…',
                                                         'sample': ''}],
                                       'body': None,
                                       'body_schema': []},
                                      {'method': 'GET',
                                       'path': '/agent-management/device-commands/v2/commands/{command_id}',
                                       'summary': 'This API lets you retrieve command details.',
                                       'operation_id': 'getDeviceCommandDetails',
                                       'sku': '',
                                       'desc': 'Retrieves detailed information and execution status for a specific device command.',
                                       'path_params': [{'name': 'command_id',
                                                        'required': True,
                                                        'desc': 'The unique identifier of the command details to return. The server accepts either the '
                                                                'UUID-formatted `command_state_ref` returned by the command-issuing POST endpoints, or the '
                                                                'opaque string `id` retur…',
                                                        'sample': '-CCS-CMD-TD6TBi8mTiWO_4TiLZy91w'}],
                                       'query_params': [],
                                       'body': None,
                                       'body_schema': []}]},
 '📊 Reporting': {'doc': 'cbx_reporting.md',
                 'permissions': ['Reports -> View Endpoint Security', 'Reports -> Manage Endpoint Security'],
                 'endpoints': [{'method': 'GET',
                                'path': '/common/reporting/v1/report-templates',
                                'summary': 'This API lets you retrieve the list of report templates.',
                                'operation_id': 'listReportTemplates',
                                'sku': '',
                                'desc': 'Retrieves a list of report templates with their configurations, filters, and scheduling information. Required '
                                        'permission: ses_view_reports. Callers without this permission will receive a 403 Forbidden response.',
                                'path_params': [],
                                'query_params': [{'name': 'page',
                                                  'type': 'integer',
                                                  'required': False,
                                                  'default': '1',
                                                  'desc': 'Page number to retrieve (1-based).',
                                                  'sample': ''},
                                                 {'name': 'page_size',
                                                  'type': 'integer',
                                                  'required': False,
                                                  'default': '25',
                                                  'desc': 'Number of records per page.',
                                                  'sample': ''},
                                                 {'name': 'report_type_id',
                                                  'type': 'string',
                                                  'required': False,
                                                  'default': '',
                                                  'desc': 'Filter by report type',
                                                  'sample': ''},
                                                 {'name': 'report_format',
                                                  'type': 'string',
                                                  'required': False,
                                                  'default': '',
                                                  'desc': 'Filter by report format. Valid values: `PDF` (Portable Document Format), `CSV` (Comma-Separated '
                                                          'Values), `HTML` (HyperText Markup Language), `EMAIL` (sent as the body of an email rather than a '
                                                          'downloa…',
                                                  'sample': ''}],
                                'body': None,
                                'body_schema': []},
                               {'method': 'POST',
                                'path': '/common/reporting/v1/report-templates',
                                'summary': 'This API lets you create a new report template.',
                                'operation_id': 'createReportTemplate',
                                'sku': '',
                                'desc': 'Creates a new report template with the provided configuration. Required permission: ses_manage_reports. Callers '
                                        'without this permission will receive a 403 Forbidden response.',
                                'path_params': [],
                                'query_params': [],
                                'body': {'name': 'Default Weekly Report',
                                         'report_type_id': 'saep-weekly-report',
                                         'report_format': 'PDF',
                                         'schedule': {'schedule_type': 'WEEKLY', 'days_of_week': ['MONDAY', 'WEDNESDAY', 'FRIDAY'], 'repeat_frequency': 1},
                                         'report_recipients': [{'email': 'john.doe@broadcom.com', 'email_notification': True, 'email_as_attachment': False}],
                                         'schedule_at': '2026-12-01T10:00:00.000Z'},
                                'body_schema': ['`name` `string` *(required)* — Name of the report template',
                                                '`report_type_id` `string` *(required)* — Identifier of the report type for this template',
                                                '`report_format` `string` *(required)* — Format in which the report will be generated. Valid values: `PDF` '
                                                '(Portable Document Format), `CSV` (Comma-Separated Values), `HTML` (HyperText Markup Language)…',
                                                '`schedule` `any` *(required)* — Configuration for how frequently the report should be generated',
                                                '`schedule_at` `string` — Schedule anchor in ISO 8601 UTC. Required when `schedule.schedule_type` is `DAILY`, '
                                                '`WEEKLY`, `MONTHLY`, or `QUARTERLY`; omit or set to `null` for `ONCE_A_DAY`, `VARIABLE`, an…',
                                                '`report_recipients` `array[object]` — Report recipient settings configuration. Omit or send null to create '
                                                'the template with no recipients.',
                                                '`report_filters` `object` — May be included in the request body only when report_type_id is '
                                                'fw-comprehensive-report or ips-comprehensive-report; including it for other report types returns 400. Omit '
                                                'o…']},
                               {'method': 'GET',
                                'path': '/common/reporting/v1/reports',
                                'summary': 'This API lets you retrieve the list of generated reports.',
                                'operation_id': 'listReports',
                                'sku': '',
                                'desc': 'Retrieves a list of all generated reports with their status, creation dates, and completion dates. Download links are '
                                        'not included in list responses: `download_link` is always `null` in results returned by this endpoint regardless of '
                                        'the `include_download_link` parameter. To obtain a usable download link, fetch the individual report by ID with '
                                        '`include_download_link=true`. Supports pagination and filtering by report type and template ID. Required permission: '
                                        'ses_view_reports. Callers without this permission will receive a 403 Forbidden response.',
                                'path_params': [],
                                'query_params': [{'name': 'page',
                                                  'type': 'integer',
                                                  'required': False,
                                                  'default': '1',
                                                  'desc': 'Page number to retrieve (1-based).',
                                                  'sample': ''},
                                                 {'name': 'page_size',
                                                  'type': 'integer',
                                                  'required': False,
                                                  'default': '25',
                                                  'desc': 'Number of records per page.',
                                                  'sample': ''},
                                                 {'name': 'report_type_id',
                                                  'type': 'string',
                                                  'required': False,
                                                  'default': '',
                                                  'desc': 'Filter by report type',
                                                  'sample': ''},
                                                 {'name': 'template_id',
                                                  'type': 'string',
                                                  'required': False,
                                                  'default': '',
                                                  'desc': 'Filter by report template ID to get all reports generated using a specific template.',
                                                  'sample': ''},
                                                 {'name': 'name',
                                                  'type': 'array',
                                                  'required': False,
                                                  'default': '',
                                                  'desc': 'Filter by report template name. Provide multiple values to search for multiple names.',
                                                  'sample': ''},
                                                 {'name': 'format',
                                                  'type': 'string',
                                                  'required': False,
                                                  'default': '',
                                                  'desc': 'Filter by report format. Valid values: `PDF` (Portable Document Format), `CSV` (Comma-Separated '
                                                          'Values), `HTML` (HyperText Markup Language), `EMAIL` (sent as the body of an email rather than a '
                                                          'downloa…',
                                                  'sample': ''},
                                                 {'name': 'status',
                                                  'type': 'string',
                                                  'required': False,
                                                  'default': '',
                                                  'desc': 'Filter by report status. Available values: IN_PROGRESS, COMPLETED, FAILED',
                                                  'sample': ''},
                                                 {'name': 'created_at',
                                                  'type': 'string',
                                                  'required': False,
                                                  'default': '',
                                                  'desc': 'Filter by creation date. Each token must be prefixed with > (after) or < (before) and the date-time '
                                                          'must be ISO 8601 UTC enclosed in single quotes. Provide two comma-separated tokens for a range, '
                                                          'e.g.…',
                                                  'sample': ''},
                                                 {'name': 'generation_mode',
                                                  'type': 'string',
                                                  'required': False,
                                                  'default': '',
                                                  'desc': 'Filter by generation mode. Available values: ad-hoc, scheduled',
                                                  'sample': ''},
                                                 {'name': 'language',
                                                  'type': 'string',
                                                  'required': False,
                                                  'default': '',
                                                  'desc': 'Filter by language/locale setting (e.g., en for English).',
                                                  'sample': ''}],
                                'body': None,
                                'body_schema': []},
                               {'method': 'POST',
                                'path': '/common/reporting/v1/report-templates/{template_id}/generate',
                                'summary': 'This API lets you generate a report using an existing report template by ID.',
                                'operation_id': 'generateReportByTemplateId',
                                'sku': '',
                                'desc': 'Generates a report using the configuration from an existing report template. This is a simplified endpoint that only '
                                        'requires the template ID. Required permission: ses_manage_reports. Callers without this permission will receive a 403 '
                                        'Forbidden response.',
                                'path_params': [{'name': 'template_id',
                                                 'required': True,
                                                 'desc': 'The UUID of the report template to use for generation.',
                                                 'sample': '3114e32c-bcb1-4bd7-b403-b73d7f297b40'}],
                                'query_params': [],
                                'body': None,
                                'body_schema': []},
                               {'method': 'GET',
                                'path': '/common/reporting/v1/reports/{report_id}',
                                'summary': 'This API lets you get the status and download link for a generated report.',
                                'operation_id': 'getReportStatus',
                                'sku': '',
                                'desc': 'Retrieves the status and metadata of a report generation job including creation date, completion date, and optional '
                                        'download link. The download link is included in the response when include_download_link=true and the report is '
                                        'completed. Required permission: ses_view_reports. Callers without this permission will receive a 403 Forbidden '
                                        'response.',
                                'path_params': [{'name': 'report_id',
                                                 'required': True,
                                                 'desc': 'The UUID of the report generation job.',
                                                 'sample': '7d16d3cd-6460-48bb-b2ff-3668afafd940'}],
                                'query_params': [{'name': 'include_download_link',
                                                  'type': 'boolean',
                                                  'required': False,
                                                  'default': 'false',
                                                  'desc': 'If set to true, includes the download link in the response when the report is completed. Download '
                                                          'link is only available for completed reports.',
                                                  'sample': ''}],
                                'body': None,
                                'body_schema': []},
                               {'method': 'GET',
                                'path': '/common/reporting/v1/report-templates/{template_id}',
                                'summary': 'This API lets you retrieve a specific report template by ID.',
                                'operation_id': 'getReportTemplate',
                                'sku': '',
                                'desc': 'Retrieves a single report template with its configuration, filters, and scheduling information. Required permission: '
                                        'ses_view_reports. Callers without this permission will receive a 403 Forbidden response.',
                                'path_params': [{'name': 'template_id',
                                                 'required': True,
                                                 'desc': 'The UUID of the report template to retrieve.',
                                                 'sample': '3114e32c-bcb1-4bd7-b403-b73d7f297b40'}],
                                'query_params': [],
                                'body': None,
                                'body_schema': []},
                               {'method': 'PUT',
                                'path': '/common/reporting/v1/report-templates/{template_id}',
                                'summary': 'This API lets you update the report template configuration.',
                                'operation_id': 'updateReportTemplate',
                                'sku': '',
                                'desc': 'Replaces the updatable fields of an existing report template: Name, Schedule, Report Format, and Report Recipient '
                                        'Settings. As a PUT, the request body must include the full representation of these fields — any updatable field '
                                        'omitted from the body is reset rather than left unchanged. Fields outside this set (e.g. template_id, report_type_id) '
                                        'are read-only and cannot be modified via this endpoint; if other fields are provided in the request body, the request '
                                        'may fail with a 400 Bad Input error. The template ID must be included in the URI path. Required permission: '
                                        'ses_manage_reports. Callers wi…',
                                'path_params': [{'name': 'template_id',
                                                 'required': True,
                                                 'desc': 'The UUID of the report template to update.',
                                                 'sample': '3114e32c-bcb1-4bd7-b403-b73d7f297b40'}],
                                'query_params': [],
                                'body': {'name': 'Updated Weekly Report',
                                         'report_format': 'PDF',
                                         'schedule': {'schedule_type': 'WEEKLY', 'days_of_week': ['MONDAY', 'WEDNESDAY', 'FRIDAY'], 'repeat_frequency': 1},
                                         'schedule_at': '2026-12-01T10:00:00.000Z'},
                                'body_schema': ['`name` `string` *(required)* — Name of the report template',
                                                '`report_format` `string` *(required)* — Format in which the report will be generated. Valid values: `PDF` '
                                                '(Portable Document Format), `CSV` (Comma-Separated Values), `HTML` (HyperText Markup Language)…',
                                                '`schedule` `any` *(required)* — Configuration for how frequently the report should be generated',
                                                '`report_recipients` `array[object]` — Report recipient settings configuration',
                                                '`schedule_at` `string` — Schedule anchor in ISO 8601 UTC. Required when schedule_type is DAILY, WEEKLY, '
                                                'MONTHLY, or QUARTERLY. Omit or set to null for NONE, VARIABLE, TWO_PER_QUARTER, or ONCE_A_DAY.',
                                                "`report_filters` `object` — Report filters configuration. Applicable only when the template's "
                                                '`report_type_id` is `fw-comprehensive-report` or `ips-comprehensive-report`. Send `null` to clear existing…']},
                               {'method': 'DELETE',
                                'path': '/common/reporting/v1/report-templates/{template_id}',
                                'summary': 'This API lets you delete a report template by ID.',
                                'operation_id': 'deleteReportTemplate',
                                'sku': '',
                                'desc': 'Deletes a report template with the specified ID. Required permission: ses_manage_reports. Callers without this '
                                        'permission will receive a 403 Forbidden response.',
                                'path_params': [{'name': 'template_id',
                                                 'required': True,
                                                 'desc': 'The UUID of the report template to delete.',
                                                 'sample': '3114e32c-bcb1-4bd7-b403-b73d7f297b40'}],
                                'query_params': [],
                                'body': None,
                                'body_schema': []},
                               {'method': 'GET',
                                'path': '/common/reporting/v1/report-templates/{template_id}/reports',
                                'summary': 'This API lets you retrieve reports generated using a specific report template.',
                                'operation_id': 'listReportsByTemplateId',
                                'sku': '',
                                'desc': 'Lists reports that are generated using the report-template id specified in the URL. Supports pagination. Required '
                                        'permission: ses_view_reports. Callers without this permission will receive a 403 Forbidden response.',
                                'path_params': [{'name': 'template_id',
                                                 'required': True,
                                                 'desc': 'The UUID of the report template.',
                                                 'sample': '9c3ff049-9f7a-4b4f-8958-add0d3328884'}],
                                'query_params': [{'name': 'page',
                                                  'type': 'integer',
                                                  'required': False,
                                                  'default': '1',
                                                  'desc': 'Page number to retrieve (1-based).',
                                                  'sample': ''},
                                                 {'name': 'page_size',
                                                  'type': 'integer',
                                                  'required': False,
                                                  'default': '25',
                                                  'desc': 'Number of records per page.',
                                                  'sample': ''}],
                                'body': None,
                                'body_schema': []}]},
 '📤 Data Forwarder': {'doc': 'cbx_data_forwarder.md',
                      'permissions': ['Data Forwarder -> View', 'Data Forwarder -> Manage'],
                      'endpoints': [{'method': 'GET',
                                     'path': '/common/data-forwarders/v3/configs',
                                     'summary': 'Get all configured forwarders',
                                     'operation_id': 'listConfigs',
                                     'sku': '',
                                     'desc': 'Returns all forwarder configurations for the environment associated with the authenticated token. Disabled '
                                             'forwarders are included. The array has no guaranteed ordering. Requires Data Forwarder `READ` permission.',
                                     'path_params': [],
                                     'query_params': [],
                                     'body': None,
                                     'body_schema': []},
                                    {'method': 'POST',
                                     'path': '/common/data-forwarders/v3/configs',
                                     'summary': 'Create a new forwarder configuration',
                                     'operation_id': 'createConfig',
                                     'sku': '',
                                     'desc': 'Creates a new forwarder. The API will make calls to check whether the forwarder can write to the specified '
                                             'storage using the configuration supplied. It will attempt to write a test message called `healthcheck.json` to '
                                             'the specified bucket or container under a sub-folder called `healthcheck`. If the bucket is misconfigured (e.g. '
                                             "incorrect permissions, principal ARN, etc.) or the configuration is incorrect (e.g. bucket prefix doesn't match "
                                             'path specified in policy), the API will respond with a `400` error with information about what was incorrect and '
                                             'how to fix the issue. Requires Data Forwarder…',
                                     'path_params': [],
                                     'query_params': [],
                                     'body': {'name': 'Alert Forwarder',
                                              'enabled': True,
                                              'type': 'alert',
                                              'version_constraint': '3.0.*',
                                              'destination_config': {'destination': 'aws_s3', 's3_bucket_name': 'demo-bucket', 's3_prefix': 'demo-alert'}},
                                     'body_schema': ['`name` `string` *(required)* — Display name to assign to the new forwarder.',
                                                     '`enabled` `boolean` — Whether to create the forwarder as enabled.',
                                                     '`type` `string` *(required)* — The datastream type being forwarded. Each type determines the data stream '
                                                     'and which features are available: - `alert`: Includes all alerts, such as Web Traffic, Behavior…',
                                                     '`version_constraint` `string` — Semantic version pattern controlling which version of the data to '
                                                     'forward. Defaults if omitted: alert=2.0.0, event=2.0.0, forensicquery=2.0.0. The major version must be…',
                                                     '`destination_config` `oneOf` *(required)* — Destination-specific storage configuration. The required and '
                                                     'permitted fields depend on the `destination` value. Supplying a field that belongs to a differe…']},
                                    {'method': 'GET',
                                     'path': '/common/data-forwarders/v3/configs/{id}',
                                     'summary': 'Get a specific forwarder configuration',
                                     'operation_id': 'getConfigById',
                                     'sku': '',
                                     'desc': 'Returns the forwarder configuration with the specified ID. The config must belong to the environment of the '
                                             'authenticated token; otherwise a `404 Not Found` is returned. Requires Data Forwarder `READ` permission.',
                                     'path_params': [{'name': 'id',
                                                      'required': True,
                                                      'desc': 'Unique identifier of the forwarder configuration.',
                                                      'sample': '011b9d03-b12d-11ec-af42-ae26c44461dc'}],
                                     'query_params': [],
                                     'body': None,
                                     'body_schema': []},
                                    {'method': 'PUT',
                                     'path': '/common/data-forwarders/v3/configs/{id}',
                                     'summary': 'Update a forwarder configuration',
                                     'operation_id': 'updateConfig',
                                     'sku': '',
                                     'desc': 'Replaces an existing forwarder configuration (full PUT — all fields required). The `type` (e.g. `event`, '
                                             '`alert`) and `destination` (e.g. `aws_s3`, `azure_blob_storage`) are immutable after creation; supply their '
                                             'current values unchanged or the request will be rejected with a `400`. All other fields — including bucket name, '
                                             'prefix, storage account, and container — can be freely modified. When editing an existing forwarder, the API '
                                             'will make additional calls to check whether the forwarder can write to the specified destination using the '
                                             'configuration supplied. It will attempt to write a test me…',
                                     'path_params': [{'name': 'id',
                                                      'required': True,
                                                      'desc': 'Unique identifier of the forwarder configuration.',
                                                      'sample': '011b9d03-b12d-11ec-af42-ae26c44461dc'}],
                                     'query_params': [],
                                     'body': {'name': 'DevRelTest',
                                              'enabled': False,
                                              'type': 'event',
                                              'version_constraint': '2.0.0',
                                              'destination_config': {'destination': 'aws_s3', 's3_bucket_name': 'DevRelTestBucket', 's3_prefix': 'test'}},
                                     'body_schema': ['`name` `string` *(required)* — Updated name for the forwarder.',
                                                     '`enabled` `boolean` *(required)* — Whether the forwarder should be enabled.',
                                                     '`type` `string` *(required)* — The datastream type being forwarded. Each type determines the data stream '
                                                     'and which features are available: - `alert`: Includes all alerts, such as Web Traffic, Behavior…',
                                                     '`version_constraint` `string` *(required)* — Updated semantic version pattern controlling which version '
                                                     'of the data to forward. Valid forms: `N.N.N`, `N.N.*`, `N.*.*`.',
                                                     '`destination_config` `oneOf` *(required)* — Destination-specific storage configuration. The required and '
                                                     'permitted fields depend on the `destination` value. Supplying a field that belongs to a differe…']},
                                    {'method': 'DELETE',
                                     'path': '/common/data-forwarders/v3/configs/{id}',
                                     'summary': 'Delete a forwarder configuration',
                                     'operation_id': 'deleteConfig',
                                     'sku': '',
                                     'desc': 'Permanently deletes a forwarder configuration by its ID. All associated filters are automatically deleted along '
                                             'with the config. Data forwarding stops within approximately 1–2 minutes of deletion. Deletion is non-reversible; '
                                             'deletion events are recorded in the audit log.',
                                     'path_params': [{'name': 'id',
                                                      'required': True,
                                                      'desc': 'Unique identifier of the forwarder configuration.',
                                                      'sample': '011b9d03-b12d-11ec-af42-ae26c44461dc'}],
                                     'query_params': [],
                                     'body': None,
                                     'body_schema': []},
                                    {'method': 'POST',
                                     'path': '/common/data-forwarders/v3/validate-filter',
                                     'summary': 'Validate a filter',
                                     'operation_id': 'validateFilter',
                                     'sku': '',
                                     'desc': 'Validates whether a filter uses compatible query syntax, field names, and values. This endpoint does not create '
                                             'or persist the filter — it only checks validity. Filters are only applicable to `event` forwarder types. To '
                                             'ensure the query will be accepted at filter creation or update time, supply the same `version_constraint` value '
                                             'as the target configuration. Validating against a different version than the config uses does not guarantee the '
                                             'query will pass when the filter is created or updated. Requires Data Forwarder `MANAGE` permission.',
                                     'path_params': [],
                                     'query_params': [],
                                     'body': {'name': 'Example Filter',
                                              'action': 'INCLUDE',
                                              'enabled': True,
                                              'query': 'device_os:WINDOWS AND alert_id:*',
                                              'version_constraint': '2.0.0'},
                                     'body_schema': ['`name` `string` *(required)* — Name for the filter being validated.',
                                                     '`enabled` `boolean` — Whether the filter would be enabled.',
                                                     '`action` `string` *(required)* — The action to validate: `INCLUDE` to forward matching events, `EXCLUDE` '
                                                     'to drop them. (enum: `INCLUDE`, `EXCLUDE`)',
                                                     '`query` `string` *(required)* — The query to validate against the specified schema version.',
                                                     '`version_constraint` `string` — Schema version to validate the filter against. If not included, the API '
                                                     'will validate against the lowest supported schema version (2.0.0). Valid forms: `N.N.N`, `N.N.*`…']},
                                    {'method': 'GET',
                                     'path': '/common/data-forwarders/v3/configs/{id}/health-check',
                                     'summary': 'Run a health check for a forwarder configuration',
                                     'operation_id': 'getHealthCheckByConfigId',
                                     'sku': '',
                                     'desc': 'Runs a health check on a forwarder to determine if the forwarder is able to write to the specified S3 Bucket, '
                                             'GCS Bucket, or Azure Container using the existing configuration. The health check can indicate if the bucket is '
                                             'misconfigured (i.e. incorrect permissions, principal ARN, etc.), if the configuration is incorrect (i.e. bucket '
                                             "prefix doesn't match path specified in policy), or if the forwarder is working as expected. If successful, the "
                                             'health check will attempt to write a test message called `healthcheck.json` to the bucket under a subfolder '
                                             'called `healthcheck` (or the Azure Container) a…',
                                     'path_params': [{'name': 'id',
                                                      'required': True,
                                                      'desc': 'Unique identifier of the forwarder configuration.',
                                                      'sample': '011b9d03-b12d-11ec-af42-ae26c44461dc'}],
                                     'query_params': [],
                                     'body': None,
                                     'body_schema': []},
                                    {'method': 'GET',
                                     'path': '/common/data-forwarders/v3/configs/{id}/filters',
                                     'summary': 'Get all filters for a configuration',
                                     'operation_id': 'listFiltersByConfig',
                                     'sku': '',
                                     'desc': 'Returns all filters for the specified forwarder configuration. A configuration supports a maximum of 25 filters. '
                                             'Filters are only applicable to `event` forwarder types — calling this endpoint on an `alert`or `forensicquery` '
                                             'config returns an empty array.',
                                     'path_params': [{'name': 'id',
                                                      'required': True,
                                                      'desc': 'Unique identifier of the forwarder configuration.',
                                                      'sample': '011b9d03-b12d-11ec-af42-ae26c44461dc'}],
                                     'query_params': [],
                                     'body': None,
                                     'body_schema': []},
                                    {'method': 'POST',
                                     'path': '/common/data-forwarders/v3/configs/{id}/filters',
                                     'summary': 'Create a filter for a configuration',
                                     'operation_id': 'createFilter',
                                     'sku': '',
                                     'desc': 'Creates a filter for the specified configuration to include or exclude data from being forwarded. Multiple '
                                             'filters for the same config ID apply logical OR to support separated complex conditions. For example, two '
                                             'include and two exclude filters would be applied as: `(IncludeFilter1 OR IncludeFilter2) AND NOT (ExcludeFilter1 '
                                             'OR ExcludeFilter2)`. If you want to create multiple filters at once check out `bulk` or `bulk-overwrite` '
                                             'endpoints. Filters are only applicable to `event` forwarder types. A configuration supports a maximum of 25 '
                                             'filters. Attempting to create a filter when the limit has alr…',
                                     'path_params': [{'name': 'id',
                                                      'required': True,
                                                      'desc': 'Unique identifier of the forwarder configuration.',
                                                      'sample': '011b9d03-b12d-11ec-af42-ae26c44461dc'}],
                                     'query_params': [],
                                     'body': {'name': 'Example Filter', 'action': 'INCLUDE', 'enabled': True, 'query': 'device_os:WINDOWS AND alert_id:*'},
                                     'body_schema': ['`name` `string` *(required)* — Display name to assign to the new filter.',
                                                     '`enabled` `boolean` — Whether the filter is active on creation. Defaults to `true`.',
                                                     '`action` `string` *(required)* — Determines whether matching events are forwarded (`INCLUDE`) or dropped '
                                                     '(`EXCLUDE`). (enum: `INCLUDE`, `EXCLUDE`)',
                                                     '`query` `string` *(required)* — The query to match against incoming data. A query cannot include fields '
                                                     'from different event types since the Data Forwarder performs filtering on individual events.']},
                                    {'method': 'POST',
                                     'path': '/common/data-forwarders/v3/configs/{id}/filters/bulk',
                                     'summary': 'Bulk create or update filters for a configuration',
                                     'operation_id': 'bulkCreateOrUpdateFilters',
                                     'sku': '',
                                     'desc': 'Creates or updates multiple filters for the specified configuration. The presence of an `id` field is the '
                                             'differentiator between create and update — items with `id` are treated as updates, items without `id` are '
                                             'treated as creates. Multiple filters for the same config ID apply logical OR to support separated complex '
                                             'conditions: `(IncludeFilter1 OR IncludeFilter2) AND NOT (ExcludeFilter1 OR ExcludeFilter2)`. Due to backend '
                                             'limitations, bulk requests are limited to a maximum of 25 total items to ensure atomicity. Filters are only '
                                             'applicable to `event` forwarder types. Filter queries are validate…',
                                     'path_params': [{'name': 'id',
                                                      'required': True,
                                                      'desc': 'Unique identifier of the forwarder configuration.',
                                                      'sample': '011b9d03-b12d-11ec-af42-ae26c44461dc'}],
                                     'query_params': [],
                                     'body': [{'action': 'INCLUDE',
                                               'enabled': True,
                                               'name': 'Example Filter',
                                               'query': 'device_os:LINUX AND alert_id:*',
                                               'id': 'f13e6723-7779-4fdc-a26e-5a95e66be891'},
                                              {'action': 'EXCLUDE', 'enabled': True, 'name': 'Example EXCLUDE Filter', 'query': 'device_os:MAC'}],
                                     'body_schema': ['`[ ]` `array[any]`']},
                                    {'method': 'POST',
                                     'path': '/common/data-forwarders/v3/configs/{id}/filters/bulk-overwrite',
                                     'summary': 'Bulk replace all filters for a configuration',
                                     'operation_id': 'bulkReplaceFilters',
                                     'sku': '',
                                     'desc': 'Replaces all existing filters for the specified configuration with the supplied set. Any previously existing '
                                             'filters not included in the request body will be deleted. Due to backend limitations, bulk requests are limited '
                                             'to a maximum of 25 total items to ensure atomicity. Filters are only applicable to `event` forwarder types. '
                                             "Filter queries are validated against the target config's own `version_constraint` at write time — filters have "
                                             'no `version_constraint` field of their own. To pre-validate queries before submitting, call `POST '
                                             '/validate-filter` with the same `version_constraint` value as…',
                                     'path_params': [{'name': 'id',
                                                      'required': True,
                                                      'desc': 'Unique identifier of the forwarder configuration.',
                                                      'sample': '011b9d03-b12d-11ec-af42-ae26c44461dc'}],
                                     'query_params': [],
                                     'body': [{'name': 'Block Malicious Processes',
                                               'action': 'EXCLUDE',
                                               'query': 'process_reputation:1_KNOWN_BAD',
                                               'enabled': True},
                                              {'name': 'Windows Events Only', 'action': 'INCLUDE', 'query': 'device_os:WINDOWS', 'enabled': True}],
                                     'body_schema': ['`[ ]` `array[any]`']},
                                    {'method': 'GET',
                                     'path': '/common/data-forwarders/v3/configs/{id}/filters/{filterId}',
                                     'summary': 'Get a specific filter by ID',
                                     'operation_id': 'getFilterById',
                                     'sku': '',
                                     'desc': 'Returns the filter with the specified ID for the given forwarder configuration. Returns `404` if either the '
                                             'config or the filter is not found.',
                                     'path_params': [{'name': 'id',
                                                      'required': True,
                                                      'desc': 'Unique identifier of the forwarder configuration.',
                                                      'sample': '011b9d03-b12d-11ec-af42-ae26c44461dc'},
                                                     {'name': 'filterId',
                                                      'required': True,
                                                      'desc': 'Unique identifier of the filter.',
                                                      'sample': 'f13e6723-7779-4fdc-a26e-5a95e66be891'}],
                                     'query_params': [],
                                     'body': None,
                                     'body_schema': []},
                                    {'method': 'PUT',
                                     'path': '/common/data-forwarders/v3/configs/{id}/filters/{filterId}',
                                     'summary': 'Update a filter',
                                     'operation_id': 'updateFilter',
                                     'sku': '',
                                     'desc': 'Replaces an existing filter (full PUT — all fields except `id` are required). The filter to update is identified '
                                             'by the `filterId` path parameter. If an `id` field is included in the request body it is ignored; `create_time` '
                                             'and `update_time` are always managed by the backend and are silently ignored if present in the body. Filters are '
                                             "only applicable to `event` forwarder types. The updated query is validated against the target config's own "
                                             '`version_constraint` — filters have no `version_constraint` field of their own. To pre-validate a query before '
                                             'updating, call `POST /validate-filter` with…',
                                     'path_params': [{'name': 'id',
                                                      'required': True,
                                                      'desc': 'Unique identifier of the forwarder configuration.',
                                                      'sample': '011b9d03-b12d-11ec-af42-ae26c44461dc'},
                                                     {'name': 'filterId',
                                                      'required': True,
                                                      'desc': 'Unique identifier of the filter.',
                                                      'sample': 'f13e6723-7779-4fdc-a26e-5a95e66be891'}],
                                     'query_params': [],
                                     'body': {'id': 'f13e6723-7779-4fdc-a26e-5a95e66be891',
                                              'name': 'Example Filter - Edited',
                                              'action': 'INCLUDE',
                                              'enabled': True,
                                              'query': 'device_os:WINDOWS AND alert_id:* AND process_reputation:1_KNOWN_BAD'},
                                     'body_schema': ['`id` `string` — Filter UUID. Optional — the server uses the `filterId` path parameter to identify the '
                                                     'filter and silently overrides this value.',
                                                     '`name` `string` *(required)* — Updated display name for the filter.',
                                                     '`enabled` `boolean` *(required)* — Whether the filter should be active after the update.',
                                                     '`action` `string` *(required)* — Whether the filter should include or exclude matching events. (enum: '
                                                     '`INCLUDE`, `EXCLUDE`)',
                                                     '`query` `string` *(required)* — Updated query to match against incoming data.']},
                                    {'method': 'DELETE',
                                     'path': '/common/data-forwarders/v3/configs/{id}/filters/{filterId}',
                                     'summary': 'Delete a filter',
                                     'operation_id': 'deleteFilter',
                                     'sku': '',
                                     'desc': 'Permanently deletes a filter from the specified forwarder configuration. Filters are only applicable to `event` '
                                             'forwarder types. Requires Data Forwarder `MANAGE` permission.',
                                     'path_params': [{'name': 'id',
                                                      'required': True,
                                                      'desc': 'Unique identifier of the forwarder configuration.',
                                                      'sample': '011b9d03-b12d-11ec-af42-ae26c44461dc'},
                                                     {'name': 'filterId',
                                                      'required': True,
                                                      'desc': 'Unique identifier of the filter.',
                                                      'sample': 'f13e6723-7779-4fdc-a26e-5a95e66be891'}],
                                     'query_params': [],
                                     'body': None,
                                     'body_schema': []},
                                    {'method': 'GET',
                                     'path': '/common/data-forwarders/v3/schemas/events',
                                     'summary': 'Get the filterable event schema',
                                     'operation_id': 'getFilterableSchema',
                                     'sku': '',
                                     'desc': 'Returns a JSON schema document describing filterable fields, their types, and available enum values for endpoint '
                                             'events. When `version_constraint` is specified, the API returns all filterable fields available for that schema '
                                             'version; if not specified, it returns filterable fields for the lowest supported schema version (2.0.0). This '
                                             'endpoint is publicly accessible — no authentication token is required.',
                                     'path_params': [],
                                     'query_params': [{'name': 'version_constraint',
                                                       'type': 'string',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'Schema version to retrieve filterable fields for (e.g. `2.0.0`, `2.1.0`, `2.2.0`). If not '
                                                               'specified, the lowest supported schema version is used. Valid forms: `N.N.N`, `N.N.*`, '
                                                               '`N.*.*`.',
                                                       'sample': ''}],
                                     'body': None,
                                     'body_schema': []},
                                    {'method': 'GET',
                                     'path': '/common/data-forwarders/v3/versions',
                                     'summary': 'Get available forwarder versions',
                                     'operation_id': 'getAvailableVersions',
                                     'sku': '',
                                     'desc': 'Returns all available GA forwarder schema versions, optionally filtered by type. Versions are returned in '
                                             'ascending order. Only released versions are included — deprecated versions are omitted. To select a '
                                             '`version_constraint` for a new config, pick the latest version in the array for the relevant type. Requires Data '
                                             'Forwarder `READ` permission.',
                                     'path_params': [],
                                     'query_params': [{'name': 'type',
                                                       'type': 'string',
                                                       'required': False,
                                                       'default': '',
                                                       'desc': 'Forwarder type to filter by. When omitted, versions for all types are returned.',
                                                       'sample': ''}],
                                     'body': None,
                                     'body_schema': []}]},
 '🧭 TI: TAXII 2.1': {'doc': 'cbx_taxii21.md',
                     'permissions': ['Threat Intel -> Read'],
                     'endpoints': [{'method': 'GET',
                                    'path': '/common/threat-intel/v1/taxii2',
                                    'summary': 'TAXII Server Discovery',
                                    'operation_id': 'getTAXII21Discovery',
                                    'sku': '',
                                    'desc': 'Returns the TAXII server title, description, and the list of API root URLs. **Required permission:** '
                                            '`ses_threat_intel_api_access` OAuth2 scope (or HTTP Basic Auth). Callers whose token lacks this scope receive a '
                                            '403 Forbidden response. **cURL example:** `curl -u <client_id>:<client_secret> -H "Content-Type: '
                                            'application/taxii+json;version=2.1" https://api.us.security.com/common/threat-intel/v1/taxii2`',
                                    'path_params': [],
                                    'query_params': [],
                                    'body': None,
                                    'body_schema': []},
                                   {'method': 'GET',
                                    'path': '/common/threat-intel/v1/taxii2/feeds/collections',
                                    'summary': 'List Collections',
                                    'operation_id': 'listTAXII21Collections',
                                    'sku': '',
                                    'desc': 'Returns the list of all available TAXII 2.1 data collections (Threat Intelligence feeds). All collections are '
                                            'read-only. This endpoint returns the complete collection list in a single response; pagination is not supported. '
                                            'The set of collections is currently fixed at three (`threat-alert`, `malicious-uri`, `malicious-file`). '
                                            '**Required permission:** `ses_threat_intel_api_access` OAuth2 scope (or HTTP Basic Auth). Callers whose token '
                                            'lacks this scope receive a 403 Forbidden response. **Python example:** `import requests; response = '
                                            'requests.get("https://api.us.security.com/common/threat-intel/v…',
                                    'path_params': [],
                                    'query_params': [],
                                    'body': None,
                                    'body_schema': []},
                                   {'method': 'GET',
                                    'path': '/common/threat-intel/v1/taxii2/feeds/collections/{collection_id}/objects',
                                    'summary': 'Get Collection Objects (STIX 2.1 Bundle)',
                                    'operation_id': 'getTAXII21Objects',
                                    'sku': '',
                                    'desc': 'Returns a STIX 2.1 bundle for the collection. **Page size:** Each response contains at most **2000 STIX '
                                            'objects**. This limit is server-enforced and fixed — there is no `limit` query parameter. Any `limit` value sent '
                                            'by the client is silently ignored. **Bulk ingestion loop:** 1. Send the first request with only `added_after` '
                                            '(omit `next`). 2. If the response contains `more: true`, send the next request with `next` set to the `next` '
                                            'value from the response body. 3. Repeat until `more: false` or `next` is absent/null in the response — that '
                                            'signals the final page. **`next` semantics:** The `next`…',
                                    'path_params': [{'name': 'collection_id',
                                                     'required': True,
                                                     'desc': 'Name of the collection to retrieve objects from. Valid values: `threat-alert` (IoC bundle '
                                                             'reports, ~1 new report/week); `malicious-uri` (high-confidence malicious URL/domain indicators, '
                                                             '~few thousand/…',
                                                     'sample': 'threat-alert'}],
                                    'query_params': [{'name': 'added_after',
                                                      'type': 'string',
                                                      'required': False,
                                                      'default': '',
                                                      'desc': 'Return only objects added after this timestamp (ISO 8601 with microsecond precision, e.g. '
                                                              '`2026-01-01T00:00:00.0000000Z`). If omitted, the server applies a rolling 30-day lookback from '
                                                              'the time of the…',
                                                      'sample': ''},
                                                     {'name': 'next',
                                                      'type': 'string',
                                                      'required': False,
                                                      'default': '',
                                                      'desc': 'Pagination cursor for the bulk ingestion loop. Omit on the first request. On subsequent '
                                                              'requests, set this to the `next` value from the previous response — a 1-based record offset '
                                                              'that advances by 200…',
                                                      'sample': ''}],
                                    'body': None,
                                    'body_schema': []}]},
 '🔗 TI: Data Related': {'doc': 'cbx_ti_data_related.md',
                        'permissions': ['Threat Intel -> Read'],
                        'endpoints': [{'method': 'GET',
                                       'path': '/common/threat-intel/v1/related/file/{file_sha256}',
                                       'summary': 'This API provides related file or network information for a given file.',
                                       'operation_id': 'listFileRelated',
                                       'sku': '',
                                       'desc': 'Returns related file and network indicators for the given file SHA-256, including arrays of related network '
                                               'indicators and related file SHA-256 values, each grouped by the relationship type (e.g. byThreatActor, '
                                               'byProcessChain). Required permission: ses_threat_intel_api_access. Callers without this permission receive a '
                                               '403 Forbidden response.',
                                       'path_params': [{'name': 'file_sha256',
                                                        'required': True,
                                                        'desc': 'SHA-256 hash of the file to look up',
                                                        'sample': 'eec3f761f7eabe9ed569f39e896be24c9bbb8861b15dbde1b3d539505cd9dd8d'}],
                                       'query_params': [{'name': 'page',
                                                         'type': 'integer',
                                                         'required': False,
                                                         'default': '1',
                                                         'desc': '1-indexed page number for paginating the related array (default: 1)',
                                                         'sample': ''},
                                                        {'name': 'page_size',
                                                         'type': 'integer',
                                                         'required': False,
                                                         'default': '50',
                                                         'desc': 'Number of related groups to return per page (default: 50, max: 200)',
                                                         'sample': ''}],
                                       'body': None,
                                       'body_schema': []},
                                      {'method': 'GET',
                                       'path': '/common/threat-intel/v1/related/network/{network}',
                                       'summary': 'This API provides related file or network information for a given network domain or IP address.',
                                       'operation_id': 'listNetworkRelated',
                                       'sku': '',
                                       'desc': 'Returns related file and network indicators for the given network domain or IP address, including related IOC '
                                               'values grouped by the relationship type (e.g. byThreatActor, bySignature). Required permission: '
                                               'ses_threat_intel_api_access. Callers without this permission receive a 403 Forbidden response.',
                                       'path_params': [{'name': 'network',
                                                        'required': True,
                                                        'desc': 'Network indicator to look up. Accepted formats: FQDN (e.g. example.com, sub.example.com), '
                                                                'full URL (scheme optional — domain is extracted and path is ignored), or public IPv4/IPv6 '
                                                                'address. IPv6 may be…',
                                                        'sample': '145.249.105.165'}],
                                       'query_params': [{'name': 'page',
                                                         'type': 'integer',
                                                         'required': False,
                                                         'default': '1',
                                                         'desc': '1-indexed page number for paginating the related array (default: 1)',
                                                         'sample': ''},
                                                        {'name': 'page_size',
                                                         'type': 'integer',
                                                         'required': False,
                                                         'default': '50',
                                                         'desc': 'Number of related groups to return per page (default: 50, max: 200)',
                                                         'sample': ''}],
                                       'body': None,
                                       'body_schema': []}]},
 '💡 TI: Insight': {'doc': 'cbx_ti_insight.md',
                   'permissions': ['Threat Intel -> Read'],
                   'endpoints': [{'method': 'GET',
                                  'path': '/common/threat-intel/v1/insight/file/{file_sha256}',
                                  'summary': 'This API returns file insight enrichments for given file sha256.',
                                  'operation_id': 'getFileInsight',
                                  'sku': '',
                                  'desc': 'Returns threat intelligence enrichments for a given file SHA-256 hash, including reputation, confidence score, '
                                          'prevalence band, targeted organisations, associated threat actors, and linked references. Required permission: '
                                          'ses_threat_intel_api_access. Callers without this permission receive a 403 Forbidden response.',
                                  'path_params': [{'name': 'file_sha256',
                                                   'required': True,
                                                   'desc': 'SHA-256 hash of the file to look up',
                                                   'sample': 'f6afa84b0847414220bb15517b8b5e2c505b64b53efbba73b753379c66ac5017'}],
                                  'query_params': [],
                                  'body': None,
                                  'body_schema': []},
                                 {'method': 'GET',
                                  'path': '/common/threat-intel/v1/insight/network',
                                  'summary': 'This API returns network enrichments for given URL, domain or IP.',
                                  'operation_id': 'getNetworkInsight',
                                  'sku': '',
                                  'desc': 'Returns threat intelligence enrichments for a given URL, domain, or IP address, including reputation, confidence '
                                          'score, prevalence, categorisation, threat risk level, targeted organisations, and associated threat actors. '
                                          'Required permission: ses_threat_intel_api_access. Callers without this permission receive a 403 Forbidden response.',
                                  'path_params': [],
                                  'query_params': [{'name': 'network',
                                                    'type': 'string',
                                                    'required': True,
                                                    'default': '',
                                                    'desc': 'Full URL, domain name, or IP address to look up. [NOTE] This value is passed as a query parameter '
                                                            "(not a path segment) because full URLs contain '/' characters that would otherwise break request "
                                                            'routi…',
                                                    'sample': '115.55.57.208'}],
                                  'body': None,
                                  'body_schema': []},
                                 {'method': 'GET',
                                  'path': '/common/threat-intel/v1/insight/network/history',
                                  'summary': 'This API returns categorization and risklevel history for given URL, domain or IP.',
                                  'operation_id': 'listNetworkInsightHistory',
                                  'sku': '',
                                  'desc': 'Returns the historical record of web content categorisation changes and threat risk level updates for a given URL, '
                                          'domain, or IP. This endpoint is not paginated: the complete history for both the categorisation and threat risk '
                                          'level arrays is returned in a single response, and the two arrays may naturally have different lengths since they '
                                          'represent independent event streams. Required permission: ses_threat_intel_api_access. Callers without this '
                                          'permission receive a 403 Forbidden response.',
                                  'path_params': [],
                                  'query_params': [{'name': 'network',
                                                    'type': 'string',
                                                    'required': True,
                                                    'default': '',
                                                    'desc': 'Full URL, domain name, or IP address to look up. [NOTE] This value is passed as a query parameter '
                                                            "(not a path segment) because full URLs contain '/' characters that would otherwise break request "
                                                            'routi…',
                                                    'sample': 'google.com'}],
                                  'body': None,
                                  'body_schema': []}]},
 '🧬 TI: Process Chain': {'doc': 'cbx_ti_process_chain.md',
                         'permissions': ['Threat Intel -> Read'],
                         'endpoints': [{'method': 'GET',
                                        'path': '/common/threat-intel/v1/process-chain/file/{file_sha256}',
                                        'summary': 'This API returns topK process lineage enrichment for the provided file sha256.',
                                        'operation_id': 'listFileProcessChain',
                                        'sku': '',
                                        'desc': 'Returns the top-K process lineage (parent–child process chain) enrichment for the given file SHA-256, showing '
                                                'how the file is typically executed and which parent processes are associated with it. Required permission: '
                                                'ses_threat_intel_api_access. Callers without this permission receive a 403 Forbidden response. To retrieve '
                                                'all results: check `total_pages` in the response body and repeat the request incrementing `page` by 1 on each '
                                                'call until `page` equals `total_pages`. Each page returns up to `page_size` entries (default 10, max 100).',
                                        'path_params': [{'name': 'file_sha256',
                                                         'required': True,
                                                         'desc': 'SHA-256 hash of the file to look up',
                                                         'sample': 'eec3f761f7eabe9ed569f39e896be24c9bbb8861b15dbde1b3d539505cd9dd8d'}],
                                        'query_params': [{'name': 'page_size',
                                                          'type': 'integer',
                                                          'required': False,
                                                          'default': '10',
                                                          'desc': 'The number of top-K process chain entries to return in a given request. [NOTE] When this '
                                                                  'field is not present, up to 10 entries are returned. The maximum number of entries '
                                                                  'supported per request is 100…',
                                                          'sample': ''},
                                                         {'name': 'page',
                                                          'type': 'integer',
                                                          'required': False,
                                                          'default': '1',
                                                          'desc': 'The page number to retrieve (1-indexed). [NOTE] When this field is not present, the first '
                                                                  'page is returned.',
                                                          'sample': ''}],
                                        'body': None,
                                        'body_schema': []}]},
 '🛡️ TI: Protected': {'doc': 'cbx_ti_protected.md',
                      'permissions': ['Threat Intel -> Read'],
                      'endpoints': [{'method': 'GET',
                                     'path': '/common/threat-intel/v1/protection/file/{file_sha256}',
                                     'summary': 'This API returns information whether a given file has been blocked by any Symantec technologies.',
                                     'operation_id': 'getFileProtection',
                                     'sku': '',
                                     'desc': 'Returns information about whether the given file (identified by SHA-256) has been blocked by any Symantec '
                                             'security technology, including the technology name, the first definition set version that blocked it, and the '
                                             'associated threat name. Required permission: ses_threat_intel_api_access. Callers without this permission '
                                             'receive a 403 Forbidden response.',
                                     'path_params': [{'name': 'file_sha256',
                                                      'required': True,
                                                      'desc': 'SHA-256 hash of the file to look up',
                                                      'sample': '9f660524a026bce8d83f9f701ac5aac3f645cd3d03ddd356c8217e424b52a7af'}],
                                     'query_params': [],
                                     'body': None,
                                     'body_schema': []},
                                    {'method': 'GET',
                                     'path': '/common/threat-intel/v1/protection/network/{network}',
                                     'summary': 'This API returns information whether given domain has been blocked by any Symantec technologies.',
                                     'operation_id': 'getNetworkProtection',
                                     'sku': '',
                                     'desc': 'Returns information about whether the given network domain has been blocked by any Symantec security technology, '
                                             'including the technology name, the first definition set version that blocked it, and the associated threat name. '
                                             'Required permission: ses_threat_intel_api_access. Callers without this permission receive a 403 Forbidden '
                                             'response.',
                                     'path_params': [{'name': 'network', 'required': True, 'desc': 'Domain name to look up', 'sample': 'paste.ee'}],
                                     'query_params': [],
                                     'body': None,
                                     'body_schema': []},
                                    {'method': 'GET',
                                     'path': '/common/threat-intel/v1/protection/cve/{cve}',
                                     'summary': 'This API returns information whether a given CVE has been blocked by any Symantec technologies.',
                                     'operation_id': 'getCveProtection',
                                     'sku': '',
                                     'desc': 'Returns information about whether the given CVE vulnerability has been blocked by any Symantec security '
                                             'technology, including the technology name, the first definition set version that blocked it, and the associated '
                                             'threat name. Required permission: ses_threat_intel_api_access. Callers without this permission receive a 403 '
                                             'Forbidden response.',
                                     'path_params': [{'name': 'cve',
                                                      'required': True,
                                                      'desc': 'CVE identifier (e.g. CVE-2017-0038)',
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
            st.markdown("**Request Body Schema:**")
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
            comma_default = any("comma-separated" in q["desc"] for q in qps if q["type"] == "array")
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
                       'endpoints': [['POST', '/detect-respond/detection/v1/custom-detections/queries/_search', 'Search query sub-resources'],
                                     ['POST', '/detect-respond/detection/v1/custom-detections/{detection_id}/queries', 'Create a query sub-resource'],
                                     ['GET', '/detect-respond/detection/v1/custom-detections/{detection_id}/queries/{query_id}', 'Get a query sub-resource'],
                                     ['PUT', '/detect-respond/detection/v1/custom-detections/{detection_id}/queries/{query_id}', 'Update a query sub-resource'],
                                     ['DELETE',
                                      '/detect-respond/detection/v1/custom-detections/{detection_id}/queries/{query_id}',
                                      'Delete a query sub-resource'],
                                     ['POST', '/detect-respond/detection/v1/custom-detections/_search', 'Search custom detections'],
                                     ['POST', '/detect-respond/detection/v1/custom-detections', 'Create a custom detection'],
                                     ['POST',
                                      '/detect-respond/detection/v1/custom-detections/_import',
                                      'Bulk import (create or append) custom detections with their queries'],
                                     ['GET', '/detect-respond/detection/v1/custom-detections/{detection_id}', 'Get a custom detection'],
                                     ['PUT', '/detect-respond/detection/v1/custom-detections/{detection_id}', 'Update a custom detection'],
                                     ['DELETE', '/detect-respond/detection/v1/custom-detections/{detection_id}', 'Delete a custom detection'],
                                     ['POST',
                                      '/detect-respond/detection/v1/custom-detections/_bulk',
                                      'Unified bulk operation on detections (DELETE or UPDATE)'],
                                     ['POST',
                                      '/detect-respond/detection/v1/custom-detections/{detection_id}/queries/_bulk',
                                      'Unified bulk operation on queries (DELETE or MOVE)']]},
 'Device Query': {'doc': 'cbx_device_query.md',
                  'endpoints': [['GET', '/detect-respond/device-query/v2/commands', 'List Device Query Commands.'],
                                ['POST', '/detect-respond/device-query/v2/commands', 'Trigger a Device Query Command (Forensic or Artifact).'],
                                ['GET', '/detect-respond/device-query/v2/commands/{commandId}', 'Get Device Query Command details by Id.'],
                                ['DELETE', '/detect-respond/device-query/v2/commands/{commandId}', 'Delete Device Query Command by Id.'],
                                ['PUT', '/detect-respond/device-query/v2/commands/{commandId}/cancel', 'Cancel a triggered Device Query Command.'],
                                ['POST', '/detect-respond/device-query/v2/commands/{commandId}/results', 'Retrieve Device Query Results'],
                                ['GET', '/detect-respond/device-query/v2/schedules', 'List Device Query Schedules with pagination and sorting.'],
                                ['POST', '/detect-respond/device-query/v2/schedules', 'Create a new Device Query Schedule.'],
                                ['DELETE', '/detect-respond/device-query/v2/schedules', 'Delete Device Query Schedules (Batch).'],
                                ['GET', '/detect-respond/device-query/v2/schedules/{scheduleId}', 'Get details of a specific Device Query Schedule.'],
                                ['PUT', '/detect-respond/device-query/v2/schedules/{scheduleId}', 'Update an existing Device Query Schedule.'],
                                ['GET',
                                 '/detect-respond/device-query/v2/schedules/{scheduleId}/commands',
                                 'List Device Query Commands for given schedule id with pagination and sorting.'],
                                ['PUT', '/detect-respond/device-query/v2/schedules/{scheduleId}/stop', 'Stop a running Device Query Schedule.']]},
 'Alerts & Threats': {'doc': 'cbx_alerts.md',
                      'endpoints': [['GET', '/detect-respond/alerts/v8/threats/{threat_id}/notes', 'Get notes for a threat'],
                                    ['POST', '/detect-respond/alerts/v8/threats/{threat_id}/notes', 'Create a threat-level note'],
                                    ['DELETE', '/detect-respond/alerts/v8/threats/{threat_id}/notes/{id}', 'Delete a threat-level note'],
                                    ['POST', '/detect-respond/alerts/v8/grouped_alerts/_facet', 'Facet alerts - grouped'],
                                    ['POST',
                                     '/detect-respond/alerts/v8/grouped_alerts/_histogram',
                                     'Get time-bucketed threat-group counts for charting and dashboards.'],
                                    ['POST',
                                     '/detect-respond/alerts/v8/grouped_alerts/_search',
                                     'Search for Alerts using query, criteria and exclusion operators. Alerts are grouped by the requested group_by field. '
                                     'Currently, only threat_id is available for grouping. The response schema varies by grouping field.'],
                                    ['GET', '/detect-respond/alerts/v8/threats/{threat_id}/history', 'Get the actions taken on a Threat such as Notes added.'],
                                    ['POST',
                                     '/detect-respond/alerts/v8/alerts/workflow',
                                     'This is an async operation that updates all existing alerts that match the search criteria of the request.'],
                                    ['POST',
                                     '/detect-respond/alerts/v8/alerts/threat/workflow/_criteria',
                                     "Bulk update threats' workflow by ids, this is an async operation"],
                                    ['GET', '/detect-respond/alerts/v8/alerts/{alert_id}/notes', 'Get notes for an alert'],
                                    ['POST', '/detect-respond/alerts/v8/alerts/{alert_id}/notes', 'Create an alert-level note'],
                                    ['PATCH', '/detect-respond/alerts/v8/alerts/{alert_id}/notes', 'Patch route to update the read_history of a customer note'],
                                    ['PUT', '/detect-respond/alerts/v8/alerts/{alert_id}/notes/{id}', 'Update alert level customer note'],
                                    ['DELETE', '/detect-respond/alerts/v8/alerts/{alert_id}/notes/{id}', 'Delete an alert-level note'],
                                    ['GET', '/detect-respond/alerts/v8/threats/{threat_id}/tags', 'Get a list of tags based on threatId'],
                                    ['POST', '/detect-respond/alerts/v8/threats/{threat_id}/tags', 'Add tags to the threat id'],
                                    ['DELETE',
                                     '/detect-respond/alerts/v8/threats/{threat_id}/tags/{tag}',
                                     'Delete a tag so it is no longer associated with the given threat ID'],
                                    ['POST',
                                     '/detect-respond/alerts/v8/alerts/_export',
                                     'Export Alerts in csv format. This is an asynchronous request which enables up to 25,000 records to be exported in each '
                                     'request. Use the Export Alerts endpoint defined here to create a job with required search criteria to…'],
                                    ['POST', '/detect-respond/alerts/v8/alerts/_facet', 'Facet alerts - ungrouped'],
                                    ['POST', '/detect-respond/alerts/v8/alerts/_histogram', 'Get time-bucketed alert counts for charting and dashboards.'],
                                    ['POST', '/detect-respond/alerts/v8/alerts/_search', 'Search for alerts using query, criteria and exclusion operators.'],
                                    ['POST',
                                     '/detect-respond/alerts/v8/alerts/_validate',
                                     'Verifies that the search is valid and returns error messages if not.'],
                                    ['GET', '/detect-respond/alerts/v8/alerts/search_suggestions', 'Get recommendations of fields to use in a search.'],
                                    ['GET', '/detect-respond/alerts/v8/alerts/{alert_id}', 'Get the details of an alert by ID'],
                                    ['GET',
                                     '/detect-respond/alerts/v8/alerts/{alert_id}/history',
                                     'Get the actions taken on an Alert such as Notes added and workflow state changes. The history route does not include the '
                                     'current state details of the alert.']]},
 'Jobs & Export': {'doc': 'cbx_jobs.md',
                   'endpoints': [['GET', '/detect-respond/jobs/v4/jobs/{job_id}/download', 'Download job output'],
                                 ['GET', '/detect-respond/jobs/v4/jobs/{job_id}', 'Get the details of a specific job'],
                                 ['POST', '/detect-respond/jobs/v4/event_export', 'Start event export job']]},
 'Live Response': {'doc': 'cbx_live_response.md',
                   'endpoints': [['GET', '/detect-respond/live-response/v7/sessions', 'Get all live response sessions'],
                                 ['POST', '/detect-respond/live-response/v7/sessions', 'Create a Live Response session'],
                                 ['GET', '/detect-respond/live-response/v7/sessions/{session_id}', 'Retrieve a Live Response session'],
                                 ['DELETE', '/detect-respond/live-response/v7/sessions/{session_id}', 'Close a Live Response session'],
                                 ['GET', '/detect-respond/live-response/v7/sessions/{session_id}/files', 'Get all files for a session'],
                                 ['POST', '/detect-respond/live-response/v7/sessions/{session_id}/files', 'Upload a file to a session'],
                                 ['GET', '/detect-respond/live-response/v7/sessions/{session_id}/files/{file_id}', 'Get a file object by ID'],
                                 ['DELETE', '/detect-respond/live-response/v7/sessions/{session_id}/files/{file_id}', 'Delete a file from a session'],
                                 ['GET', '/detect-respond/live-response/v7/sessions/{session_id}/files/{file_id}/content', 'Download file content'],
                                 ['GET', '/detect-respond/live-response/v7/sessions/{session_id}/commands', 'Get all commands for a session'],
                                 ['POST', '/detect-respond/live-response/v7/sessions/{session_id}/commands', 'Queue a Live Response command'],
                                 ['GET',
                                  '/detect-respond/live-response/v7/sessions/{session_id}/commands/{command_id}',
                                  'Retrieve a Live Response command by ID'],
                                 ['DELETE', '/detect-respond/live-response/v7/sessions/{session_id}/commands/{command_id}', 'Cancel a Live Response command']]},
 'Notifications': {'doc': 'cbx_notifications.md',
                   'endpoints': [['GET', '/detect-respond/notifications/v2/rules', 'Fetch notification rules'],
                                 ['POST', '/detect-respond/notifications/v2/rules', 'Create notification rule'],
                                 ['PUT', '/detect-respond/notifications/v2/rules/{ruleId}', 'Update the details of a rule by ID'],
                                 ['DELETE', '/detect-respond/notifications/v2/rules/{ruleId}', 'Delete rule by ID'],
                                 ['POST', '/detect-respond/notifications/v2/history/_search', 'Fetch notification history for a specific rule']]},
 'Policy Management': {'doc': 'cbx_policy_management.md',
                       'endpoints': [['POST',
                                      '/common/policy-management/v2/policies/copy',
                                      'This API lets you copy workspace policies to another environment.'],
                                     ['GET', '/common/policy-management/v2/policies', 'This API lets you retrieve a list of your policies.'],
                                     ['PUT', '/common/policy-management/v2/policies', 'This API lets you update policy configurations.'],
                                     ['POST', '/common/policy-management/v2/policies', 'This API lets you create a policy.'],
                                     ['DELETE', '/common/policy-management/v2/policies/{policy-id}', 'This API lets you delete a policy.'],
                                     ['GET',
                                      '/common/policy-management/v2/policies/{policy-id}/versions/{policy-version}',
                                      'This API lets you retrieve the details for a policy by id and version.'],
                                     ['GET',
                                      '/common/policy-management/v2/policies/{policy-id}/versions',
                                      'This API lets you retrieve the versions of a policy.'],
                                     ['PATCH',
                                      '/common/policy-management/v2/policies/allow-list/{policy-id}/versions/{policy-version}',
                                      'This API lets you perform a partial update of the Allow list policy.'],
                                     ['PUT',
                                      '/common/policy-management/v2/policies/allow-list/{policy-id}/versions/{policy-version}',
                                      'This API lets you perform update of Allow list policy.'],
                                     ['PATCH',
                                      '/common/policy-management/v2/policies/deny-list/{policy-id}/versions/{policy-version}',
                                      'This API lets you perform partial update of Deny list policy.'],
                                     ['PUT',
                                      '/common/policy-management/v2/policies/deny-list/{policy-id}/versions/{policy-version}',
                                      'This API lets you perform update of Deny list policy.'],
                                     ['GET',
                                      '/common/policy-management/v2/policies/device-groups/{group-id}/policies',
                                      'This API lets you retrieve a list of policies assigned to the device group.'],
                                     ['POST',
                                      '/common/policy-management/v2/policies/{policy-id}/versions/{policy-version}/device-groups',
                                      'This API lets you apply a policy to device groups.'],
                                     ['DELETE',
                                      '/common/policy-management/v2/policies/{policy-id}/versions/{policy-version}/device-groups',
                                      'This API lets you remove a policy from device groups.'],
                                     ['GET',
                                      '/common/policy-management/v2/policies/export/{export-id}/status',
                                      'This API lets you check the status of a policy export operation.'],
                                     ['POST', '/common/policy-management/v2/policies/export/all', 'This API lets you export all policies.'],
                                     ['POST',
                                      '/common/policy-management/v2/policies/export/types',
                                      'This API lets you export policies filtered by policy types.'],
                                     ['POST',
                                      '/common/policy-management/v2/policies/export/names',
                                      'This API lets you export policies filtered by policy names.'],
                                     ['POST', '/common/policy-management/v2/policies/import', 'This API lets you import policies from a file.'],
                                     ['GET',
                                      '/common/policy-management/v2/policies/import/{import-id}/status',
                                      'This API lets you check the status of a policy import operation.'],
                                     ['POST', '/common/policy-management/v2/policies/target-rules/export/all', 'This API lets you export all target rules.'],
                                     ['POST',
                                      '/common/policy-management/v2/policies/target-rules/export/names',
                                      'This API lets you export target rules by names.'],
                                     ['GET',
                                      '/common/policy-management/v2/policies/target-rules/export/{export-id}/status',
                                      'This API lets you check the status of a target rule export operation.'],
                                     ['POST',
                                      '/common/policy-management/v2/policies/target-rules/import',
                                      'This API lets you import target rules from a file.'],
                                     ['GET',
                                      '/common/policy-management/v2/policies/target-rules/import/{import-id}/status',
                                      'This API lets you check the status of a target rule import operation.'],
                                     ['GET', '/common/policy-management/v2/policies/target-rules', 'This API lets you retrieve a list of target rules.']]},
 'Script Deobfuscation': {'doc': 'cbx_script_deob.md',
                          'endpoints': [['POST', '/detect-respond/script-deobfuscation/v3/reveal', 'Deobfuscate an obfuscated PowerShell script']]},
 'Threat Intel': {'doc': 'cbx_taxii11.md',
                  'endpoints': [['POST', '/common/threat-intel/v1/taxii11/discovery', 'TAXII Discovery'],
                                ['POST', '/common/threat-intel/v1/taxii11/collection-management', 'TAXII Collection Management'],
                                ['POST', '/common/threat-intel/v1/taxii11/poll', 'TAXII Poll – retrieve STIX CTI feed']]},
 'Vulnerability Assessment': {'doc': 'cbx_vuln_assessment.md',
                              'endpoints': [['GET',
                                             '/endpoint-security/vulnerability/assessment/v3/vulnerabilities/summary',
                                             'Get organization vulnerability summary rollup'],
                                            ['POST',
                                             '/endpoint-security/vulnerability/assessment/v3/devices/vulnerabilities/summary/_search',
                                             'Search vulnerable devices for organization'],
                                            ['POST',
                                             '/endpoint-security/vulnerability/assessment/v3/devices/vulnerabilities/summary/_facets',
                                             'Get filter facets for vulnerable devices'],
                                            ['POST',
                                             '/endpoint-security/vulnerability/assessment/v3/devices/vulnerabilities/summary/export',
                                             'Export vulnerable devices list as CSV'],
                                            ['POST',
                                             '/endpoint-security/vulnerability/assessment/v3/devices/vulnerabilities/_search',
                                             'Search vulnerabilities across organization'],
                                            ['POST',
                                             '/endpoint-security/vulnerability/assessment/v3/devices/vulnerabilities/_facets',
                                             'Get filter facets for vulnerabilities'],
                                            ['POST',
                                             '/endpoint-security/vulnerability/assessment/v3/devices/vulnerabilities/export',
                                             'Export vulnerabilities list as CSV'],
                                            ['GET', '/endpoint-security/vulnerability/assessment/v3/vulnerabilities/{cve_id}', 'Get vulnerability details'],
                                            ['GET',
                                             '/endpoint-security/vulnerability/assessment/v3/vulnerabilities/{cve_id}/summary',
                                             'Get CVE flyout summary'],
                                            ['POST',
                                             '/endpoint-security/vulnerability/assessment/v3/vulnerabilities/{cve_id}/devices',
                                             'Search devices affected by specific CVE'],
                                            ['POST',
                                             '/endpoint-security/vulnerability/assessment/v3/vulnerabilities/{cve_id}/software/_search',
                                             'List vulnerable software configurations for a specific CVE'],
                                            ['POST',
                                             '/endpoint-security/vulnerability/assessment/v3/vulnerabilities/{cve_id}/actions',
                                             'Perform action on vulnerability'],
                                            ['GET',
                                             '/endpoint-security/vulnerability/assessment/v3/devices/{device_uid}/vulnerabilities/summary',
                                             'Get vulnerability summary for device'],
                                            ['POST',
                                             '/endpoint-security/vulnerability/assessment/v3/devices/{device_uid}/vulnerabilities/_search',
                                             'Search vulnerabilities on device'],
                                            ['POST',
                                             '/endpoint-security/vulnerability/assessment/v3/devices/{device_uid}/vulnerabilities/export',
                                             'Export device vulnerabilities list as CSV'],
                                            ['POST',
                                             '/endpoint-security/vulnerability/assessment/v3/devices/{device_uid}/device-actions',
                                             'Perform action on device']]}}

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

api_token = st.sidebar.text_input(
    "OAuth Bearer / Basic Token",
    value=DEFAULT_TOKEN,
    type="password"
)

client_cred = st.sidebar.text_input(
    "OAuth Client Credentials（Basic / Base64）※トークン取得・TAXII用",
    value="",
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

    col_in1, col_in2 = st.columns([1, 1])

    with col_in1:
        if "Authentication" in module_choice:
            op = st.selectbox("Endpoint", ["POST /common/v1/oauth2/tokens"])
            t_method, t_endpoint = op.split(" ", 1)
            grant_type = st.text_input("grant_type", value="client_credentials")
            scope = st.text_input("scope", value="domain")
            t_data = {"grant_type": grant_type, "scope": scope}
            # cbx_auth.md: Basic 認証（Client Credentials）+ application/x-www-form-urlencoded
            t_auth = "Basic"
            t_ctype = "application/x-www-form-urlencoded"
            st.caption("認証: サイドバーの『OAuth Client Credentials (Basic)』を使用し、フォーム形式で送信します。")

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
            st.caption("認証: サイドバーの『OAuth Client Credentials (Basic)』（client_id:client_secret の Base64）を使用します。")
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
                                 help="Bearer: サイドバーのトークン / Basic: サイドバーの Client Credentials")
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
        _cred = client_cred.strip()
        if not _cred:
            st.warning("サイドバーの『OAuth Client Credentials (Basic)』が未入力です。")
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
