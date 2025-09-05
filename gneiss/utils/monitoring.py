"""
Monitoring and observability utilities for Gneiss Engine.
"""

import time
from contextlib import contextmanager
from typing import Dict, Optional

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import Status, StatusCode
from prometheus_client import Counter, Gauge, Histogram

# Metrics
IMAGE_PROCESSING_TIME = Histogram(
    "image_processing_seconds",
    "Time spent processing images",
    ["operation", "model"]
)

IMAGE_PROCESSED_COUNT = Counter(
    "images_processed_total",
    "Total number of images processed",
    ["operation", "status"]
)

AI_MODEL_LOAD_TIME = Gauge(
    "ai_model_load_seconds",
    "Time taken to load AI models",
    ["model_name"]
)

GPU_MEMORY_USAGE = Gauge(
    "gpu_memory_usage_bytes",
    "GPU memory usage in bytes",
    ["device_id"]
)

def setup_tracing(app, service_name: str = "gneiss-engine"):
    """Setup OpenTelemetry tracing."""
    resource = Resource.create({"service.name": service_name})
    
    tracer_provider = TracerProvider(resource=resource)
    tracer_provider.add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter())
    )
    
    trace.set_tracer_provider(tracer_provider)
    
    return trace.get_tracer(__name__)

def setup_metrics(app):
    """Setup Prometheus metrics."""
    # Add metrics middleware to FastAPI app
    from prometheus_fastapi_instrumentator import Instrumentator
    Instrumentator().instrument(app).expose(app)

@contextmanager
def track_operation(operation: str, model: Optional[str] = None):
    """Context manager to track operation performance."""
    start_time = time.time()
    status = "success"
    
    try:
        yield
    except Exception:
        status = "error"
        raise
    finally:
        duration = time.time() - start_time
        IMAGE_PROCESSING_TIME.labels(operation=operation, model=model or "none").observe(duration)
        IMAGE_PROCESSED_COUNT.labels(operation=operation, status=status).inc()

def track_gpu_usage():
    """Track GPU memory usage if available."""
    if not torch.cuda.is_available():
        return
    
    for i in range(torch.cuda.device_count()):
        memory_used = torch.cuda.memory_allocated(i)
        GPU_MEMORY_USAGE.labels(device_id=str(i)).set(memory_used)

class PerformanceMonitor:
    """Advanced performance monitoring with context support."""
    
    def __init__(self, operation_name: str):
        self.operation_name = operation_name
        self.start_time = None
        self.span = None
        
    def __enter__(self):
        self.start_time = time.time()
        tracer = trace.get_tracer(__name__)
        self.span = tracer.start_span(self.operation_name)
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start_time
        IMAGE_PROCESSING_TIME.labels(operation=self.operation_name).observe(duration)
        
        if exc_type:
            self.span.set_status(Status(StatusCode.ERROR, str(exc_val)))
            IMAGE_PROCESSED_COUNT.labels(operation=self.operation_name, status="error").inc()
        else:
            self.span.set_status(Status(StatusCode.OK))
            IMAGE_PROCESSED_COUNT.labels(operation=self.operation_name, status="success").inc()
        
        self.span.end()