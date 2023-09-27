# YAZGPT
Copyright (c) 2023 Sebastian Hammer, see LICENSE file for details   

The purpose of this little project is to build a basic platform
where I can experiment with the ability of an LLM to generate queries,
issue searches against a bibliographic database, and
interpret the results. I'm incredibly rusty as a developer and know no
Python, so please don't judge.

**Prerequisites**

Not much. YAZPT.py needs to zee "zoomsh" somewhere in its path.
You Zoomsh is part of the
[YAZ toolkit](https://www.indexdata.com/resources/software/yaz).

You need an OpenAI API key. The code looks for it in the
OPENAI_API_KEY environment variable.

**TODO**

Refine the mapping of records. Is it possible to give access to additional fields/detailed records
on demand?

Would it make sense to predefine multiple search targets and let the LLM choose the modst appropriate one?

Explore use cases: General research, copy cataloging, resource sharing
