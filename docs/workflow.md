# End-to-End Workflow

## Setup Phase
1. **Environment Setup**
   - Install dependencies from `requirements.txt`
   - Set up environment variables in `.env`
   - Start Qdrant server

2. **Data Preparation**
   - Place raw documents in `data/raw/` (reports, meeting_notes, decisions)
   - Place images in `data/raw/images/`
   - Process documents into JSON format with modality metadata
   - Generate unified metadata for text and images

3. **System Initialization**
   - Run `scripts/setup_qdrant.py` to create collections
   - Run `scripts/ingest_data.py` to populate database with text and images

## Query Phase
1. **User Query**
   - User submits text query via API, CLI, or Streamlit frontend

2. **Query Processing**
   - Query converted to CLIP text vector embedding
   - Semantic search performed across unified vector space (text + images)
   - Metadata filters applied (department, date, type, etc.)

3. **Multimodal Retrieval**
   - Relevant historical records retrieved (text documents + images)
   - Memories structured and validated with modality information

4. **Reasoning & Synthesis**
   - Retrieved multimodal memories fed to reasoning engine
   - AI generates analysis and recommendations referencing both text and images
   - Response structured for clarity with image captions and sources

5. **Response Generation**
   - Comprehensive answer returned with text summaries and image references
   - Includes source memories, modality types, and explanations

## Ingest Phase
1. **Content Submission**
   - User submits text or image via API or frontend

2. **Processing**
   - Text: Generate CLIP text embedding
   - Image: Generate CLIP vision embedding
   - Add metadata (department, date, type, tags)

3. **Storage**
   - Store vector and metadata in Qdrant collection
   - Enable immediate searchability

## Maintenance Phase
- **Data Updates**: New documents and images can be ingested incrementally
- **Model Updates**: CLIP embeddings remain consistent across modalities
- **Performance Monitoring**: Query logs and response times tracked

## Example Workflow
```
User Query (text) → API/Frontend → CLIP Text Embedding → Qdrant Multimodal Search → Memory Retrieval (text+images) → AI Reasoning → Structured Response (text + image refs)
```

## Qdrant Vector Retrieval + Metadata Filtering
- **Collection**: Single "memories" collection with 512D CLIP vectors
- **Search**: Cosine similarity across text and image embeddings
- **Filtering**: Department, date range, outcome, type (text/image), tags
- **Results**: Top-k similar items with full metadata and content references