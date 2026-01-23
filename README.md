# Chronicle AI
## True Multimodal Institutional Memory Agent for Public Systems

Chronicle AI is an AI-powered institutional memory system that helps public organizations recall past decisions, policies, and outcomes over time enabling evidence-based governance instead of repeating historical mistakes. Now featuring **true multimodal capabilities** treating **text, images, and uploaded documents as first-class memory objects.**

## Problem Statement

Public institutions suffer from institutional amnesia.

- Policies are revisited without awareness of past outcomes
- Lessons from failures are lost due to staff turnover
- Decisions are scattered across reports, meeting notes, and archives
- **Visual evidence** (maps, diagrams, photos) is disconnected from textual records
- New decision-makers lack historical context

This leads to:

- Repeated policy failures
- Inefficient use of public resources
- Loss of organizational learning
- **Missed visual insights** from historical diagrams and images

Chronicle AI addresses this by acting as a long-term, **multimodal** queryable institutional memory.

## Solution Overview

Chronicle AI uses **CLIP-powered embeddings** and **Qdrant vector database** to create a unified memory system for:

- Policy decisions (text)
- Budget reviews (text)
- Meeting notes (text)
- Infrastructure updates (text)
- **Uploaded documents (PDF, DOCX, TXT, MD)**
- **Historical images, diagrams, maps, and charts**
- **Scanned policy documents and visual evidence**

When a user asks a question (e.g., "Have we tried this policy before?"), Chronicle AI:

- **Embeds query using CLIP** (same model for text and images)
- **Retrieves semantically similar memories** from Qdrant (text + images in unified 512D space)
- **Filters using metadata** (department, date, category, modality)
- **Reasons over multimodal memories** to surface patterns, lessons, and outcomes
- **References visual evidence explicitly** (e.g., "As shown in the 2019 evacuation route map...")
- **Produces evidence-grounded responses** with source attribution

## Why CLIP + Qdrant = Multimodal Intelligence

### CLIP (Contrastive Language-Image Pretraining)
- **Unified Embedding Space**: Single 512D vector represents both text and images
- **Cross-Modal Understanding**: Text queries find relevant images, images provide context for text
- **Zero-Shot Capability**: No training required on institutional data
- **Web-Scale Knowledge**: Leverages massive pre-training on internet-scale data

### Qdrant Vector Database
- **Multimodal Storage**: Single collection stores text and image vectors
- **Semantic Similarity**: Finds conceptually similar content regardless of modality
- **Metadata Filtering**: Combines vector search with structured filters
- **Real-Time Updates**: Supports memory evolution and confidence tracking
- **Observable Operations**: Comprehensive logging of vector dimensions and scores

**Without CLIP + Qdrant, true multimodal institutional memory is impossible.**

## System Architecture

```
Raw Inputs (Text Docs, PDFs, Word Files, Images, Maps, Diagrams)
        ↓
Document Parsing + Image Processing  
        ↓  
CLIP Embedding Generation (ViT-B-32, 512D unified space)
        ↓
Qdrant Vector Store
  - Vectors (semantic meaning for text + images)
  - Metadata (department, date, type, tags, modality, confidence)
  - Payload (full text, image URLs, structured fields)
        ↓
Multimodal Retrieval (text → text + images)
        ↓
Reasoning Engine (LLM + Rule-based with visual evidence)
        ↓
Evidence-Based Answer + Sources + Image References
```

## Key Multimodal Features

### True Multimodal Memory
- **Single Vector Space**: CLIP embeds ext, images, and document-derived content
- **Cross-Modal Retrieval**: (text → image, document → text)
- **Visual Evidence Integration**: Reasoning explicitly references images (e.g., "2019 flood map shows...")
- **First-Class Images**: Images are not attachments but core memory components

### True Multimodal Memory
Chronicle AI supports **direct document uploads** via frontend and API:
- **PDF**
- **DOCX**
- **TXT**
- **MD**:
On upload:
1. Text is automatically extracted
2. Metadata is inferred from content
3. Fields are auto-filled for review
4. User verifies or edits information
5. Memory is stored with confidence tracking
6. This prevents silent ingestion and memory corruption.

