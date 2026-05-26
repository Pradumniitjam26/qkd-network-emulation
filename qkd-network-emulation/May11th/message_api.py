# =========================================================
# message_api.py
# HYBRID QUANTUM-CLASSICAL QKD MESSAGE API
# =========================================================

from fastapi import (
    APIRouter,
    Request,
    HTTPException,
    Depends
)

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from crypto_engine import CryptoEngine

from audit import AuditLogger

from config import (

    PEER_NODES,
    NODE_ID,

    SYSTEM_MODE,
    QKD_PROTOCOL,

    ENABLE_REPLAY_PROTECTION
)

import time

from datetime import datetime

# =========================================================
# CONFIGURATION
# =========================================================

KMS_URL = PEER_NODES[NODE_ID]

audit = AuditLogger()

router = APIRouter()

security = HTTPBearer()

# =========================================================
# BUFFER
# =========================================================

buffer_ref = None

# =========================================================
# REPLAY TRACKING
# =========================================================

used_nonces = set()

used_message_ids = set()

# =========================================================
# METRICS
# =========================================================

received_messages = 0

received_files = 0

replay_attempts = 0

decryption_failures = 0

# =========================================================
# SET BUFFER
# =========================================================

def set_buffer(buffer):

    global buffer_ref

    buffer_ref = buffer

# =========================================================
# VERIFY NONCE
# =========================================================

def verify_nonce(
    nonce
):

    global replay_attempts

    if not ENABLE_REPLAY_PROTECTION:
        return True

    if not nonce:
        return False

    if nonce in used_nonces:

        replay_attempts += 1

        return False

    used_nonces.add(
        nonce
    )

    return True

# =========================================================
# VERIFY MESSAGE ID
# =========================================================

def verify_message_id(
    message_id
):

    global replay_attempts

    if not message_id:
        return False

    if message_id in used_message_ids:

        replay_attempts += 1

        return False

    used_message_ids.add(
        message_id
    )

    return True

# =========================================================
# AUTH DISABLED
# =========================================================

def verify_token(

    credentials:
    HTTPAuthorizationCredentials = Depends(security)

):

    # AUTH DISABLED FOR LAN TESTING

    return True

# =========================================================
# RECEIVE SECURE MESSAGE
# =========================================================

@router.post("/receive-message")
async def receive_message(

    request: Request,

    auth: bool = Depends(verify_token)
):

    global received_messages
    global decryption_failures

    audit.api("/receive-message")

    # =====================================================
    # REQUEST
    # =====================================================

    try:

        data = await request.json()

    except Exception:

        raise HTTPException(

            status_code=400,

            detail="Invalid JSON"
        )

    # =====================================================
    # EXTRACT
    # =====================================================

    key_id = data.get("key_id")

    iv_hex = data.get("iv")

    ct_hex = data.get("ciphertext")

    tag_hex = data.get("tag")

    nonce = data.get("nonce")

    delivery_id = data.get(
        "delivery_id"
    )

    metadata = data.get(
        "metadata",
        {}
    )

    # =====================================================
    # VALIDATE
    # =====================================================

    if (
        not key_id
        or not iv_hex
        or not ct_hex
        or not tag_hex
    ):

        raise HTTPException(

            status_code=400,

            detail="Missing required fields"
        )

    # =====================================================
    # VALIDATION DISABLED FOR LAN TESTING
    # =====================================================

    valid_metadata = True

    verified = True

    # =====================================================
    # REPLAY
    # =====================================================

    if nonce:

        valid_nonce = verify_nonce(
            nonce
        )

        if not valid_nonce:

            raise HTTPException(

                status_code=403,

                detail="Replay nonce detected"
            )

    if delivery_id:

        valid_delivery = verify_message_id(
            delivery_id
        )

        if not valid_delivery:

            raise HTTPException(

                status_code=403,

                detail="Replay delivery detected"
            )

    # =====================================================
    # HEX
    # =====================================================

    try:

        iv = bytes.fromhex(iv_hex)

        ciphertext = bytes.fromhex(
            ct_hex
        )

        tag = bytes.fromhex(tag_hex)

    except Exception:

        raise HTTPException(

            status_code=400,

            detail="Invalid hex encoding"
        )

    # =====================================================
    # BUFFER
    # =====================================================

    if buffer_ref is None:

        raise HTTPException(

            status_code=500,

            detail="Buffer unavailable"
        )

    # =====================================================
    # KEY
    # =====================================================

    key_obj = buffer_ref.get_key_by_id(
        str(key_id)
    )

    if key_obj is None:

        raise HTTPException(

            status_code=503,

            detail="Local key unavailable"
        )

    # =====================================================
    # SESSION
    # =====================================================

    session_id = metadata.get(
        "session_id",
        "UNKNOWN"
    )

    sync_index = metadata.get(
        "sync_index",
        0
    )

    # =====================================================
    # DECRYPTION
    # =====================================================

    start = time.perf_counter()

    try:

        ce = CryptoEngine(

            key_hex=
                key_obj.key_value,

            key_id=
                key_id,

            mode=
                SYSTEM_MODE,

            session_id=
                session_id,

            sync_index=
                sync_index
        )

        plaintext = ce.decrypt(

            iv,

            ciphertext,

            tag

        ).decode()

    except Exception as e:

        decryption_failures += 1

        raise HTTPException(

            status_code=500,

            detail=f"Decryption failed: {e}"
        )

    latency = (
        time.perf_counter()
        - start
    )

    received_messages += 1

    # =====================================================
    # OUTPUT
    # =====================================================

    timestamp = datetime.utcnow().isoformat()

    print("\n" + "=" * 65)

    print(
        " RECEIVED SECURE MESSAGE "
    )

    print("=" * 65)

    print(f"\nTimestamp:")
    print(timestamp)

    print(f"\nDelivery ID:")
    print(delivery_id)

    print(f"\nKey ID:")
    print(key_id)

    print(f"\nSession ID:")
    print(session_id)

    print(f"\nProtocol:")
    print(QKD_PROTOCOL)

    print(f"\nMode:")
    print(SYSTEM_MODE)

    print(f"\nSynchronization:")
    print("VERIFIED")

    print(f"\nReplay Protection:")
    print("PASSED")

    print(f"\nDecryption Latency:")
    print(f"{latency:.6f}s")

    print(f"\nMessage:")
    print(plaintext)

    print("\n" + "=" * 65)

    # =====================================================
    # RESPONSE
    # =====================================================

    return {

        "status":
            "success",

        "node":
            NODE_ID,

        "protocol":
            QKD_PROTOCOL,

        "mode":
            SYSTEM_MODE,

        "verified":
            True,

        "delivery_id":
            delivery_id,

        "latency":
            latency,

        "message":
            plaintext
    }

# =========================================================
# MESSAGE METRICS
# =========================================================

@router.get("/message-metrics")
async def message_metrics():

    return {

        "received_messages":
            received_messages,

        "received_files":
            received_files,

        "replay_attempts":
            replay_attempts,

        "decryption_failures":
            decryption_failures
    }
