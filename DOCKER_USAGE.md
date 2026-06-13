# Docker Usage

This Docker setup runs the same project without changing your local code, Python, Java, or Spark installation.

There are two ways to use Docker here:

- image-only mode: everything is copied into the image during build
- dev mode: your local folder is mounted into the container for live editing

Use image-only mode when you want the container to run without taking code from your local folder.

Use dev mode when you want local edits to appear immediately inside Docker.

## Image-Only Mode

This mode does not mount local code. Everything comes from the built Docker image.

Build the image:

```powershell
cd A:\Spark_practice
docker build -t spark-practice .
```

Run a normal Python solution:

```powershell
docker run --rm spark-practice python easy_run.py solution1.py --problem nth_highest_salary --testcase case1.json
```

Run a PySpark solution:

```powershell
docker run --rm -p 4040-4050:4040-4050 spark-practice python easy_run.py solution_join_spark_simple.py --testcase case_join.json
```

Run a SQL solution:

```powershell
docker run --rm -p 4040-4050:4040-4050 spark-practice python easy_run.py solution_join.sql --problem Second_Highest_Sal
```

Start image-only container with always-on Spark UI:

```powershell
docker compose -f docker-compose.image.yml up -d --build
```

Open shell inside image-only container:

```powershell
docker exec -it spark-practice-image bash
```

Inside container:

```bash
cd /app/project
python easy_run.py solution_join.sql --problem Second_Highest_Sal
```

Stop image-only container:

```powershell
docker compose -f docker-compose.image.yml down
```

Important: if you change local files, rebuild the image:

```powershell
docker build -t spark-practice .
```

## Dev Mode With Local Mount

Recommended for active coding:

- mount your local `A:\Spark_practice\project` folder into the container
- publish Spark UI ports `4040-4050`

Then every local edit is immediately visible inside Docker, and Spark UI can be opened from the host.

Run commands from the repository root:

```powershell
cd A:\Spark_practice
```

## Build The Docker Image

```powershell
docker build -t spark-practice .
```

## Best Dev Flow: Keep Container Running

Build and start the long-running dev container:

```powershell
docker compose up -d --build
```

If you already had the container running, restart it after Dockerfile or compose changes:

```powershell
docker compose down
docker compose up -d --build
```

If Docker shows this warning:

```text
Error loading config file: open C:\Users\...\ .docker\config.json: Access is denied
```

run this once in the same PowerShell window:

```powershell
.\docker-env.ps1
```

Then run Docker commands again.

Check it is running:

```powershell
docker ps
```

Check Spark UI server logs:

```powershell
docker logs -f spark-practice-dev
```

You should see:

```text
Spark UI server is running.
Open: http://localhost:4040
```

Open Spark UI:

```text
http://localhost:4040
```

If `4040` is busy, try:

```text
http://localhost:4041
http://localhost:4042
...
http://localhost:4050
```

Open a shell inside it:

```powershell
docker exec -it spark-practice-dev bash
```

Inside the container:

```bash
cd /app/project
python easy_run.py solution_join.sql --problem Second_Highest_Sal
python easy_run.py solution_join_spark_simple.py --testcase case_join.json
python easy_run.py solution1.py --problem nth_highest_salary --testcase case1.json
```

Stop the dev container:

```powershell
docker compose down
```

This mode mounts:

```text
A:\Spark_practice\project -> /app/project
A:\Spark_practice         -> /workspace/Spark_practice
```

So code changes from Windows are immediately visible inside the running container.

Spark UI ports:

```text
http://localhost:4040
http://localhost:4041
...
http://localhost:4050
```

Important: the compose container starts `spark_ui_server.py` automatically. That means a small Spark session is always running and Spark UI should be visible even before you run a solution.

For always-visible Spark UI, use `docker compose up -d --build`. One-off `docker run` commands are useful for quick tests, but the UI only exists while that one-off command is running.

## VS Code Dev Container

This repo includes:

```text
.devcontainer/devcontainer.json
docker-compose.yml
```

Open `A:\Spark_practice` in VS Code, then choose:

```text
Dev Containers: Reopen in Container
```

VS Code will open the workspace at:

```text
/workspace/Spark_practice
```

Run code from:

```bash
cd /workspace/Spark_practice/project
python easy_run.py solution_join.sql --problem Second_Highest_Sal
```

## Run With Local Project Mounted

PowerShell command shape:

```powershell
docker run --rm -p 4040-4050:4040-4050 -v "A:\Spark_practice\project:/app/project" spark-practice python easy_run.py <solution_file> --problem <problem_name>
```

Spark UI, while a Spark job is running:

```text
http://localhost:4040
```

## Run A Normal Python Solution

```powershell
docker run --rm -p 4040-4050:4040-4050 -v "A:\Spark_practice\project:/app/project" spark-practice python easy_run.py solution1.py --problem nth_highest_salary --testcase case1.json
```

Run all testcases:

```powershell
docker run --rm -p 4040-4050:4040-4050 -v "A:\Spark_practice\project:/app/project" spark-practice python easy_run.py solution1.py --problem nth_highest_salary
```

## Run A PySpark Solution

```powershell
docker run --rm -p 4040-4050:4040-4050 -v "A:\Spark_practice\project:/app/project" spark-practice python easy_run.py solution_join_spark_simple.py --testcase case_join.json
```

## Run A SQL Solution

```powershell
docker run --rm -p 4040-4050:4040-4050 -v "A:\Spark_practice\project:/app/project" spark-practice python easy_run.py solution_join.sql --problem Second_Highest_Sal
```

## Mount The Whole Spark Practice Folder

Use this when another tool, such as Airflow DAGs, needs to see the full local repository layout.

```powershell
docker run --rm -p 4040-4050:4040-4050 -v "A:\Spark_practice:/workspace/Spark_practice" -w /workspace/Spark_practice/project spark-practice python easy_run.py solution_join.sql --problem Second_Highest_Sal
```

Inside the container:

```text
/workspace/Spark_practice
  project/
  Dockerfile
  DOCKER_USAGE.md
```

If an Airflow container needs the same files, mount the same local folder into that Airflow container's DAGs path, for example:

```powershell
-v "A:\Spark_practice:/opt/airflow/dags/Spark_practice"
```

Then DAG code can reference:

```text
/opt/airflow/dags/Spark_practice/project
```

## Open A Shell Inside The Container

```powershell
docker run --rm -it -p 4040-4050:4040-4050 -v "A:\Spark_practice\project:/app/project" spark-practice bash
```

Inside the container, the working folder is already:

```text
/app/project
```

So you can run:

```bash
python easy_run.py solution_join.sql --problem Second_Highest_Sal
```

## Notes

- The Docker image uses Python 3.14, Java 21, and PySpark 4.1.x.
- Your local `project` folder is mounted into the container with `-v`.
- Spark UI ports `4040-4050` are published with `-p 4040-4050:4040-4050`.
- If you edit files locally, you do not need to rebuild the image.
- Rebuild only when you change the Dockerfile or dependencies.
- Spark warning logs are normal. The important line is the test result, for example `2/2 tests passed`.
