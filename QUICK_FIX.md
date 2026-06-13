# Quick Fix: "SparkSession' object is not subscriptable"

## The Error
```
ERROR: 'SparkSession' object is not subscriptable
```

## The Fix (in 3 words)
**Use `inputs`, not `spark`!**

## Before → After

```python
# ❌ BEFORE (causes error)
def solve(spark, inputs):
    df = spark["my_table"]  # WRONG!
    
# ✅ AFTER (correct)
def solve(spark, inputs):
    df = inputs["my_table"]  # CORRECT!
```

## Rules
1. Access tables: `inputs["table_name"]` ✅
2. Use spark for: `spark.read()`, `spark.sql()`, `spark.createDataFrame()` ✅
3. Never use: `spark["something"]` ❌ or `spark[0]` ❌

## Example

```python
from pyspark.sql import functions as F

def solve(spark, inputs):
    # ✅ Get tables from inputs dict
    employees = inputs["employees"]
    departments = inputs["departments"]
    
    # ✅ Use spark for operations
    result = spark.sql("""
        SELECT e.id, e.name, d.name as dept
        FROM employees e
        LEFT JOIN departments d ON e.dept_id = d.id
    """)
    
    return result
```

## Why?
- `spark` = SparkSession object (doesn't support indexing with `[]`)
- `inputs` = Dictionary of DataFrames (supports indexing with `[]`)

---

**For detailed help, see:** `SPARK_ERRORS_FIXED.md`  
**For templates, see:** `project/PYSPARK_SOLUTION_TEMPLATE.py`
