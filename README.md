# 🌊 Offshore Risk Intelligence Agent

AI-powered risk management system for offshore industry. Identifies, analyzes, and benchmarks critical risks from global news, vessel data, and industry reports.

**Coverage:** FPSO Hook-ups, Windmill Installation, Cable Laying, Heavy Lift Operations

## Features

- **Global Data Ingestion**: Real-time news feeds, incident databases, regulatory notices
- **Risk Extraction & Classification**: NLP-powered risk identification from unstructured sources
- **Financial Impact Modeling**: Cost, time, and consequence estimation
- **Competitor Benchmarking**: Compare risk exposure across industry operators
- **Monte Carlo Simulation**: Probabilistic risk scenarios (P50/P80/P90/P95)
- **Interactive Dashboard**: Risk matrices, driver relationships, ORR registers
- **Multi-Operation Support**: FPSO, Windmills, Cable, Heavy Lift

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run data pipeline
python -m pipelines.news_ingestion

# Start risk agent
python -m agents.risk_orchestrator

# Launch dashboard
python -m dashboard.server
```

## Project Structure

```
.
├── data/                      # Raw/processed datasets
│   ├── taxonomy/             # Risk classifications
│   ├── incidents/            # Historical incident DB
│   └── benchmarks/           # Industry comparisons
├── agents/                    # AI agent orchestration
│   ├── risk_orchestrator.py  # Main agent controller
│   ├── extractors.py         # Risk extraction from news
│   └── reasoner.py           # Multi-step reasoning
├── models/                    # Risk scoring & simulation
│   ├── taxonomy.py           # Risk classification schema
│   ├── financial_impact.py   # Cost/time modeling
│   └── monte_carlo.py        # Probabilistic simulation
├── pipelines/                 # Data ingestion
│   ├── news_ingestion.py     # News feed processing
│   ├── vessel_tracking.py    # AIS/vessel data
│   └── regulatory.py         # DNV/ABS notices
├── services/                  # APIs & utilities
│   ├── llm_service.py        # LLM integration (Claude/GPT-4)
│   ├── vector_store.py       # Competitor data retrieval
│   └── notifications.py      # Alert system
├── prompts/                   # Agent reasoning templates
│   ├── risk_extraction.md    # Extract risk from news
│   ├── benchmarking.md       # Compare competitor response
│   └── impact_analysis.md    # Financial impact calculation
├── schemas/                   # Data models
│   ├── orr.py               # Opportunity & Risk Register
│   └── incident.py          # Incident schema
├── dashboard/                 # Web UI
│   ├── server.py            # FastAPI backend
│   ├── static/              # React/Vue frontend
│   └── templates/           # HTML templates
└── tests/
    ├── test_agents.py
    └── test_models.py
```

## Risk Taxonomy

### Operation Types
- **FPSO Hook-up**: Installation & station-keeping
- **Windmill Installation**: Foundation, nacelle, blade work
- **Subsea Cable Laying**: Power, comms, umbilical routes
- **Heavy Lift**: Derrick, crane, load-out operations

### Risk Categories
- **Vessel/Equipment**: DP failure, crane breakdown, weather downtime
- **Operational**: Collision, dropped object, interface failures
- **Regulatory**: Compliance changes, permit delays
- **Commercial**: Cost escalation, LD penalties, contract disputes
- **HSE**: Personnel incident, environmental breach
- **Market**: Commodity prices, insurance premiums, currency

## Example Agent Workflow

```python
from agents.risk_orchestrator import OffshoreRiskAgent

agent = OffshoreRiskAgent()

# Analyze a global incident
incident = """
Windmill installation vessel (DP2 class) suffered blackout 
during foundation work, North Sea, Oct 2026. Estimated cost 
impact: €2.5M, 3-day delay. Competitor response: Similar 
vessel downtime, insurance claim processing.
"""

analysis = agent.analyze_incident(
    description=incident,
    operation_type="windmill_installation",
    geography="North Sea"
)

print(f"Risk severity: {analysis.severity}")
print(f"Financial impact: €{analysis.cost_impact_mean} (P95: €{analysis.cost_impact_p95})")
print(f"Industry benchmark: {analysis.peer_comparison}")
print(f"Recommended actions: {analysis.corrective_actions}")
```

## Data Sources

- **Maritime News**: MarineTraffic, VesselFinder, shipping news feeds
- **Regulatory**: DNV GL, ABS, Lloyd's Register, flag states
- **Market**: Bloomberg, Reuters, industry reports
- **Historical**: IMCA DROPS, IOPC Fund, insurance claims
- **Company Data**: Internal incident logs, contracts, vessel specs

## Dashboard Sections

1. **Tender Overview**: Project context, assets, timeline
2. **Executive Risk**: Risk budget distribution (P50/P80/P95)
3. **Driver Relationships**: Frequency vs impact scatter, correlation analysis
4. **ORR Register**: Full risk register with filtering & drill-down
5. **Simulation**: Monte Carlo methodology, diagnostics
6. **Benchmarking**: How peers handle similar risks

## Simulation Output

- **Mean Risk Budget**: Expected total cost/time impact
- **Percentiles**: P50 (median), P80 (planning), P95 (contingency)
- **Distribution Shape**: Skewness, tail behavior, negative probability
- **Driver Contribution**: Which risks drive the output?
- **WBS Analysis**: By project workstream

## API Endpoints

```
GET  /api/risks
POST /api/risks/analyze
GET  /api/incidents
GET  /api/benchmarks/{competitor}
GET  /api/dashboard/{project_id}
WS   /api/alerts  # WebSocket for real-time updates
```

## Configuration

```bash
# .env
LLM_PROVIDER=claude  # or gpt-4, llama
LLM_API_KEY=sk-...
VECTOR_DB_URL=pinecone://...
NEWS_API_KEYS=...
AIS_API_KEY=...
```

## Development

```bash
# Run tests
pytest

# Format code
black .

# Type checking
mypy .

# Build dashboard
npm run build --prefix dashboard
```

## License

Proprietary

## Contact

Manish Singh | Risk Intelligence Team
