import os

workers = 4
timeout = 120
bind = f"0.0.0.0:{os.environ.get('PORT', '10000')}"
worker_class = 'sync'
max_requests = 1000
max_requests_jitter = 50
forwarded_allow_ips = '*'
