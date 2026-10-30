#!/usr/bin/env python3
"""Provider stub: replies to any request with a malformed JSON-RPC frame, then disconnects."""
import sys

sys.stdin.readline()
sys.stdout.write("Content-Length: 5\r\n\r\n{nope")
sys.stdout.flush()
