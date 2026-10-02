# ASER Pakistan 2019 (rural): extraction notes

Source: `aser_2019.pdf` (223 pages) and `t_2019.txt`. Parser: `parse_1921.py` (regex over the layout text, with column-position and Total=100 checks). Validation: `validate_1921.py`. Output: `out_2019.csv`, 1,674 data rows.

## Geographies and pages
Each geography has a fixed 3-page block: page 1 is ACCESS (1.1 enrolment), page 2 is QUALITY (2.1 language, 2.2 English) and page 3 is 2.3 Arithmetic. The PDF page is always the printed page + 5.

| geography (CSV) | printed header | enrolment | language (label) | english | arithmetic |
|---|---|---|---|---|---|
| Pakistan | NATIONAL - RURAL | p72 (pr. 67) | p73 (68), Urdu/Sindhi/Pashto | p73 | p74 (69) |
| Balochistan | BALOCHISTAN - RURAL | p91 (86) | p92 (87), Urdu | p92 | p93 (88) |
| Gilgit-Baltistan | GILGIT-BALTISTAN - RURAL | p109 (104) | p110 (105), Urdu | p110 | p111 (106) |
| ICT | ISLAMABAD - RURAL | p121 (116) | p122 (117), Urdu | p122 | p123 (118) |
| Khyber Pakhtunkhwa | KHYBER PAKHTUNKHWA - RURAL | p137 (132) | p138 (133), Urdu/Pashto | p138 | p139 (134) |
| FATA | KP-NEWLY MERGED DISTRICTS - RURAL | p155 (150) | p156 (151), Urdu/Pashto | p156 | p157 (152) |
| Punjab | PUNJAB - RURAL | p173 (168) | p174 (169), Urdu | p174 | p175 (170) |
| Sindh | SINDH - RURAL | p191 (186) | p192 (187), Urdu/Sindhi | p192 | p193 (188) |
| AJK | AZAD JAMMU & KASHMIR - RURAL | p209 (204) | p210 (205), Urdu | p210 | p211 (206) |

FATA = "KP-Newly Merged Districts" (the former FATA). The report does not say whether the "Khyber Pakhtunkhwa" block includes or excludes the merged districts.

Rows per table: language 450, English 450, arithmetic 540 (9 geographies x 10 classes x 6 levels), enrolment 234 (9 x 26).

## Labels (printed, then the CSV label)
- Language: Nothing, Letters, Words, Sentences, Story (each table also prints a Total = 100 column).
- English: Nothing, Letters-Capital becomes `Capital letters`, Letters-Small becomes `Small letters`, Words, Sentences.
- Arithmetic: Nothing, Number recognition 1-9 / 10-99 / 100-200 (CSV `1-9`, `10-99`, `100-200`), "Subtraction (2 digits)" becomes `Subtraction 2-digit`, "Division (2 digits)" becomes `Division`. There is no 3-digit subtraction column in 2019.
- Enrolment: Govt. becomes `Government`, Pvt. becomes `Private`, Madrasah becomes `Madrassah`, NFE/Others becomes `Others`, "Never enrolled", "Drop-out" becomes `Dropped out`.
- Enrolment is given by **age band, not single age**: rows 6-10, 11-13, 14-16 and 6-16 (`class_or_age` = `6-10`, `11-13`, `14-16`, `6-16`). The printed "Total" row (all enrolled vs all out-of-school, 6-16) is stored as `class_or_age=6-16` with levels `Enrolled` and `Out of school`, and a note saying so.

## Skipped (not core, or chart-only)
- The "By Type" enrolment row: its denominator is enrolled children only, not all children.
- Comprehension questions (Urdu Q1/Q2), English word/sentence meanings, word problems, time recognition, general knowledge, paid tuition, pre-school (1.2) and the age-class composition table.
- Bar charts: learning levels by school type, by gender, the out-of-school children's learning levels and the multi-year trend lines. These are chart labels, not table rows. The out-of-school learning levels exist only as rounded chart values, so no `OOS` class rows were created.
- District-level tables and the urban section.

## Parsing problems handled
- In three rows the text layer puts the class label on a different line from its data: ICT arithmetic class 5 (p123), KP arithmetic class 7 (p139) and AJK arithmetic class 4 (p211). The parser re-attached each label to the adjacent orphan data line, and I confirmed all three rows against the page renders. Those CSV rows carry a note.
- Printed page numbers come from the page footer. All of them agree with pdf_page - 5.

## Validation
- **Row sums**: all 315 row groups (270 class rows, 36 age-band partitions and 9 Total rows) are within 100 +/- 1.5. The maximum |sum - 100| is 0.2. No rows are flagged.
- **Total row vs 6-16 row**: for every geography the sum of the four school types and the sum of the two out-of-school columns in the 6-16 row match the printed Total row within 0.1.
- **Render checks (pdftoppm -r 110)**: I compared full tables against the page images on p73 (national language and English, all 100 cells), p123, p139 and p211 (arithmetic) and p155 (FATA enrolment, all rows). Everything matched. Three examples: national class 5 Story = 59.1 (p73); ICT class 10 Division = 70.6 (p123); FATA 6-16 Never enrolled = 19.7 (p155).
- **Headline cross-checks against the national row** (pp. 14-15, 20 of the report):
  - "41% in grade 5 cannot read a story" vs 100 - 59.1 = 40.9. OK.
  - "82% in grade 3 cannot" vs 100 - 18.3 = 81.7. OK.
  - "14% in grade 8 cannot" vs 100 - 86.2 = 13.8. OK.
  - "59% children of class 5 who could read a story" vs 59.1. OK.
  - Table 2 (class 5, national rural): story 59%, English sentences 55%, division 57% vs 59.1 / 55.4 / 56.9. OK.
  - "Sindh: 44% children in grade 5 can read story" vs Sindh class 5 Story 43.8. OK.
  - The trend chart on p73 (story: class 3 18, class 4 38, class 5 59, class 6 70) matches the table (18.3 / 38.4 / 59.1 / 70.5).
- **Report oddity, not used**: the national p72 "How to read" line says "40.3% (20.1+17.7+2.0+0.5) children of age group 6-10 are enrolled", which contradicts the table (Govt. 65.8). It looks like stale template text. The table values were kept.
