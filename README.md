# YAZGPT - an experimental Z39.50 chatbot
Copyright (c) 2023 Sebastian Hammer, see LICENSE file for details   

The purpose of this little project is to build a basic platform
where I can experiment with the ability of an LLM to generate queries,
issue searches against a bibliographic database, and
interpret the results. The idea is to use a chatbot as a way to quickly
explore and prototype prompts and models that might support different types
of library applications like cataloging, collection analysis, resource sharing, etc.

I'm incredibly rusty as a developer and know no
Python, so please don't judge.

**Caveat**

In its present form, this is not a useful tool -- it is just meant to be a fun way
to explore whether generative API can have a role in bibliographic data flows. The
present version is hardwired to search the Libray of Congress.

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

YAZGPT>> find publications by Robert Pirsig, combine the results by title and list editions under each title
Function Call search {
  "author": "Pirsig, Robert"
}
Hitcount:  11
Here are the publications by Robert Pirsig, grouped by title and listed with their editions:

1. Title: John Dewey, Robert Pirsig, and the art of living
   - Edition 1: New York: Palgrave Macmillan, 2006

2. Title: Lila
   - Edition 1: New York: Bantam Books, 1991
   - Edition 2: New York, N.Y.: Bantam Audio, p1991 (Contributor: Will Patton)

3. Title: On quality
   - Edition 1: Boston: Mariner Books, [2022] (Editor: Wendy K. Pirsig)

4. Title: Zen and the art of motorcycle maintenance
   - Edition 1: New York: W. Morrow, 1999
   - Edition 2: New York: Morrow, 1974
   - Edition 3: New York: Quill, 1999
   - Edition 4: New York: Morrow, 1984, c1974
   - Edition 5: Los Angeles, CA: Audio Renaissance ; p1999 (Contributor: Lawrence Pressman)

5. Title: Zen and now
   - Edition 1: New York: Alfred A. Knopf, 2008

Please note that "Lila" and "Zen and the art of motorcycle maintenance" have multiple editions.

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

Make the temperature a command line setting to allow experimentation. Possibly, t=0 would be preferable for 
these kinds of explorations.
