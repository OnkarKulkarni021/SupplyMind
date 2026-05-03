# 🏗️ SupplyMind - Monolith Architecture

## Overview

SupplyMind is implemented as a **monolithic application** with **stateful external services** for databases and observability. This approach provides:

- **Simplified deployment** and management
- **Easier local development** with Docker Compose
- **Single deployment unit** for the application logic
- **Separate containers** for data and observability services

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      Kubernetes / Local Dev                     │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────┐
│    Ingress / Load Balancer       │
│    (Kubernetes Ingress / k8s)    │
└────────────────┬─────────────────┘
                 ↓
┌─────────────────────────────────────────────────────────┐
│       SupplyMind Monolith Container                     │
│  (Python FastAPI + LangGraph + All Agents)             │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │  API Gateway (FastAPI)                           │ │
│  │  - REST Endpoints                                │ │
│  │  - Authentication                                │ │
│  └───────────────────────────────────────────────────┘ │
│                      ↓                                  │
│  ┌───────────────────────────────────────────────────┐ │
│  │  LangGraph Orchestrator                          │ │
│  │  - Workflow orchestration                        │ │
│  │  - State management                              │ │
│  └───────────────────────────────────────────────────┘ │
│         ↙        ↓         ↓         ↘                 │
│  ┌────────┐┌────────┐┌────────┐┌────────┐             │
│  │Inventory││Demand ││Vendor  ││Procure-│             │
│  │Monitoring││Forecast││Intelli-││ment  │             │
│  │Agent   ││Agent  ││gence  ││Agent  │             │
│  │        ││       ││Agent  ││       │             │
│  └────────┘└────────┘└────────┘└────────┘             │
│  ┌────────┐┌────────┐┌────────┐                       │
│  │Logistics││Exception││Human   │                       │
│  │Tracking ││Handling ││Approval │                       │
│  │Agent   ││Agent   ││Agent   │                       │
│  └────────┘└────────┘└────────┘                       │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │  RAG Service                                      │ │
│  │  - Embedding generation                          │ │
│  │  - Vector search                                 │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │  Guardrails & Safety Layer                        │ │
│  │  - Output validation                             │ │
│  │  - Policy enforcement                            │ │
│  │  - Audit logging                                 │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │  Internal State & Caching                         │ │
│  │  - In-memory cache                               │ │
│  │  - Session management                            │ │
│  │  - Temporary workflow state                      │ │
│  └───────────────────────────────────────────────────┘ │
└──────┬────────────────────────────────────┬────────────┘
       │                                    │
       ↓                                    ↓
┌──────────────────────────────────┐  ┌──────────────────────────────┐
│   Database Container             │  │  Cache Container             │
│   (PostgreSQL)                   │  │  (Redis)                     │
│                                  │  │                              │
│  - Inventory data                │  │  - Session cache             │
│  - Purchase orders               │  │  - Query cache               │
│  - Vendor information            │  │  - Message queue             │
│  - Execution history             │  │  - Rate limiting             │
│  - User approvals                │  │  - Workflow state            │
│  - Audit logs                    │  │                              │
└──────────────────────────────────┘  └──────────────────────────────┘
       ↑                                        ↑
       └────────────────┬─────────────────────┘
                        │
┌───────────────────────────────────────────────────────────────────┐
│              UI Container (Streamlit)                            │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │  Human Approval Dashboard                                │    │
│  │  - PO approval workflows                                 │    │
│  │  - Decision visualization                                │    │
│  │  - Agent activity monitoring                             │    │
│  │  - Real-time notifications                               │    │
│  └──────────────────────────────────────────────────────────┘    │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │  Admin Dashboard                                         │    │
│  │  - System health monitoring                              │    │
│  │  - Agent performance metrics                             │    │
│  │  - Configuration management                              │    │
│  │  - Audit trail review                                    │    │
│  └──────────────────────────────────────────────────────────┘    │
└───────────────────────────────────────────────────────────────────┘
                        ↑
