"""Loader stub: loads testcases from a directory. Testcases are simple JSON files describing input and expected output.

This loader is flexible: it supports
- JSON files containing a single testcase object {"input":..., "expected":...}
- JSON files containing a list of such objects
- ASCII table strings embedded in `input` or `expected` (parsed into list-of-dicts)
- LeetCode-style pasted Input:/Output: blocks (parsed heuristically)
"""

import json
import os
from typing import List, Dict
import re
import ast


def load_testcases(dirpath: str) -> List[Dict]:
    """Load all .json files in dirpath and return as a list.

    Files may contain JSON or may be pasted LeetCode-style text. The loader
    normalizes to a flat list of testcase dicts with keys 'input' and 'expected'.
    """
    cases = []
    for name in sorted(os.listdir(dirpath)):
        if name.endswith('.json'):
            path = os.path.join(dirpath, name)
            with open(path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                except Exception:
                    # fallback: file may be a direct LeetCode paste (not JSON). Rewind and read raw to try to parse Input/Output blocks
                    f.seek(0)
                    raw = f.read()
                    raw = raw.strip()
                    # strip code fences if present
                    raw = re.sub(r"^```[a-zA-Z0-9]*\n|\n```$", "", raw, flags=re.S)
                    parsed = _parse_leetcode_paste(raw)
                    if parsed is None:
                        # give up, store raw as single testcase
                        data = {"input": raw, "expected": None}
                    else:
                        data = parsed

                # If the file contains a single testcase (object), normalize to a list
                if isinstance(data, list):
                    items = data
                else:
                    items = [data]

                # Normalize and parse ascii-table strings or inline assignments inside each testcase
                for item in items:
                    if not isinstance(item, dict):
                        # unexpected shape, append as-is
                        cases.append(item)
                        continue
                    item['__source__'] = name
                    # parse input/expected if they are strings
                    for key in ('input', 'expected'):
                        if key in item and isinstance(item[key], str):
                            text = item[key]
                            # ASCII table
                            if _looks_like_ascii_table(text):
                                try:
                                    item[key] = _parse_ascii_table(text)
                                except Exception:
                                    # leave as-is on parse failure
                                    pass
                            else:
                                # try to interpret LeetCode-style assignments or Python literals
                                assigned = _try_parse_assignments(text)
                                if assigned is not None:
                                    if len(assigned) == 1:
                                        item[key] = list(assigned.values())[0]
                                    else:
                                        item[key] = assigned
                                else:
                                    # try literal_eval
                                    try:
                                        item[key] = ast.literal_eval(text)
                                    except Exception:
                                        # keep as raw string
                                        item[key] = text
                    cases.append(item)
    return cases


def _looks_like_ascii_table(text: str) -> bool:
    """Heuristic: returns True if text contains an ASCII-style table with '|' separators."""
    if not isinstance(text, str):
        return False
    lines = [l for l in text.splitlines() if l.strip()]
    if len(lines) < 2:
        return False
    # look for a header line with '|' and a separator line with '+'
    has_pipe = any('|' in l for l in lines)
    has_plus = any(l.strip().startswith('+') and '+' in l for l in lines)
    return has_pipe and has_plus


def _parse_ascii_table(text: str) -> List[Dict]:
    """Parse a simple ASCII table into a list of dicts.

    Example table format:
    +---------+-------+
    | user_id | name  |
    +---------+-------+
    | 1       | aLice |
    | 2       | bOB   |
    +---------+-------+
    """
    lines = [l for l in text.splitlines() if l.strip()]
    # find first line that contains '|' and looks like header
    header_line = None
    for i, l in enumerate(lines):
        if '|' in l and not l.strip().startswith('+'):
            header_line = i
            break
    if header_line is None:
        raise ValueError('no header line found')

    # header is that line; following lines that contain '|' and are not separators are rows
    header = lines[header_line]
    # extract column names
    cols = [c.strip() for c in header.strip().strip('|').split('|')]

    rows = []
    for l in lines[header_line+1:]:
        if '|' not in l:
            continue
        if l.strip().startswith('+'):
            # separator or footer
            continue
        parts = [p.strip() for p in l.strip().strip('|').split('|')]
        # If parts length doesn't match cols, try to pad/truncate
        if len(parts) != len(cols):
            # try to normalize by trimming empty leading/trailing
            # fallback: skip malformed row
            continue
        row = {cols[i]: _coerce_value(parts[i]) for i in range(len(cols))}
        rows.append(row)
    return rows


def _coerce_value(s: str):
    """Try to coerce a cell string to int if appropriate, else strip and return string."""
    s = s.strip()
    if re.fullmatch(r"-?\d+", s):
        try:
            return int(s)
        except Exception:
            return s
    return s


def _parse_leetcode_paste(raw: str):
    """Parse a raw LeetCode-style paste that contains 'Input:' and 'Output:' sections.

    Returns a dict like {"input": ..., "expected": ...} or None on failure.
    """
    if not isinstance(raw, str):
        return None
    text = raw.strip()
    # Look for Input: ... Output: ... blocks
    m = re.search(r"Input:\s*(.*?)(?:\n\s*Output:|\n\s*Expected:|\Z)(.*)", text, flags=re.S | re.I)
    if not m:
        return None
    input_text = m.group(1).strip()
    expected_text = m.group(2).strip() if m.group(2) else None

    # If the input contains multiple labeled blocks like "Person table:\n...\nAddress table:\n..."
    # extract each labeled block and parse separately.
    blocks = list(re.finditer(r"([A-Za-z][A-Za-z0-9 _]*?):\s*\n(.*?)(?=(?:[A-Za-z][A-Za-z0-9 _]*?:\s*\n)|\Z)", input_text, flags=re.S))
    if blocks:
        parsed_input = {}
        for b in blocks:
            label = b.group(1).strip()
            content = b.group(2).strip()
            # normalize label to a dict key: drop trailing 'table' and non-alphanum -> underscore
            key = re.sub(r"\W+", "_", re.sub(r"(?i)\btable\b$", "", label).strip()).strip('_').lower()
            if _looks_like_ascii_table(content):
                try:
                    parsed_input[key] = _parse_ascii_table(content)
                    continue
                except Exception:
                    parsed_input[key] = content
                    continue
            # try assignments or literal
            assigned = _try_parse_assignments(content)
            if assigned is not None:
                # if multiple assignments inside this block, store dict, else single value
                if len(assigned) == 1:
                    parsed_input[key] = list(assigned.values())[0]
                else:
                    parsed_input[key] = assigned
            else:
                try:
                    parsed_input[key] = ast.literal_eval(content)
                except Exception:
                    parsed_input[key] = content
    else:
        # single unlabeled block: behave like before
        # If input_text contains a label like 'Users table:' remove the leading label line
        input_text = re.sub(r"^\w[\w ]*:\s*\n", "", input_text)

        parsed_input = None
        if _looks_like_ascii_table(input_text):
            try:
                parsed_input = _parse_ascii_table(input_text)
            except Exception:
                parsed_input = input_text
        else:
            assigned = _try_parse_assignments(input_text)
            if assigned is not None:
                if len(assigned) == 1:
                    parsed_input = list(assigned.values())[0]
                else:
                    parsed_input = assigned
            else:
                try:
                    parsed_input = ast.literal_eval(input_text)
                except Exception:
                    parsed_input = input_text

    parsed_expected = None
    if expected_text:
        if _looks_like_ascii_table(expected_text):
            try:
                parsed_expected = _parse_ascii_table(expected_text)
            except Exception:
                parsed_expected = expected_text
        else:
            try:
                parsed_expected = ast.literal_eval(expected_text)
            except Exception:
                assigned = _try_parse_assignments(expected_text)
                if assigned is not None:
                    if len(assigned) == 1:
                        parsed_expected = list(assigned.values())[0]
                    else:
                        parsed_expected = assigned
                else:
                    parsed_expected = expected_text

    return {"input": parsed_input, "expected": parsed_expected}


def _try_parse_assignments(text: str):
    """Try to parse simple variable assignments in text into a dict.

    Supports patterns like:
      products = [..], searchWord = "mouse"
      matrix = [[...]]
      a = 1\n b = 2
    Returns dict or None.
    """
    s = text.strip()
    if '=' not in s:
        return None
    i = 0
    n = len(s)
    result = {}
    while i < n:
        # skip whitespace and commas
        while i < n and s[i] in ' \t\n,':
            i += 1
        # parse variable name
        m = re.match(r"([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*", s[i:])
        if not m:
            break
        var = m.group(1)
        i += m.end()
        # parse expression starting at i
        if i >= n:
            result[var] = None
            break
        ch = s[i]
        if ch in ('[', '{', '('):
            # parse balanced bracket expression
            start = i
            stack = [ch]
            i += 1
            while i < n and stack:
                if s[i] in ('[', '{', '('):
                    stack.append(s[i])
                elif s[i] in (']', '}', ')'):
                    # match
                    stack.pop()
                elif s[i] in ('"', "'"):
                    # skip quoted string
                    quote = s[i]
                    i += 1
                    while i < n and s[i] != quote:
                        if s[i] == '\\':
                            i += 2
                        else:
                            i += 1
                i += 1
            expr = s[start:i].strip()
        elif ch in ('"', "'"):
            # quoted string
            quote = ch
            start = i
            i += 1
            while i < n and s[i] != quote:
                if s[i] == '\\':
                    i += 2
                else:
                    i += 1
            i += 1
            expr = s[start:i].strip()
        else:
            # unquoted token: read until comma or newline
            start = i
            while i < n and s[i] not in ',\n':
                i += 1
            expr = s[start:i].strip()

        # try to evaluate expr safely
        try:
            val = ast.literal_eval(expr)
        except Exception:
            # as fallback, strip quotes
            val = expr.strip(' "')
        result[var] = val
        # skip trailing separators
        while i < n and s[i] in ' \t\n,':
            i += 1
    return result if result else None
