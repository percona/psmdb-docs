# Copilot Documentation Style Guide Instructions

These guidelines are for GitHub Copilot when performing a code review on documentation files. The goal is to align with the **Simple Documentation** principle, focusing on clarity, accuracy, and a user-centric approach.

## 1. General Writing & Tone

* **Be direct.** Use a conversational but professional, attentive, and emotionally neutral tone. Avoid a playful or frivolous tone.
* **Focus on the user.** Write with the user's needs and expectations in mind, as if helping a professional acquaintance.
* **Write in the second person and imperative mood** where appropriate (e.g., "Do this," "Open the file").
* **Use present tense.**
* **Prefer active voice.** Passive voice is acceptable when the system performs the action, the focus is on the receiver of the action, or to avoid blaming the user.
* **Do not use subjective attributes** like "simple" or "easy" to describe features.
* **Remove modal verbs** (must, may, could, should) if they don't add to the meaning.

---

## 2. Grammar & Syntax

* **Avoid multiple attributes** before a noun.
* **Do not omit "that"** when it introduces a subordinate clause.
* **Do not use jargon or metaphors.**
* **Use consistent terminology.** Do not use synonyms for the same concept.
* **Avoid pronouns** like "it" or "they" to refer to previously mentioned facts. Reuse the term instead.
* **Keep sentences short.** A sentence should have no more than two clauses.
* **Use the indicative or imperative mood.** The subjunctive mood should be used sparingly, for example, when presenting a command output that may vary ("Your results should be similar").
* **Wrap lines at 80 characters.**
* **Spell words using American English.**
* **Use American punctuation.**

---

## 3. Structure & Formatting

* **Break up long paragraphs.** Paragraphs should be 3-7 lines long.
* **Make text scannable** by using sections and lists.
* **Use a dash "-" as a word separator** in filenames. Filenames should be short, descriptive, and avoid common words like "a," "the," or "for."
* **Use hyphens only when necessary** for clarity.
* **Add a lead-in paragraph** before tables.
* **Add a caption** to each diagram or screenshot.
* **Do not use stacked headings.**
* **Avoid one or two-word headings.**
* **Keep headings brief but descriptive.**
* **Do not format headings** with bold, italics, etc., or end them with a period or colon.
* **Use sentence-style capitalization** for headings and captions.
* **Do not use consecutive tables** or tables with column or row spans.

---

## 4. Lists

* **Start each list with an introductory sentence** ending in a colon.
* **Ensure all list items have an aligned grammatical structure** (e.g., all start with a noun or a verb).
* **Keep lists 2-7 items long.** Shorter lists should be paragraphs; longer lists should be split.
* **Limit multilevel lists to two levels.**
* **Use sentence punctuation** if every list item is a complete sentence.
* **Do not use punctuation** (commas, semicolons) if list items are not sentences.
* **Use numbered lists** only when the order of items is important (e.g., steps in a process). Use bullet lists for items where order does not matter. If unsure, consider whether the sequence affects meaning—if not, prefer a bullet list.
* **Avoid inline lists** unless enumerating simple, known facts.

---

## 5. Specific Content Guidelines

* **Introduce abbreviations** before their first use by placing the expanded version in parentheses.
* **When referring to GUI elements, match the capitalization** used on the interface.
* **Spell out numbers one through nine, except in technical contexts** (such as version numbers, quantities, measurements, or error codes), where numerals should be used. Use a dot "." for decimals.
* **Code samples should use spaces for indentation** and have no trailing whitespace.
* **Do not use screenshots for code samples.**
* **Split commands and output into separate blocks.**
* **SQL keywords should be in uppercase.** For multiline statements, each column or logical statement should be on a new line with indentation.
* **Use "enable" instead of "allow."**
* **Do not refer to images or tables using "above" or "below."** Instead, use phrases like "the following table" or "in the previous example."
* **When linking, use the resource's title or section heading** (e.g., "For more information about X, see Y."). Avoid phrases like "click here."

---

## 6. Callouts

* **Use callouts sparingly** to emphasize helpful information not essential for the user to complete a task.
* **Callouts should not contain information necessary** for a task to succeed.
* **Separate callouts from text paragraphs** and avoid grouping them.
* **Avoid using code blocks inside callouts.**
* **The available callout types are:** Tip, Important, Warning/Caution, Note/Info, See also, and Example.

