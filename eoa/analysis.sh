#!/bin/bash

echo "=== Code Analysis Report ==="
echo

total_lines=0
total_classes=0
total_functions=0
total_imports=0
total_comments=0

declare -A file_types
declare -A file_type_lines

echo "File Analysis:"
echo "----------------------------------------"

while IFS= read -r file; do
    extension="${file##*.}"
    [ -z "$extension" ] && extension="no_extension"
    file_types[$extension]=$((file_types[$extension] + 1))

    echo -n "$file: "

    lines=$(grep -v '^\s*$' "$file" | wc -l)
    total_lines=$((total_lines + lines))
    file_type_lines[$extension]=$((file_type_lines[$extension] + lines))

    case "$extension" in
        py)
            classes=$(grep -c "^class " "$file")
            functions=$(grep -c "^def " "$file")
            imports=$(grep -cE "^import |^from " "$file")
            comments=$(grep -c "^\s*#" "$file")
            ;;
        js|ts)
            classes=$(grep -c "class " "$file")
            functions=$(grep -c -E "function |=>|^\s*\w+\s*\(" "$file")
            imports=$(grep -c "import " "$file")
            comments=$(grep -c "//" "$file")
            ;;
        java)
            classes=$(grep -c "class " "$file")
            functions=$(grep -c -E "void |public |private |protected " "$file")
            imports=$(grep -c "import " "$file")
            comments=$(grep -c "//" "$file")
            ;;
        c|cpp|cc|cxx)
            classes=0
            functions=$(grep -c -E "^[a-zA-Z_][a-zA-Z0-9_]*\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\(.*\)\s*\{" "$file")
            imports=$(grep -c "#include" "$file")
            comments=$(grep -c "//" "$file")
            ;;
        *)
            classes=0
            functions=0
            imports=0
            comments=0
            ;;
    esac

    total_classes=$((total_classes + classes))
    total_functions=$((total_functions + functions))
    total_imports=$((total_imports + imports))
    total_comments=$((total_comments + comments))

    echo "$lines lines, $classes classes, $functions functions, $imports imports, $comments comments"
done < <(find . -type d \( -name .git -o -name .venv \) -prune -o -type f -print)

echo "----------------------------------------"
echo "Summary by File Type:"
echo "----------------------------------------"
for ext in "${!file_types[@]}"; do
    echo "$ext files: ${file_types[$ext]} (${file_type_lines[$ext]} lines)"
done

echo "----------------------------------------"
echo "Overall Code Summary:"
echo "Total lines of code: $total_lines"
echo "Total classes: $total_classes"
echo "Total functions: $total_functions"
echo "Total imports: $total_imports"
echo "Total comments: $total_comments"
echo
echo "Code Structure:"

total_files=$(find . -type d \( -name .git -o -name .venv \) -prune -o -type f -print | wc -l)

if [ "$total_classes" -gt 0 ]; then
    avg_functions=$(echo "scale=2; $total_functions/$total_classes" | bc 2>/dev/null || echo "N/A")
    echo "- Average functions per class: $avg_functions"
else
    echo "- Average functions per class: N/A (no classes found)"
fi

if [ "$total_files" -gt 0 ]; then
    avg_lines=$(echo "scale=2; $total_lines/$total_files" | bc 2>/dev/null || echo "N/A")
    echo "- Average lines per file: $avg_lines"
else
    echo "- Average lines per file: N/A (no files)"
fi

if [ "$total_lines" -gt 0 ]; then
    comment_ratio=$(echo "scale=2; $total_comments/$total_lines*100" | bc 2>/dev/null || echo "N/A")
    echo "- Comment ratio: $comment_ratio%"
else
    echo "- Comment ratio: N/A (no lines of code)"
fi
