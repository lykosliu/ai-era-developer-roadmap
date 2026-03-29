import os
import json
import re

# Configuration
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(ROOT_DIR, "docs/roadmap_data.json")
ROADMAP_HTML = os.path.join(ROOT_DIR, "docs/index.html")
HOST = "https://lykosliu.github.io/ai-era-developer-roadmap"
IGNORE_DIRS = {".git", ".venv", "node_modules", "contributions", "demos", "docs"}

def parse_front_matter(content):
    """Parses Jekyll-style front matter from markdown content."""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return None
    
    fm_content = match.group(1)
    fm = {}
    for line in fm_content.split('\n'):
        if ':' in line:
            key, val = line.split(':', 1)
            fm[key.strip()] = val.strip()
    return fm

def should_include(file_path, fm):
    """Checks if the file meets the inclusion criteria."""
    if not fm:
        return False
    
    filename = os.path.basename(file_path)
    name_in_fm = fm.get('name')
    
    if filename == "overview.md" or filename == "README.md":
        return True
    
    if name_in_fm:
        # Check if filename matches name (allowing for space/underscore differences)
        clean_name = name_in_fm.replace(' ', '_')
        if filename == f"{clean_name}.md":
            return True
        
    return False

def build_tree():
    """Scans the directory and builds the knowledge tree."""
    tree = {
        "n": "AI-Era-Developer-Roadmap",
        "h": HOST,
        "c": []
    }
    
    # Map to keep track of folder nodes
    folder_nodes = {}

    for root, dirs, files in os.walk(ROOT_DIR):
        # Filter directories
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith('.')]
        
        rel_path = os.path.relpath(root, ROOT_DIR)
        
        for file in files:
            # Skip top-level README and STRUCTURE_DESC
            if rel_path == "." and (file == "README.md" or file == "STRUCTURE_DESC.md"):
                continue
            
            if not file.endswith('.md'):
                continue
                
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            fm = parse_front_matter(content)
            if should_include(file_path, fm):
                # Only replace underscores with spaces in the display name
                name = fm.get('name', file).replace('_', ' ')
                node = {
                    "n": name
                }
                if fm.get('description'):
                    node["d"] = fm.get('description')
                node["l"] = os.path.relpath(file_path, ROOT_DIR)
                
                if rel_path == ".":
                    tree["c"].append(node)
                else:
                    # Find or create parent folders
                    path_parts = rel_path.split(os.sep)
                    current_level = tree["c"]
                    
                    current_path = ""
                    parent_node = None
                    for part in path_parts:
                        current_path = os.path.join(current_path, part)
                        if current_path not in folder_nodes:
                            # Use the actual folder name, but replace underscores with spaces for display
                            display_name = part.replace('_', ' ')
                            
                            new_folder = {
                                "n": display_name,
                                "c": []
                            }
                            current_level.append(new_folder)
                            folder_nodes[current_path] = new_folder
                        
                        parent_node = folder_nodes[current_path]
                        current_level = parent_node["c"]
                    
                    if (file == "overview.md" or file == "README.md") and parent_node:
                        # Update parent folder node with overview metadata instead of adding a child
                        parent_node["n"] = node["n"]
                        if node.get("d"):
                            parent_node["d"] = node["d"]
                        parent_node["l"] = node["l"]
                    else:
                        # Check if this node already exists in this level (e.g., from overview.md)
                        existing_node = next((n for n in current_level if n.get('n') == node['n']), None)
                        if existing_node:
                            existing_node.update(node)
                        else:
                            current_level.append(node)

    # Post-process: remove empty children arrays to save space
    def prune(node):
        if "c" in node:
            if not node["c"]:
                del node["c"]
            else:
                for child in node["c"]:
                    prune(child)
    
    prune(tree)
    return tree

def main():
    print("Scanning project for roadmap nodes...")
    tree = build_tree()
    
    # Minify JSON for both file and HTML embedding
    minified_json = json.dumps(tree, separators=(',', ':'))
    
    print(f"Updating {DATA_FILE} (minified)...")
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        f.write(minified_json)
        
    print(f"Updating embedded data in {ROADMAP_HTML} (minified)...")
    update_html(tree)
    
    print("Done!")

def update_html(data):
    """Updates the embedded roadmapData in ROADMAP.html."""
    if not os.path.exists(ROADMAP_HTML):
        print("ROADMAP.html not found.")
        return

    with open(ROADMAP_HTML, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find roadmapData object (handles both single line and multi-line)
    pattern = r'(const roadmapData = ).*?([ \t\n]*;)'
    # Minify JSON for embedding
    minified_json = json.dumps(data, separators=(',', ':'))
    replacement = f'\\1{minified_json};'
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open(ROADMAP_HTML, 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == "__main__":
    main()
