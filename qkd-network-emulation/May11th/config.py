# config.py
# HYBRID QUANTUM-CLASSICAL QKD ARCHITECTURE CONFIGURATION

import os


# =========================================================
# NODE CONFIGURATION
# =========================================================

"""
IITR -> Server-side QKD node
IITJ -> Client-side QKD node
"""

NODE_ID = os.getenv(
    "NODE_ID",
    "IITR"
)

NODE_ROLE = os.getenv(
    "NODE_ROLE",
    "SERVER"
)


# =========================================================
# SYSTEM MODE
# =========================================================

SYSTEM_MODE = "ETSI"

SYNC_ENABLED = True


# =========================================================
# QUANTUM LAYER
# =========================================================

QUANTUM_LAYER_ENABLED = True

QKD_PROTOCOL = "BB84"

SIMULAQRON_ENABLED = True

ENABLE_RUNTIME_KEY_REGENERATION = True

KEY_REGENERATION_INTERVAL = 30


# =========================================================
# QUANTUM CHANNEL
# =========================================================

QUANTUM_CHANNEL_TYPE = "SIMULAQRON"

SIMULAQRON_ALICE_IP = "10.11.80.93"

SIMULAQRON_BOB_IP = "10.11.80.94"

# WORKING PORTS
SIMULAQRON_ALICE_PORT = 8001

SIMULAQRON_BOB_PORT = 8004


# =========================================================
# BB84 CONFIGURATION
# =========================================================

BB84_NUM_QUBITS = 10

BB84_BASIS_VALUES = [0, 1]

MAX_QBER_THRESHOLD = 0.11


# =========================================================
# SYNCHRONIZATION
# =========================================================

SYNC_SEED = "QKD_SHARED_SEED_2026"

ENABLE_SHA256_SYNC = True

ENABLE_METADATA_SYNC = False

METADATA_SYNC_ONLY = False


# =========================================================
# SESSION CONFIGURATION
# =========================================================

ENABLE_SESSION_IDS = True

SESSION_TIMEOUT_SECONDS = 300


# =========================================================
# DEPLOYMENT
# =========================================================

DEPLOYMENT_MODE = "REMOTE"


# =========================================================
# PUBLIC CLASSICAL CHANNEL
# =========================================================

IITR_BASE_URL = "http://10.11.80.93:8000"

IITJ_BASE_URL = "http://10.11.80.94:8001"


# =========================================================
# SERVER CONFIGURATION
# =========================================================

HOST = "0.0.0.0"

if NODE_ID == "IITR":

    PORT = 8000
    EXPECTED_ROLE = "SERVER"

else:

    PORT = 8001
    EXPECTED_ROLE = "CLIENT"


# =========================================================
# VALIDATION
# =========================================================

if NODE_ROLE != EXPECTED_ROLE:

    raise ValueError(
        f"Invalid NODE_ROLE for {NODE_ID}. "
        f"Expected {EXPECTED_ROLE}, "
        f"got {NODE_ROLE}"
    )


# =========================================================
# PEER CONFIGURATION
# =========================================================

PEER_NODES = {

    "IITR": IITR_BASE_URL,

    "IITJ": IITJ_BASE_URL
}


def get_peer_url():

    if NODE_ID == "IITR":
        return PEER_NODES["IITJ"]

    return PEER_NODES["IITR"]


# =========================================================
# KEY CONFIGURATION
# =========================================================

KEY_SIZE = 256

DEFAULT_TTL_SECONDS = 300

INITIAL_KEY_POOL_SIZE = 20

MAX_BUFFER_SIZE = 1000

MAX_BYTES_PER_KEY = 32


# =========================================================
# KEY ROTATION
# =========================================================

ENABLE_KEY_ROTATION = True

KEY_ROTATION_INTERVAL = 60


# =========================================================
# AUTH CONFIGURATION
# =========================================================

AUTH_ENABLED = False

AUTH_TOKEN = (
    "ETSI_DEMO_SECURE_TOKEN_2026"
)

NODE_SHARED_SECRET = (
    "INTERKMS_SHARED_SECRET_2026"
)


# =========================================================
# INTER-KMS
# =========================================================

INTERKMS_TIMEOUT_SECONDS = 5

INTERKMS_MAX_RETRIES = 3

INTERKMS_SYNC_INTERVAL = 10


# =========================================================
# METADATA SYNCHRONIZATION
# =========================================================

ENABLE_METADATA_SYNC = False

SYNC_METADATA_FIELDS = [

    "key_id",

    "session_id",

    "sync_index",

    "key_hash",

    "timestamp"
]


# =========================================================
# HASHING
# =========================================================

HASH_ALGORITHM = "SHA-256"


# =========================================================
# CRYPTOGRAPHY
# =========================================================

ENCRYPTION_ALGORITHM = "AES-256-GCM"

AES_BLOCK_SIZE = 16


# =========================================================
# OBSERVABILITY
# =========================================================

ENABLE_DEBUG_LOGS = True

ENABLE_QKD_LOGS = True

ENABLE_SYNC_LOGS = True


# =========================================================
# DASHBOARD
# =========================================================

ENABLE_STREAMLIT_DASHBOARD = True

DASHBOARD_PORT = 8501


# =========================================================
# REVERSE PROXY
# =========================================================

ENABLE_CADDY_PROXY = False

REVERSE_PROXY_PORT = 443


# =========================================================
# NGROK
# =========================================================

ENABLE_NGROK = False


# =========================================================
# SECURITY
# =========================================================

ENABLE_QBER_MONITORING = True

ENABLE_INTRUSION_ALERTS = True


# =========================================================
# STRESS TEST
# =========================================================

ENABLE_STRESS_TEST = False

STRESS_REQUEST_RATE = 50


# =========================================================
# RESEARCH FLAGS
# =========================================================

ENABLE_SDN_ROUTING = False

ENABLE_MULTI_NODE_QKD = False

ENABLE_TELEPORTATION = True
# =========================================================
# REPLAY PROTECTION
# =========================================================

ENABLE_REPLAY_PROTECTION = True

REPLAY_WINDOW_SECONDS = 60


# =========================================================
# MESSAGE SECURITY
# =========================================================

ENABLE_MESSAGE_AUTH = True

ENABLE_MESSAGE_ENCRYPTION = True


# =========================================================
# FILE TRANSFER
# =========================================================

ENABLE_FILE_TRANSFER = True

MAX_FILE_SIZE_MB = 100


# =========================================================
# API SECURITY
# =========================================================

ENABLE_API_TOKEN_AUTH = False


# =========================================================
# PERFORMANCE
# =========================================================

ENABLE_PERFORMANCE_METRICS = True


# =========================================================
# STORAGE
# =========================================================

ENABLE_PERSISTENT_STORAGE = False
# =========================================================
# SYNC CONFIGURATION
# =========================================================

MAX_SYNC_DRIFT = 5

SYNC_RETRY_LIMIT = 3

SYNC_TIMEOUT_SECONDS = 10

ENABLE_AUTO_RESYNC = True

ENABLE_CLOCK_SYNC = True
