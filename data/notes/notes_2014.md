# ASER Pakistan 2014 -- extraction notes (rural)

Source: `aser_2014.pdf` / `t_2014.txt`. Output: `out_2014.csv` (1584 data rows: language 450, english 450, arithmetic 450, enrolment 234 = 9 geographies x 26).

## Geographies found and pages (pdf page, printed page in brackets)
| Geography | Header as printed | Enrolment | Language (label) + English | Arithmetic |
|---|---|---|---|---|
| Pakistan (national) | National - Rural | p75 (printed 71) | p76 (72), Urdu/Sindhi/Pashto | p77 (73) |
| Balochistan | Balochistan - Rural | p103 (99) | p104 (100), Urdu | p105 (101) |
| FATA | Federally Administrated Tribal Area - Rural | p119 (115) | p120 (116), Urdu/Pashto | p121 (117) |
| Gilgit-Baltistan | Gilgit-Baltistan - Rural | p135 (131) | p136 (132), Urdu | p137 (133) |
| ICT | Islamabad - ICT | p145 (141) | p146 (142), Urdu | p147 (143) |
| Khyber Pakhtunkhwa | Khyber Pakhtunkhwa - Rural | p161 (157) | p162 (158), Urdu/Pashto | p163 (159) |
| Punjab | Punjab - Rural | p177 (173) | p178 (174), Urdu | p179 (175) |
| Sindh | Sindh - Rural | p193 (189) | p194 (190), Urdu/Sindhi | p195 (191) |
| AJK | Azad Jammu & Kashmir - Rural | p209 (205) | p210 (206), Urdu | p211 (207) |

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
- Urban tables (National - Urban, pp. 85-87) and all district-level tables.

## Method
Python regex parser (`parse_1415.py`) over the `pdftotext -layout` text, anchored on lines of the form `<class> v1..v5 100` / `<a - b> v1..v6 100`, within the section that follows each "Learning levels (...)" / "School enrollment" header. Every geography returned exactly 10 class rows per learning table and 4 age-band rows plus Total. Where the enrolment Total row's two values sat on the line above the "Total ... 100" label in the text layout (GB p135, Punjab p177, Sindh p193), they were taken from that line; this was checked visually (see spot-checks). Printed page numbers taken from the page footer ("ASER Pakistan 2014  NN"); offset pdf - printed = 4 throughout.

## Validation
- Row sums: all 270 class rows (9 geos x 3 learning tables x 10 classes) and all 36 age-band enrolment rows sum to 100 +/- 0.2 (max deviation 0.2); 0 rows flagged at +/- 1.5. Total-row pairs (enrolled + out of school) also sum to 100.
- Enrolment Total row vs 6-16 row: enrolled and out-of-school sums agree within 0.1 in every geography.
- Each table's printed "How to read" sentence (e.g. "6.9 % (4.7+2.2) children of class 1 ...") was checked against the parsed class-1 / age 6-10 row: 36/36 match.
- Visual spot-checks against PNGs rendered at 110 dpi:
- p76 (National language + English, all 20 rows) -- match.
- p135 (GB enrolment incl. merged Total row 85.7 / 14.3) -- match.
- p195 (Sindh arithmetic, all 10 rows) -- match.
- Headline cross-check:
National rural (pp. 80-81 text) vs table:
- "54% class 5 children could not read story" -> 100 - 46.4 = 53.6. OK
- "84% of class 3 children could not read story in Urdu/Sindhi/Pashto" -> 100 - 15.9 = 84.1. OK
- English: "58% class 5 children could not read sentences" -> 100 - 42.3 = 57.7; "86% class 3" -> 100 - 14.0 = 86.0. OK
- "60% class 5 children could not do two digit division" -> 100 - 40.4 = 59.6; "89% ... class 3" -> 100 - 10.9 = 89.1. OK
- "21% of children (age 6-16)" out of school -> 21.0; "6% have dropped out" -> 6.3. OK

## Problems / caveats
- No single-year age rows exist; enrolment uses printed age bands rather than `age_6`..`age_16`.
- Nothing was left out for being unreadable.
