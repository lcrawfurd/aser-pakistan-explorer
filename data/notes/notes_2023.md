# ASER Pakistan 2023 (Rural): extraction notes

Source: `aser_2023.pdf` (183 pages), `t_2023.txt`. Output: `out_2023.csv`, 1,372 data rows.
Parser: `work/parse2023.py` (regex over the `pdftotext -layout` text). Validation: `work/validate.py`.

## Geographies and pages
Every section is headed "<AREA> - RURAL". The national class-wise tables are in the NATIONAL - RURAL
section (PDF pp. 62-64), not in a separate annex. Each section has the same 3-page block:
enrolment page, then Urdu + English page, then arithmetic page.

| geography | enrolment | language + English | arithmetic | printed pages |
|---|---|---|---|---|
| Pakistan (national) | 62 | 63 | 64 | 57-59 |
| Balochistan | 78 | 79 | 80 | 73-75 |
| Gilgit-Baltistan | 92 | 93 | 94 | 87-89 |
| Khyber Pakhtunkhwa | 106 | 107 | 108 | 101-103 |
| Punjab | 120 | 121 | 122 | 115-117 |
| Sindh | 134 | 135 | 136 | 129-131 |
| AJK | 148 | 149 | 150 | 143-145 |

Not present: ICT has no section (it appears only on the maps). FATA has no section, since the
merged districts are inside KP.

## Rows per table
language 350 (7 geographies x 10 classes x 5 levels), english 350, arithmetic 490 (x 7 levels),
enrolment 182 (7 x (4 age bands x 6 columns + 2 summary values)).

## Label variants
- Language heading: "URDU/SINDHI" for Pakistan, Sindh, Balochistan, GB and AJK, and "URDU" for KP and
  Punjab. The printed heading is used as `language_label`. In Balochistan and AJK the heading says
  URDU/SINDHI but the charts on the same page say "Urdu". This is probably a template carry-over.
  The label is kept as printed.
- Language levels: Nothing, Letters, Words, Sentences, Story. English: Nothing, Capital letters,
  Small letters, Words, Sentences. Arithmetic: Nothing, Number recognition 1-9 / 10-99 / 100-200,
  Subtraction 2 Digits / 3 Digits, Division (2 Digits).
- Enrolment is given by **age band**, not single year of age: 6-10, 11-13, 14-16 and 6-16. The
  separator is printed as "6 - 10" in most sections and "6 to 10" in Balochistan, and both are
  normalised to `6-10`. Columns: Govt., Non-state providers (Pvt., Madrasah, Others), Out-of-school
  (Never enrolled, Drop-out), stored as Government, Private, Madrassah, Others, Never enrolled,
  Dropped out.
- The enrolment "Total" row (enrolled vs out-of-school, 6-16) is stored as class_or_age `6-16` with
  levels `Enrolled` / `Out of school`, and the note marks it as a summary row.

## Skipped
- "By Type" row of the enrolment table (shares of enrolled children by school type, a different
  denominator).
- Pre-school (age 3-5) table, age-class composition, all charts (by school type, gender,
  out-of-school learning, trends), and the district tables.
- Urban tables: none were found in this report, which is rural only.

## Validation
- Row sums: all 245 row groups are within 100 +/- 1.5. These are 210 learning class rows, 28
  enrolment age rows and 7 enrolment Total rows. The largest deviation is 0.3 (Punjab arithmetic,
  class 5). No rows were flagged.
- Every table returned all 10 classes / 4 age bands, and every row ends in the printed Total = 100.
- Spot-checks against rendered PNGs (110 dpi) all match:
  1. Balochistan p79, Urdu class 5: 15.19 / 1.63 / 18.1 / 19.4 / 45.68.
  2. KP p108, arithmetic class 7: 1.6 / 2.7 / 6.2 / 12.2 / 22.8 / 18.6 / 35.9.
  3. Sindh p134, enrolment 11-13: 72.3 / 10.0 / 0.3 / 1.1 / 10.7 / 5.6.
- National headline cross-check (summary text, PDF p69) against the table, all consistent:
  - Class 3 story in Urdu/Sindhi 18%: table 17.5.
  - Class 5 story 50%: table 50.0.
  - Class 3 English sentences 18%: table 17.9.
  - Class 5 English sentences 54%: table 54.0.
  - Class 3 division 13%: table 12.6.
  - Class 5 division 46%: table 46.3.
  - Out of school 14%: table 13.7.
  - Never enrolled ~9%: table 8.96.
  - Dropped out 5%: table 4.75.
  - Enrolled 6-16 86%: table 86.3.
- Provincial headline sentences (Balochistan p84, GB p98, KP p112, Punjab p126, AJK p154) for class
  3/5 story, sentences and division also round-match the tables.
- Values are kept exactly as printed. The number of decimals varies by table: for example the
  Balochistan learning tables and the national enrolment table use 2 decimals.
