# ASER Pakistan 2021 (rural): extraction notes

Source: `aser_2021.pdf` and `t_2021.txt`. Parser: `parse_1921.py`. Validation: `validate_1921.py`. Output: `out_2021.csv`, 1,567 data rows.

## Geographies and pages
Each geography has a 3-page block: ACCESS (1.1 enrolment), QUALITY (2.1 language, 2.2 English) and 2.3 Arithmetic. The PDF page is always the printed page + 4.

| geography (CSV) | printed header | enrolment | language (label) | english | arithmetic |
|---|---|---|---|---|---|
| Pakistan | NATIONAL - RURAL | p43 (pr. 39) | p44 (40), URDU/SINDHI/PASHTO | p44 | p45 (41) |
| Balochistan | BALOCHISTAN - RURAL | p66 (62) | p67 (63), URDU | p67 | p68 (64) |
| Gilgit-Baltistan | GILGIT-BALTISTAN - RURAL | p86 (82) | p87 (83), URDU | p87 | p88 (84) |
| ICT | ISLAMABAD - RURAL | p99 (95) | p100 (96), URDU | p100 | p101 (97) |
| Khyber Pakhtunkhwa | KHYBER PAKHTUNKHWA - RURAL | p120 (116) | p121 (117), URDU/PASHTO | p121 | p122 (118) |
| Punjab | PUNJAB - RURAL | p140 (136) | p141 (137), URDU | p141 | p142 (138) |
| Sindh | SINDH - RURAL | p160 (156) | p161 (157), URDU/SINDHI | p161 | p162 (158) |
| AJK | AZAD JAMMU & KASHMIR - RURAL | p180 (176) | p181 (177), URDU | p181 | p182 (178) |

- **There is no FATA / Newly Merged Districts block in 2021.** The 2021 trend charts (pp. 36-42) list "KP- Newly Merged Districts" only for the 2019 comparison. The report does not say whether the 2021 KP figures include the merged districts.
- Language labels are printed in capitals and were stored in title case (`Urdu`, `Urdu/Pashto`, `Urdu/Sindhi`, `Urdu/Sindhi/Pashto`).

Rows per table: language 400, English 400, arithmetic 560 (8 geographies x 10 classes x 7 levels), enrolment 207 (8 x 26, minus 1 omitted cell).

## Labels (printed, then the CSV label)
- Language: Nothing, Letters, Words, Sentences, Story (plus a Total = 100 column).
- English: Nothing, Letters Capital / Small (CSV `Capital letters` / `Small letters`), Words, Sentences.
- Arithmetic: Nothing, Number recognition 1-9 / 10-99 / 100-200, Subtraction "2 Digits" becomes `Subtraction 2-digit`, Subtraction "3 Digits" becomes `Subtraction 3-digit`, "Division (2 Digits)" becomes `Division`. The 3-digit subtraction column is new compared with 2019.
- Enrolment: Govt., Pvt., Madrasah, then "Others" (national page) or "other" (all provincial pages), which becomes `Others`; Never enrolled; "Drop-out" becomes `Dropped out`. Rows are age bands 6-10, 11-13, 14-16 and 6-16. The printed "Total" row is stored as `6-16`, with levels `Enrolled` and `Out of school` and a note.

## Skipped
- Same as 2019: the "By Type" row, bonus questions (comprehension, word/sentence meanings, time, word problems), general knowledge, pre-school, age-class composition, paid tuition, all bar and trend charts (including the out-of-school learning levels, which are chart-only), and district and urban tables.
- **Balochistan enrolment, 11-13, Madrassah (p66)**: printed as `4..4` in both the text layer and the rendered page. This is ambiguous, so the cell was omitted. The other five cells of that row were kept and carry a note. The kept cells already sum to 100.3, so a value of 4.4 would make the row sum 104.7. The row is internally inconsistent whatever the intended value.

## Parsing notes
- The KP pages (p120, p122) carry a hidden "000" text object in the footer. The visible printed page number (116, 118) was confirmed on the render and used.
- No offset class labels occurred in 2021.

## Validation
- **Row sums**: 280 row groups. 274 are within 100 +/- 1.5. These 6 are outside, and all were confirmed on the render as printed:
  - Balochistan English class 9: 98.0 (p67)
  - Punjab arithmetic classes 2, 3, 4, 5: 105.4 / 112.3 / 136.9 / 135.1 (p142)
  - Sindh arithmetic class 4: 102.0 (p162)

  The values are kept as printed, and those CSV rows carry a "printed row sums to X" note. These look like errors in the report itself.
- **Total row vs 6-16 row**: these agree within 0.1 everywhere except AJK (p180). There the 6-16 row gives enrolled 91.2 and out of school 8.8, but the printed Total row says 91.8 / 8.2. I confirmed both on the render. Both are kept as printed.
- **Caution, plausibility**: many 2021 tables show exact 0.0 in the lower levels for higher classes. For example, national language Nothing = 0.0 for classes 7-10, and Punjab arithmetic classes 6-10 are 0.0 in every column below Subtraction 3-digit. 148 "Nothing = 0.0" cells appear in 2021, against 15 in 2019. They are printed that way (confirmed on renders for national p44, Punjab p142, Sindh p162 and Balochistan p67), but they may reflect a processing artifact in the report. Treat the 2021 provincial upper-class distributions with care.
- **Render checks (pdftoppm -r 110)**: I compared full tables against the images on p44 (national language and English), p142 (Punjab arithmetic), p162 (Sindh arithmetic), p67 (Balochistan language and English), p66 (Balochistan enrolment) and p180 (AJK enrolment). Everything matched. Three examples: national class 5 Story = 54.9 (p44); Punjab class 4 Division = 59.7 (p142); Balochistan 6-10 Never enrolled = 16.8 (p66).
- **Headline cross-checks** (report p18, national rural):
  - Grade 3 story 15% vs 15.2. OK.
  - Grade 5 story 55% vs 54.9. OK.
  - Grade 8 story 74% vs 74.0. OK.
  - Grade 3 division 20% vs 19.8. OK.
  - Grade 5 division 51% vs 51.4. OK.
  - Grade 8 division 63% vs 63.4. OK.
  - The 2019 comparison figures quoted there (18 / 59 / 86 story; 21 / 57 / 65 division) also match `out_2019.csv` (18.3 / 59.1 / 86.2; 21.4 / 56.9 / 64.7).
  - The p44 trend charts (story: 15 / 37 / 55 / 64; English sentences: 20 / 45 / 56 / 65 for classes 3-6) match the tables.