┌───────────────────────────────────────────────────────────────────┐
│              External Services & Integrations                     │
│                                                                   │
│  ┌──────────────────────────┐  ┌──────────────────────────────┐  │
│  │  Vector Database         │  │  LLM Providers              │  │
│  │  (Chroma)                │  │  (OpenAI/Anthropic/etc)    │  │
│  │                          │  │                             │  │
│  └──────────────────────────┘  └──────────────────────────────┘  │
│                                                                   │
│  ┌──────────────────────────┐  ┌──────────────────────────────┐  │
│  │  ERP Integration         │  │  Vendor APIs                │  │
│  │  (SAP/Oracle/etc)        │  │  (Email, webhooks)         │  │
│  └──────────────────────────┘  └──────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────┘
                        ↑
┌───────────────────────────────────────────────────────────────────┐
│              Observability Stack (Separate Containers)            │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │  ELK Stack                                               │    │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐    │    │
│  │  │ Elasticsearch│ │  Logstash    │ │   Kibana     │    │    │
│  │  │ (Logs store) │ │ (Processing) │ │ (Dashboard)  │    │    │
│  │  └──────────────┘ └──────────────┘ └──────────────┘    │    │
│  └──────────────────────────────────────────────────────────┘    │
│                                                                   │
│  ┌──────────────────────────┐  ┌──────────────────────────────┐  │
│  │  Prometheus              │  │  Grafana                     │  │
│  │  - Metrics collection    │  │  - Metrics dashboards        │  │
│  │  - Time series DB        │  │  - Alerting                  │  │
│  └──────────────────────────┘  └──────────────────────────────┘  │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │  Langfuse                                                │    │
│  │  - LLM-specific tracing                                  │    │
│  │  - Prompt/response tracking                             │    │
│  │  - Token usage monitoring                               │    │
│  └──────────────────────────────────────────────────────────┘    │
└───────────────────────────────────────────────────────────────────┘
```

---

## Monolith Architecture Details

### Core Monolith Container

The SupplyMind application is a **single, stateless container** that bundles:

#### 1. **API Layer**
- **FastAPI** REST API
- Request validation
- Authentication & authorization
- OpenAPI documentation

#### 2. **Orchestration Layer**
- **LangGraph** for workflow management
- State management
- Agent choreography

#### 3. **Agent Services** (All in one process)
- **Inventory Monitoring Agent**: Tracks stock levels
- **Demand Forecasting Agent**: Predicts future demand
- **Vendor Intelligence Agent**: RAG-powered vendor analysis
- **Procurement Agent**: Core decision engine
- **Logistics/Tracking Agent**: Order tracking
- **Exception Handling Agent**: Anomaly response
- **Human Approval Agent**: Approval workflow

#### 4. **Supporting Services**
- **RAG Engine**: Embedding generation & retrieval
- **Guardrails Layer**: Safety & policy validation
- **Audit Service**: Decision logging
- **Integration Layer**: ERP, vendor APIs, webhooks

---

## Separate Container Services

### Database Container (PostgreSQL)

**Purpose**: Persistent data storage

**Contains**:
```
- inventory (current stock levels)
- purchase_orders (all POs)
- vendors (vendor master data)
- vendor_performance (historical metrics)
- contracts (vendor contracts & terms)
- users (system users)
- approvals (approval history & logs)
- audit_logs (all decisions & changes)
- rag_documents (uploaded knowledge documents)
- workflow_history (execution traces)
```

**Deployment**:
- Docker Compose: `postgres:15` service
- Kubernetes: `StatefulSet` with persistent volume

---

### Cache Container (Redis)

**Purpose**: High-speed caching & temporary state

**Contains**:
```
- Session data
- Query result cache
- Workflow execution state
- Message queue (for async tasks)
- Rate limiting counters
- Distributed locks
```

**Deployment**:
- Docker Compose: `redis:7` service
- Kubernetes: `Deployment` or `StatefulSet`

---

### Vector Database Container (Chroma)

**Purpose**: Store and retrieve vector embeddings for RAG (Retrieval-Augmented Generation)

**Contains**:
```
- Vendor contract embeddings
- Historical PO embeddings
- Pricing agreement embeddings
- Email communication embeddings
- Decision context vectors
- Knowledge base embeddings
```

**Features**:
- In-memory vector search (fast retrieval)
- Persistent storage (if enabled)
- HTTP API for easy integration
- Supports multiple embedding models
- Built-in similarity search

**Deployment**:
- Docker Compose: `ghcr.io/chroma-core/chroma:latest` service
  - Persistent data volume: `chroma_data`
  - HTTP endpoint: `http://chroma:8000`
  - Environment: `IS_PERSISTENT=true`
