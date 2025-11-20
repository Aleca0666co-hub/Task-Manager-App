# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).


## [0.1.0] - 2025-11-15
### Added
- Bootstrap of FastAPI + SQLAlchemy project
- Minimal functional endpoints for basic operations
- `settings.py` for centralized configuration and environment variable management via `.env`
- Logging system with file output in `/logs` directory for error tracking
- Refactored CRUD logic for better maintainability using try-except blocks
- `GET` endpoint to search tasks by name

### Changed
- Replaced logging calls inside except blocks with logger.exception(...) to capture full tracebacks for better debugging.
