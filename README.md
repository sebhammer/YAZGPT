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
[YAZ toolkit](https://www.indexdata.com/resources/software/yaz).

You need an OpenAI API key. The code looks for it in the
OPENAI_API_KEY environment variable.

Example session:

```

Welcome to the YAZGPT AI-powered Z39.50 client

YAZGPT>> find motorcycle in the title by pirsig
Function Call search {
  "title": "motorcycle",
  "author": "pirsig"
}
Hitcount:  7
I found 6 editions related to the title "Zen and the Art of Motorcycle Maintenance" by Robert M. Pirsig:

1. Zen and the Art of Motorcycle Maintenance:
   - Author: Pirsig, Robert M.
   - Publication: New York, Morrow, 1974.

2. Zen and the Art of Motorcycle Maintenance:
   - Author: Pirsig, Robert M.
   - Publication: New York, Morrow, 1984, c1974.

3. Zen and the Art of Motorcycle Maintenance:
   - Author: Pirsig, Robert M.
   - Publication: New York, W. Morrow, 1999.

4. Zen and the Art of Motorcycle Maintenance:
   - Author: Pirsig, Robert M.
   - Publication: New York, Quill, 1999.

5. Zen and the Art of Motorcycle Maintenance:
   - Author: Pirsig, Robert M.
   - Publication: Los Angeles, CA, Audio Renaissance, 1999.
   - Contributor: Pressman, Lawrence.

6. Zen and Now:
   - Author: Richardson, Mark
   - Publication: New York, Alfred A. Knopf, 2008.

Please let me know if you need any further assistance.

YAZGPT>> What are the unique creative works in the list?
The unique creative works in the list are:

1. Zen and the Art of Motorcycle Maintenance by Robert M. Pirsig.
2. Zen and Now by Mark Richardson.

Please let me know if there is anything else I can help you with.

YAZGPT>> Give me a list of editions for each of those works
Sure! Here are the editions for each of the unique creative works:

1. Zen and the Art of Motorcycle Maintenance by Robert M. Pirsig:
   - Edition 1:
     - Publication: New York, Morrow, 1974.
   - Edition 2:
     - Publication: New York, Morrow, 1984, c1974.
   - Edition 3:
     - Publication: New York, W. Morrow, 1999.
   - Edition 4:
     - Publication: New York, Quill, 1999.
   - Edition 5:
     - Publication: Los Angeles, CA, Audio Renaissance, 1999.
     - Contributor: Pressman, Lawrence.

2. Zen and Now by Mark Richardson:
   - Edition 1:
     - Publication: New York, Alfred A. Knopf, 2008.

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
