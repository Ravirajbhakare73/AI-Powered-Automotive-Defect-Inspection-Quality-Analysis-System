#!/bin/bash

echo "Creating project structure..."

# Backend
mkdir -p backend/api
mkdir -p backend/services
mkdir -p backend/utils

touch backend/main.py

touch backend/api/inspection.py
touch backend/api/agent.py

touch backend/services/detector.py
touch backend/services/video_processor.py
touch backend/services/rag.py
touch backend/services/agent.py
touch backend/services/report.py

touch backend/utils/helpers.py


# RAG knowledge base
mkdir -p knowledge

touch knowledge/scratch.md
touch knowledge/dent.md
touch knowledge/crack.md

touch knowledge/fixture_contact.md
touch knowledge/handling_damage.md
touch knowledge/contamination.md
touch knowledge/process_variation.md

touch knowledge/inspection_guidelines.md
touch knowledge/corrective_actions.md


# YOLO model
mkdir -p models


# Utility scripts
mkdir -p scripts
touch scripts/build_knowledge_base.py


# Reports
mkdir -p reports


# Python configuration
touch requirements.txt
touch .env

echo "Project structure created successfully."