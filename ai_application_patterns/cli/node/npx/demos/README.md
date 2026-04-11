---
name: hello-pnx Demo
description: Step-by-step guide to building an npx-executable package.
---

# Building an npx-Executable Package

This demo shows how to create a simple Node.js package that can be executed directly via `npx`.

## Prerequisites

-   Node.js and npm installed on your system.
-   Basic knowledge of the command line.

## Step-by-Step Guide

### 1. Initialize Your Package
Create a new directory for your project and initialize it with a `package.json` file.

```bash
mkdir hello-npx-demo
cd hello-npx-demo
npm init -y
```

### 2. Create Your Executable Script
Create an `index.js` file. This script **must** start with a "shebang" line (`#!/usr/bin/env node`) to tell the operating system to use Node.js to run it.

```javascript
#!/usr/bin/env node

console.log("Hello, World! 🚀");
```

### 3. Configure the `bin` Field
In your `package.json`, add a `bin` field. This maps the command name (e.g., `hello-npx`) to the script you want to run.

```json
{
  "name": "hello-npx-demo",
  "version": "1.0.0",
  "bin": {
    "hello-npx": "./index.js"
  }
}
```

### 4. Make the Script Executable
On Unix-based systems (Linux/macOS), you need to give the script execution permissions.

```bash
chmod +x index.js
```

### 5. Test It Locally with `npx`
You can test your package locally without publishing it to npm. From inside your project directory, run:

```bash
npx .
```

`npx .` tells npx to look at the current directory's `package.json`, find the `bin` field, and execute the corresponding script.

## Final Script Example

The final structure of your demo package should look like this:

-   `package.json`:
    ```json
    {
      "name": "hello-npx-demo",
      "version": "1.0.0",
      "bin": {
        "hello-npx": "./index.js"
      }
    }
    ```
-   `index.js`:
    ```javascript
    #!/usr/bin/env node
    console.log("Hello, World! 🚀");
    ```

## How to Run This Demo

1.  Navigate to the `demos/` directory.
2.  Run the setup script:
    ```bash
    bash setup.sh
    ```
    This script will make `index.js` executable and run `npx .` to show the output.
