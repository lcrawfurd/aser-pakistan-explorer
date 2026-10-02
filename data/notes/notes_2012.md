# ASER Pakistan 2012 (Rural) - extraction notes

Source: `aser_2012.pdf` (155 pages) / `t_2012.txt`. Parser: `work/parse_1213.py` (layout text), CSV written by `work/validate.py`.

## Geographies and pages (pdf page / printed page)
Each geography has a 3-page block: enrolment (p1), language + English (p2), arithmetic (p3).

| Geography | PDF pages | Printed pages | Language label |
|---|---|---|---|
| Pakistan (National Rural) | 66-68 | 62-64 | Urdu/Sindhi/Pashto |
| Balochistan | 82-84 | 78-80 | Urdu |
| FATA | 88-90 | 84-86 | Urdu/Pashto (printed "Urdu / Pashto") |
| Gilgit-Baltistan | 94-96 | 90-92 | Urdu |
| ICT (printed "Islamabad - ICT") | 100-102 | 96-98 | Urdu |
| Khyber Pakhtunkhwa | 106-108 | 102-104 | Urdu/Pashto |
| Punjab | 112-114 | 108-110 | Urdu |
| Sindh | 118-120 | 114-116 | Urdu/Sindhi |
| AJK (printed "Azad Jammu and Kashmir") | 124-126 | 120-122 | Urdu |

Printed page numbers were read from the page footers ("ASER 2012 - National").

## Rows written (1584 total)
- language: 450 (9 geographies x classes 1-10 x 5 levels)
- english: 450
- arithmetic: 450
- enrolment: 234 (9 x [4 age bands x 6 columns + 2 Total-row values])

## Label variants / decisions
- Language levels as printed: Nothing, Letters, Words, Sentences, Story.
- English levels: Nothing, Letters (Capital, Small), Words, Sentences -> `Capital letters`, `Small letters`.
- Arithmetic: Nothing, Number recognition 1-9, 10-99, Subtraction (2 Digits), Division (3 digits) -> levels `1-9`, `10-99`, `Subtraction 2-digit`, `Division`. The 2012 header prints "Division (3 digits)" (2013 prints "2 digits"); kept in the `note` column of each Division row. The text on p73 also says "3-digit division sums".
- Enrolment: the report gives AGE BANDS only (6-10, 11-13, 14-16, 6-16), not single ages; recorded as `class_or_age` = `6-10`, `11-13`, `14-16`, `6-16`. Columns: Govt., Pvt., Madrasah, Others, Never enrolled, Drop-out -> `Government`, `Private`, `Madrassah`, `Others`, `Never enrolled`, `Dropped out`.
- The printed "Total" row (in school vs out of school, 6-16) is recorded as `6-16` / `In school` and `6-16` / `Out of school` with a note.
- No OOS or Total rows exist in the class-wise learning tables, so none were recorded.

## Skipped (and why)
- "By type" enrolment row (share of enrolled children by school type; different denominator) - not part of the spec.
- Pre-school (age 3-5) table, age-class charts, learning by school type/gender/out-of-school charts, school report card pages, and the national summary/theme pages 70-75 (whose class-wise tables on p72-73 duplicate p67-68; all 30 rows there were checked and are identical).
- National (Urban) pages 131-141 and district-level pages.

## Validation
- Row sums: all 315 rows (270 class rows + 45 enrolment band rows) sum to 100 +/- 0.1; none flagged. Total row: in school + out of school = 100 for all geographies.
- Parser checks: every class/age row had exactly the expected number of numeric cells followed by the printed Total "100"; trailing tokens after the Total (chart labels from the adjacent graphs) were ignored and logged.
- PNG spot checks (pdftoppm -r 110): p66 (national enrolment, all 26 values), p68 (national arithmetic, full table), p119 (Sindh Urdu/Sindhi + English, full tables), plus crops of p107 (KP language) and p120 (Sindh arithmetic). All match the CSV.
- Headline cross-checks (national row):
  - "51% of Class 5 students ... able to read a story" (p72): table Story class 5 = 50.9. OK.
  - "43% of Class 3 students were able to read Class 2 sentence" (p72): Sentences + Story class 3 = 22.5 + 20.1 = 42.6. OK.
  - "48% of Class 5 students ... read Class 2 English sentences" (p72): 48.0. OK.
  - "Forty-four percent of Class 5 students were able to do 3-digit division" (p73): 43.8. OK.
  - "23% of rural ... children aged 6-16 are not in school" (p12) / "dropped out (5%)" (p70): Total out of school 22.8; dropped out 6-16 = 4.7. OK.
  - The "children who can read story / English sentences / do division" charts (class 3-6) on p67-68 match the table values rounded.
- Report's own inconsistencies (table values kept as printed; confirmed on PNG):
  - p119 Sindh English: caption says "16.8% (12.1+4.7) children of class 1 can read words", but the table row for class 1 is Words 2.6, Sentences 1.8.
  - p120 Sindh arithmetic: caption says "8.8% (4.8+4.0)", table class 1 has Subtraction 1.6, Division 1.3.
  - p107 KP language: caption "(4.3+4.8)" lists the two values in reverse order; the sum agrees.
- Observation: in 2012, Nothing/Letters (and 1-9/10-99, Capital/Small) are printed as 0.0 for classes 8-10 in most geographies (166 of 216 such cells). Recorded as printed. This probably reflects the report's tabulation, not a parsing error.
