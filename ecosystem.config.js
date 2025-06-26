module.exports = {
    apps: [
      {
        name: "influencer-api",
        script: "uvicorn",
        args: "main:app --host 0.0.0.0 --port 8090",
        cwd: "./",
        autorestart: true,
        max_memory_restart: "1G",
        log_date_format: "YYYY-MM-DD HH:mm Z",
        error_file: "./logs/influencer-api-error.log",
        out_file: "./logs/influencer-api-out.log",
        merge_logs: true,
        instances: 1,
        exec_mode: "fork",
        interpreter: "venv/bin/python3",
        watch: false,
        env: {
          PYTHONUNBUFFERED: "1"
        }
      }
    ]
  };
  