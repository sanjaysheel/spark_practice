# PySpark Solutions - Quick Cheat Sheet

## ✅ DO THIS

```python
def solve(spark, inputs):
    # Access input tables from the inputs DICT
    df = inputs["employees"]          # ✅ Correct
    df = inputs.get("employees")      # ✅ Also correct
    
    # Use spark for operations
    result = spark.sql("SELECT * FROM ...")      # ✅
    result = spark.createDataFrame([...])         # ✅
    result = spark.read.csv("path")               # ✅
    
    return result
```

---

## ❌ DON'T DO THIS

```python
def solve(spark, inputs):
    # ❌ NEVER try to index spark like a dict!
    df = spark["employees"]           # ❌ ERROR: not subscriptable
    df = spark[0]                     # ❌ ERROR: not subscriptable
    
    # ❌ Don't pass parameters in wrong order
    # If signature is solve(spark, inputs), first param must be spark!
    
    return df
```

---

## Common Operations

| Task | Code |
|------|------|
| Get input table | `employees = inputs["employees"]` |
| Show table | `employees.show()` |
| Filter rows | `employees.filter(employees.age > 30)` |
| Select columns | `employees.select("name", "salary")` |
| Join tables | `emp.join(dept, "dept_id", how="left")` |
| Group & aggregate | `df.groupBy("dept").agg(sum("salary"))` |
| Add column | `df.withColumn("new_col", ...)` |
| Run SQL | `spark.sql("SELECT * FROM table")` |

---

## Function Signature

```python
# Signature 1 (spark first)
def solve(spark, inputs):
    employee = inputs["employee"]
    return employee
```

```python
# Signature 2 (inputs first) - also works!
def solve(inputs, spark):
    employee = inputs["employee"]  # Still use inputs, not first param
    return employee
```

**⚠️ Important:** Regardless of parameter order, always access tables via the `inputs` dict parameter, not the `spark` parameter!

---

## If You Get "SparkSession' object is not subscriptable"

1. **Find the line** with `spark["something"]` or `spark[0]`
2. **Replace with** `inputs["something"]`
3. **Test again**

That's it! 🎉

