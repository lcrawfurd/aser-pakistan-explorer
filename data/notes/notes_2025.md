# ASER Pakistan 2025: extraction notes

Source: `aser_2025.pdf` (156 pages), `t_2025.txt`. Output: `out_2025.csv`, 1,608 data rows.
Scripts are in `work/`:
- `parse2025text.py`: text-layer pages.
- `crop.sh`: renders a table region at 600 dpi, runs tesseract on it, and makes a 200 dpi crop to
  check by eye.
- `build2025.py`: merges everything and adds notes.
- `validate.py`: row-sum checks.

## Key differences from earlier rounds (read before using)
1. **Rural and urban are combined, not rural only.** The 2025 survey sampled rural and urban
   enumeration blocks. Sections for National, Balochistan, KP, Punjab, Sindh and Islamabad are headed
   "Rural-Urban", and their class-wise learning and enrolment tables are **rural+urban combined**.
   There are no rural-only class-wise tables. As the spec allows, the closest equivalent was
   extracted, and every such row has `note` = "rural+urban combined". The AJK and Gilgit-Baltistan
   sections are headed "Rural", so their rows carry no such note.
2. **Rural-only enrolment panel.** The enrolment page also has a "% Enrollment by Area: Ages (6-16)"
   panel with Rural and Urban columns, each split into Enrolled and OOSC. This panel is the only
   rural-only access data. It was extracted as levels `Enrolled (rural)` / `Out of school (rural)`
   for ages 6-10, 11-13, 14-16 and 6-16, for Pakistan, Balochistan, KP, Punjab and Sindh. The note
   says it is from the RURAL-only panel. ICT, AJK and GB have no such panel; a boys/girls chart takes
   its place. The urban columns and the rural Government/Private shares were not extracted.
3. **Many table pages are images with no text layer.** For these pages the values came from a
   600 dpi tesseract OCR of the cropped table, checked cell by cell against a 200 dpi rendered crop.
   OCR and the visual reading agreed on every cell, and the note says "transcribed from rendered page
   image".

## Geographies and pages (PDF page / printed page; printed = PDF - 5 throughout, verified on every page used)
| geography | enrolment | language + English | arithmetic | section label |
|---|---|---|---|---|
| Pakistan (national) | 63 img / 58 | 64 text / 59 | 65 img / 60 | Rural-Urban |
| Balochistan | 74 img / 69 | 75 img / 70 | 76 img / 71 | Rural-Urban |
| Khyber Pakhtunkhwa | 86 img / 81 | 87 text / 82 | 88 img / 83 | Rural-Urban |
| Punjab | 98 img / 93 | 99 text / 94 | 100 img / 95 | Rural-Urban |
| Sindh | 110 img / 105 | 111 text / 106 | 112 img / 107 | Rural-Urban |
| ICT (Islamabad) | 122 img / 117 | 123 img / 118 | 124 img / 119 | Rural-Urban |
| AJK | 134 img / 129 | 135 text / 130 | 136 text / 131 | Rural |
| Gilgit-Baltistan | 146 img / 141 | 147 text / 142 | 148 text / 143 | Rural |

FATA has no section.

## Rows per table
language 400 (8 geographies x 10 x 5), english 400, arithmetic 560 (8 x 10 x 7), enrolment 248:
- 8 geographies x 4 age bands x 6 columns.
- 8 x 2 "Total" summary values.
- 5 geographies x 4 bands x 2 rural-panel values.

## Label variants
- Language heading: "Urdu/Sindhi/Pashto" for all except GB ("Urdu/Sindhi"). It is kept as printed.
- Arithmetic is labelled "Subtrction" on the national page and "Div. (2 digits)". Levels are
  normalised to the same set as 2023.
- Enrolment columns: Govt., Pvt., Madrasah, NFE/Others, Never enrolled, Drop-out. "NFE/Others" is
  stored as `Others`. Age bands are 6-10, 11-13, 14-16 and 6-16, with no single years of age.
- The "Total" row (enrolled vs out-of-school, 6-16) is stored as `Enrolled` / `Out of school`
  summary rows.

## Problems found in the report (values kept as printed, flagged)
- **AJK and GB English and arithmetic tables are identical, cell for cell.** This covers AJK pp. 135
  and 136 and GB pp. 147 and 148, and was confirmed visually on the rendered pages. The language
  tables differ. The GB summary text (p154) repeats the AJK headline figures (class 3 / 5 division
  34% / 68%, class 5 English sentences 77%). It is probably a copy error in the report, and it cannot
  be told which geography the tables really belong to. All 240 affected rows carry a CAUTION note.
  Consider dropping them for GB or AJK, or both.
- ICT summary text (p130) says "Less than 1% of children enrolled in class 3 could do two-digit
  division", but the table (p124) prints 5.0. The ICT arithmetic "How to read" line also cites
  figures (39.8+3.8, class 1) that are not in the table. The table value is kept.
- The Balochistan English "How to read" line (3.0% = 2.8+0.2) is copied from the national page and
  does not match the Balochistan table (1.7+0.2). It does not affect the extracted values.
- AJK and GB label the enrolment "By Type" row "6-16". It was skipped, like every By Type row.

## Skipped
- "By Type" rows.
- Pre-school (3-5) tables, age-class composition, and all charts (school type, gender, area, OOS
  learning).
- Urban-only columns, and district tables (none present).

## Validation
- Row sums: all 300 row groups are within 100 +/- 1.5. These are 240 learning class rows, 32
  enrolment age rows, 8 Total rows and 20 rural-panel rows. The largest deviation is 1.0 (ICT
  arithmetic, class 8, sum 101.0). Nothing else deviates by more than 0.2.
- Spot-checks against rendered PNGs (beyond the full visual check of every image table) all match:
  1. Punjab p99, Urdu class 4: 21.6 / 28.9 / 11.1 / 7.3 / 31.1.
  2. Sindh p111, English class 6: 13.2 / 0.4 / 10.5 / 23.1 / 52.8.
  3. GB p148, arithmetic class 4: 0.0 / 3.9 / 11.6 / 12.8 / 12.4 / 15.6 / 43.7.
- National headline cross-check (summary text, PDF p71), all consistent:
  - Class 3 story 7%: table 7.0.
  - Class 5 story 51%: table 51.4.
  - Class 3 English sentences 10%: table 9.8.
  - Class 5 English sentences 54%: table 53.7.
  - Class 3 division 8%: table 8.4.
  - Class 5 division 48%: table 48.2.
  - OOS 8.5%: Total row 8.5.
  - Never enrolled 8.3%: table 8.3.
  - Dropped out 0.3%: table 0.3.
  - Enrolled 91.5%: table 91.5.
- Provincial summaries:
  - Balochistan, KP, Punjab, Sindh, AJK and GB: the class 3/5 division and OOS headlines
    round-match.
  - KP, Sindh, AJK and GB: the class 3/5 English sentences headlines also round-match.
  - ICT: the class 3 division figure does not match (see above).
