# Changelog
All notable changes to this project will be documented in this file.

## v1.6.0

### Added
- Concurrent file organization using ThreadPoolExecutor
- Atomic rollback mechanism for failed operations
- Performance tracking (Transfer Time)
- Persistent JSON-based operation logging for undo functionality
- Dynamic configuration directory handling
- Strict filesystem existence validation for restoration

### Improved
- Structural refactor: decoupled business logic into modular components
- Performance: removed artificial terminal delays
- Reliability: implemented emergency rollback for partial failures
- Data integrity: added file flushing (fsync) for category updates
- Maintenance: isolated log files from scan targets to prevent recursion
- User experience: streamlined category management and configuration persistence


## v1.5.0

### Added
- Undo Last Organization feature
- Operation logging system
- JSON-based organization history
- Undo summary reporting
- Corrupted log detection
- Skipped file protection
- Menu-based startup interface

### Improved
- Safer file organization workflow
- Recovery support after organization
- Automatic cleanup of completed operation logs
- Validation for startup menu selection
- BroccoliFlow log file exclusion during scans


## v1.4.0

### Added
- Duplicate filename protection
- Automatic duplicate renaming
- Duplicate reporting

### Improved
- Safer file organization
- Collision-free file moves


## v1.3.0

### Added
- Automatic file organization
- Category based file sorting
- Category folder creation
- Organization preview system
- Archive file detection
- Installation media detection
- Organization reports

### Improved
- Expanded file extension support
- Better destination path preview
- Improved organization summaries


## v1.2.0 (Internal Milestone)

### Added
- Folder content analysis
- File type detection
- Organization preview system
- File category classification
- Analysis reports

### Improved
- Expanded file extension support
- Better scan statistics
- Root folder identification


## v1.1.0

### Added
- Folder scanning
- Folder structure display
- File and folder counting
- File type detection
- Scan summary reporting

### Improved
- Better folder validation messages
- Alphabetical sorting
- Permission error handling


## v1.0.0

### Added
- Folder path validation
- Basic command line interface
