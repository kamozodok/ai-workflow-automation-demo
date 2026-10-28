# Automated Invoice & Bank Reconciliation Pipeline

An automated data reconciliation system built in Python designed to eliminate manual spreadsheet auditing between Order Management Systems (e.g., SellerCloud) and Accounting Ledger Records (e.g., QuickBooks/Stripe).

## Problem Statement
Growing e-commerce operations frequently process hundreds of daily orders across fragmented platforms. Manual reconciliation of order invoices against actual bank payouts often leads to delayed financial reporting, undetected payment gateway fee discrepancies, and uncollected revenue.

## Solution
This tool automates cross-platform reconciliation by:
- **Ingesting Multi-Source Records:** Standardizes schema across invoice registries and bank settlements.
- **Automated Matching Logic:** Merges records on transaction keys and computes exact variance.
- **Exception Categorization:** Classifies transactions into standard audit statuses (`RECONCILED`, `AMOUNT_DISCREPANCY`, `UNPAID_INVOICE`, `UNMATCHED_DEPOSIT`).
- **Audit Reporting:** Generates a structured summary output ready for accounting review.

## Key Features & Business Impact
- **Time Savings:** Reduces daily manual reconciliation overhead by ~80%.
- **Error Reduction:** Highlights exact dollar variance down to the transaction ID.
- **Scalability:** Handles thousand-row ledger exports in seconds using Pandas vectorized operations.

## Technology Stack
- **Language:** Python 3
- **Libraries:** Pandas, NumPy
- **Development Environment:** VS Code, Git, Claude Code assistance

```markdown
## Quickstart
1. Clone the repository:
   ```bash
   git clone [https://github.com/kamozodok/ai-workflow-automation-demo.git](https://github.com/kamozodok/ai-workflow-automation-demo.git)
   cd ai-workflow-automation-demo