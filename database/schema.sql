CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    amount REAL NOT NULL,
    type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
    category TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS budgets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    month TEXT NOT NULL,
    category TEXT NOT NULL,
    limit_amount REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(month, category)
);

CREATE TABLE IF NOT EXISTS savings_goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    target_amount REAL NOT NULL,
    current_amount REAL NOT NULL DEFAULT 0.0,
    target_date TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'in_progress' CHECK(status IN ('in_progress', 'achieved', 'paused')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS financial_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_month TEXT NOT NULL UNIQUE,
    total_income REAL NOT NULL DEFAULT 0.0,
    total_expense REAL NOT NULL DEFAULT 0.0,
    net_savings REAL NOT NULL DEFAULT 0.0,
    savings_rate REAL NOT NULL DEFAULT 0.0,
    health_score REAL NOT NULL DEFAULT 0.0,
    risk_level TEXT DEFAULT 'Balanced',
    ai_recommendation TEXT,
    improvement_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS system_settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
