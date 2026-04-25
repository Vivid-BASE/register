
import re

file_path = '/Volumes/Untitled/AI/register/index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all patterns of getCurrencySymbol() + amount.toLocaleString()
# Pattern: ${getCurrencySymbol()}${X.toLocaleString()} -> ${formatCurrency(X)}
content = re.sub(
    r'\$\{getCurrencySymbol\(\)\}\$\{([^}]+)\.toLocaleString\(\)\}',
    r'${formatCurrency(\1)}',
    content
)

# Replace: `${getCurrencySymbol()}0` -> `${formatCurrency(0)}`
content = content.replace('`${getCurrencySymbol()}0`', '`${formatCurrency(0)}`')

# Replace: getCurrencySymbol()}0` -> formatCurrency(0)}`
# Handle the placeholder case for amountReceived input
# input.placeholder = `${getCurrencySymbol()}0`;
content = content.replace(
    'input.placeholder = `${getCurrencySymbol()}0`;',
    'input.placeholder = formatCurrency(0);'
)

# Replace showDailyDetail
content = content.replace(
    '${t(\'total\')}: ${getCurrencySymbol()}${total.toLocaleString()}',
    '${t(\'total\')}: ${formatCurrency(total)}'
)
content = content.replace(
    '(${t(\'cash\')}: ${getCurrencySymbol()}${paymentTotals.cash.toLocaleString()} / ${t(\'credit\')}: ${getCurrencySymbol()}${paymentTotals.credit.toLocaleString()})',
    '(${t(\'cash\')}: ${formatCurrency(paymentTotals.cash)} / ${t(\'credit\')}: ${formatCurrency(paymentTotals.credit)})'
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

# Count remaining getCurrencySymbol references
remaining = content.count('getCurrencySymbol()')
print(f"Done. Remaining getCurrencySymbol() references: {remaining}")
