"""
Monitoring Middleware - Performance Monitoring
"""
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict

from app.core.logging import logger


class MonitoringMiddleware(BaseHTTPMiddleware):
    """Middleware for performance monitoring"""
    
    def __init__(self, app):
        super().__init__(app)
        self.metrics = defaultdict(list)
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Store metric
        endpoint = f"{request.method}:{request.url.path}"
        self.metrics[endpoint].append(duration)
        
        # Keep only last 100 requests per endpoint
        if len(self.metrics[endpoint]) > 100:
            self.metrics[endpoint] = self.metrics[endpoint][-100:]
        
        # Log slow requests
        if duration > 5.0:  # 5 seconds
            logger.warning(
                f"Slow request detected",
                extra={
                    "endpoint": endpoint,
                    "duration_seconds": round(duration, 2),
                    "status_code": response.status_code
                }
            )
        
        return response
    
    def get_metrics(self):
        """Get performance metrics"""
        stats = {}
        for endpoint, durations in self.metrics.items():
            if durations:
                stats[endpoint] = {
                    "count": len(durations),
                    "avg_ms": round(sum(durations) / len(durations) * 1000, 2),
                    "max_ms": round(max(durations) * 1000, 2),
                    "min_ms": round(min(durations) * 1000, 2)
                }
        return stats
