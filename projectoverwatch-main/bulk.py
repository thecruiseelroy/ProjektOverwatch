from url_middle_out import process_query
from report_generator import generate_final_report
from agents.openrouter_agent import OpenRouterAgent
import os
import json

def sanitize_filename(text):
    return "".join(c if c.isalnum() else "_" for c in text)

def process_bulk_keywords():
    with open('config.json') as config_file:
        config = json.load(config_file)
    
    agent = OpenRouterAgent(
        config['openrouter']['api_key'],
        config['openrouter']['model']
    )

    with open('bulk_keyword.txt') as f:
        keywords = [line.strip() for line in f if line.strip()]

    for keyword in keywords:
        print(f"\nProcessing keyword: {keyword}")
        folder_name = sanitize_filename(keyword)
        os.makedirs(f'data/{folder_name}', exist_ok=True)
        db_path = f'data/{folder_name}/{sanitize_filename(keyword)}_data.db'
        
        # Process the query and save to database
        process_query(keyword, agent, db_path)
        
        # Generate and save the report
        report = generate_final_report(db_path, agent)
        report_path = f'data/{folder_name}/{sanitize_filename(keyword)}_final_summary.txt'
        with open(report_path, 'w') as report_file:
            report_file.write(report)
        
        print(f"Completed processing and report generation for: {keyword}")

if __name__ == "__main__":
    process_bulk_keywords() 