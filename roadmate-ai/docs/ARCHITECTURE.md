# RoadMate AI Architecture

The browser/mobile client provides text, microphone input, location and optional camera frames. FastAPI exposes REST and WebSocket interfaces. The orchestrator interprets intent and calls isolated tools for Places, Routes, Spotify, RAG and ML ranking.

The included web client provides browser speech recognition and speech synthesis so the project works locally. The production path replaces the local speech loop with Gemini Live for persistent bidirectional audio/video/text sessions while preserving the same tool interfaces.

Places search finds candidate POIs. The recommendation layer ranks results. Routes computes directions and traffic-aware ETA when credentials are configured.

PDF/text documents are chunked and indexed locally with TF-IDF for a dependency-light demo. Production can replace this with Vertex AI embeddings plus a managed vector store.

Every interaction can emit structured events locally and later to Pub/Sub. BigQuery stores analytics/model features for recommendation acceptance, agent latency, tool success and model evaluation.
