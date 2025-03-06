# Stock Order Matching System

## Overview

This project implements a simple stock order matching system. The system uses hash tables to store buy and sell orders for different tickers and sorted arrays to maintain the order of buy and sell prices for each stock.

## Data Structure Design

### Hash Table:
- **Buy Orders**: Stores all buy orders grouped by their ticker symbol.
- **Sell Orders**: Stores all sell orders grouped by their ticker symbol.

### Sorted Array:
- **Buy Orders**: For each stock, the buy orders are stored in a descending order based on the price (highest to lowest).
- **Sell Orders**: For each stock, the sell orders are stored in an ascending order based on the price (lowest to highest).

## Time Complexity

- **Add Order**:
  - **Best Case**: O(1) (If the order can be inserted quickly without needing to reorder the list)
  - **Worst Case**: O(N) (If the order needs to be inserted at the correct position in a sorted array, requiring a traversal of the list)
  
- **Match Order**:
  - **Best Case**: O(1) (If a match is found immediately)
  - **Worst Case**: O(N) (If the entire list of buy or sell orders needs to be checked)

## How to Run

1. Clone this repository.
2. Navigate to the directory containing the `stock.py` file.
3. Run the following command to execute the file:

```bash
python stock.py
