# ASER Pakistan 2013 (Rural) - extraction notes

Source: `aser_2013.pdf` (219 pages) / `t_2013.txt`. Parser: `work/parse_1213.py` (layout text), CSV written by `work/validate.py`.

## Geographies and pages (pdf page / printed page)
Each geography has a block: enrolment (p1), language + English (p2), arithmetic (p3).

| Geography | PDF pages | Printed pages | Language label |
|---|---|---|---|
| Pakistan (National Rural) | 71-73 | 66-68 | Urdu/Sindhi/Pashto |
| Balochistan | 99-101 | 93-95 | Urdu |
| FATA (printed "Federally Administrated Tribal Areas") | 115-117 | 109-111 | Urdu/Pashto |
| Gilgit-Baltistan | 131-133 | 125-127 | Urdu |
| ICT (printed "Islamabad-ICT") | 141-143 | 135-137 | Urdu |
| Khyber Pakhtunkhwa | 157-159 | 151-153 | Urdu/Pashto |
| Punjab | 173-175 | 167-169 | Urdu |
| Sindh | 189-191 | 183-185 | Urdu/Sindhi |
| AJK (printed "Azad Jammu & Kashmir") | 205-207 | 199-201 | Urdu |

Printed page numbers were read from the page footers ("ASER Pakistan 2013"). The pdf-to-printed offset is 5 for the national block and 6 for the provinces. Both come from the footers; p141 = printed 135 was confirmed on the PNG.

## Rows written (1584 total)
- language: 450 (9 geographies x classes 1-10 x 5 levels)
- english: 450
- arithmetic: 450
- enrolment: 234 (9 x [4 age bands x 6 columns + 2 Total-row values])

## Label variants / decisions
- Language: Nothing, Letters, Words, Sentences, Story.
- English: Nothing, Letters (Capital, Small), Words, Sentences -> `Capital letters`, `Small letters`.
- Arithmetic: Nothing, Number recognition 1-9, 10-99, Subtraction (2 Digits), Division (2 digits) -> `1-9`, `10-99`, `Subtraction 2-digit`, `Division`. The printed "(2 digits)" for Division is in the note column. 2012 printed "(3 digits)", so take care when comparing years.
- Enrolment: AGE BANDS only (printed "6 - 10", "11 - 13", "14 - 16", "6 - 16") -> `6-10`, `11-13`, `14-16`, `6-16`. Columns Govt., Pvt., Madrasah, Others, Never enrolled, Drop-out -> `Government`, `Private`, `Madrassah`, `Others`, `Never enrolled`, `Dropped out`.
- The printed "Total" row is recorded as `6-16` / `In school` and `6-16` / `Out of school`. For ICT (p141) the layout text put the two values on the line above "Total". The parser took them from that line (95.1, 4.9), and they were confirmed on the rendered PNG.
- No OOS or Total rows exist in the class-wise learning tables.

## Skipped (and why)
- "By type" enrolment row (share of enrolled by school type), the pre-school 3-5 table, the Age-Class Composition matrix (merged cells), the gender/school-type/out-of-school charts, the school report card pages, the national summary pages 75-77, the National (Urban) pages 81-87, and district pages.

## Validation
- Row sums: all 315 rows sum to 100 +/- 0.2; none flagged. In school + out of school = 100 for every geography.
- Parser checks: every row had the expected number of numeric cells followed by the printed Total "100". Trailing chart labels were ignored and logged.
- PNG spot checks (pdftoppm -r 110): p141 (ICT enrolment incl. the wrapped Total row), p175 (Punjab arithmetic, full table), p116 (FATA Urdu/Pashto + English, full tables). All match the CSV.
- Each table's "How to read" caption (class 1 values) agrees with the table. The only differences are formatting, e.g. "1" vs "1.0".
- Headline cross-checks (national row):
  - "Half of the children from Class 5 still cannot read Class 2 ... story" (p76): Story class 5 = 49.8. OK.
  - "Fifty-nine [percent] of class 3 children could not read sentences in Urdu/Pashto/Sindhi compared to 57% in the previous [year]" (p76): 100 - (25.1 + 15.5) = 59.4; 2012: 100 - 42.6 = 57.4. OK.
  - "Fifteen percent class 3 children can read class 2 level sentences as compared to 19% in 2012" (p76; the jumbled layout implies English): English Sentences class 3 = 14.9 (2012: 18.7). OK.
  - "43% class 5 children can do division as compared to 44% in 2012" (p76): 43.2 (2012: 43.8). OK.
  - "21% children 6-16 out of school ... 23% in 2012" (p14) and "6% have dropped out" (p76): Total out of school 21.1; dropped out 6-16 = 6.0. OK.
  - p14: "57% of class 5 children cannot read English sentences" and "57% cannot do two-digit division": 100 - 43.3 = 56.7 and 100 - 43.2 = 56.8. OK. p14 also cites 51% of class 5 unable to read a story, while the rural table gives 100 - 49.8 = 50.2. This is a small rounding/scope difference (p14 is the RTE overview and may mix rural and urban). Noted only.