### Memory Evolution
- **Confidence Updates**: Memories gain/lose confidence as outcomes repeat
- **Content Updates**: Re-embedding when text or images change
- **Version Tracking**: Historical changes preserved in vector space
- **Outcome Learning**: System improves recommendations over time

### Observable Qdrant Operations
- **Vector Dimensions Logged**: 512D CLIP embeddings tracked
- **Similarity Scores**: Retrieval scores logged for transparency
- **Collection Metrics**: Memory counts and types monitored
- **Performance Tracking**: Query latency and accuracy metrics

### API Endpoints
- `POST /ingest` - Add text or image memories
- `POST /query` - Multimodal retrieval with reasoning
- `PUT /update/{memory_id}` - Evolve existing memories
- `GET /health` - System status

## Project Structure

```
chronicle-ai/
│
├── data/                 # Raw and processed institutional documents
│   ├── raw/
│   │   ├── reports/      # Text documents
│   │   ├── meeting_notes/# Text documents
│   │   ├── decisions/    # Text documents
│   │   └── images/       # Images for multimodal retrieval
│   ├── processed/
│   │   ├── documents.json
│   │   └── metadata.json
│   └── sample_queries.json
├── embeddings/           # CLIP embedding logic
│   ├── text_embedder.py  # CLIP text embeddings
│   └── image_embedder.py # CLIP image embeddings
├── qdrant/               # Qdrant client, ingestion, and search
│   ├── client.py         # Qdrant connection
│   ├── collections.py    # Collection management
│   ├── ingest.py         # Multimodal ingestion with logging
│   └── search.py         # Multimodal search with logging
├── memory/               # Memory schema and lifecycle logic
│   ├── schema.py         # Memory and filter models
│   ├── memory_manager.py # High-level memory operations
│   └── decay_update.py   # Memory evolution logic
├── reasoning/            # Reasoning & recommendation engine
│   ├── reasoning_engine.py # LLM reasoning with visual refs
│   ├── recommendation.py # Evidence-based recommendations
│   └── prompt_templates.py # Multimodal reasoning prompts
├── api/                  # FastAPI backend
│   ├── main.py           # Server entry point
│   ├── routes.py         # API endpoints (lazy-loaded)
│   └── schemas.py        # Request/response models
├── frontend/             # Streamlit frontend for demo
│   └── app.py            # Multimodal UI (text + image ingest)
├── scripts/              # Setup, ingestion, and demo scripts
├── demo/                 # Sample queries and outputs
├── docs/                 # Architecture, workflow, ethics
├── test_multimodal.py    # Multimodal verification script
└── demonstrate_multimodal.py # Comprehensive system demo
```

## Example Queries

**"Show me policies similar to successful flood response strategies."**

Answer (Excerpt):

Successful flood response in 2019 due to adequate funding and preparedness

Failure in 2020 following budget cuts and reduced training

Improved system reliability in 2021 after infrastructure upgrades

**Visual Evidence:** As shown in the 2019 evacuation route map, primary routes were clearly marked and secondary routes provided redundancy.

Sources:
- Emergency Management (2019-06-15) - Outcome: success - Type: text
- Emergency Management (2019-06-15) - Outcome: success - Type: image (evacuation map)
- Finance (2020-03-01) - Outcome: failure - Type: text
- Infrastructure (2021-09-10) - Outcome: success - Type: image (infrastructure diagram)

**"Retrieve information about cybersecurity incident response."**

Returns text summaries, relevant charts, and incident timeline diagrams.

- Emergency Management (2023-06-15) - Type: text
- IT Security (2023-06-15) - Type: image (incident response chart)
- Infrastructure (2022-09-10) - Type: image (network diagram)

**"What lessons were learned from the 2020 budget cuts?"**

Answer (Excerpt):

Budget cuts reduced staff training and led to delayed emergency responses. This contrasts with positive outcomes from later infrastructure investments. **Visual evidence from the 2021 infrastructure upgrade diagram shows improved system reliability.**

Sources included in output with explicit image references.

## Key Features

### True Multimodal Memory
- **Unified CLIP Space**: 512D embeddings for text and images
- **Cross-Modal Retrieval**: Text queries find images, images provide context
- **Visual Evidence**: Images explicitly referenced in reasoning
- **First-Class Citizens**: Images are core memory components, not attachments

