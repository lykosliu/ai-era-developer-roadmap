---
name: A2UI Protocol
description: A declarative UI protocol for agent-driven interfaces, enabling rich, interactive, and native rendering across platforms.
---

# A2UI Protocol (Agent-to-UI Protocol)

## Overview
A2UI (Agent-to-UI) is a declarative UI protocol specifically designed for agent-driven interfaces. It allows AI agents to generate rich, interactive user interfaces that render natively across multiple platforms (web, mobile, desktop) without the need for executing arbitrary code. 

By transmitting UI structure and state as JSON messages rather than raw HTML or JavaScript, A2UI ensures that the client remains in control of security and styling while providing a seamless, native-feeling experience for the user.

## Why it Matters
Text-only interactions between agents and users are often inefficient for complex tasks. A2UI addresses several critical challenges:
- **Efficiency**: Instead of multi-turn text dialogues (e.g., "What date?", "What time?"), agents can present interactive forms, date pickers, and selectors in a single turn.
- **Security**: Traditional approaches like sending HTML/JS in iframes introduce security risks and visual inconsistencies. A2UI uses declarative data, which is safe to transmit and process.
- **Native Experience**: Because the client renders the UI using its own native components (React, Flutter, etc.), the agent-generated UI inherits the app's styling, accessibility, and performance.
- **Portability**: A single agent response can be rendered across different platforms (Web, iOS, Android, Desktop) using the client's respective UI framework.

## Key Principles
A2UI is built on three core architectural pillars:

### 1. Streaming Messages
UI updates flow as a sequence of structured JSON messages from the agent to the client. This supports progressive rendering and real-time updates as the agent "thinks" or gathers more data.

### 2. Declarative Components
UIs are described as data (JSON), not code. The agent sends an abstract component tree that refers to IDs in a **Catalog**— a set of trusted components predefined by the client.
- **Surface**: The canvas or container for components (e.g., a dialog, sidebar, or main view).
- **Component**: Individual UI elements like `Button`, `TextField`, or `Card`.

### 3. Data Binding
A2UI separates UI structure from application state. Components bind to a **Data Model** using JSON Pointer paths, enabling reactive updates. When the data model changes, the UI updates automatically.

## Core Message Types (v0.9)
The protocol uses specific message types to manage the UI lifecycle:
- **`createSurface`**: Initializes a new UI surface and specifies the component catalog to be used.
- **`updateComponents`**: Adds, removes, or modifies UI components within a surface using a flat, ID-based structure.
- **`updateDataModel`**: Updates the application state that components are bound to.
- **`deleteSurface`**: Removes a UI surface when it is no longer needed.

## AI Context
In the evolving agentic ecosystem, A2UI serves as the "Visual Layer" for agents. While protocols like **MCP** handle how agents talk to tools and **A2A** handles how agents talk to each other, A2UI standardizes how agents present information to humans. 

It is particularly powerful for **Multi-Agent Systems** where agents may be running on remote servers. A2UI allows these remote agents to provide a high-quality UI experience without needing direct access to the client's frontend codebase.

## Ecosystem & Tools
The A2UI ecosystem includes several tools and experimental projects that demonstrate the protocol's power:
- **[A2UI Lab](https://a2ui-lab.southleft.com/)**: A demonstration of adaptive, role-based UI generation. It shows how the same underlying infrastructure data can be presented differently (e.g., for a DevOps Lead vs. a Security Analyst) based on AI analysis and A2UI rendering.
- **[A2UI Composer](https://a2ui-composer.ag-ui.com/)**: A visual builder (powered by CopilotKit) that allows developers to create and experiment with A2UI-compatible interfaces, simplifying the process of building agent-driven surfaces.

## References
- [Official A2UI Introduction](https://a2ui.org/introduction/what-is-a2ui/)
- [Core Concepts & Overview](https://a2ui.org/concepts/overview/)
- [Component Structure Specification](https://a2ui.org/concepts/overview/#component-structure)
- [A2UI GitHub Repository](https://github.com/a2ui-org/a2ui)
- [A2UI Lab Demo](https://a2ui-lab.southleft.com/)
- [A2UI Composer](https://a2ui-composer.ag-ui.com/)
