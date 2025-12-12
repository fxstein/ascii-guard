# Test Document with Nested Boxes

This document contains nested ASCII boxes that demonstrate issue #17.

```ascii
┌─────────────────────────────────────────────────────────┐
│                  Core Logic (Python)                    │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Task Management Module                           │  │
│  │  - Task CRUD operations                          ││  │
│  │  - Subtask management                            ││  │
│  │  - Archive/restore                               ││  │
│  └───────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────┐  │
│  │  File Operations Module                           │  │
│  │  - TODO.md parsing/generation                     │  │
│  │  - Serial file management                        ││  │
│  │  - Log file operations                           ││  │
│  └───────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Coordination Module                              │  │
│  │  - Multi-user coordination (4 modes)             ││  │
│  │  - Git integration                               ││  │
│  │  - Conflict resolution                           ││  │
│  └───────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────┐  │
│  │  GitHub Integration Module                        │  │
│  │  - Issue management                              ││  │
│  │  - Bug reporting                                 ││  │
│  │  - API client                                    ││  │
│  └───────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Migration System Module                          │  │
│  │  - Migration registry                            ││  │
│  │  - Execution tracking                           │ │  │
│  │  - Version management                           │ │  │
│  └───────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Configuration Module                             │  │
│  │  - YAML config parsing                           ││  │
│  │  - Environment variables                         ││  │
│  │  - Default values                                ││  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
         │                              │
         │                              │
    ┌────▼────┐                    ┌────▼────┐
    │   MCP   ││                   ││   CLI  │
    │  Server ││                   ││Interfac│
    └────────┘                     └────────┘┘
```