- Kubernetes: `Deployment` with PersistentVolumeClaim for data storage

**How It Works**:
1. Monolith generates embeddings from documents (contracts, emails, past decisions)
2. Stores embeddings in Chroma via HTTP API
3. When Vendor Intelligence Agent needs context, queries Chroma for similar past decisions
4. Retrieves most relevant context to inform vendor selection
5. Reduces latency compared to external vector DB services

---

### UI Container (Streamlit)

**Purpose**: Human-in-the-loop interface for approval workflows and system monitoring

**Contains**:
```
- Human Approval Dashboard
  - Pending PO approvals with AI recommendations
  - Decision reasoning visualization
  - Vendor comparison tables
  - Risk assessment scores
  - Approval/rejection workflow

- Admin Dashboard
  - Real-time agent activity monitoring
  - System health metrics
  - Workflow execution timelines
  - Configuration management
  - Audit trail review
  - Performance analytics
```

**Features**:
- Interactive data visualizations
- Real-time updates via WebSocket/polling
- Responsive design for desktop/mobile
- Role-based access control
- Notification system for pending approvals
- Historical decision analysis

**Deployment**:
- Docker Compose: `streamlit:latest` service
  - Port: 8501 (Streamlit default)
  - Environment variables for API connectivity
  - Volume mounts for custom themes/assets
- Kubernetes: `Deployment` with horizontal scaling

**Integration**:
- Connects to monolith API for data retrieval
- Receives real-time notifications via Redis pub/sub
- Stores user actions in PostgreSQL
- Displays metrics from Prometheus

---

### Observability Containers

#### Elasticsearch
- Stores all application and system logs
- Searchable, indexed log storage

#### Logstash
- Collects logs from monolith container
- Processes and enriches logs
- Sends to Elasticsearch

#### Kibana
- Dashboard for log analysis
- Real-time monitoring

#### Prometheus
- Metrics collection from monolith
- Time-series database

#### Grafana
- Metrics dashboards
- Alerting

#### Langfuse
- LLM tracing and monitoring
- Prompt/response tracking

---

## Data Flow

### 1. **Inventory Low Stock Event**
```
Monolith Container:
1. Inventory Agent detects low stock
2. Publishes event to internal queue
3. Demand Forecasting Agent receives event
4. Queries PostgreSQL for historical data
5. Generates demand forecast
6. Stores forecast in PostgreSQL
7. Publishes forecast event
```

### 2. **Vendor Selection with RAG**
```
Monolith Container:
1. Procurement Agent triggered
2. Queries Chroma Vector DB for similar past decisions (via RAG retrieval)
3. Retrieves vendor performance from PostgreSQL
4. Vendor Intelligence Agent ranks vendors using RAG context
5. Applies Guardrails validation
6. Generates PO draft with reasoning
```

### 3. **Human Approval**
```
Streamlit UI Container:
1. Displays pending PO approvals with AI recommendations
2. Shows decision reasoning, vendor comparisons, and risk scores
3. User reviews and approves/rejects via interactive dashboard
4. Sends approval decision to monolith API

Monolith Container:
1. API endpoint receives approval request from Streamlit
2. Updates PostgreSQL with approval decision and user feedback
3. Publishes execution event to workflow orchestrator
4. Procurement execution begins
5. Sends logs to ELK Stack for audit trail
6. Metrics sent to Prometheus for monitoring
7. Updates Chroma with new decision context for future learning
```

---

## Deployment Models

### Local Development (Docker Compose)

