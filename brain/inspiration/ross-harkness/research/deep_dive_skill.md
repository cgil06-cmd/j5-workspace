---
name: deep-dive-analysis
description: "Conducts a comprehensive deep-dive investigation into a person, topic, or company, and synthesizes the findings into a structured, in-depth report."
user-invocable: true
metadata: '{"openclaw":{"emoji":"🕵️","requires":{"tools":["browser","search","file"]}}}'
---

# Deep-Dive Analysis & Synthesis

## 🎯 What It Does

This skill enables you to perform a comprehensive, multi-faceted research investigation into any given subject (a person, a company, a concept) and synthesize the raw findings into a polished, well-structured, and insightful report. It is designed for when you need to go beyond a simple search and build a deep, foundational understanding.

## ⚙️ Workflow

This workflow is structured in three distinct phases. You MUST proceed through them in order.

### Phase 1: Foundational Research & Information Gathering

Your goal in this phase is to cast a wide net and gather all potentially relevant raw information. Do not filter or analyze too heavily at this stage.

1.  **Initial Search**: Begin with broad `search` queries to understand the general landscape of the topic. Use `info`, `news`, and `research` search types. If the topic is a person, include searches for their social media profiles (LinkedIn, Twitter/X), personal websites, and any companies they are associated with.
2.  **Source Exploration**: From the initial search results, identify the top 5-10 most promising and authoritative sources (e.g., official websites, key interviews, major news articles, documentation). Systematically navigate to each of these URLs using the `browser` tool.
3.  **Content Extraction**: For each source visited, read the entire page content. Save the full markdown content of each page to a dedicated file in a `research/` directory (e.g., `research/source_1.md`, `research/source_2.md`). This creates your local knowledge base.
4.  **Iterative Deepening**: As you review the initial sources, new names, projects, or concepts will emerge. Create a running list of these new entities in a `scratchpad.md` file. For each new entity, spawn a new branch of research, starting again from step 1. Continue this process until you are no longer discovering significant new information.
5.  **Asset Collection**: If the research subject is visual or has associated media (e.g., videos, podcasts, images), use the appropriate tools to gather these assets. Transcribe videos and audio to text. Save key images.

### Phase 2: Synthesis & Framework-Building

Your goal in this phase is to move from raw information to structured knowledge. You will read, analyze, and categorize your findings to identify the core ideas and frameworks.

1.  **Consolidated Review**: Read through all the saved `.md` files in your `research/` directory. As you read, your goal is to identify recurring themes, core principles, key timelines, and fundamental frameworks.
2.  **Thematic Clustering**: Create a new document called `synthesis.md`. In this document, create high-level headings for the major themes you've identified (e.g., "Core Philosophy," "Key Methodologies," "Career History," "Business Model").
3.  **Information Mapping**: Go back through your research files and copy/paste key quotes, facts, and data points under the appropriate headings in `synthesis.md`. For each piece of information, add a citation pointing back to the source file (e.g., `[Source 1]`).
4.  **Framework Distillation**: Pay special attention to any explicit frameworks or models the subject uses. Dedicate a specific section in your `synthesis.md` to outlining these frameworks in a clear, structured way. Use tables to compare and contrast different concepts.

### Phase 3: Documentation & Report Generation

Your goal in this phase is to transform your synthesized notes into a polished, professional, and easy-to-read report.

1.  **Outline Creation**: Based on your `synthesis.md` document, create a final outline for the report. The structure should be logical and tell a coherent story. A good default structure is: Introduction, Core Concepts, Practical Application/Methodology, and Conclusion/Summary.
2.  **Drafting the Report**: Create a new file, `Final_Report.md`. Write the full report based on your outline, using the content from `synthesis.md`. **Do not simply copy-paste**. Rewrite and rephrase the content in your own words, ensuring a consistent and professional tone. Use clear headings, paragraphs, and tables.
3.  **Citation and Referencing**: Create a "References" section at the end of the report. List all the original source URLs you used in your research, corresponding to the citations you made during the synthesis phase.
4.  **Review and Refine**: Read through the entire report one last time. Check for clarity, consistency, and completeness. Ensure that the report directly addresses the user's original request.

## 📤 Output Format

The final deliverable MUST be a single, comprehensive Markdown document. The document should be well-structured, with clear headings, tables, and citations as described in Phase 3.

## 🛡️ Guardrails

*   **Bias Awareness**: Be mindful of the potential for bias in your sources. If you encounter conflicting information, note the discrepancy in your report.
*   **Privacy**: Do not include sensitive personal information (e.g., home addresses, private phone numbers) in the final report.
*   **Attribution**: Always attribute ideas and frameworks to their original source.

## ✨ Examples

*   `/deep-dive-analysis on Ross Harkness`
*   `/deep-dive-analysis on the concept of "second brain"`
*   `/deep-dive-analysis on the company "Superhuman"`
