# Results generated from all raw outputs

Primary metric requires an exact unique `FINAL:` marker, a valid number, and the correct rational value. Format failures and truncation count as incorrect.

| Mode | EN /12 | KO /12 | Correct /24 | Truncated | Format failure | Wrong valid number | Median seconds | Total seconds | Completion tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| on | 7 | 3 | 10 | 8 | 4 | 2 | 10.227 | 252.0 | 26817 |
| off | 5 | 2 | 7 | 0 | 5 | 12 | 0.836 | 45.641 | 2442 |

## Every item

| Mode | Item | Expected | Parsed | Primary category |
|---|---|---:|---:|---|
| on | discount1-en | 29150 | 29150 | correct |
| on | discount1-ko | 29150 | 30150 | wrong_number |
| on | discount2-en | 38780 | 38780 | correct |
| on | discount2-ko | 38780 | 38780 | correct |
| on | net1-en | 73990 | None | truncated |
| on | net1-ko | 73990 | None | format_failure |
| on | net2-en | 58170 | None | truncated |
| on | net2-ko | 58170 | None | format_failure |
| on | pack1-en | 86800 | 86800 | correct |
| on | pack1-ko | 86800 | None | format_failure |
| on | pack2-en | 74100 | 74100 | correct |
| on | pack2-ko | 74100 | None | truncated |
| on | tier1-en | 10500 | 10500 | correct |
| on | tier1-ko | 10500 | None | format_failure |
| on | tier2-en | 10600 | None | truncated |
| on | tier2-ko | 10600 | None | truncated |
| on | mix1-en | 26 | 26 | correct |
| on | mix1-ko | 26 | 26 | correct |
| on | mix2-en | 22 | 22 | correct |
| on | mix2-ko | 22 | 22 | correct |
| on | time1-en | 130 | None | truncated |
| on | time1-ko | 130 | None | truncated |
| on | time2-en | 123 | 110 | wrong_number |
| on | time2-ko | 123 | None | truncated |
| off | discount1-en | 29150 | None | format_failure |
| off | discount1-ko | 29150 | 3250 | wrong_number |
| off | discount2-en | 38780 | None | format_failure |
| off | discount2-ko | 38780 | 3820 | wrong_number |
| off | net1-en | 73990 | 73990 | correct |
| off | net1-ko | 73990 | -5810 | wrong_number |
| off | net2-en | 58170 | 728800 | wrong_number |
| off | net2-ko | 58170 | -6030 | wrong_number |
| off | pack1-en | 86800 | 80600 | wrong_number |
| off | pack1-ko | 86800 | 68200 | wrong_number |
| off | pack2-en | 74100 | 68400 | wrong_number |
| off | pack2-ko | 74100 | 68400 | wrong_number |
| off | tier1-en | 10500 | 10500 | correct |
| off | tier1-ko | 10500 | None | format_failure |
| off | tier2-en | 10600 | 10600 | correct |
| off | tier2-ko | 10600 | None | format_failure |
| off | mix1-en | 26 | 26 | correct |
| off | mix1-ko | 26 | 26 | correct |
| off | mix2-en | 22 | 22 | correct |
| off | mix2-ko | 22 | 22 | correct |
| off | time1-en | 130 | 147 | wrong_number |
| off | time1-ko | 130 | 170 | wrong_number |
| off | time2-en | 123 | 136 | wrong_number |
| off | time2-ko | 123 | None | format_failure |
