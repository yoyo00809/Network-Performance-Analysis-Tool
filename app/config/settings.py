# ==========================================
# Network Performance Analysis Tool (NPAT)
# Application Configuration
# ==========================================


# Application Information
APP_NAME = "Network Performance Analysis Tool"
APP_SHORT_NAME = "NPAT"
APP_VERSION = "1.0.0"


# ------------------------------------------
# Ping Configuration
# ------------------------------------------

# Default number of ping requests
DEFAULT_PING_COUNT = 4

# Maximum time allowed for a ping operation
PING_TIMEOUT = 30


# ------------------------------------------
# Network Performance Thresholds
# ------------------------------------------

# Latency thresholds (milliseconds)
LATENCY_GOOD = 50
LATENCY_AVERAGE = 100


# Jitter thresholds (milliseconds)
JITTER_GOOD = 20
JITTER_AVERAGE = 50


# Packet loss thresholds (percentage)
PACKET_LOSS_GOOD = 1
PACKET_LOSS_AVERAGE = 5


# ------------------------------------------
# Database Configuration
# ------------------------------------------

DATABASE_NAME = "npat.db"