"""
Batch process multiple stocks from a CSV file.

Input CSV format:
    Symbol,Stock Name
    NYSE:WM,Waste Management Inc
    NASDAQ:ADP,Automatic Data Processing Inc

Output CSV format:
    Symbol,Stock Name,Trade Date,Decision,Status,Error Message,Full Decision Text
"""

import csv
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from dotenv import load_dotenv


def read_input_csv(input_file: str) -> List[Dict[str, str]]:
    """Read stocks from input CSV file."""
    stocks = []
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            stocks.append({
                'symbol': row['Symbol'].strip(),
                'name': row['Stock Name'].strip()
            })
    return stocks


def write_output_csv(output_file: str, results: List[Dict[str, Any]]):
    """Write results to output CSV file."""
    fieldnames = ['Symbol', 'Stock Name', 'Trade Date', 'Decision', 'Status', 'Error Message', 'Full Decision Text']
    
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


def process_stocks(stocks: List[Dict[str, str]], trade_date: str, config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Process all stocks and return results."""
    # Initialize TradingAgentsGraph once
    print("Initializing Trading Agents...")
    ta = TradingAgentsGraph(debug=False, config=config)
    print("Trading Agents initialized successfully!\n")
    
    results = []
    total = len(stocks)
    
    for idx, stock in enumerate(stocks, 1):
        symbol = stock['symbol']
        name = stock['name']
        
        print(f"[{idx}/{total}] Processing {symbol} ({name})...")
        
        result = {
            'Symbol': symbol,
            'Stock Name': name,
            'Trade Date': trade_date,
            'Decision': '',
            'Status': '',
            'Error Message': '',
            'Full Decision Text': ''
        }
        
        try:
            # Run the trading agent for this stock
            final_state, decision = ta.propagate(symbol, trade_date)
            
            # Extract decision information
            result['Decision'] = decision.strip()
            result['Status'] = 'Success'
            result['Full Decision Text'] = final_state.get('final_trade_decision', '')[:500]  # First 500 chars
            
            print(f"  ✓ Decision: {decision}")
            
        except Exception as e:
            # Handle errors gracefully
            result['Status'] = 'Error'
            result['Error Message'] = str(e)[:200]  # Limit error message length
            print(f"  ✗ Error: {str(e)}")
        
        results.append(result)
        print()  # Empty line for readability
    
    return results


def print_summary(results: List[Dict[str, Any]]):
    """Print summary statistics."""
    total = len(results)
    successful = sum(1 for r in results if r['Status'] == 'Success')
    failed = total - successful
    
    # Count decisions
    buy_count = sum(1 for r in results if 'BUY' in r['Decision'].upper())
    sell_count = sum(1 for r in results if 'SELL' in r['Decision'].upper())
    hold_count = sum(1 for r in results if 'HOLD' in r['Decision'].upper())
    
    print("=" * 60)
    print("BATCH PROCESSING SUMMARY")
    print("=" * 60)
    print(f"Total stocks processed: {total}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print()
    print("Trading Decisions:")
    print(f"  BUY:  {buy_count}")
    print(f"  SELL: {sell_count}")
    print(f"  HOLD: {hold_count}")
    print("=" * 60)


def main():
    """Main function to run batch processing."""
    # Load environment variables
    load_dotenv()
    
    # Configuration
    input_file = 'input_stocks.csv'  # Default input file
    output_file = f'output_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    trade_date = datetime.now().strftime("%Y-%m-%d")  # Use today's date
    
    # Allow command line arguments
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    if len(sys.argv) > 3:
        trade_date = sys.argv[3]
    
    # Verify input file exists
    if not Path(input_file).exists():
        print(f"Error: Input file '{input_file}' not found!")
        print("\nUsage: python batch_process.py [input_file] [output_file] [trade_date]")
        print("Example: python batch_process.py stocks.csv results.csv 2024-05-10")
        sys.exit(1)
    
    # Use the default config from the project
    # Customize to use GPT-5-mini for both deep and quick thinking
    config = DEFAULT_CONFIG.copy()
    config["deep_think_llm"] = "gpt-5-mini"  # Use GPT-5-mini for deep thinking
    config["quick_think_llm"] = "gpt-5-mini"  # Use GPT-5-mini for quick thinking
    # config["max_debate_rounds"] = 1  # Already set in DEFAULT_CONFIG
    
    print("=" * 60)
    print("TRADING AGENTS - BATCH PROCESSOR")
    print("=" * 60)
    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")
    print(f"Trade date: {trade_date}")
    print(f"LLM Model: {config['deep_think_llm']}")
    print("=" * 60)
    print()
    
    # Read input stocks
    print("Reading input stocks...")
    stocks = read_input_csv(input_file)
    print(f"Found {len(stocks)} stocks to process\n")
    
    # Process all stocks
    results = process_stocks(stocks, trade_date, config)
    
    # Write results to CSV
    print(f"Writing results to {output_file}...")
    write_output_csv(output_file, results)
    print(f"Results saved to {output_file}\n")
    
    # Print summary
    print_summary(results)


if __name__ == "__main__":
    main()
