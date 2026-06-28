# MASTER_PROMPT.md

# 🚀 CodeForge AI - Persona Driven Multi-Agent Software Engineering Platform

## ROLE

You are a Principal AI Engineer and Software Architect with over 15 years of experience building production-grade AI systems.

You specialize in:

- LangGraph
- LangChain
- Multi-Agent Systems
- ChatGroq
- FastAPI
- React
- Software Architecture
- Python
- Java
- SQL
- JavaScript
- TypeScript
- PySpark
- Prompt Engineering
- System Design
- Clean Code
- Design Patterns

Your responsibility is NOT simply generating code.

Your responsibility is to architect and build a production-ready AI Software Engineering Platform suitable for winning an AI Hackathon.

The output must be modular, scalable, reusable, maintainable and presentation-ready.

---

# CONTEXT

I am participating in an AI Hackathon.

The challenge is to build a **Natural Language → Code Generation Multi-Agent System**.

However, instead of creating a simple code generator, I want to build an AI Software Engineering Team.

The system should convert natural language into production-quality code using multiple collaborating AI agents.

The project should demonstrate advanced AI Engineering concepts while remaining implementable within a hackathon timeline.

The architecture should impress judges through modularity, extensibility, explainability and engineering best practices.

---

# OBJECTIVE

Build **CodeForge AI**

A Persona-Driven Multi-Agent AI Software Engineering Platform capable of generating, reviewing, optimizing, testing and explaining code.

The platform must support multiple programming languages, multiple developer personas and automatic software engineering workflows.

---

# TECH STACK

## Backend

Python

FastAPI

LangGraph

LangChain

ChatGroq

Pydantic

TypedDict

FAISS

HuggingFace Embeddings

Python REPL Tool

SQLAlchemy

Pytest

Docker

Logging

Environment Variables

Configuration Management

---

## Frontend

React

TypeScript

TailwindCSS

Shadcn UI

Monaco Editor

Framer Motion

React Flow

Axios

WebSockets

Dark Mode

Responsive Design

---

# LLM

Use GROQ API.

Design reusable wrappers so models can be swapped easily.

Supported models include

- Llama 3.x
- DeepSeek
- Qwen
- Mixtral
- Gemma

---

# PROGRAMMING LANGUAGES

Support the following languages.

- Python
- SQL
- Java
- JavaScript
- TypeScript
- C++
- Go
- Bash
- PySpark

The Router Agent should automatically determine the requested language and route the request to the appropriate specialist.

---

# PERSONA ENGINE

The platform must support multiple developer personas.

Each persona should influence:

- Prompting
- Code style
- Documentation
- Complexity
- Review standards
- Explanation style
- Testing strategy

Supported personas include:

## 1. Interview Preparation

Generate:

- Brute Force
- Better Approach
- Optimal Solution
- Dry Run
- Complexity Analysis
- Interview Tips
- Follow-up Questions

---

## 2. Product Ready Engineer

Generate

- Enterprise Architecture
- Logging
- Exception Handling
- SOLID Principles
- Configuration Management
- Security
- Documentation
- Modular Code
- CI/CD Friendly Structure

---

## 3. Beginner Developer

Generate

- Beginner-friendly code
- Step-by-step explanation
- More comments
- Simple naming

---

## 4. Mid-Level Engineer

Focus on

- Readability
- Clean Code
- Type Hints
- Unit Testing

---

## 5. Senior Engineer

Generate

- Maintainable code
- Design Patterns
- Performance
- Scalability

---

## 6. Principal Engineer

Generate

- Extensible Architecture
- Distributed Design
- Performance Optimization
- Future-proof Design

---

## 7. Competitive Programmer

Generate

- Fastest Algorithm
- Lowest Memory Usage
- Minimal Code
- Fast IO

---

## 8. Data Engineer

Generate

- SQL
- PySpark
- Pandas
- ETL Pipelines
- Window Functions

---

## 9. AI Engineer

Generate

- LangChain
- LangGraph
- RAG
- Vector Search
- LLM Integrations

---

## 10. Code Mentor

Generate

- Algorithm Explanation
- Code Walkthrough
- Learning Notes
- Practice Questions

---

# MULTI AGENT ARCHITECTURE

Design a LangGraph workflow.

Each agent must have:

- Single Responsibility
- Prompt Template
- Input
- Output
- Typed State
- Error Handling

---

## Agent 1

Router Agent

Responsibilities

- Detect language
- Detect intent
- Detect persona
- Detect ambiguity
- Route workflow

---

## Agent 2

Requirement Extraction Agent

Extract

- Inputs
- Outputs
- Constraints
- Edge Cases
- Libraries
- Functional Requirements
- Non-functional Requirements

Return structured JSON.

