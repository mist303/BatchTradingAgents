# TradingAgents: Batch Stock Analysis Tool

A batch processing extension for the TradingAgents framework that enables efficient analysis of multiple stocks simultaneously.

## About

This project extends the [TradingAgents Multi-Agent LLM Financial Trading Framework](https://github.com/TauricResearch/TradingAgents) with batch processing capabilities. The original TradingAgents framework was created by TauricResearch and uses multi-agent LLM systems to analyze stocks through specialized analyst, researcher, trader, and risk management agents.

**Original Framework**: [github.com/TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents)

**Research Paper**: [TradingAgents: Multi-Agents LLM Financial Trading Framework](https://arxiv.org/abs/2412.20138)

> TradingAgents framework is designed for research purposes. Trading performance may vary based on many factors, including the chosen backbone language models, model temperature, trading periods, the quality of data, and other non-deterministic factors. It is not intended as financial, investment, or trading advice.

## What This Fork Adds

This repository adds batch processing functionality to analyze multiple stocks from a CSV file and output results to another CSV. Perfect for:

**Portfolio Analysis** - Analyze all stocks in your portfolio at once

**Market Screening** - Screen hundreds of stocks systematically

**Comparative Analysis** - Compare trading signals across multiple symbols

**Automated Research** - Generate trading decisions for watchlists

## Installation

Clone this repository:
```bash
git clone https://github.com/yourusername/TradingAgents.git
cd TradingAgents
```

Create a virtual environment:
```bash
conda create -n tradingagents python=3.13
conda activate tradingagents
```

Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Set your OpenAI API key:
```bash
export OPENAI_API_KEY=your_key_here
```

Or copy `.env.example` to `.env` and add your key there:
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

## Usage

### Batch Processing Multiple Stocks

Create an input CSV file with your stocks:

```csv
Symbol,Stock Name
NASDAQ:AAPL,Apple Inc
NYSE:JPM,JPMorgan Chase & Co
NASDAQ:MSFT,Microsoft Corporation
NYSE:WM,Waste Management Inc
NASDAQ:ADP,Automatic Data Processing Inc
```

Run the batch processor:

```bash
python batch_process.py
```

This will:
1. Read stocks from `input_stocks.csv` (default)
2. Analyze each stock using the TradingAgents framework
3. Output results to `output_results_YYYYMMDD_HHMMSS.csv`

### Advanced Usage

Specify custom input/output files:
```bash
python batch_process.py my_stocks.csv my_results.csv
```

Specify a custom trade date:
```bash
python batch_process.py stocks.csv results.csv 2024-05-10
```

### Output Format

The output CSV includes:

**Symbol** - Stock ticker symbol

**Stock Name** - Company name

**Trade Date** - Analysis date

**Decision** - BUY, SELL, or HOLD

**Status** - Success or Error

**Error Message** - Error details if analysis failed

**Full Decision Text** - First 500 characters of the detailed analysis

### Example Output

```csv
Symbol,Stock Name,Trade Date,Decision,Status,Error Message,Full Decision Text
NASDAQ:AAPL,Apple Inc,2024-05-10,BUY,Success,,Based on comprehensive analysis from our analyst team...
NYSE:JPM,JPMorgan Chase & Co,2024-05-10,HOLD,Success,,After reviewing market conditions and fundamentals...
NASDAQ:MSFT,Microsoft Corporation,2024-05-10,BUY,Success,,Strong technical indicators combined with...
```

## Single Stock Analysis

For analyzing individual stocks, use the original framework pattern:

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

ta = TradingAgentsGraph(debug=True, config=DEFAULT_CONFIG.copy())
_, decision = ta.propagate("NVDA", "2024-05-10")
print(decision)
```

## Customization

Modify the configuration in `batch_process.py`:

```python
config = DEFAULT_CONFIG.copy()
config["deep_think_llm"] = "gpt-5-mini"     # Change LLM model
config["quick_think_llm"] = "gpt-5-mini"
config["max_debate_rounds"] = 2             # Increase analysis depth
```

Available LLM providers: OpenAI, Google (Gemini), Anthropic (Claude), xAI (Grok), OpenRouter, Ollama

## Features

**Error Recovery** - Continues processing if individual stocks fail

**Progress Tracking** - Shows real-time progress for each stock

**Summary Statistics** - Displays aggregate BUY/SELL/HOLD counts

**Flexible Configuration** - Customize LLM models and analysis depth

**Timestamped Output** - Automatic unique output filenames

## Interactive CLI

Try the interactive CLI for single stock analysis:
```bash
python -m cli.main
```

## Credits

This batch processing extension was built on top of the excellent [TradingAgents framework](https://github.com/TauricResearch/TradingAgents) by TauricResearch.

**Original Authors**: Yijia Xiao, Edward Sun, Di Luo, Wei Wang

**Original Repository**: https://github.com/TauricResearch/TradingAgents

**Research Paper**: https://arxiv.org/abs/2412.20138

## Citation

If you use this tool in your research, please cite the original TradingAgents work:

```
@misc{xiao2025tradingagentsmultiagentsllmfinancial,
      title={TradingAgents: Multi-Agents LLM Financial Trading Framework}, 
      author={Yijia Xiao and Edward Sun and Di Luo and Wei Wang},
      year={2025},
      eprint={2412.20138},
      archivePrefix={arXiv},
      primaryClass={q-fin.TR},
      url={https://arxiv.org/abs/2412.20138}, 
}
```

## License

This project maintains the same license as the original TradingAgents framework. See LICENSE file for details.
