---
description: Generate a show-ready journal club presentation from a scientific paper PDF
---

# paper2slides Workflow

This workflow uses the `paper2slides` skill. Read the full skill instructions first:

```
view_file /Users/ihlee/Desktop/.agent/skills/paper2slides/SKILL.md
```

## Steps

### 1. Ensure paper2slides is installed

// turbo
```bash
cd ~/Desktop/Journal_Club_Presentation/paper2slides_lib && pip install -e . 2>&1 | tail -5
```

### 2. Run mechanical extraction

```bash
paper2slides "<path/to/paper.pdf>" -o "<output_dir>"
```

Replace `<path/to/paper.pdf>` with the actual PDF path.

### 3. Read and comprehend the paper

Use PyMuPDF to extract text from the PDF. Read all pages. Identify: title, authors, core hypothesis, key figures, validation, applications, and limitations.

### 4. Inspect extracted panels

Open `<output_dir>/index.html` in the browser. Map panel filenames to their scientific content.

### 5. Build the curated presentation

Create `<output_dir>/show_ready/index.html` using the template from:
```
/Users/ihlee/Desktop/.agent/skills/paper2slides/resources/template_shell.html
```

Copy CSS:
// turbo
```bash
mkdir -p <output_dir>/show_ready/assets/{css,img/panels}
cp <output_dir>/assets/css/style.css <output_dir>/show_ready/assets/css/
cp <output_dir>/assets/img/panels/*.png <output_dir>/show_ready/assets/img/panels/
```

Write 15-25 curated slides with embedded `<aside class="notes">` speaker notes.

### 6. Create standalone speaker notes

Write `<output_dir>/show_ready/speaker_notes.md` following the template from:
```
/Users/ihlee/Desktop/.agent/skills/paper2slides/resources/speaker_notes_template.md
```

### 7. Verify in browser

Open the final presentation and navigate through all slides. Press S to check speaker notes.
