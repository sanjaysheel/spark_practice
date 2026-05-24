"""
Setup script: detects Java/Python versions and installs a compatible PySpark.

Python 3.14 needs current PySpark 4.1+, which requires Java 17+.
Older Python versions can use PySpark 3.5.x with Java 8/11/17.

Run: python setup_spark.py
"""
import os
import re
import subprocess
import sys

COMMON_JDKS = [
    r"C:\Program Files\Eclipse Adoptium",
    r"C:\Program Files\Java",
    r"C:\Program Files\Eclipse Adoptium\jdk-21",
    r"C:\Program Files\Eclipse Adoptium\jdk-17",
    r"C:\Program Files\Java\jdk-17",
    r"C:\Tools\temurin-17",
    r"C:\Tools\temurin-11\jdk-11.0.23+9",
]


def _prepend_java_home(java_home):
    os.environ["JAVA_HOME"] = java_home
    os.environ["PATH"] = os.path.join(java_home, "bin") + os.pathsep + os.environ.get("PATH", "")


def _find_installed_jdk(min_major=8):
    candidates = []
    for base in COMMON_JDKS:
        if os.path.isdir(base):
            candidates.append(base)
            try:
                candidates.extend(
                    os.path.join(base, name)
                    for name in os.listdir(base)
                    if os.path.isdir(os.path.join(base, name))
                )
            except OSError:
                pass

    candidates.sort(key=lambda p: _path_hint_major(p) or 0, reverse=True)
    for path in candidates:
        java_exe = os.path.join(path, "bin", "java.exe")
        if not os.path.isfile(java_exe):
            continue
        version = get_java_version(java_exe)
        if version and version >= min_major:
            return path, version
    return None, None


def _path_hint_major(path):
    match = re.search(r"(?:jdk-|jdk)(\d+)", path, flags=re.I)
    return int(match.group(1)) if match else None


def get_java_version(java_cmd="java"):
    """Return Java major version (e.g., 8, 11, 17) or None if not found."""
    try:
        result = subprocess.run([java_cmd, '-version'], capture_output=True, text=True, timeout=5)
        output = result.stderr or result.stdout
        # parse "java version "1.8.0_461" (Java 8) or "11.0.x" (Java 11+)
        m = re.search(r'java version "(\d+)\.(\d+)', output)
        if m:
            major = int(m.group(1))
            minor = int(m.group(2))
            # Java 1.8 is actually Java 8, Java 1.7 is Java 7, etc.
            if major == 1:
                return minor
            else:
                return major
        # try newer format: "major.minor"
        m = re.search(r'"(\d+)\.', output)
        if m:
            return int(m.group(1))
    except Exception:
        pass
    return None


def main():
    java_ver = get_java_version()
    python_ver = sys.version_info[:2]

    if python_ver >= (3, 14):
        required_java = 17
        pyspark_spec = "pyspark>=4.1,<4.2"
    else:
        required_java = 8
        pyspark_spec = "pyspark>=3.5,<3.6"

    if java_ver is None or java_ver < required_java:
        java_home, found_ver = _find_installed_jdk(required_java)
        if java_home:
            _prepend_java_home(java_home)
            java_ver = found_ver

    print(f"Detected Java version: {java_ver}")
    print(f"Detected Python version: {python_ver[0]}.{python_ver[1]}")
    
    if java_ver is None:
        print("ERROR: Java not found or version could not be detected.")
        print(f"Please install JDK {required_java}+ and set JAVA_HOME.")
        sys.exit(1)

    if java_ver < required_java:
        print(f"ERROR: Python {python_ver[0]}.{python_ver[1]} needs {pyspark_spec}, which requires Java {required_java}+.")
        print("Install Temurin/OpenJDK 17+ or run with Python 3.11/3.12 for older Spark.")
        sys.exit(1)
    
    print(f"Installing compatible PySpark: {pyspark_spec}")
    result = subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', pyspark_spec],
                            capture_output=False)
    if result.returncode != 0:
        print("ERROR: Failed to install PySpark.")
        sys.exit(1)
    print(f"SUCCESS: PySpark is ready for Python {python_ver[0]}.{python_ver[1]} and Java {java_ver}.")

if __name__ == '__main__':
    main()