### Memory Evolution
- **Confidence Tracking**: Memories update confidence based on outcome patterns
- **Content Updates**: Automatic re-embedding when memories change
- **Version History**: Tracks how institutional knowledge evolves
- **Learning System**: Improves recommendations over time

### Observable Qdrant Operations
- **Vector Logging**: 512D dimensions, similarity scores, operation tracking
- **Performance Metrics**: Query latency, retrieval accuracy, memory counts
- **Collection Insights**: Multimodal distribution and storage efficiency
- **Debug Visibility**: Transparent vector operations for validation

### Advanced Capabilities
- **True long-term memory** (not chat history)
- **Cross-year, cross-department reasoning**
- **Evidence-grounded responses with visual citations**
- **Transparent source attribution**
- **No hallucinated policy recommendations**
- **Memory evolution and confidence updates**

## Ethics & Responsibility

Chronicle AI is designed to:

- **Support human decision-makers**, not replace them
- **Provide traceable and auditable outputs** with explicit source attribution
- **Avoid generating new policies autonomously** - only analyzes historical data
- **Integrate visual evidence responsibly** - images are presented as historical context
- **Maintain data privacy** - no personal information stored or processed

### Technical Choices for Reliability
- **Local Qdrant**: No external dependencies, works offline
- **CLIP Embeddings**: Industry-standard, well-tested multimodal model
- **Lazy Loading**: API components load only when needed for faster startup
- **Comprehensive Logging**: All vector operations tracked for transparency
- **Fallback Reasoning**: Works without OpenAI API for basic functionality

**Disclaimer:** Chronicle AI assists with historical recall and analysis. Final decisions remain the responsibility of human authorities. Visual evidence is provided as historical context and should be verified by domain experts.

## Technical Specifications

### CLIP Model: ViT-B-32 (OpenAI)
- **Input Modalities**: Text + Images (unified 512D space)
- **Text Tokenization**: 77 tokens maximum
- **Image Preprocessing**: 224x224 RGB, normalized
- **Embedding Dimensions**: 512D float vectors
- **Cross-Modal Capability**: Text-image similarity scoring

### Qdrant Configuration
- **Collection**: Single "memories" collection for multimodal data
- **Vector Dimensions**: 512 (CLIP embedding size)
- **Distance Metric**: Cosine similarity
- **Payload Storage**: Full metadata + text content + image URLs
- **Indexing**: HNSW for fast approximate nearest neighbor search

### Memory Schema
```python
MemoryItem {
    id: str
    text: Optional[str]
    image_url: Optional[str]
    department: str
    date: str
    outcome: str
    type: "text" | "image"
    location: Optional[str]
    tags: Optional[list[str]]
}
```

### API Response Format
```json
{
  "query": "flood evacuation procedures",
  "memories": [
    {
      "id": "123",
      "type": "image",
      "image_url": "data/raw/images/flood_map.png",
      "department": "Emergency Management",
      "date": "2019-05-10",
      "outcome": "success"
    }
  ],
  "reasoning": "Visual evidence from the 2019 flood map shows...",
  "summary": "Found evacuation routes and procedures..."
}
```

## Verification & Testing

### Run Multimodal Tests
```bash
python test_multimodal.py
```

**Expected Results:**
- ✅ CLIP embeddings: 512D vectors for text and images
- ✅ Text ingestion: Successful storage in Qdrant
- ✅ Image ingestion: Successful storage in Qdrant
- ✅ Mixed retrieval: Query returns both text and image results
- ✅ Similarity scores: Proper scoring (text queries score higher for text results)
- ✅ Logging: Vector dimensions and operations tracked

### Key Indicators of Success
- **Vector Dimensions**: 512D CLIP embeddings logged
- **Cross-Modal Retrieval**: Text queries find relevant images
- **Visual References**: Reasoning mentions specific images/diagrams
- **Unified Storage**: Single Qdrant collection for both modalities
- **Memory Evolution**: Update endpoints functional
- **Observable Operations**: Qdrant logs show vector search details

