# YAZGPT
Copyright (c) 2023 Sebastian Hammer, see LICENSE file for details   

The purpose of this little project is to build a basic platform
where I can experiment with the ability of an LLM to generate queries,
issue searches against a bibliographic database, and
interpret the results. The idea is to use a chatbot as a way to quickly
explore and prototype prompts and models that might support different types
of library applications like cataloging, collection analysis, resource sharing, etc.

I'm incredibly rusty as a developer and know no
Python, so please don't judge.

**Prerequisites**

YAZGPT.py needs to zee "zoomsh" in its path.
Zoomsh is part of the
[YAZ toolkit](https://www.indexdata.com/resources/software/yaz). You can easily
find it for almost any platform.

You need an OpenAI API key. The code looks for it in the
OPENAI_API_KEY environment variable.

Example session:

```

Welcome to the YAZGPT AI-powered Z39.50 client

YAZGPT>> find titles by Robert Pirsig, FRBRize the results by grouping them by work
Function Call search {
  "author": "Pirsig, Robert"
}
Hitcount:  11
Here are the titles by Robert Pirsig, grouped by work:

1. Work: Zen and the art of motorcycle maintenance
   - Title: Zen and the art of motorcycle maintenance :
     - Publication: New York : W. Morrow, 1999.
   - Title: Zen and the art of motorcycle maintenance:
     - Publication: New York, Morrow, 1974.
   - Title: Zen and the art of motorcycle maintenance :
     - Publication: New York : Quill, 1999.
   - Title: Zen and the art of motorcycle maintenance :
     - Publication: New York : Morrow, 1984, c1974.
   - Title: Zen and the art of motorcycle maintenance
     - Publication: Los Angeles, CA : Audio Renaissance, p1999.
     - Contributor: Pressman, Lawrence.

2. Work: Lila
   - Title: Lila :
     - Publication: New York : Bantam Books, 1991.
   - Title: Lila
     - Publication: New York, N.Y. : Bantam Audio, p1991.
     - Contributor: Patton, Will.

3. Work: On quality
   - Title: On quality :
     - Publication: Boston : Mariner Books, [2022]
     - Publication: ©2022
     - Contributor: Pirsig, Wendy K., editor.

I couldn't find any additional works by Robert Pirsig in the provided database.

YAZGPT>> 

YAZGPT>> 


```


**TODO**

Break initial prompt into a file and make the file a commmand line option to allow tuning of the prompt to the
use case.

Add logging of query/result details for auditing the results

Refine the mapping of records. Is it possible to give access to additional fields/detailed records
on demand?

Would it make sense to predefine multiple search targets and let the LLM choose the modst appropriate one?

Explore use cases: General research, copy cataloging, resource sharing

List remaining context buffer space; add some kind of cleanout/compression of older messages.
