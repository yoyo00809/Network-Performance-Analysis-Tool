# ==========================================
# Network Performance Analysis Tool (NPAT)
# Network Failure & Recovery Detection
# ==========================================

from datetime import datetime


class NetworkFailureRecoveryTracker:
    """
    Track network availability across repeated checks.

    The tracker detects:
    - Network failure: a transition from available to unavailable.
    - Network recovery: a transition from unavailable to available.
    - Failure duration.
    - Number of consecutive failed checks.
    """

    def __init__(self, initial_state="Unknown"):
        if initial_state not in {
            "Unknown",
            "Available",
            "Unavailable",
        }:
            raise ValueError(
                "initial_state must be Unknown, Available, or Unavailable."
            )

        self.state = initial_state
        self.failure_started_at = None
        self.failure_count = 0

    def process_check(self, available, timestamp=None):
        """
        Process one network availability check.

        Args:
            available (bool): True when the network is reachable.
            timestamp (datetime, optional): Timestamp for this check.
                If omitted, the current time is used.

        Returns:
            dict: Current state and any failure/recovery event.
        """

        if not isinstance(available, bool):
            raise TypeError("available must be a boolean.")

        if timestamp is None:
            timestamp = datetime.now()

        if not isinstance(timestamp, datetime):
            raise TypeError("timestamp must be a datetime.")

        previous_state = self.state

        if available:
            current_state = "Available"
        else:
            current_state = "Unavailable"

        failure_detected = (
            previous_state == "Available"
            and current_state == "Unavailable"
        )

        recovery_detected = (
            previous_state == "Unavailable"
            and current_state == "Available"
        )

        failure_duration = None

        if failure_detected:
            self.failure_started_at = timestamp
            self.failure_count = 1

        elif current_state == "Unavailable":
            if self.failure_started_at is None:
                self.failure_started_at = timestamp

            self.failure_count += 1

        elif recovery_detected:
            if self.failure_started_at is not None:
                failure_duration = round(
                    (
                        timestamp
                        - self.failure_started_at
                    ).total_seconds(),
                    2
                )

            self.failure_started_at = None
            self.failure_count = 0

        elif current_state == "Available":
            self.failure_started_at = None
            self.failure_count = 0

        self.state = current_state

        return {
            "state": self.state,
            "previous_state": previous_state,
            "failure_detected": failure_detected,
            "recovery_detected": recovery_detected,
            "failure_count": self.failure_count,
            "failure_duration_seconds": failure_duration,
            "timestamp": timestamp,
        }

    def get_status(self):
        """
        Return the current tracker status without changing state.
        """

        failure_duration = None

        if self.failure_started_at is not None:
            failure_duration = round(
                (
                    datetime.now()
                    - self.failure_started_at
                ).total_seconds(),
                2
            )

        return {
            "state": self.state,
            "failure_count": self.failure_count,
            "failure_duration_seconds": failure_duration,
        }

    def reset(self):
        """
        Reset the tracker to an unknown state.
        """

        self.state = "Unknown"
        self.failure_started_at = None
        self.failure_count = 0


def is_network_available(ping_result):
    """
    Determine network availability from an NPAT ping result.

    A host is considered available when at least one packet
    was received.
    """

    if not isinstance(ping_result, dict):
        raise TypeError("ping_result must be a dictionary.")

    packets_received = ping_result.get(
        "packets_received",
        0
    )

    return packets_received > 0


def process_ping_result(tracker, ping_result, timestamp=None):
    """
    Process an NPAT ping result using a tracker.
    """

    if not isinstance(
        tracker,
        NetworkFailureRecoveryTracker
    ):
        raise TypeError(
            "tracker must be a NetworkFailureRecoveryTracker."
        )

    available = is_network_available(
        ping_result
    )

    return tracker.process_check(
        available,
        timestamp=timestamp
    )
