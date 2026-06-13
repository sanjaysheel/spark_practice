# Common PySpark Errors - Fixed

## Error: "SparkSession' object is not subscriptable"

### What does it mean?
This error occurs when you try to use bracket notation `[]` on a SparkSession object, which doesn't support subscripting.

### Common Causes & Fixes

#### 1. **Wrong Parameter Name in solve()**
❌ **WRONG:**
```python
def solve(spark, inputs):
    df = spark["my_table"]  # ❌ Can't access like this
    return df
```

✅ **CORRECT:**
```python
def solve(spark, inputs):
    df = inputs["my_table"]  # ✅ Access through inputs dict
    return df
```

#### 2. **Parameters in Wrong Order**
❌ **WRONG:**
```python
def solve(inputs, spark):
    df = inputs["my_table"]
    return df
# But you're treating the first parameter as if it's the inputs dict
# when it's actually spark!
```

✅ **CORRECT:**
```python
def solve(spark, inputs):
    df = inputs["my_table"]
    return df

# OR if you want inputs first:
def solve(inputs, spark):
    df = inputs["my_table"]
    return df
    # Make sure the actual call matches this signature
```

#### 3. **Treating Spark Object Like a Dict**
❌ **WRONG:**
```python
def solve(spark, inputs):
    # Trying to treat spark as a dict
    result = spark[0]  # ❌ SparkSession doesn't support indexing
    return result
```

✅ **CORRECT:**
```python
def solve(spark, inputs):
    # Use spark methods properly
    df = spark.read.csv("path/to/file.csv")
    return df
```

### Solution Template

Here's the correct template for PySpark solutions:

```python
from pyspark.sql import functions as F

def solve(spark, inputs):
    """
    Args:
        spark: SparkSession object
        inputs: Dict of table_name -> DataFrame
                Example: {"employees": DataFrame, "departments": DataFrame}
    
    Returns:
        DataFrame or list of dicts
    """
    # Access DataFrames from inputs dict
    employees = inputs["employees"]
    departments = inputs["departments"]
    
    # Perform your operations
    result = employees.join(
        departments,
        employees.dept_id == departments.id,
        "left"
    )
    
    return result
```

### Debugging Tips

1. **Check parameter names**: Make sure your function signature is `def solve(spark, inputs):` or `def solve(inputs, spark):`
2. **Access data correctly**: Always use `inputs["table_name"]` not `spark["table_name"]`
3. **Check for copy-paste errors**: This error often happens when copying code and accidentally using `spark` instead of `inputs`

---

## Other Related Errors

### "TypeError: 'PipelineContext' object is not subscriptable"
Same solution - you're trying to index an object that doesn't support it. Check your variable names and data types.

### "KeyError: 'table_name'"
This means the table exists in your inputs dict with a different key name. Check:
- The exact spelling and case of the table name
- What keys are actually in the inputs dict

---

## Need Help?

If you're still getting errors:
1. Print the inputs dict to see what tables are available: `print(list(inputs.keys()))`
2. Check that your function signature matches what the runner expects
3. Use `df.show()` to debug DataFrames

