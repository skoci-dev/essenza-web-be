"""
System Service

Handles system status and metrics operations with caching support.
Provides real-time system metrics including CPU, memory, disk, and network stats.
"""

import logging
import platform
from datetime import datetime, timedelta
from typing import Any, ClassVar, Dict, Optional

import psutil
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone

from core.service import BaseService

logger = logging.getLogger(__name__)


class SystemService(BaseService):
    """
    Service class for system-related operations.

    Provides methods to retrieve system status, metrics, and application uptime.
    Implements intelligent caching for performance optimization.
    """

    # Class-level variables
    _app_start_time: ClassVar[Optional[datetime]] = None

    # Cache configuration constants
    METRICS_CACHE_KEY: ClassVar[str] = "system:metrics"
    METRICS_CACHE_TIMEOUT: ClassVar[int] = 30  # Cache duration in seconds

    @classmethod
    def initialize_start_time(cls) -> None:
        """
        Initialize application start time when Django boots up.

        This method should be called once during application startup
        to track the actual Django application uptime.
        """
        if cls._app_start_time is None:
            cls._app_start_time = timezone.now()
            logger.info(f"Application start time initialized: {cls._app_start_time}")

    @staticmethod
    def _format_bytes(bytes_value: float) -> str:
        """
        Convert bytes to human-readable format.

        Args:
            bytes_value: Size in bytes to format

        Returns:
            Formatted string with appropriate unit (B, KB, MB, GB, TB, PB)
        """
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if bytes_value < 1024.0:
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.2f} PB"

    @staticmethod
    def _format_uptime(uptime_seconds: float) -> str:
        """
        Convert uptime seconds to human-readable format.

        Args:
            uptime_seconds: Duration in seconds

        Returns:
            Formatted string like "1d 5h 30m 45s"
        """
        uptime_delta = timedelta(seconds=int(uptime_seconds))
        days = uptime_delta.days
        hours, remainder = divmod(uptime_delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        parts = []
        if days > 0:
            parts.append(f"{days}d")
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0:
            parts.append(f"{minutes}m")
        if seconds > 0 or not parts:
            parts.append(f"{seconds}s")

        return " ".join(parts)

    def get_system_status(self) -> Dict[str, Any]:
        """
        Retrieve comprehensive system status information.

        Provides Django application uptime, version information, and platform details.
        Unlike metrics, this data is not cached as it's lightweight and rarely changes.

        Returns:
            Dictionary containing:
                - status: Current operational status
                - uptime: Human-readable application uptime
                - uptime_seconds: Uptime in seconds
                - app_start_time: ISO formatted start time
                - version: Application version
                - django_version: Django framework version
                - python_version: Python interpreter version
                - platform: Operating system name
                - platform_release: OS release version
                - hostname: Server hostname
                - timestamp: Current timestamp in ISO format

        Raises:
            Exception: If unable to fetch system status
        """
        try:
            logger.debug("Fetching system status information.")

            # Ensure start time is initialized
            self.initialize_start_time()

            # Calculate Django application uptime (not OS uptime)
            if self._app_start_time:
                current_time = timezone.now()
                uptime_seconds = (current_time - self._app_start_time).total_seconds()
                app_start_time = self._app_start_time.isoformat()
            else:
                # Fallback to OS boot time if app start time unavailable
                boot_time = datetime.fromtimestamp(psutil.boot_time())
                uptime_seconds = (datetime.now() - boot_time).total_seconds()
                app_start_time = boot_time.isoformat()
                logger.warning(
                    "App start time not set, using OS boot time as fallback."
                )

            # Import Django lazily to avoid circular imports
            import django

            status_info: Dict[str, Any] = {
                "status": "operational",
                "uptime": self._format_uptime(uptime_seconds),
                "uptime_seconds": int(uptime_seconds),
                "app_start_time": app_start_time,
                "version": getattr(settings, "VERSION", "1.0.0"),
                "django_version": django.get_version(),
                "python_version": platform.python_version(),
                "platform": platform.system(),
                "platform_release": platform.release(),
                "hostname": platform.node(),
                "timestamp": timezone.now().isoformat(),
            }

            return status_info
        except Exception as e:
            logger.error(f"Failed to fetch system status: {str(e)}", exc_info=True)
            raise

    def _fetch_system_metrics(self) -> Dict[str, Any]:
        """
        Internal method to fetch fresh system metrics from psutil.

        Performs actual system calls to gather CPU, memory, disk, and network metrics.
        This method bypasses caching and always returns real-time data.

        Note: CPU usage calculation includes a 1-second sampling interval for accuracy.

        Returns:
            Dictionary containing comprehensive system metrics with the following structure:
                - cpu: CPU usage, core count, and frequency
                - memory: RAM usage statistics (formatted and raw bytes)
                - swap: Swap memory statistics
                - disk: Root partition disk usage
                - network: Network I/O counters (may be None if unavailable)
                - timestamp: ISO formatted current timestamp
                - cached: Boolean flag indicating data source (always False here)

        Raises:
            Exception: If unable to gather system metrics
        """
        logger.debug("Fetching fresh system metrics via psutil.")

        # CPU metrics with 1-second sampling for accuracy
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()

        # Memory and swap metrics
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()

        # Root partition disk usage
        disk = psutil.disk_usage("/")

        # Network I/O counters (may fail on some platforms)
        network_info: Optional[Dict[str, Any]] = None
        try:
            net_io = psutil.net_io_counters()
            network_info = {
                "bytes_sent": self._format_bytes(net_io.bytes_sent),
                "bytes_received": self._format_bytes(net_io.bytes_recv),
                "packets_sent": net_io.packets_sent,
                "packets_received": net_io.packets_recv,
                "errors_in": net_io.errin,
                "errors_out": net_io.errout,
                "drops_in": net_io.dropin,
                "drops_out": net_io.dropout,
            }
        except (AttributeError, RuntimeError) as net_error:
            logger.warning(f"Network metrics unavailable: {str(net_error)}")

        # Build comprehensive metrics dictionary
        metrics: Dict[str, Any] = {
            "cpu": {
                "usage_percent": round(cpu_percent, 2),
                "count": cpu_count,
                "frequency_mhz": round(cpu_freq.current, 2) if cpu_freq else None,
            },
            "memory": {
                "total": self._format_bytes(memory.total),
                "available": self._format_bytes(memory.available),
                "used": self._format_bytes(memory.used),
                "usage_percent": round(memory.percent, 2),
                "total_bytes": memory.total,
                "available_bytes": memory.available,
                "used_bytes": memory.used,
            },
            "swap": {
                "total": self._format_bytes(swap.total),
                "used": self._format_bytes(swap.used),
                "free": self._format_bytes(swap.free),
                "usage_percent": round(swap.percent, 2),
            },
            "disk": {
                "total": self._format_bytes(disk.total),
                "used": self._format_bytes(disk.used),
                "free": self._format_bytes(disk.free),
                "usage_percent": round(disk.percent, 2),
                "total_bytes": disk.total,
                "free_bytes": disk.free,
            },
            "network": network_info,
            "timestamp": timezone.now().isoformat(),
            "cached": False,
        }

        return metrics

    def get_system_metrics(self, use_cache: bool = True) -> Dict[str, Any]:
        """
        Retrieve comprehensive system metrics with intelligent caching.

        Fetches CPU, memory, disk, and network metrics. Implements caching to minimize
        expensive system calls. Cache backend automatically adapts based on Django settings:
        - Development: In-memory cache (LocMemCache)
        - Production: Redis cache (if configured)

        The 'cached' field in response indicates whether data came from cache.

        Args:
            use_cache: Enable cache lookup and storage. Set to False to force fresh data.
                      Defaults to True for optimal performance.

        Returns:
            Dictionary containing comprehensive system metrics. See _fetch_system_metrics()
            for detailed structure. Includes 'cached' boolean field.

        Raises:
            Exception: If unable to fetch or cache system metrics

        Examples:
            >>> service.get_system_metrics()  # Use cache if available
            >>> service.get_system_metrics(use_cache=False)  # Force refresh
        """
        try:
            # Attempt cache lookup if enabled
            if use_cache:
                if cached_metrics := cache.get(self.METRICS_CACHE_KEY):
                    logger.debug("Retrieved system metrics from cache.")
                    cached_metrics["cached"] = True
                    return cached_metrics

            # Fetch fresh metrics from system
            metrics = self._fetch_system_metrics()

            # Store in cache for subsequent requests
            if use_cache:
                cache.set(self.METRICS_CACHE_KEY, metrics, self.METRICS_CACHE_TIMEOUT)
                logger.debug(
                    f"Cached system metrics for {self.METRICS_CACHE_TIMEOUT} seconds."
                )

            return metrics
        except Exception as e:
            logger.error(f"Failed to fetch system metrics: {str(e)}", exc_info=True)
            raise

    def clear_metrics_cache(self) -> bool:
        """
        Manually clear the system metrics cache.

        Useful for forcing a refresh on the next metrics request or during
        maintenance operations. Cache will automatically be repopulated on
        the next call to get_system_metrics().

        Returns:
            True if cache was successfully cleared, False otherwise

        Note:
            Failures are logged but not raised to prevent disruption of
            cache management operations.
        """
        try:
            cache.delete(self.METRICS_CACHE_KEY)
            logger.info("System metrics cache cleared successfully.")
            return True
        except Exception as e:
            logger.error(f"Failed to clear metrics cache: {str(e)}", exc_info=True)
            return False