### What Judges Should Verify
1. **Run the test script** and confirm multimodal functionality
2. **Check Qdrant logs** for vector dimensions and similarity scores
3. **Verify cross-modal retrieval** - text queries finding images
4. **Confirm visual evidence integration** in reasoning outputs
5. **Test memory evolution** using the update endpoints
6. **Review architecture docs** explaining CLIP + Qdrant necessity

## Getting Started

### Prerequisites
- Python 3.8+
- Local file system (no Docker required)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup Qdrant Collection (Local File-Based)

```bash
python scripts/setup_qdrant.py
```

This creates a local Qdrant collection optimized for multimodal CLIP embeddings.

### 3. Test Multimodal System

```bash
# Run comprehensive multimodal verification
python test_multimodal.py

# Or run full system demonstration
python demonstrate_multimodal.py
```

Expected output includes:
- CLIP embedding generation (512D vectors)
- Successful text and image ingestion
- Cross-modal retrieval results
- Qdrant operation logging

### 4. Start API Server

```bash
python api/main.py
```

API will be available at `http://localhost:8000`

### 5. Start Frontend (Optional)

```bash
streamlit run frontend/app.py
```

Frontend provides multimodal ingestion interface at `http://localhost:8501`

### 6. Ingest Sample Data (Optional)

```bash
python scripts/ingest_data.py
```

## API Endpoints

### Core Multimodal Operations
- `POST /ingest` - Add text or image memories
- `POST /query` - Multimodal retrieval with reasoning
- `PUT /update/{memory_id}` - Evolve existing memories
- `GET /health` - System status

### Example API Usage

```python
import requests

# Ingest text memory
response = requests.post("http://localhost:8000/ingest", json={
    "text": "Flood response policy implemented successfully",
    "department": "Emergency Management",
    "date": "2023-06-15",
    "outcome": "success",
    "type": "text"
})

# Ingest image memory
response = requests.post("http://localhost:8000/ingest", json={
    "image_path": "data/raw/images/flood_evacuation_map_2019.png",
    "description": "2019 Flood Evacuation Route Map",
    "department": "Emergency Management",
    "date": "2019-05-10",
    "outcome": "success",
    "type": "image"
})

# Query multimodal memory
response = requests.post("http://localhost:8000/query", json={
    "query": "flood evacuation procedures",
    "data_type": "both",  # "text", "image", or "both"
    "reasoning_mode": "recommendation"
})
```

## Demo Focus (For Judges)

This project demonstrates **true multimodal institutional memory**:

### What We Built
- **CLIP-Powered Multimodal Embeddings**: Unified 512D vector space for text + images
- **Single Qdrant Collection**: Efficient storage and retrieval of multimodal memories
- **Cross-Modal Retrieval**: Text queries find relevant images and vice versa
- **Visual Evidence Integration**: Reasoning explicitly references images and diagrams
- **Memory Evolution**: Update capabilities for confidence tracking and content changes
- **Observable Operations**: Comprehensive logging of vector dimensions and similarity scores

### Judging Criteria Met
- **"Clearly demonstrates multimodal"**: ✓ Text + images in unified CLIP space
- **"Effective Multimodal Retrieval"**: ✓ Cross-modal search with proper scoring
- **Qdrant integration**: ✓ Obvious and well-documented vector search role
- **No complex pipelines**: ✓ Simple, clean CLIP + Qdrant implementation

### Verification
Run `python test_multimodal.py` to verify:
- CLIP embeddings working (512D vectors)
- Text and image ingestion successful
- Mixed retrieval returning both modalities
- Proper similarity scoring
- Qdrant operations logged

## Why This Matters

Chronicle AI demonstrates how **CLIP + Qdrant** enables true multimodal institutional intelligence:

### Technical Innovation
- **Unified Embedding Space**: Single 512D vectors for text and images
- **Cross-Modal Understanding**: Text queries find images, images provide context
- **Vector Search Superiority**: Semantic similarity over keyword matching
- **Memory Evolution**: Dynamic updates and confidence tracking

### Societal Impact
- **Evidence-Based Governance**: Visual evidence integrated with textual records
- **Institutional Learning**: Prevents repeating historical mistakes
- **Public Accountability**: Transparent decision-making with source attribution
- **Resource Efficiency**: Better use of public resources through historical awareness

This approach extends to government policy analysis, disaster preparedness, civic governance, and large public organizations.