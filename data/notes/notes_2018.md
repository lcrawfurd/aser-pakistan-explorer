# ASER Pakistan 2018 (rural): extraction notes

Source: `aser_2018.pdf` / `t_2018.txt`. Parser: `parse_1618.py 2018`. Validation: `validate_1618.py 2018`.
Output: `out_2018.csv`, 1,584 data rows (language 450, english 450, arithmetic 450, enrolment 234).

## Geographies and pages
Each geography has a 3-page block. Page L-1 has enrolment, page L has language and English, page L+1 has arithmetic.
Printed page = PDF page - 5 throughout. This was read from each page footer.

| geography | report heading (text layer) | enrolment | language + English | arithmetic | language label |
|---|---|---|---|---|---|
| Pakistan (national) | NATIONAL - RURAL | 82 (p.77) | 83 (p.78) | 84 (p.79) | Urdu/Sindhi/Pashto |
| Balochistan | BALOCHISTAN - RURAL | 101 | 102 | 103 | Urdu |
| Gilgit-Baltistan | GILGIT-BALTISTAN - RURAL | 119 | 120 | 121 | Urdu |
| ICT | ISLAMABAD (ICT) - RURAL | 131 | 132 | 133 | Urdu |
| Khyber Pakhtunkhwa | KHYBER PAKHTUNKHWA - RURAL | 149 | 150 | 151 | Urdu/Pashto |
| FATA | KP-NEWLY MERGED DISTRICTS - RURAL | 167 | 168 | 169 | Urdu/Pashto |
| Punjab | PUNJAB - RURAL | 185 | 186 | 187 | Urdu |
| Sindh | SINDH - RURAL | 203 | 204 | 205 | Urdu/Sindhi |
| AJK | AZAD JAMMU & KASHMIR - RURAL | 221 | 222 | 223 | Urdu |

- In 2018 the former FATA is reported as "KP-Newly Merged Districts". It is coded `FATA`, and its rows carry no note.
- "Khyber Pakhtunkhwa - Rural" is reported separately from the merged districts. It is presumably KP excluding them, but the page does not say so explicitly.

## Label variants and mapping
- Language: Nothing, Letters, Words, Sentences, Story.
- English: Nothing, Letters (Capital, Small), Words, Sentences. These map to `Capital letters` and `Small letters`.
- Arithmetic: Nothing, Number recognition (1-9, 10-99), Subtraction (2 Digits), Division (2 digits). These map to `1-9`, `10-99`, `Subtraction 2-digit` and `Division`. There is no 100-200 or 3-digit level.
- Enrolment: Govt., Pvt., Madrasah, Others, Never enrolled, Drop-out. These map to `Government`, `Private`, `Madrassah`, `Others`, `Never enrolled` and `Dropped out`.
- **Enrolment is by age band (6-10, 11-13, 14-16, 6-16), not single age.** The "Total" row (enrolled vs out of school) is recorded as `6-16` with levels `Enrolled` and `Out of school`. Its `note` field says it is a summary row, and it is excluded from the partition sum check.

## Skipped (and why)
- "By Type" row: the distribution of enrolled children by school type, which has a different denominator.
- Pre-school (3-5) table.
- Age-class composition matrix.
- All charts, including the out-of-school learning-level charts, which have no labelled table rows.
- District tables and urban tables.
- Nothing was unreadable, and no cell was left out.

## Validation
- **Row sums.** All 306 partition rows are within 100 ± 1.5. The maximum deviation is 0.1. Every parsed row ended in a printed Total of "100".
- **Total-row consistency.** Enrolled equals the sum of the four school types, and Out of school equals Never + Dropped, to within 0.1 for every geography.
- **Header check.** Every page contains the expected column labels and no 100-200 or 3-digit labels.
- **PNG spot checks (pdftoppm -r 110).** All of the following match the CSV exactly:
  - p82 national enrolment, all rows plus Total 83.2 / 16.8
  - p168 merged districts (FATA) language and English, all 20 rows (for example English class 4: 15.8 / 5.6 / 11.7 / 50.8 / 16.1)
  - p187 Punjab arithmetic, all 10 rows (for example class 9: 14.4 / 7.4 / 6.9 / 12.0 / 59.3)
- **Headline cross-check.** These are the national statements on p87 (printed p.82):

| statement on p87 | table value | result |
|---|---|---|
| 44% of class 5 cannot read a story | 100-56.1 = 43.9 | matches |
| 83% of class 3 cannot read a story | 100-17.1 = 82.9 | matches |
| 48% of class 5 cannot read English sentences | 100-52.3 = 47.7 | matches |
| 95% of class 3 cannot read English sentences | 100-4.8 = 95.2 | matches |
| 47% of class 5 cannot do division | 100-52.5 = 47.5 | matches |
| 72% of class 3 cannot do division | 100-28.3 = 71.7 | matches |
| 17% out of school / 10% never enrolled | 16.8 / 10.4 | matches |
| 83% enrolled | 83.2 | matches |
| 77% government / 20% private among enrolled | "By Type" row 76.7 / 19.7 | matches |

## Discrepancies in the report itself (values kept as printed in the tables)
- The text says 7% have dropped out, but the national 6-16 table gives 6.4 (Never enrolled 10.4 + Dropped out 6.4 = 16.8).
- The text says arithmetic "improved: 47% class 5 children could not do two digit division as compared to 42% in 2016". That is internally inconsistent, because 47% is higher than 42%. The 2016 report itself gives 52% (100-48.4).
- Learning levels in the upper classes fall in several tables. For example, in Punjab arithmetic the Nothing share rises from 5.7% in class 5 to 14.4% in class 9, and the national arithmetic Division share is 65.6 in class 7 and 61.5 in class 8. These figures are as printed and were confirmed on the images. Treat them with care when comparing over time.

## Problems
None in the extraction. The report's own text and table discrepancies are listed above.
