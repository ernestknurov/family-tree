# Family Tree
An intuitive UI tool for creating, editing, storing, and visualizing family trees.

<img width="1281" alt="image" src="https://github.com/ernestknurov/family-tree/assets/100434509/0b1eeb2f-da85-417e-8612-50a8967f9384">

## Overview

Family Tree provides a clear user interface that allows users to store, edit, and locate their relatives within a database. It visualizes family connections through a graph tree, making it easier to understand familial relationships.

## Getting Started

Follow these instructions to get Family Tree set up and running on your local machine.

### Prerequisites

Before running the project, ensure you have the following installed:

- Python (version 3.10 or later)
- Poetry (Dependency Management for Python)

### Configuration

Before starting the application, you need to create a `person.json` file which will store the data of relatives. Follow these steps:

1. Create a file named person.json in a secure and accessible location on your machine.
2. Add your relatives' data to `person.json`.
3. Configure the path to `person.json` by creating or editing the `.streamlit/secrets.toml` file in your project directory. Add the following line, replacing <path_to_your_file> with the actual path to person.json:
   
```toml
path_to_database = "<path_to_your_file>"
```

#### Notion Integration (Optional)

To sync your family tree with a Notion database:

1. Create a Notion integration at https://www.notion.so/my-integrations
2. Create a database in Notion with the appropriate properties to store person data
3. Share your database with the integration you created
4. Add your Notion API key and database ID to `.streamlit/secrets.toml`:

```toml
notion_api_key = "your-notion-api-key"
notion_database_id = "your-notion-database-id"
```

### Installation

Clone the project and install the required libraries:

```bash
git clone https://github.com/ernestknurov/family-tree.git
cd family-tree
poetry shell
poetry install
```

### Usage

Run the application using the following command:

```bash
poetry run streamlit run app.py
```

### Features

- Create, edit, and delete person records in your family tree
- Search for people by name and surname
- Visualize family connections through a graph
- Backup your data automatically when making changes
- Sync your family tree with a Notion database (new!)
