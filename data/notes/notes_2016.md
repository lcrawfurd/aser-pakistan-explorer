# ASER Pakistan 2016 (rural): extraction notes

Source: `aser_2016.pdf` / `t_2016.txt`. Parser: `parse_1618.py 2016`. Validation: `validate_1618.py 2016`.
Output: `out_2016.csv`, 1,584 data rows (language 450, english 450, arithmetic 450, enrolment 234).

## Geographies and pages
Each geography has a 3-page block. Page L-1 has enrolment, page L has language and English, page L+1 has arithmetic.
Printed page = PDF page - 5 throughout. This was read from each page footer and matches the rendered images.

| geography | report heading (rendered image) | enrolment | language + English | arithmetic | language label |
|---|---|---|---|---|---|
| Pakistan (national) | NATIONAL - RURAL | 69 (p.64) | 70 (p.65) | 71 (p.66) | Urdu/Sindhi/Pashto |
| Balochistan | BALOCHISTAN - RURAL | 91 | 92 | 93 | Urdu |
| FATA | FEDERALLY ADMINISTRATED TRIBAL AREAS - RURAL | 111 | 112 | 113 | Urdu/Pashto |
| Gilgit-Baltistan | GILGIT-BALTISTAN - RURAL | 131 | 132 | 133 | Urdu |
| ICT | ISLAMABAD (ICT) - RURAL | 145 | 146 | 147 | Urdu |
| Khyber Pakhtunkhwa | KHYBER PAKHTUNKHWA - RURAL | 165 | 166 | 167 | Urdu/Pashto |
| Punjab | PUNJAB - RURAL | 185 | 186 | 187 | Urdu |
| Sindh | SINDH - RURAL | 205 | 206 | 207 | Urdu/Sindhi |
| AJK | AZAD JAMMU AND KASHMIR - RURAL | 225 | 226 | 227 | Urdu |

The page-header font did not survive in the text layer (for example "N N RURAL"). I identified each geography from a rendered PNG of the header on the language page.

## Label variants and mapping
- Language: Nothing, Letters, Words, Sentences, Story. The text layer shows "ords" because the "W" glyph is missing; the image confirms "Words".
- English: Nothing, Letters (Capital, Small), Words, Sentences. These map to `Capital letters` and `Small letters`.
- Arithmetic: Nothing, Number recognition (1-9, 10-99), Subtraction (2 Digits), Division (2 digits). These map to `1-9`, `10-99`, `Subtraction 2-digit` and `Division`. There is no 100-200 or 3-digit level.
- Enrolment: Govt., Pvt., Madrasah, Others (non-state providers), plus Never enrolled and Drop-out (% out of school). These map to `Government`, `Private`, `Madrassah`, `Others`, `Never enrolled` and `Dropped out`.
- **Enrolment is reported by age band, not single age.** The bands are 6-10, 11-13, 14-16 and 6-16. `class_or_age` uses these bands. There are no age_6..age_16 rows.
- The "Total" row (enrolled vs out of school, 6-16) is recorded as `class_or_age=6-16` with levels `Enrolled` and `Out of school`. Its `note` field says it is a summary row. It is excluded from the partition sum check.

## Skipped (and why)
- "By Type" row: the distribution of enrolled children by school type, which has a different denominator.
- Early-years (pre-school) table for ages 3-5: outside the 6-16 scope, and its columns differ.
- Age-class composition matrix.
- All charts: by school type, gender, out-of-school learning levels, trends, tuition, parental education. The out-of-school learning levels are chart-only, with no clearly labelled table row, so there are no OOS class rows.
- District tables and urban tables.
- Nothing was unreadable, and no cell was left out.

## Parsing caveats
- On Balochistan p91 and Punjab p185, the Total-row values (65.2/34.8 and 86.4/13.6) sit on the text line above the "Total" label. The parser takes them from that line, keeping only numbers to the left of the Total-100 column. The Balochistan values were confirmed against the rendered image.
- On AJK p225, a chart line ("11 13 10 9 11 ...") looks like an 11-13 row. Only the first, real table row is used.

## Validation
- **Row sums.** All 306 partition rows (270 class rows and 36 age-band rows) are within 100 ± 1.5. The maximum deviation is 0.2. Every parsed row also ended in a printed Total of "100".
- **Total-row consistency.** For every geography, Enrolled equals the sum of the four school types and Out of school equals Never + Dropped, to within 0.1 (rounding).
- **Header check.** Every enrolment, language and arithmetic page contains the expected column labels and no 100-200 or 3-digit labels.
- **PNG spot checks (pdftoppm -r 110).** All of the following match the CSV exactly:
  - p70 national language and English tables (full page)
  - p71 national arithmetic, all 10 rows (for example class 5: 7.2 / 2.9 / 13.0 / 28.6 / 48.4)
  - p91 Balochistan enrolment, all rows including Total 65.2 / 34.8
  - p186 Punjab Urdu and English (for example Urdu class 7 Story 80.2; English class 3 Small letters 32.7)
- **Headline cross-check.** These are the national statements on p74 (printed p.69). Each is reported as 100 minus the cumulative table value:

| statement on p74 | table value | result |
|---|---|---|
| 48% of class 5 cannot read a story | 100-52.1 = 47.9 | matches |
| 83% of class 3 cannot read a story | 100-16.7 = 83.3 | matches |
| 54% of class 5 cannot read English sentences | 100-45.7 = 54.3 | matches |
| 85% of class 3 cannot read English sentences | 100-14.7 = 85.3 | matches |
| 52% of class 5 cannot do division | 100-48.4 = 51.6 | matches |
| 85% of class 3 cannot do division | 100-14.5 = 85.5 | matches (rounding) |
| 19% out of school / 13% never enrolled / 6% dropped out | 19.3 / 12.9 / 6.4 | matches |
| 81% enrolled | 80.7 | matches |
| 74% government / 23% private among enrolled | "By Type" row 74.1 / 23.5 | matches |

## Problems
None outstanding.
