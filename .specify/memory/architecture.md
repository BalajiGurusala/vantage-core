# Vantage Architecture & Protocol Specification (v1)
## 1. System Topology
Vantage operates as a decoupled, distributed system. The AI never touches the hardware directly.
* **Control Plane (Node 1):** The `mcp-server` (Python). Runs on the developer's laptop or CI/CD runner. Handles AI interactions, artifact downloading, and DWARF math.
* **Data Plane (Node 2):** The `edge-daemon` (Rust). Runs natively on the embedded Linux target. Receives hex addresses, injects eBPF bytecode via `libbpf`, and streams telemetry back.

---

## 2. The Bridge (Communication Protocol)
The two nodes communicate via **JSON-over-WebSockets**. WebSockets are required because the edge daemon must continuously stream eBPF ring-buffer telemetry back to the MCP server after a probe is injected.

### 2.1. Payload: Injection Request (MCP -> Edge)
Sent by the MCP server to command the edge daemon to attach a new eBPF probe.
```json
{
  "message_type": "inject_request",
  "payload": {
    "target_binary_path": "/usr/bin/drone_flight_controller",
    "hex_offset": "0x4015A0",
    "probe_type": "uprobe",
    "telemetry_format": "latency_histogram"
  }
}

### 2.2. Payload: Injection Response (Edge -> MCP)
Sent immediately by the edge daemon to confirm the libbpf injection succeeded or failed.
```json
{
  "message_type": "inject_response",
  "payload": {
    "status": "success",
    "probe_id": "probe_8f72a1",
    "error_message": null
  }
}

### 2.3. Payload: Telemetry Stream (Edge -> MCP)
Fired continuously by the edge daemon as the hardware executes the probed memory address. The MCP server catches this, translates the raw data back to human-readable text, and passes it to the AI or Dashboard.
```json
{
  "message_type": "telemetry_event",
  "payload": {
    "probe_id": "probe_8f72a1",
    "timestamp_ns": 1718294958102934,
    "raw_data": {
      "execution_time_ns": 14500,
      "cpu_core": 1
    }
  }
}


## 3. Security Boundaries
No Symbol Transmission: The MCP Server MUST NOT send strings like sendThrottle over the network. The Edge Daemon only understands raw hex offsets (0x4015A0).

Read-Only Probes: For v1, the Edge Daemon will strictly reject any eBPF bytecode that attempts to overwrite kernel memory (bpf_probe_write_user). Probes are strictly for passive telemetry and tracing.