```yaml
services:
  supplymind:
    image: supplymind:latest
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/supplymind
      - REDIS_URL=redis://redis:6379
      - CHROMA_DB_URL=http://chroma:8000
    depends_on:
      - postgres
      - redis
      - chroma
  
  postgres:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7
  
  chroma:
    image: ghcr.io/chroma-core/chroma:latest
    ports:
      - "8001:8000"
    environment:
      - IS_PERSISTENT=true
    volumes:
      - chroma_data:/chroma/data
  
  streamlit:
    image: streamlit:latest
    ports:
      - "8501:8501"
    environment:
      - SUPPLYMIND_API_URL=http://supplymind:8000
      - DATABASE_URL=postgresql://user:pass@postgres:5432/supplymind
      - REDIS_URL=redis://redis:6379
    depends_on:
      - supplymind
      - postgres
      - redis
    volumes:
      - ./ui:/app
    command: streamlit run app.py --server.port 8501 --server.address 0.0.0.0
    
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.0.0
  
  kibana:
    image: docker.elastic.co/kibana/kibana:8.0.0
  
  prometheus:
    image: prom/prometheus:latest
  
  grafana:
    image: grafana/grafana:latest
```

**Benefits**:
- Single command to start entire stack: `docker-compose up`
- Identical environment for all developers
- No external infrastructure needed

---

### Kubernetes Deployment

#### Deployment Manifest

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: supplymind
spec:
  replicas: 3
  selector:
    matchLabels:
      app: supplymind
  template:
    metadata:
      labels:
        app: supplymind
    spec:
      containers:
      - name: supplymind
        image: supplymind:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: supplymind-secrets
              key: database-url
        - name: REDIS_URL
          value: redis://redis:6379
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

#### Database StatefulSet

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
spec:
  serviceName: postgres
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
  - metadata:
      name: postgres-storage
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 100Gi
```

#### Chroma Vector Database StatefulSet

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: chroma
spec:
  serviceName: chroma
  replicas: 1
  selector:
    matchLabels:
      app: chroma
  template:
    metadata:
      labels:
        app: chroma
    spec:
      containers:
      - name: chroma
        image: ghcr.io/chroma-core/chroma:latest
        ports:
        - containerPort: 8000
        env:
        - name: IS_PERSISTENT
          value: "true"
        volumeMounts:
        - name: chroma-storage
          mountPath: /chroma/data
        resources:
          limits:
            memory: "2Gi"
            cpu: "1"
          requests:
            memory: "1Gi"
            cpu: "500m"
  volumeClaimTemplates:
  - metadata:
      name: chroma-storage
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 50Gi
```

**Benefits**:
- Horizontal scaling of monolith instances
- Load balancing across replicas
- Automatic failover
- Persistent storage for database
- Rolling updates with zero downtime

---

## Communication Patterns

### Within Monolith
- **Synchronous**: Direct Python function calls
- **Asynchronous**: Internal event queue via Redis
- **No network overhead**: Same process

### Monolith → External Services
- **Database**: TCP connection pooling via SQLAlchemy
- **Redis**: TCP connection pooling
- **Chroma Vector DB**: HTTP API calls (localhost:8000)
- **LLM APIs**: HTTP requests
- **ERP/Vendor APIs**: HTTP/webhooks

### Observability
- **Application logs**: Sent to Logstash (via stdout or log shipper)
- **Metrics**: Prometheus scrapes `/metrics` endpoint
- **LLM traces**: Sent to Langfuse API
- **Structured logging**: JSON format for easier parsing

---

## State Management

### Monolith State
- **Stateless design**: Each container instance is interchangeable
- **No sticky sessions**: Any instance can handle any request
- **Session data**: Stored in Redis (shared across instances)
- **Workflow state**: Stored in PostgreSQL & Redis

### Database State
- **PostgreSQL**: Source of truth for all persistent data
- **Atomic transactions**: ACID compliance for data integrity
- **Audit trail**: Every change logged

### Cache State
- **Redis**: Temporary state, can be lost
- **Not a bottleneck**: Falls back to PostgreSQL if cache misses

