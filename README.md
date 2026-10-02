# Patent Intelligence Assistant

For my Computer Engineering undergraduate thesis, I developed a Question Answering system that used a Multi-Agent architecture to retrieve relevant information from patent databases. In this project, I used React for the frontend and Python (FastAPI) for the backend, as well as an MCP (Model Context Protocol) server to standardize the use of tools by the intelligent agents implemented through the Agno framework. The final goal of the project was, through the intelligence of the agents, to be able to answer complex questions and generate insights for users from a knowledge base as complex as patent documents. Project completed in July 2026, presented as my undergraduate thesis, and receiving the highest possible grade.

## Overview

This project combines a Python backend, a multi-agent reasoning workflow, and a modern Next.js frontend to support patent analysis and retrieval. The system interprets the user query, searches relevant patent information, formulates a technical response, and evaluates answer quality before presenting the result.

## Key Features

- Natural-language patent question answering
- Multi-agent workflow for semantic analysis, patent search, and response generation
- Integration with external patent data sources through MCP-based services
- AI-assisted quality review for answer relevance and consistency
- User-friendly chat interface built with Next.js and React

## Tech Stack

- Backend: Python, FastAPI, Agno, OpenAI / Gemini models
- Frontend: Next.js, React, TypeScript, Tailwind CSS
- Integration: Model Context Protocol (MCP)

## Project Structure

- backend/app/ - API server, prompt definitions, agent logic, and workflow orchestration
- frontend/app/ - chat interface and web application
