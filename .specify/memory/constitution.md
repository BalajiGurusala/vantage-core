Vantage Core - Project Constitution

1. System Architecture
Vantage is a distributed eBPF observability platform. It consists of two entirely separate nodes that communicate over the network:

The MCP Server (apps/mcp-server): Written in Python. Responsible for parsing DWARF files, calculating memory offsets, and exposing tools to Claude via the Model Context Protocol.

The Edge Daemon (apps/edge-daemon): Written in Rust. Responsible for running on the embedded Linux target, receiving raw hex offsets, and injecting eBPF using libbpf.

2. Strict Boundary Rules

Never mix languages. Python stays in mcp-server, Rust stays in edge-daemon.

The two systems do not share source code. They only share network payloads defined in libs/protocol.

3. Engineering Standards

Rust: Must use cargo clippy and safe Rust. Avoid unwrap()—handle Result and Option gracefully.

Python: Must use strictly typed Python (mypy standards).

eBPF: Assume the target is an ARM64 or x86_64 stripped Linux binary. No source code or headers exist on the edge target.

4. Spec-Driven Execution
You must never write code until you have written an Implementation Plan and Task List, and the user has explicitly approved it.