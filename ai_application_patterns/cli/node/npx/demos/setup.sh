#!/bin/bash

# Ensure index.js is executable (crucial for npx)
chmod +x ./hello-npx/index.js

echo "Testing hello-npx-demo locally using npx..."
echo "-----------------------------------------"

# Running npx from the parent directory of the package
# npx will pick up the package in the current or sub-directory if we point to it
# Or more commonly, we run it from the directory where the package is located.

cd hello-npx
npx .

echo "-----------------------------------------"
echo "Demo execution complete."
