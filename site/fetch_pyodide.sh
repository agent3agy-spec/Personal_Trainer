#!/bin/sh
# fetch_pyodide.sh · puts Pyodide 0.26.4 beside the page, in site/pyodide/.
# The web trainer cannot load anything from another site, so Python must ship next to index.html.
# The stdlib is renamed .zip.wasm because a .zip is not a type the page host serves.
#   sh site/fetch_pyodide.sh
set -eu
V=0.26.4
BASE="https://cdn.jsdelivr.net/npm/pyodide@$V"
DIR="$(cd "$(dirname "$0")" && pwd)/pyodide"
mkdir -p "$DIR"
for f in pyodide.js pyodide.asm.js pyodide.asm.wasm pyodide-lock.json python_stdlib.zip; do
  echo "fetching $f"
  curl -fsSL "$BASE/$f" -o "$DIR/$f"
done
mv -f "$DIR/python_stdlib.zip" "$DIR/python_stdlib.zip.wasm"
echo "done: $(ls "$DIR" | wc -l | tr -d ' ') files in $DIR"