### Vector Database State
- **Chroma**: Stores embeddings for RAG retrieval
- **Persistent**: Data persists across container restarts
- **Auto-indexing**: Vectors are indexed for fast similarity search
- **Initialization**: On startup, monolith seeds Chroma with vendor contracts, historical POs, and past decision context
- **Updates**: New documents and decisions are continuously added to Chroma for improved future recommendations

---

## Scalability

### Horizontal Scaling

1. **Application Tier**:
   - Deploy multiple monolith instances
   - Kubernetes Horizontal Pod Autoscaler (HPA) scales based on CPU/memory
   - Load balancer distributes requests

2. **Database Tier**:
   - PostgreSQL primary with read replicas (if needed)
   - Vertical scaling for most use cases

3. **Cache Tier**:
   - Redis cluster mode for distributed caching
   - Or single Redis instance (sufficient for most cases)

### Example Kubernetes HPA

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: supplymind-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: supplymind
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

---

## Observability Stack

### Logging (ELK Stack)

**What is logged**:
- API request/response logs
- Agent decision logs with reasoning
- RAG retrieval context
- Guardrail validations
- Error traces
- Audit trail (all changes)

**Kibana Dashboards**:
- Real-time request flow
- Agent decision timelines
- Error rate trends
- Performance metrics

---

### Metrics (Prometheus + Grafana)

**Collected Metrics**:
- HTTP request latency (p50, p95, p99)
- Agent execution time
- Database query latency
- Cache hit/miss rate
- Error rate
- Active workflows
- Memory/CPU usage

---

### Tracing (Langfuse)

**Tracked**:
- LLM prompt inputs
- LLM outputs
- Token usage
- Latency per LLM call
- Cost tracking
- Error logs

---

## Security Considerations

### Container Security
- Run as non-root user
- Read-only root filesystem where possible
- Resource limits (CPU, memory)
- Network policies for pod-to-pod communication

### Data Security
- PostgreSQL encryption at rest
- TLS/SSL for all external API calls
- Secrets stored in Kubernetes Secrets or HashiCorp Vault
- RBAC for database access

### API Security
- Authentication via JWT/OAuth2
- API rate limiting
- Input validation
- CORS configuration

---

## Development Workflow

### Local Development
```bash
# Start all services locally
docker-compose up

# Access application
curl http://localhost:8000/docs

# View logs in Kibana
open http://localhost:5601
```

### Staging/Production
```bash
# Build and push image
docker build -t supplymind:v1.0 .
docker push registry.example.com/supplymind:v1.0

# Deploy to Kubernetes
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/statefulset-postgres.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
```

---

## Advantages of Monolith Architecture

✅ **Simplified Development**: Single codebase, easier debugging  
✅ **Lower Latency**: No network calls between services  
✅ **Easier Testing**: Integrated testing, no distributed tracing needed  
✅ **Unified State**: Shared memory for workflow coordination  
✅ **Easy Deployment**: One container to manage  
✅ **Cost Effective**: Fewer infrastructure components  

---

## Migration Path (If Needed)

If monolith becomes a bottleneck, you can extract agents to microservices:

1. **Inventory Monitoring** → Independent service
2. **Demand Forecasting** → Independent service
3. **Vendor Intelligence** → Independent service
4. **Etc.**

**Communication**: Message queue (Kafka/RabbitMQ) between services

---

## Summary

SupplyMind's monolith architecture provides:

| Aspect | Details |
|--------|---------|
| **Core App** | Single Python/FastAPI container with all agents |
| **Data** | PostgreSQL for persistence, Redis for caching |
| **Scalability** | Horizontal scaling via Kubernetes deployment replicas |
| **Observability** | ELK, Prometheus, Grafana, Langfuse |
| **Local Dev** | Docker Compose with all services |
| **Production** | Kubernetes with StatefulSets for databases |
| **State Management** | Stateless design, external state storage |

This design balances **simplicity** with **production-readiness** while maintaining the flexibility to scale and evolve.
