# ASER Pakistan 2015 -- extraction notes (rural)

Source: `aser_2015.pdf` / `t_2015.txt`. Output: `out_2015.csv` (1584 data rows: language 450, english 450, arithmetic 450, enrolment 234 = 9 geographies x 26).

## Geographies found and pages (pdf page, printed page in brackets)
| Geography | Header as printed | Enrolment | Language (label) + English | Arithmetic |
|---|---|---|---|---|
| Pakistan (national) | NATIONAL - RURAL | p77 (printed 73) | p78 (74), Urdu/Sindhi/Pashto | p79 (75) |
| Balochistan | Balochistan - Rural | p95 (91) | p96 (92), Urdu | p97 (93) |
| FATA | Federally Administrated Tribal Areas - Rural | p111 (107) | p112 (108), Urdu/Pashto | p113 (109) |
| Gilgit-Baltistan | Gilgit - Baltistan - Rural | p127 (123) | p128 (124), Urdu | p129 (125) |
| ICT | Islamabad - ICT | p137 (133) | p138 (134), Urdu | p139 (135) |
| Khyber Pakhtunkhwa | Khyber Pakhtunkhwa - Rural | p153 (149) | p154 (150), Urdu/Pashto | p155 (151) |
| Punjab | Punjab - Rural | p169 (165) | p170 (166), Urdu | p171 (167) |
| Sindh | Sindh - Rural | p185 (181) | p186 (182), Urdu/Sindhi | p187 (183) |
| AJK | Azad Jammu and Kashmir - Rural | p201 (197) | p202 (198), Urdu | p203 (199) |

ICT: the page header reads "Islamabad - ICT" with no Rural/Urban qualifier (unlike all other areas). It sits in the rural provincial sequence and was included as `ICT`; treat with that caveat.

## Table structure (identical layout for every geography)
Each geography has a 3-page block: page A = "School enrollment and out-of-school children" (plus pre-school and age-class composition tables);
page B = "Learning levels (<language>)" and "Learning levels (English)"; page C = "Learning levels (Arithmetic)" (plus parental education and paid tuition).

- **enrolment**: rows are age bands `6-10`, `11-13`, `14-16`, `6-16` (no single-year ages in this report); columns Govt., Pvt., Madrasah, Others (non-state), Never enrolled, Drop-out, Total(=100).
  Labels normalised to Government, Private, Madrassah, Others, Never enrolled, Dropped out. The table's own "Total" row (one merged enrolled cell and one merged out-of-school cell)
  is recorded as class_or_age `6-16`, levels `Enrolled (total)` and `Out of school (total)`, with a note. It agrees with the 6-16 row sums to within 0.1 everywhere.
- **language**: Class 1-10 x Nothing, Letters, Words, Sentences, Story.
- **english**: Class 1-10 x Nothing, Letters-Capital, Letters-Small, Words, Sentences (normalised to `Capital letters`, `Small letters`).
- **arithmetic**: Class 1-10 x Nothing, Number recognition 1-9, 10-99, Subtraction (2 Digits), Division (2 digits) (normalised to `1-9`, `10-99`, `Subtraction 2-digit`, `Division 2-digit`). No 100-200 or 3-digit levels this year.
- No OOS/Total class rows exist in the class-wise tables.

## Skipped (and why)
- "By Type" row of the enrolment table (shares among enrolled children, not a partition of all children); pre-school table (ages 3-5); age-class composition table; all charts (gender, school type, out-of-school learning, trends); parental education; paid tuition.
- Urban tables (none found in this report; no "Urban" table pages exist) and all district-level tables.

## Method
Python regex parser (`parse_1415.py`) over the `pdftotext -layout` text, anchored on lines of the form `<class> v1..v5 100` / `<a - b> v1..v6 100`, within the section that follows each "Learning levels (...)" / "School enrollment" header. Every geography returned exactly 10 class rows per learning table and 4 age-band rows plus Total. Where the enrolment Total row's two values sat on the line above the "Total ... 100" label in the text layout (none needed; all Total rows were on one line), they were taken from that line; this was checked visually (see spot-checks). Printed page numbers taken from the page footer ("ASER Pakistan 2015  NN"); offset pdf - printed = 4 throughout.

## Validation
- Row sums: all 270 class rows (9 geos x 3 learning tables x 10 classes) and all 36 age-band enrolment rows sum to 100 +/- 0.2 (max deviation 0.2); 0 rows flagged at +/- 1.5. Total-row pairs (enrolled + out of school) also sum to 100.
- Enrolment Total row vs 6-16 row: enrolled and out-of-school sums agree within 0.1 in every geography.
- Each table's printed "How to read" sentence (e.g. "6.9 % (4.7+2.2) children of class 1 ...") was checked against the parsed class-1 / age 6-10 row: 36/36 match.
- Visual spot-checks against PNGs rendered at 110 dpi:
- p79 (National arithmetic, all 10 rows) -- match.
- p186 (Sindh language + English, all 20 rows) -- match.
- p201 (AJK enrolment incl. Total row 96.0 / 4.0) -- match.
- Headline cross-check:
National rural (pp. 82-83 text) vs table:
- "45% class 5 children could not read story" -> 100 - 54.9 = 45.1; "84% of class 3" -> 100 - 15.7 = 84.3. OK
- English: "51% class 5 could not read sentences" -> 100 - 48.7 = 51.3; "87% class 3" -> 100 - 13.4 = 86.6. OK
- "50% class 5 could not do two digit division" -> 100 - 49.8 = 50.2. OK; "87% ... class 3" -> 100 - 12.5 = 87.5 (consistent up to rounding of .5).
- "81% ... 6-16 enrolled" -> 80.8; "6% have dropped out" -> 5.8. OK

## Problems / caveats
- No single-year age rows exist; enrolment uses printed age bands rather than `age_6`..`age_16`.
- Nothing was left out for being unreadable.
