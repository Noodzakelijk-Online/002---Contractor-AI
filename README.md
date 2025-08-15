# Manus - AI-Powered Field Service Assistant

This repository contains the source code for Manus, an AI-powered platform designed to automate the operational management of a field service business.

## Project Structure

This is a monorepo containing two main projects:

-   `/backend`: The AI Brain. A Python application built with FastAPI that houses all the business logic, state management, and AI integrations.
-   `/frontend`: The Command Center. A React application built with Vite that serves as the user interface for the contractor.

## Getting Started

### Backend

1.  Navigate to the `backend` directory: `cd backend`
2.  Create a virtual environment: `python -m venv venv`
3.  Activate the virtual environment: `source venv/bin/activate`
4.  Install the dependencies: `pip install -r requirements.txt`
5.  Run the development server: `uvicorn main:app --reload`

### Frontend

1.  Navigate to the `frontend` directory: `cd frontend`
2.  Install the dependencies: `npm install`
3.  Run the development server: `npm run dev`
