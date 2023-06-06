import os

required_env_vars = ['OPENAI_API_KEY', 'NOTION_API_KEY', 'CONTENT_DB_ID', 'NEWSLETTER_WRITER_PROMPT']
missing_env_vars = [var for var in required_env_vars if var not in os.environ or os.environ[var] == ""]

def check_env_vars():
    """
    Verify that all env vars are preset and have been set
    """
    if missing_env_vars:
        error_message = f"""
        Error: Missing environment variable(s): {', '.join(missing_env_vars)}.
        
        To use this application, you need to set the following environment variables:
        {', '.join(required_env_vars)}
        
        Please follow these steps:
        
        1. Export the variables as environment variables:
        
        For Linux/macOS:
        export VARIABLE_NAME=value
        
        For Windows (Command Prompt):
        set VARIABLE_NAME=value
        
        For Windows (PowerShell):
        $env:VARIABLE_NAME="value"
    
        2. Alternatively, you can create a .env file in the project directory and add the following lines:
        
        VARIABLE_NAME=value
        
        Note: Ensure that the .env file is in the same directory as this script.
        """
        raise EnvironmentError(error_message.strip())
