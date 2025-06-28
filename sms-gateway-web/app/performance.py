"""
Performance monitoring and optimization utilities
"""
import time
import functools
import psutil
import logging
from flask import request, g, current_app
from datetime import datetime

logger = logging.getLogger(__name__)


class PerformanceMonitor:
    """Performance monitoring utilities"""
    
    @staticmethod
    def monitor_request_time(f):
        """Decorator to monitor request execution time"""
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = f(*args, **kwargs)
                execution_time = time.time() - start_time
                
                # Log slow requests
                if execution_time > 1.0:  # Log requests taking more than 1 second
                    logger.warning(
                        f"Slow request: {request.endpoint} took {execution_time:.3f}s"
                    )
                
                # Store in request context for metrics
                g.execution_time = execution_time
                
                return result
                
            except Exception as e:
                execution_time = time.time() - start_time
                logger.error(
                    f"Request error: {request.endpoint} failed after {execution_time:.3f}s - {e}"
                )
                raise
                
        return decorated_function
    
    @staticmethod
    def get_system_metrics():
        """Get current system metrics"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_used_mb': memory.used / 1024 / 1024,
                'memory_total_mb': memory.total / 1024 / 1024,
                'disk_percent': disk.percent,
                'disk_used_gb': disk.used / 1024 / 1024 / 1024,
                'disk_total_gb': disk.total / 1024 / 1024 / 1024,
                'timestamp': datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting system metrics: {e}")
            return {}
    
    @staticmethod
    def log_performance_metrics():
        """Log performance metrics"""
        try:
            metrics = PerformanceMonitor.get_system_metrics()
            
            # Log warnings for high resource usage
            if metrics.get('cpu_percent', 0) > 80:
                logger.warning(f"High CPU usage: {metrics['cpu_percent']:.1f}%")
            
            if metrics.get('memory_percent', 0) > 80:
                logger.warning(f"High memory usage: {metrics['memory_percent']:.1f}%")
            
            if metrics.get('disk_percent', 0) > 90:
                logger.warning(f"High disk usage: {metrics['disk_percent']:.1f}%")
                
        except Exception as e:
            logger.error(f"Error logging performance metrics: {e}")


def optimize_database_query(query, limit=100):
    """Optimize database query with limits"""
    # Add limit to prevent large result sets
    if hasattr(query, 'limit') and not hasattr(query, '_limit'):
        query = query.limit(limit)
    
    return query


def compress_response(response):
    """Compress response if applicable"""
    if (response.content_length and 
        response.content_length > 1024 and 
        'gzip' in request.headers.get('Accept-Encoding', '')):
        
        # Flask-Compress would handle this automatically
        # This is a placeholder for manual compression if needed
        pass
    
    return response


class DatabaseConnectionPool:
    """Simple database connection pool manager"""
    
    def __init__(self, max_connections=10):
        self.max_connections = max_connections
        self.active_connections = 0
        self.connection_times = []
    
    def get_connection(self):
        """Get database connection with monitoring"""
        start_time = time.time()
        
        try:
            # This would integrate with SQLAlchemy's connection pool
            self.active_connections += 1
            
            if self.active_connections > self.max_connections:
                logger.warning(f"High database connection count: {self.active_connections}")
            
            return True  # Placeholder
            
        finally:
            connection_time = time.time() - start_time
            self.connection_times.append(connection_time)
            
            # Keep only last 100 connection times
            if len(self.connection_times) > 100:
                self.connection_times = self.connection_times[-100:]
    
    def release_connection(self):
        """Release database connection"""
        self.active_connections = max(0, self.active_connections - 1)
    
    def get_stats(self):
        """Get connection pool statistics"""
        if not self.connection_times:
            return {}
        
        avg_time = sum(self.connection_times) / len(self.connection_times)
        max_time = max(self.connection_times)
        
        return {
            'active_connections': self.active_connections,
            'max_connections': self.max_connections,
            'avg_connection_time': avg_time,
            'max_connection_time': max_time
        }


# Global connection pool
db_pool = DatabaseConnectionPool()