---

## Agent 3

Persona Agent

Modify prompts according to selected persona.

---

## Agent 4

Context Retrieval Agent

Optional

Use

- FAISS
- HuggingFace Embeddings

Retrieve relevant coding examples.

---

## Agent 5

Language Specialist Agent

Generate code.

Support

Python

SQL

Java

JavaScript

TypeScript

C++

Go

PySpark

---

## Agent 6

Optimization Agent

This is mandatory.

Responsibilities

Generate

Brute Force Solution

↓

Optimized Solution

↓

Compare

↓

Choose Best Solution

Estimate

Time Complexity

Space Complexity

Memory Usage

Alternative Algorithms

Regenerate if a better solution exists.

---

## Agent 7

Code Review Agent

Review

Readability

Performance

Maintainability

Security

PEP8

Java Standards

SQL Optimization

Best Practices

Correctness

---

## Agent 8

Security Review Agent

Check

SQL Injection

Unsafe Code

Secrets

Input Validation

Authentication Risks

Resource Leaks

---

## Agent 9

Unit Test Generator

Generate

Pytest

JUnit

SQL Test Cases

Edge Cases

Negative Cases

Boundary Cases

---

## Agent 10

Execution Agent

Run

Python

JUnit

SQL Validation

Capture

stdout

stderr

Errors

Tracebacks

---

## Agent 11

Evaluator Agent

Evaluate

Correctness

Completeness

Confidence

Return

PASS

FAIL

Confidence Score

Improvement Suggestions

---

## Agent 12

Explanation Agent

Explain

Algorithm

Complexity

Trade-offs

Alternative Solutions

---

## Agent 13

Documentation Agent

Generate

README

API Docs

Markdown

Mermaid Flowcharts

UML

---

# LANGGRAPH STATE

Create a strongly typed Graph State using TypedDict or Pydantic.

Example

request

persona

language

requirements

generated_code

optimized_code

reviewed_code

security_report

tests

execution_result

evaluation

documentation

---

# FRONTEND

Build a professional React dashboard.

Features

Modern UI

Dark Mode

Responsive Layout

Streaming Responses

Agent Timeline

Workflow Visualization

Mermaid Graph

React Flow Graph

Monaco Code Editor

Syntax Highlighting

Copy Button

Download Code

Download Tests

Download README

Complexity Dashboard

Execution Logs

Model Selector

Persona Selector

Language Selector

Theme Toggle

---

# BACKEND

Use FastAPI.

Create APIs for

/chat

/generate

/review

/test

/evaluate

/persona

/workflow

/models

/download

Use WebSockets for streaming responses.

---

# PROJECT STRUCTURE

Generate a scalable production folder structure.

project/

backend/

frontend/

agents/

graph/

prompts/

models/

tools/

config/

services/

api/

utils/

tests/

docs/

assets/

README.md

requirements.txt

docker-compose.yml

Dockerfile

.env.example

---

# CODE QUALITY

All generated code must include

Type Hints

Docstrings

Logging

Exception Handling

Configuration Management

Dependency Injection where appropriate

No duplicated logic

Modular Architecture

---

# PERFORMANCE

Always generate the most efficient algorithm possible.

Include

Time Complexity

Space Complexity

Memory Optimization

Alternative Algorithms

Trade-offs

---

# TESTING

Automatically generate

Unit Tests

Integration Tests

Edge Cases

Boundary Cases

Performance Tests

---

# DOCUMENTATION

Generate

README

Architecture Diagram

Mermaid Flowcharts

Sequence Diagram

API Documentation

Installation Guide

Deployment Guide

Presentation Notes

---

# PRESENTATION

Generate a professional 10-slide presentation.

Slides

1 Problem Statement

2 Motivation

3 Architecture

4 Multi-Agent Workflow

5 Personas

6 LangGraph

7 Frontend Demo

8 Backend APIs

9 Challenges

10 Future Scope

Include speaker notes.

---

# HACKATHON DIFFERENTIATORS

Highlight

Persona-driven AI

Optimization Agent

Security Review Agent

Live Agent Timeline

Modern React Frontend

Multi-language Support

Best Time Complexity

Best Space Complexity

LangGraph Orchestration

Production Architecture

Documentation Generation

Automatic Testing

Automatic Evaluation

Explainability

---

# DELIVERABLES

Generate the project in phases.

Phase 1

Architecture

Phase 2

Folder Structure

Phase 3

Backend

Phase 4

Frontend

Phase 5

LangGraph

Phase 6

Prompt Templates

Phase 7

API Development

Phase 8

Testing

Phase 9

Documentation

Phase 10

Presentation

Do NOT use placeholders.

Do NOT skip files.

Implement every file completely.

Generate production-quality code throughout.