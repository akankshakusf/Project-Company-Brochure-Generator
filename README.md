# 🎉 OpenAI-MyFunBrochurePal

Turn boring company websites into hilarious, brochure-worthy markdown content powered by OpenAI's GPT-4o-mini. This Streamlit app scrapes a company’s landing page, analyzes useful links (like About or Careers), and generates a fun, marketing-style brochure for download.

---

## 🧠 What It Does

- Scrapes the landing page and links from a given company website
- Uses OpenAI GPT-4o-mini to:
  - Identify key links like "About" , "What we do?", "Careers" etc
  - Create a funny, markdown-style brochure about the company
- Displays the most useful links and offers a downloadable brochure

---

## 📌 Features

- 🌐 Web scraping with `requests` + `BeautifulSoup`
- 🤖 OpenAI GPT-4o-mini for intelligent & humorous copy generation
- 🧵 Multi-stage prompting system: first for link extraction, for brochure generation etc
- 🎨 Streamlit front-end with image upload, input box, and download button
- 📥 Option to download the final markdown brochure

---

## 🔮 Advanced Prompt Engineering

This project showcases real-world **prompt engineering** techniques that are in high demand in the AI industry:

- **Two-stage LLM interaction**:
  - **Stage 1**: Prompted to extract brochure-worthy links like About, Careers, etc.
  - **Stage 2**: Prompted to transform page content into an engaging, markdown-style brochure.

- **Role Separation**:
  - System and User roles are clearly defined to guide LLM behavior.

- **Persona Injection**:
  - GPT is instructed to act like *“the world’s funniest marketing assistant”*—adding voice, tone, and creative flair automatically.

> 🧠 This kind of advanced prompting makes your AI apps more controllable, more personalized, and more valuable in real-world content pipelines.

---

## 🏦 How Companies (Especially Banks) Can Use This

### 💬 Automated Brand Storytelling at Scale

**Banks**, financial institutions, and other enterprises can use this tool to transform bland web pages into engaging content—instantly.

### ✅ Real Business Applications:

| Use Case                         | Benefit                                                             |
|----------------------------------|----------------------------------------------------------------------|
| Internal Team Pages              | Make internal project descriptions more readable and fun             |
| Recruitment Portals              | Summarize and humanize career pages for Gen Z applicants             |
| Customer Education Brochures     | Create simplified overviews of banking products and services         |
| Partner Pitch Decks              | Convert your website into a creative pitch deck in seconds           |
| Compliance & Legal Summaries     | Use humor internally to simplify complex policy documentation         |

By automating content creation with LLMs, banks can:
- Cut down content production time
- Present complex services in a lighter, more digestible tone
- Stay competitive with digital-first fintechs through better storytelling

> ✨ Combine web scraping, GPT, and smart prompting to **make your brand voice shine—no matter your industry**.
