# STRUCTURE_DESC.md: Content Organization Standards

To maintain clarity and consistency across the  project, all contributions must adhere to the following directory and file structure.

## 📁 Knowledge Point Classification

All topics are classified into top-level directories based on their domain. We avoid "Junior" or "Senior" labels, focusing instead on **Breadth-First** coverage. **Multi-level nested directories** are supported and encouraged for complex domains.

---

## 🛠️ Content Formats

There are two primary ways to organize a knowledge point:

### 1. Simple Knowledge Point (Single Markdown File)
Use this for focused concepts that can be explained within a single document without complex code examples.

- **File Name:** `Topic_Name.md` (e.g., `Prompt_Engineering.md`)
- **Required Header (Front Matter):**
  ```markdown
  ---
  name: Topic_Name
  description: Topic_Name simple description
  ---
  ```
- **Required Content Sections:**
  - **Overview:** Definition and core concept.
  - **Why it matters:** Its role and value in the AI era.
  - **Key Principles:** The underlying logic or background.
  - **AI Context:** How this topic relates to AI systems or development.

---

### 2. Complex Knowledge Point (Single Topic Directory)
Use this for tools, frameworks, or multi-faceted technologies that require runnable code examples.

- **Directory Name:** `topic_name/` (e.g., `vector_databases/`)
- **Required Files:**
  - `overview.md`:
    - **Scope:** Used for a **single topic** description.
    - **Required Header (Front Matter):**
      ```markdown
      ---
      name: Topic_Name
      description: Topic_Name simple description
      ---
      ```
    - Explains the technology, its value proposition, and how it fits into the AI ecosystem.
  - `demos/` directory:
    - `README.md`:
      - **Required Header (Front Matter):**
        ```markdown
        ---
        name: Demos
        description: Hands-on examples and runnable code.
        ---
        ```
      - Explaining the demos and how to run them.
    - `setup.sh`: Script to install dependencies (if any).
    - `demo_*.py` (or other languages): Runnable code samples demonstrating the core value.

---

### 3. Topic Collection (Multi-Topic Directory)
Use this for directories that serve as a collection of multiple topics or sub-categories.

- **Directory Name:** `category_name/` (e.g., `ai_agent_frameworks/`)
- **Required Files:**
  - `README.md`:
    - **Scope:** Used for a **collection of topics**.
    - **Required Header (Front Matter):**
      ```markdown
      ---
      name: Category_Name
      description: Category_Name simple description
      ---
      ```
    - Provides a high-level overview of the category and lists/links the included sub-topics.

---

## 🏗️ File Coexistence Rules

- **Mutual Exclusion:** A directory must **not** contain both `README.md` and `overview.md` at the same level.
- **Consistency:** Both files share the same internal structure (Front Matter + Sections), differing only in their purpose (Single Topic vs. Topic Collection).

---

## �️ Roadmap Integration

The interactive roadmap ([ROADMAP.html](./ROADMAP.html)) is automatically synchronized with the project structure:
- **Metadata Source:** The `name` and `description` fields in the Front Matter are used as the display title and tooltip on the roadmap.
- **Directory Nodes:** For directories, the roadmap logic prioritizes `README.md` or `overview.md` to extract the category's metadata.
- **Auto-Sync:** Run `bash sync.sh` after adding new content to update the roadmap data.

---

## �🛑 Quality Standards

- **Language:** Strictly English.
- **Tone:** Objective, technical, and educational.
- **Depth:** Aim for "conceptual understanding + actionable starting point."
- **Neutrality:** Avoid political, ideological, or country-specific discussions.
