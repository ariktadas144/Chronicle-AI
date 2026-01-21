# System Architecture

## Overview
The Institutional Memory Agent follows a modular architecture designed for scalability, maintainability, and explainability. Now supports multimodal content including text and images.

## Components

### Data Layer
- **Raw Data**: Institutional documents and images in various formats
- **Processed Data**: Cleaned and structured JSON data with modality metadata
- **Embeddings**: Unified vector representations using CLIP (text + images)

### Vector Database (Qdrant)
- **Storage**: Persistent vector storage with multimodal metadata
- **Search**: Semantic similarity search across text and images with filtering
- **Indexing**: Optimized for fast multimodal retrieval

### Memory Management
- **Schema**: Structured representation of institutional memories (text + images)
- **Retrieval**: High-level memory access with modality and metadata filtering

### Reasoning Layer
- **Prompt Engineering**: Structured prompts for AI reasoning over multimodal data
- **Synthesis**: Combining retrieved memories (text + images) into insights
- **Recommendations**: Evidence-based suggestions with image references

### API Layer
- **REST API**: Query interface using FastAPI for multimodal queries
- **Schemas**: Type-safe request/response models supporting text and images
- **Endpoints**: Query, ingest (text/image), and health check endpoints

### Frontend Layer
- **Streamlit App**: User-friendly interface for querying and ingesting multimodal content
- **Visualization**: Display text summaries, image thumbnails, and metadata

## Data Flow
1. Documents/Images → Processing → CLIP Embeddings → Qdrant Storage
2. Query (text) → CLIP Embedding → Multimodal Search → Retrieval → Reasoning → Response (text + images)

## Embedding Flow per Modality
- **Text Documents**: CLIP text encoder → 512D vector
- **Images**: CLIP vision encoder → 512D vector
- **Query**: CLIP text encoder → Search across all vectors

## Why Vector Search is Critical

### Limitations of Traditional Relational Databases
- **Keyword Matching**: RDBMS can only find exact matches or simple pattern matches
- **Semantic Gap**: Cannot understand meaning, context, or similarity between documents
- **Multimodal Impossibility**: No native support for comparing text descriptions with visual content
- **Query Complexity**: Requires complex JOINs and full-text search extensions for basic similarity

### Vector Search Advantages
- **Semantic Similarity**: Finds conceptually similar content regardless of exact wording
- **Unified Multimodal Space**: Single 512D vector space represents both text and images
- **Contextual Understanding**: Captures nuanced relationships between institutional experiences
- **Efficient Filtering**: Combines semantic search with metadata filters (department, date, outcome)

### CLIP's Role in Multimodal Understanding
- **Joint Embedding Space**: Text and images are embedded in the same vector space
- **Cross-Modal Retrieval**: Text queries can find relevant images, image context aids text understanding
- **Zero-Shot Capability**: No training required on institutional data - leverages web-scale pre-training

### Qdrant's Technical Superiority
- **Vector Dimensions**: Handles 512D CLIP embeddings efficiently
- **Payload Filtering**: Combines vector similarity with metadata constraints
- **Real-time Updates**: Supports dynamic memory evolution and confidence updates
- **Scalability**: Handles millions of multimodal memories with sub-second query times