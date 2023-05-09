# Research_GPT
Simple example of autonomous research ran in parallel for an eventual cluster compute solution from my Aetherius Ai Assistant project.  Mainly meant for others to use in their projects.

**Websearch Implemented!**

**Change Log**

Version 0.11

-Research GPT now decides for itself if it should conduct a web search or not.  Also serves as a showcase on how to implement simple tools.

**Side Project of the Aetherius Ai Assistant**

Aetherius GitHub: https://github.com/libraryofcelsus/Aetherius_AI_Assistant

![Example](http://www.libraryofcelsus.com/wp-content/uploads/2023/05/Research_GPT-1.gif)

## Install Guide

1. Install Git: https://git-scm.com/ (Git can be skipped by downloading the repo as a zip file under the green code button)

2. Install Python 3.10.6, Make sure you add it to PATH: https://www.python.org/downloads/release/python-3106/

3. Open the program "Git Bash".

4. Run git clone: git clone https://github.com/libraryofcelsus/Research_GPT.git

5. Open CMD as Admin

6. Navigate to Project folder: cd PATH_TO_RESEARCH_GPT_INSTALL

7. Create a virtual environment: python -m venv venv

8. Activate the environment: .\venv\scripts\activate (This must be done before running Research GPT each time, using an IDE like PyCharm can let you skip this.)

9. Install OpenAi's packages with **pip install openai**

10. Copy your OpenAI api key to key_openai.txt (https://openai.com/blog/openai-api)

11. Copy you Bing api key to key_bing.txt (https://www.microsoft.com/en-us/bing/apis/bing-web-search-api)

12. Run Research GPT with **python Research_GPT.py

