# Probable-Giggle

Probable-Giggle is a comprehensive CLI-based learning and management tool that empowers users to tackle LeetCode problems systematically. With dynamic scheduling, progress tracking, and rich visualizations, it optimizes your preparation for coding interviews and competitive programming.

## Table of Contents
- [Features](#features)
- [Setup](#setup)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
- [Usage](#usage)
   - [CLI Commands](#cli-commands)
   - [Example Workflows](#example-workflows)
- [Detailed Modules](#detailed-modules)
- [Configuration](#configuration)
   - [Rationale for Configurations](#rationale-for-configurations)
- [Using --help](#using---help)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features
- **Spaced Repetition:** Adaptive scheduling of problem reviews to ensure retention and mastery.
- **Dynamic Problem Prioritization:** Adjusts problem schedules based on difficulty, mastery level, and frequency.
- **Comprehensive Progress Tracking:** Logs attempts, successes, hints used, and time spent for every problem.
- **Detailed Analytics:**
   - Success rate trends over time.
   - Mastery progress by topic and difficulty.
   - Problem-solving efficiency metrics.
- **Customizable Settings:** Fine-tune scoring weights, thresholds, and intervals for a personalized experience.
- **Rich Visualizations:** Generate graphs and charts to understand your performance and areas of improvement.
- **Interactive CLI:** Seamlessly manage problems, track progress, and explore analytics with user-friendly commands.

## Setup

### Prerequisites
- Python 3.8 or higher
- SQLite (included with Python)
- Required Python libraries (install via `requirements.txt`)

### Installation
Clone the repository:
```sh
git clone https://github.com/philip068/probable-giggle.git
cd leetcode-mastery
```

Install dependencies:
```sh
pip install -r requirements.txt
```

Initialize the database:
```sh
python db_init.py
```

"""
Optional but recommended: Seed the database with `add_problems.py` since it uses `sample_problems.py`.
This can speed up CLI readiness for usefulness.
"""

## Usage

### CLI Commands

#### Database Management
Initialize or Reset Database:
```sh
python cli.py reset
```

#### Problem Management
Add a Problem:
```sh
python cli.py problem add
```

Bulk Add Problems:
```sh
python add_problems.py
```

List Problems:
```sh
python cli.py problem list --difficulty Medium --topic Array
```

#### Progress Tracking
View Overall Progress:
```sh
python cli.py view-progress
```

Simulate Problem Mastery (Testing Feature):
** this can be useful to manually alter problem progressions
```sh
python simulate_mastery.py --problem-id <ID> --attempts <NUM> --successes <NUM>
```

#### Visualization
Generate Visual Insights:
```sh
python cli.py visualize
```

#### Daily Scheduler
Get Today’s Problems:
```sh
python cli.py today
```

### Example Workflows
Add Problems and Track Progress:
```sh
python cli.py problem add
python cli.py view-progress
```

Analyze Weak Topics:
```sh
python cli.py problem list --topic "Dynamic Programming"
python cli.py today
```

Visualize Success Trends:
```sh
python cli.py visualize
```

## Detailed Modules

### Key Modules and Their Roles

#### Database Initialization (`db_init.py`)
- Sets up database schemas for topics, problems, patterns, and progress.
- Handles resetting and re-initializing the database.

#### Problem Management (`add_problems.py`, `list_problems_by_topic.py`)
- Add, list, and validate problems with metadata like patterns, difficulty, and prerequisites.

#### Dynamic Scheduler (`scheduler.py`)
- Implements adaptive scheduling based on spaced repetition and mastery.
- Integrates user performance to prioritize future problems dynamically.

#### Progress Tracker (`view_progress.py`)
- Tracks attempts, successes, hints used, and mastery for every problem.
- Aggregates statistics by topic and difficulty.

#### Visualization Tools (`visualize_progress.py`)
- Generate success trends, topic-wise mastery, and difficulty analysis charts.
- Supports saving graphs for detailed reporting.

#### Configuration Manager (`config.ini`)
- Central repository for adjustable thresholds and weights.

#### Logging Utilities (`logger.py`)
- Ensures every action and error is logged for debugging and review.

## Configuration

Settings can be customized in the `config.ini` file:

### Database Configuration:
```ini
[Database]
db_path = leetcode_mastery.db
```

### Scheduling Settings:
```ini
[Scheduling]
spaced_intervals = 1,3,7,14,30
mastery_threshold_ratio = 0.8
min_attempts_for_mastery = 3
```

### Scoring Weights:
```ini
[Scoring]
difficulty_weight_multiplier = 2
pattern_weight_multiplier = 1.5
frequency_weight_multiplier = 2.0
base_urgency_score = 5.0
attempt_penalty = 0.1
hints_factor = 1.0
topic_priority_offset = 20
```

### Rationale for Configurations

#### Database Path
- **Purpose:** Specifies the location of the SQLite database file to store problems and progress data.
- **Why:** Centralized data management ensures consistency across CLI commands.

#### Scheduling Settings
- **Spaced Intervals:** Defines review intervals (1, 3, 7, 14, 30 days).
   - **Why:** Based on spaced repetition theory to reinforce long-term memory.
- **Mastery Threshold Ratio:** A ratio (e.g., 0.8) indicating the success rate required to master a problem.
   - **Why:** Ensures users consistently succeed before marking problems as mastered.
- **Minimum Attempts for Mastery:** Sets a floor for how many times a problem must be attempted before mastery is considered.
   - **Why:** Prevents premature mastery classification from occasional success.

#### Scoring Weights
- **Difficulty Weight Multiplier:** Increases priority for harder problems.
   - **Why:** Aligns focus with challenging areas to maximize learning impact.
- **Pattern and Frequency Multipliers:** Prioritizes frequent or pattern-rich problems to align with industry trends.
   - **Why:** Emphasizes real-world relevance.
- **Base Urgency Score:** Default score applied to new or unsolved problems.
   - **Why:** Encourages initial focus on neglected areas.
- **Hints and Attempt Penalties:** Adjust scores for over-reliance on hints or repeated attempts.
   - **Why:** Drives better problem-solving habits.

## Using --help

The `--help` flag is available for all CLI commands to guide users through usage and options. For example:

### Global Help:
```sh
python cli.py --help
```
Displays a summary of all available commands and their purpose.

### Command-Specific Help:
View options and descriptions for a specific command:
```sh
python cli.py problem add --help
```
Provides detailed guidance for using the `add` subcommand under `problem`.

### Interactive Prompts:
For commands like `add` and `today`, users are guided through prompts to input required data.

**Tip:** Always use `--help` if unsure about a command's syntax or options. It ensures correct usage and prevents errors.

## Troubleshooting

### Common Issues and Resolutions

#### Database Not Found:
Ensure `config.ini` has the correct path:
```ini
db_path = leetcode_mastery.db
```
Reinitialize if necessary:
```sh
python db_init.py
```

#### Dependencies Missing:
Install required libraries:
```sh
pip install -r requirements.txt
```

#### Visualization Issues:
Ensure `matplotlib` is installed:
```sh
pip install matplotlib
```

#### CLI Command Errors:
Verify correct syntax and parameters:
```sh
python cli.py --help
```

## Contributing

We welcome contributions to enhance this tool:

Fork the repository and create a new branch:
```sh
git checkout -b feature-name
```

Commit and push your changes:
```sh
git commit -m "Add feature-name"
git push origin feature-name
```

Submit a pull request with detailed explanations of your changes.

## License
This project is licensed under the MIT License. See the LICENSE file for full details.

## Contact

For feedback, feature requests, or bug reports, please open an issue on GitHub or reach out to the project maintainer via email.